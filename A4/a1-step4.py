'''
    NTMI - Project Exercises
    Part a, step 4: POS tagging

    Authors:
        Alex Khawalid (10634207)
        Wessel Klijnsma (10172432)
        Winand Renkema (10643478)
'''

import sys, argparse, re
from collections import defaultdict
from nltk.ccg import lexicon

data = [
        ('<s>', ['q1', 'q2']),
        ('x', ['q1', 'q2']),
        ('z', ['q1', 'q2']),
        ('y', ['q1', 'q2'])
        ]

wprobs = {
         ('z', 'q1'): 0.3,
         ('z', 'q2'): 0.2,
         ('x', 'q1'): 0.6,
         ('x', 'q2'): 0.1,
         ('y', 'q1'): 0.1,
         ('y', 'q2'): 0.7,
         ('<s>', 'q1'): 1,
           ('<s>', 'q2'): 0        
         }
tprobs = {
           ('q1', 'q1'): 0.7,
           ('q1', 'q2'): 0.5,
           ('q2', 'q1'): 0.3,
           ('q2', 'q2'): 0.5,
           ('q1', '<s>'): 1,
           ('q2', '<s>'): 0
          }


def viterbi(word_tag, transitional_dictionary, lexical_dictionary):
    layers = [[]]
    # Compute zeroth layer
    (word, current_states) = data[0]
    for current_state in current_states:
        layers[0].append(tprobs[(current_state, word)])
    
    # Compute layers
    for t in range(1, len(data)):
        (word, current_states)  = data[t]
        (_   , previous_states) = data[t-1]
        
        # Add layer list to layers
        layers.append([])
        for current_state in current_states:
            # Find maximum value for current state
            maximum = 0
            for i in range(0, len(previous_states)):
                value =  layers[t-1][i] * wprobs[(word, current_state)]
                if t > 1: value *= tprobs[(current_state, previous_states[i])]
    
                if value > maximum:
                    maximum = value
            layers[t].append(maximum)
    
    print layers
    
    path=[]
    for t in range(len(layers)-1, 0, -1):
        path = [data[t][1][layers[t].index(max(layers[t]))]] + path
    
    print path
    #for values in reversed(layers):
    #    print values.index(max(values))
    
    #[1,2,10,11].index(max([1,2,10,11]))

# Read n-grams from file per line
def parse_pos_file(file_handle):
    sequences = [[]]
    index = 0
    # Read file per line
    for line in file_handle.readlines():
        # Remove unwanted characters from lines
        line = re.sub('([^$\w]+/[^.\w\s]+)|([\[\]\n+])', '', line)
        # Trim line
        line = re.sub('(^\s+)|(\s+$)', '', line)
        # Split line into chunks containing word/tag combinations
        if len(line) > 0:
            chunks = re.split('\s+', line)
            
            for chunk in chunks:
                # When chunk matches end of line, continue on new line.
                if re.match("[=]+|([\.]/[\.])", chunk):
                    if len(sequences[index]) > 0:
                        sequences.append([])
                        index+=1
                else:
                    sequences[index].append(tuple(chunk.rsplit('/', 1)))
    # Removing last element, if empty
    if len(sequences[index]) == 0: del sequences[index]    
    
    return sequences

# Convert list of sequences to dictionary containing word/tag tuples.
def sequences_to_model_dictionaries(sequences):
    # Make dictionary which maps each unique occurrence of a bi-gram to an
    # integer.
    language_dictionaries = (defaultdict(int), defaultdict(int))
    lexical_dictionary = defaultdict(int)
    
    # For each found bi-gram, increment the corresponding integer of the
    # bi-gram in the dictionary.    
    for sequence in sequences:
        tag_previous = 'START'
        for (word, tag) in sequence:
            lexical_dictionary[(word, tag)] += 1
            language_dictionaries[0][tag] += 1
            language_dictionaries[1][(tag_previous, tag)] += 1
            tag_previous = tag
        language_dictionaries[1][(tag_previous, 'STOP')] += 1
        
    return (language_dictionaries, (language_dictionaries[0], lexical_dictionary))

# Compute conditional probability of sequence
def conditional_probability(bi_gram, dictionaries):
    # In case no smoothing method is set or when frequency of n-gram for 
    # Good-Turing smoothing are greater than k.
    if dictionaries[0][bi_gram[1]] == 0:
        return 0
    else:
        return (dictionaries[1][bi_gram] /
                (dictionaries[0][bi_gram[1]] + 0.0))


# Process command line arguments
parser = argparse.ArgumentParser(description='NTMI')
parser.add_argument('-training-set', action='store', dest='training_set',
                    type=argparse.FileType('r'), required=True)
parser.add_argument('-test-set', action='store', dest='test_set',
                    type=argparse.FileType('r'), required=True)
parser.add_argument('-test-set-predicted', action='store', dest='test_set_predicted',
                    type=argparse.FileType('r'), required=False)
parser.add_argument('-smoothing', action='store', dest='smoothing',
                    choices=['yes', 'no'], default='no')
parameters = parser.parse_args(sys.argv[1:])

(language_dictionaries, lexical_dictionaries) = sequences_to_model_dictionaries(
    parse_pos_file(parameters.training_set)
)

print conditional_probability(('DT', 'NN'), language_dictionaries)