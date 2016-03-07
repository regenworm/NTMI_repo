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
#from nltk.ccg import lexicon

# Read words and tags from file
def parse_pos_file(file_handle):
    sequences = [[]]
    index = 0
    # Read file per line
    for line in file_handle.readlines():
        # Remove unwanted characters from lines
        line = re.sub('([^$\w]+/[^.\w\s]+)|([\[\]\n+])', '', line)
        # Trim line
        line = re.sub('(^\s+)|(\s+$)', '', line)
        # When line is not empty
        if len(line) > 0:
            # Split line into chunks containing word/tag combinations            
            for chunk in re.split('\s+', line):
                # When chunk matches end of line, continue on new line.
                if re.match('[=]+|(.+/[\.])', chunk):
                    # When current sequence is not empty, append a new one.
                    if len(sequences[index]) > 0:
                        sequences.append([])
                        index+=1
                else:
                    chunk = re.sub('\|.*$', '', chunk)
                    sequences[index].append(tuple(chunk.rsplit('/', 1)))
    
    # Removing last element, if empty
    if len(sequences[index]) == 0: del sequences[index]    
    
    return sequences

# Converse regular sequence to input data for viterbi algorithm.
def sequence_to_data(sequence, language_dictionaries):
    data = []
    data.append(('', ['START']))
    for word in sequence:
        data.append((word, language_dictionaries[0].keys()))

    data.append(('', ['STOP']))
    return data

# Viterbi algorithm
def viterbi(data, dictionaries, smoothing):
  
    layers = [[]]
    # Compute zeroth layer
    (word, current_states) = data[0]
    for current_state in current_states:
        if current_state == 'START':
            layers[0].append(1)
        else:
            layers[0].append(
                conditional_probability(
                    'lexical', (word, current_state), dictionaries[1], smoothing
                )
            )
          
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
                value =  layers[t-1][i] * \
                conditional_probability(
                    'lexical', (word, current_state), dictionaries[1], smoothing               
                )
                
                if t > 1: 
                    value *= conditional_probability(
                        'language', (current_state, previous_states[i]), 
                        dictionaries[0], smoothing
                    )
    
                if value > maximum:
                    maximum = value

            layers[t].append(maximum)
       
    path=[]
    for t in range(len(layers) - 1, -1, -1):
        path = [data[t][1][layers[t].index(max(layers[t]))]] + path
    
    return path

# Convert list of sequences to dictionary containing word/tag tuples.
def sequences_to_model_dictionaries(sequences):
    # Make dictionary which maps each unique occurrence of a bi-gram to an
    # integer.
    language_dictionaries = [defaultdict(int), defaultdict(int)]
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
        
    return (language_dictionaries, [language_dictionaries[0], lexical_dictionary])

# Compute conditional probability of sequence
def conditional_probability(model, bi_gram, dictionaries, smoothing):
    
    if model == 'language': k = 4
    elif model == 'lexical': k = 1
    
    c = dictionaries[1][bi_gram]
    if smoothing == 'yes' and model == 'lexical' and c <= k:
        (word, tag) = bi_gram
        if c == 0:
            
            if dictionaries[3].has_key(word):
                return 0
            
            if dictionaries[0][tag] == 0:
                return 0;
            else:
                return (0.5)*(dictionaries[2][tag]/(dictionaries[0][tag]+ 0.0))
        else: 
            return 0.5/(dictionaries[0][tag] + 0.0)
        
    elif smoothing == 'yes' and model == 'language' and c <= k:
        N = dictionaries[2]
        
        if c == 0:
            return N[1] / (N[0] + 0.0)
        else:
            numerator = ((c + 1) * (N[c + 1] / (N[c] + 0.0))) - \
                        (c * ((k + 1) * N[k + 1]) / (N[1] + 0.0))
            denominator = 1 - (((k + 1) * N[k + 1]) / (N[1] + 0.0))
            return numerator / (denominator + 0.0)
            
    # In case no smoothing method is set or when frequency of n-gram for 
    # Good-Turing smoothing are greater than k.
    if dictionaries[0][bi_gram[1]] == 0: # When denominator is zero.
        return 0.0
    else:
        return c / (dictionaries[0][bi_gram[1]] + 0.0)

# Process command line arguments
parser = argparse.ArgumentParser(description='NTMI')
parser.add_argument('-training-set', action='store', dest='training_set',
                    type=argparse.FileType('r'), required=True)
parser.add_argument('-test-set', action='store', dest='test_set',
                    type=argparse.FileType('r'), required=True)
parser.add_argument('-test-set-predicted', action='store', dest='test_set_predicted',
                    type=argparse.FileType('w'), required=True)
parser.add_argument('-smoothing', action='store', dest='smoothing',
                    choices=['yes', 'no'], default='no')
parameters = parser.parse_args(sys.argv[1:])

smoothing = parameters.smoothing

# Compute unigrams and bigrams from training set: index 0 = unigrams, 
# 1 = bigrams
(language_dictionaries, lexical_dictionaries) = sequences_to_model_dictionaries(
    parse_pos_file(parameters.training_set)
)

# Compute occurence count when smoothing is enabled. 
if smoothing == 'yes':
    language_dictionaries.append(
        [len([i for i in language_dictionaries[1].values() if i == frequency])
            for frequency in range(1, 8) # For range 1 to 7
        ]
    )
    # Computing number of occurences per tag for lexical model
    lexical_dictionaries.append(defaultdict(int))
    for (word, tag) in lexical_dictionaries[1].keys(): 
        if lexical_dictionaries[1][(word, tag)] == 1:
            lexical_dictionaries[2][tag] += 1

            
    # Computing number of occurences per tag for lexical model
    lexical_dictionaries.append(defaultdict(list))
    for (word, tag) in lexical_dictionaries[1].keys(): 
        lexical_dictionaries[3][word].append(tag)
 
file_handle = parameters.test_set_predicted

# Computing accuracy per sentence and overall accuracy
correct = 0
total = 0
for sequence in parse_pos_file(parameters.test_set):
    (word_sequence, tag_sequence) = zip(*sequence)

    tag_sequence = ['START'] + list(tag_sequence) + ['STOP']
    tag_sequence_predicted = viterbi(
        sequence_to_data(word_sequence, lexical_dictionaries),
        (language_dictionaries, lexical_dictionaries),
        smoothing
    )
    
    current = 0
        
    for index in range(1, len(tag_sequence)-1):
        if (tag_sequence[index] == tag_sequence_predicted[index]): 
            current += 1       
    
    # Writing accuracy per sentence to output file
    file_handle.write('Word sequence:\t\t' + ', '.join(word_sequence) + '\n')
    file_handle.write('Tag sequence:\t\t' + ', '.join(tag_sequence) + '\n')
    file_handle.write('Predicted sequence:\t' + ', '.join(tag_sequence_predicted) + '\n')
    file_handle.write('Accuracy:\t\t')
    file_handle.write( str("%.2f" % ((current / (index + 0.0)) * 100)) + '%\n' )
    file_handle.write( '\n' )
  
    correct += current 
    total += index+1
            
file_handle.close()

print 'Accuracy: ' + str(correct/(total + 0.0))