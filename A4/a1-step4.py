'''
    NTMI - Project Exercises
    Part a, step 4: POS tagging

    Authors:
        Alex Khawalid (10634207)
        Wessel Klijnsma (10172432)
        Winand Renkema (10643478)
'''

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


