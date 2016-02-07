import sys, argparse, re
from collections import defaultdict


def read_n_grams_per_line(corpus, n):
    # Split text in corpus by one or more occurences of newline
    lines = re.split('[\n]+', corpus.read());
    # Set read pointer to begin of corpus.
    corpus.seek(0)
    # Get all lines where number of words equals n
    return [line for line in lines if line.count(' ') == (n - 1)]


# Replace with number of whitespaces

def read_n_grams_per_paragraph(corpus, n):
    # Normalize the number of newlines, so occurences of more than two
    # lines become two lines
    lines = re.sub('[\n]{2,}', '\n\n', corpus.read())
    # Set read pointer to begin of corpus.
    corpus.seek(0)
    # Add initial START and END symbol
    lines = '[START] ' + lines.strip() + ' [END]'
    # Add addition START and END symbols, by replacing two newlines by
    # end, newline en start. This way paragraphs are considered sentences.
    lines = re.sub('\n\n', ' [END]\n[START] ', lines)
    # Split text in corpus by one or more occurences of newline or space.
    words = re.split('[\n\s]+', lines);
    # Make ngrams from word list elements, by selecting range i to i+n,
    # when a ngram can be made
    return [' '.join(words[i:(i + n)]) for i in range(0, len(words)) if len(words) - i >= n]


def n_grams_to_dictionary(ngrams):
    # Make dictionary which maps each unique occurence of a n-gram to an
    # integer.
    mapping = defaultdict(int)
    # mapping = { sequence:0 for sequence in set(ngrams)}
    # For each found n-gram, increment the corresponding integer of the
    # n-gram in the dictionary.
    for ngram in ngrams: mapping[ngram] += 1

    return mapping


def conditional_probability(sequence, dictionary, dictionary_minus):
    history = sequence[:sequence.rfind(' ')]
    if dictionary_minus[history] == 0:
        return 0
    else:
        return (dictionary[sequence] / (dictionary_minus[history] + 0.0))


def sequence_probability(sequence, n, dictionaries):
    words = sequence.split(' ')
    # Removes [START]
    initialgrams = [' '.join(words[0:i]) for i in range(1, n)][1:]

    product = 1.0
    for ngram in initialgrams:
        product *= conditional_probability(
            ngram,
            dictionaries[ngram.count(' ')],
            dictionaries[ngram.count(' ') - 1]
        )

    ngrams = [' '.join(words[i:(i + n)])
              for i in range(0, len(words)) if (len(words) - i) >= n]

    for ngram in ngrams:
        product *= conditional_probability(ngram, dictionaries[n - 1], dictionaries[n - 2])

    return product


def permute_words(words, n, dictionaries_ngrams):
    import itertools
    permutations = []
    for permutation in list(itertools.permutations(words)):
        line = ' '.join(permutation)
        permutations.append(('[START] ' + line + ' [END]',
                             sequence_probability(line, n, dictionaries_ngrams)))

    return permutations


# Start of program

# Process command line arguments
parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-corpus', action='store', dest='corpus',
                    type=argparse.FileType('r'), required=True)
parser.add_argument('-n', action='store', dest='n', type=int,
                    required=False, default=2)
parser.add_argument('-m', action='store', dest="m", type=int,
                    required=True)
parser.add_argument('-conditional-prob-file', action='store',
                    dest='conditional_probability', type=argparse.FileType('r'),
                    required=False)
parser.add_argument('-sequence-prob-file', action='store',
                    dest='sequence_probability', type=argparse.FileType('r'),
                    required=False)
parser.add_argument('-scored-permutations', action='store',
                    dest='scored', type=bool,
                    required=False, default=False)
parameters = parser.parse_args(sys.argv[1:])


# File handle for corpus
corpus = parameters.corpus
# Size of ngram
n = parameters.n
# Number of results to output
m = parameters.m
# File handle for conditional file
cp_file = parameters.conditional_probability
# File handle for sequence file
sq_file = parameters.sequence_probability
# Scoring boolean
scored = parameters.scored

# Building dictionaries of ngrams
dictionaries_ngrams = []
for i in range(1, n + 1):
    dictionaries_ngrams.append(
        n_grams_to_dictionary(read_n_grams_per_paragraph(corpus, i))
    )

# Print m most frequent n-grams
if scored:
    A = ['know', 'I', 'opinion', 'do', 'be', 'your', 'not', 'may', 'what']
    B = ['I', 'do', 'not', 'know']

    for rank in sorted(permute_words(A, 2, dictionaries_ngrams),
                       key=lambda x: x[1], reverse=True)[:2]:
        print rank

    for rank in sorted(permute_words(B, 2, dictionaries_ngrams),
                       key=lambda x: x[1], reverse=True)[:2]:
        print rank
if cp_file == None and sq_file == None:
    bigrams = sorted(dictionaries_ngrams[1].items(),
                     key=lambda x: x[1], reverse=True)
    for index in range(m):
        print bigrams[index]
elif not cp_file == None and sq_file == None:
    for ngram in read_n_grams_per_line(cp_file, n):
        print (ngram, conditional_probability(
            ngram, dictionaries_ngrams[n - 1], dictionaries_ngrams[n - 2])
               )
else:
    for line in sq_file.readlines():
        line = '[START] ' + line[:-1] + ' [END]'
        print (line, sequence_probability(line, n, dictionaries_ngrams))
