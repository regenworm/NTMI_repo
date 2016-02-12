'''
	NTMI - Project Exercises
	Part a, step 3: Smoothing n-gram statistics

	Authors:
		Alex Khawalid (10634207)
		Wessel Klijnsma (10172432)
		Winand Renkema (10643478)
'''

import sys, argparse, re
from collections import defaultdict

# Read n-grams from file per line
def read_n_grams_per_line (file_handle, n):
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

def conditional_probability(sequence, n_gram_dictionaries, n,
	(method, lengths_or_frequencies)):

	history = sequence[:sequence.rfind(' ')];
	if not method == 'no' and n_gram_dictionaries[n][sequence] <= 5:
		# In case smoothing method is set to add1
		if method == 'add1':
			return (
				(n_gram_dictionaries[n][sequence] + 1) / 
				(n_gram_dictionaries[n-1][history] + lengths_or_frequencies[n] 
				+ 0.0)
			)
		elif method == 'gt':
			# Threshold 
			k = 5
			c = n_gram_dictionaries[n][sequence]
			N = lengths_or_frequencies;
			if c == 0:	
				return N[1] / (N[0] + 0.0);
			elif c <= k:
				numerator = ((c + 1)*(N[c+1] / (N[c] + 0.0))) - \
					(c*( (k+1)*N[k+1] )/ (N[1] + 0.0))
				denominator = 1 - ( ( (k+1) * N[k+1] ) / ( N[1] + 0.0) )
				return numerator / (denominator + 0.0)
			
	# No smoothing is done. 
	if n_gram_dictionaries[n-1][history] == 0:
		return 0
	else:
		return (n_gram_dictionaries[n][sequence] / 
			(n_gram_dictionaries[n-1][history] + 0.0))

# Compute probability of a sequence of words.
def sequence_probability(sequence, n, n_gram_dictionaries, smoothing):
	# Splits sequence into words by splitting on space.
	words = re.split('[\n\s]+', sequence);

	probability = 1.0;
	# Computing initial part of formula, ignore first element because
	# unigram '[START]' can be ignored.
	for ngram in [' '.join(words[0:i]) for i in range(1, n)][1:]:
		s = ngram.count(' ')+1;
		probability *= conditional_probability (
			ngram, n_gram_dictionaries, n, smoothing
		);
		
	# Computing remaining part of formula.
	for ngram in [' '.join(words[i:(i+n)]) 
			for i in range(0, len(words)) if (len(words) - i) >= n
	]:
		probability *= conditional_probability(
			ngram, n_gram_dictionaries, n, smoothing
		);
	
	return probability;
		
# Process command line arguments
parser = argparse.ArgumentParser(description='NTMI')
parser.add_argument('-training-corpus', action='store', dest='training_corpus',
	type=argparse.FileType('r'), required=True)
parser.add_argument('-test-corpus', action='store', dest='test_corpus',
	type=argparse.FileType('r'), required=True)
parser.add_argument('-n', action='store', dest='n', type=int, required=False,
	default=2)
parser.add_argument('-smoothing', action='store', dest='smoothing', 
	choices=['no', 'add1', 'gt'], default='no')
parser.add_argument('-m', action='store', dest="m", type=int, required=False,
	default=10)
parameters = parser.parse_args(sys.argv[1:])

# File handle for training corpus
training_file	= parameters.training_corpus
# File handle for test corpus
test_file 		= parameters.test_corpus
# Size of ngram
n				= parameters.n
# Smoothing method
smoothing		= parameters.smoothing
# Number of results to output
m				= parameters.m # Remove?

# Creating required n-gram dictionaries based on given n. The default value is 
# a empty dict, so the index of a dict corresponds to the related n value.
n_gram_dictionaries = [{}]
for i in range(1, n+1):
	n_gram_dictionaries.append(
		n_grams_to_dictionary(read_n_grams_per_paragraph(training_file, i))
	)

# Creating vocabulary count or n-gram frequencies
if smoothing == 'add1':
	smoothing = ('add1', [len(dictionary) 
						for dictionary in n_gram_dictionaries]);
elif smoothing == 'gt':
	smoothing = ('gt', [len(n_gram_dictionaries[n])] + \
		# Computing frequencies of n-grams. The first case is the total number
		# of n-grams (hence N).
		[	len([i for i in n_gram_dictionaries[n].values() if i == frequency])
			for frequency in range(1, 7)	] # For range 1 to 6
		);

# Computing probability for lines in test corpus.
lines = [	('[START] ' + line[:-1] + ' [END]', 
			sequence_probability(line, n, n_gram_dictionaries, smoothing)
			)
			for line in re.split('[\n]+', test_file.read())
		];

# Printing percentage of zero probabilities.
print "Percentage of zero probabilities: " + str(round(
	(len([(w, p) for (w, p) in lines if p == 0]) / (len(lines) + 0.0)) 
	* 100, 2) )
	
# Print first five occurences of zero probability
print "Five first occurences of zero probability: "
for line in [(w, p) for (w, p) in 
	sorted(lines, key=lambda x: x[1], reverse=True)	if p == 0][:5]:
		print line;
