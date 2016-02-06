import sys, argparse, re
from collections import defaultdict

# Read n-grams from file per line
def read_n_grams_per_line (file_handle, n):
	
	# Todo: Not sure of START END also needs to appear here.
	
	# Split text in file by one or more occurrences of newline
	lines = re.split('[\n]+', file_handle.read());
	# Set pointer to begin of file.
	file_handle.seek(0);
	# Get all lines where number of words equals n;
	return [ line for line in lines if line.count(' ') == (n-1)];
	# Replace with number of whitespaces

# Read n-gram from file per paragraphs (number of newlines > 1)	
def read_n_grams_per_paragraph (file_handle, n):
	# Normalize the number of newlines, so occurrences of more than two lines
	# become two lines
	lines = re.sub('[\n]{2,}', '\n\n', file_handle.read());
	# Set pointer to begin of file_handle.
	file_handle.seek(0);
	# Add initial START and END symbol to lines.
	lines = '[START] ' + lines.strip() + ' [END]';
	# Add addition START and END symbols, by replacing two newlines by end,
	# newline en start. In this context paragraphs are considered sentences.
	lines = re.sub('\n\n', ' [END]\n[START] ', lines);
	# Split text in lines by one or more occurrences of newline or space.
	words = re.split('[\n\s]+', lines);
	# Make n-grams from word list elements, by selecting range i to i+n, when a
	# n-gram can be made
	l = len(words);
	return [' '.join(words[i:(i+n)]) for i in range(0, l) if l - i >= n];

# Convert list of n-grams to dictionary containing number of occurrences.
def n_grams_to_dictionary(n_grams):
	# Make dictionary which maps each unique occurrence of a n-gram to an
	# integer.
	dictionary = defaultdict(int)
	# For each found n-gram, increment the corresponding integer of the 
	# n-gram in the dictionary.  
	for n_gram in n_grams: dictionary[n_gram] += 1
	return dictionary

def conditional_probability(sequence, dictionary, dictionary_minus):
	history = sequence[:sequence.rfind(' ')]
	if dictionary_minus[history] == 0:
		return 0
	else:
		return (dictionary[sequence] / (dictionary_minus[history] + 0.0))

# Compute probability of a sequence of words.
def sequence_probability(sequence, n, n_gram_dictionaries):
	# Splits sequence into words by splitting on space.
	words = sequence.split(' ');

	probability = 1.0;
	# Computing initial part of formula, ignore first element because
	# unigram '[START]' can be ignored.
	for ngram in [' '.join(words[0:i]) for i in range(1, n)][1:]:
		s = ngram.count(' ')+1;
		probability *= conditional_probability (
			ngram, n_gram_dictionaries[s], n_gram_dictionaries[s-1] 
		);

	# Computing remaining part of formula.
	for ngram in [' '.join(words[i:(i+n)]) 
			for i in range(0, len(words)) if (len(words) - i) >= n
	]:
		probability *= conditional_probability(
			ngram, n_gram_dictionaries[n], n_gram_dictionaries[n-1]
		);
	
	return probability;

# Permutes list of words and return tuples of permutation and probability.
def permute_words(words, n, n_gram_dictionaries):
	import itertools
	permutations = []
	for permutation in list(itertools.permutations(words)):
		line = '[START] ' + ' '.join(permutation) + ' [END]';
		permutations.append ((line, 
			sequence_probability(line, n, n_gram_dictionaries)))
		
	return permutations
		
# Process command line arguments
parser = argparse.ArgumentParser(description='NTMI')
parser.add_argument('-corpus', action='store', dest='corpus',
	type=argparse.FileType('r'), required=True)
parser.add_argument('-n', action='store', dest='n', type=int, required=False,
	default=2)
parser.add_argument('-m', action='store', dest="m", type=int, required=False,
	default=10)
parser.add_argument('-conditional-prob-file', action='store', 
	dest='conditional_probability', type=argparse.FileType('r'), required=False)
parser.add_argument('-sequence-prob-file', action='store', 
	dest='sequence_probability', type=argparse.FileType('r'),
	required=False)
parser.add_argument('-scored-permutations', action='store', 
	dest='scored_permutations', type=str, required=False)		
parameters = parser.parse_args(sys.argv[1:])

# File handle for c_file
c_file	= parameters.corpus
# Size of ngram
n		= parameters.n
# Number of results to output
m		= parameters.m
# File handle for conditional file
cp_file	= parameters.conditional_probability
# File handle for sequence file
sq_file	= parameters.sequence_probability
# Scoring boolean
scored = parameters.scored_permutations

# Creating required n-gram dictionaries based on given n. The default value is 
# a empty dict, so the index of a dict corresponds to the related n value.
n_gram_dictionaries = [{}]
for i in range(1, n+1):
	n_gram_dictionaries.append(
		n_grams_to_dictionary(read_n_grams_per_paragraph(c_file, i))
	)

# Checking which paramaters where set during command line initialization.
if scored:
	# In case the 'scored-permutations' parameter is set, permute the given
	# string and compute the two most permutations with the highest probability.
	for rank in sorted(permute_words(scored.split(' '), 2, n_gram_dictionaries), 
		key=lambda x: x[1], reverse=True)[:2]:
		print rank
	
elif not cp_file == None:
	# In case the 'conditional-prob-file' parameter is set return probability of
	# the n-grams in the given file that are n long.
	for ngram in read_n_grams_per_line(cp_file, n):
		print (ngram, conditional_probability(
			ngram, n_gram_dictionaries[n], n_gram_dictionaries[n-1])
		)
		
elif not sq_file == None:
	# In case the 'sequential-prob-file' parameter is set return probability of
	# the sequences in the given file.
	for line in sq_file.readlines():
		line = '[START] ' + line[:-1] + ' [END]'
		print (line, sequence_probability(line, n, n_gram_dictionaries))

else:
	# In all other cases, return the ten most common (n-1)-grams and n-grams.
	n_grams_1 = sorted(n_gram_dictionaries[n-1].items(), key=lambda x: x[1], 
		reverse=True);
	n_grams_2 = sorted(n_gram_dictionaries[n].items(), key=lambda x: x[1], 
		reverse=True);
	
	print 'n = ' + str(n-1);	print 'm = ' + str(m); 
	for index in range(m): print n_grams_1[index]
	
	print 'n = ' + str(n);	print 'm = ' + str(m); 
	for index in range(m): print n_grams_2[index]



	


