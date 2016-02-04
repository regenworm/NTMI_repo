'''
	NTMI - Project Exercises
	Part a, step 1: Extracting ngram statistics

	Authors:
		Alex Khawalid (10634207)
		Wessel Klijnsma (10172432)
		Winand Renkema (10643478)
'''

import sys, argparse, re

# Process command line arguments
parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('-corpus', action='store', dest='corpus', type=argparse.FileType('r'), required=True)
parser.add_argument('-n', action="store", dest='n', type=int, required=True)
parser.add_argument('-m', action="store", dest="m", type=int, required=True)
parameters = parser.parse_args(sys.argv[1:])

# File handle for corpus
corpus = parameters.corpus
# Size of ngram
n      = parameters.n
# Number of results to output
m      = parameters.m

# Split text in corpus by one or more occurences of newline or space.
words   = re.split('[\n\s]+', corpus.read());
# Make ngrams from word list elements, by selecting range i to i+n,
# when a ngram can be made
ngrams = [' '.join(words[i:(i+n)]) for i in range(0, len(words)) if len(words) - i > n]

# Make dictionary which maps each unique occurence of a n-gram to an integer. 
mapping = { sequence:0 for sequence in set(ngrams)}
# For each found n-gram, increment the corresponding integer of the n-gram 
# in the dictionary.  
for ngram in ngrams: mapping[ngram] += 1
# Sort the n-grams by there occurence value.
mapping = sorted(mapping.items(), key=lambda x: x[1], reverse=True)

print 'n = ' + str(n)
print 'm = ' + str(m)
# Print m most occuring n-grams
for index in range(m): 
	print mapping[index]
	
print 'sum: ' + str(len(ngrams))
