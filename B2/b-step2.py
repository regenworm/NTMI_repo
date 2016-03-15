'''
    NTMI - Project Exercises
    Part b, step 1: Binarization

    Authors:
        Alex Khawalid (10634207)
        Wessel Klijnsma (10172432)
        Winand Renkema (10643478)
'''

def parse(tree):
    buffer = ''
    level = 0
    tag = ''
    children = []
    for character in tree:
        if character == '(':
            if level == 1:
                if tag == '': tag = buffer.strip()
                buffer = '('
            elif level > 1: buffer += '('
            level += 1
        elif character == ')':
            level -= 1
            if level == 1:
                buffer += ')'
                children.append(buffer)
                buffer = ''
            elif level > 1: buffer += ')' 
        else:
            buffer += character

    if len(children) == 0:  
        (tag, word) = buffer.split(' ')
        return ([tag], word)
    else:                   
        return ([tag], [parse(child) for child in children])

def binarize((parents, children), h, v):

    if isinstance(parents, list) and v > 0 and len(parents) > v:
        parents = parents[0:-1]
    elif v == 0:
        parents = []
    
    if isinstance(children, list) and len(children) > 1:
        
        triples = []
        prefix = []
        for index in range(0, len(children)):
            
            (parents2, children2) = children[index]
            
            triples.append(
                ('@' + '^'.join(parents) + \
                ('->_' if h != 0 else '' ) + \
                '_'.join(prefix), \
                parents2,\
                children2)
            )

            prefix.append('^'.join(parents2))

            if h > 0 and len(prefix) > h:
                prefix = prefix[1:]
            elif h == 0:
                prefix = []

        for index in range(len(triples)-1, 0, -1):
            (left, right) = triples[index][1:]
            if index == len(triples)-1:
                subtree = (triples[index][0], binarize((left + parents, right), h, v))
            else:
                subtree = (triples[index][0], binarize((left + parents, right), h, v), subtree)
                
        (left, right) = children[0]
        return ('^'.join(parents), binarize((left + parents, right), h, v), subtree)
    
    
    elif isinstance(children, list) and len(children) == 1:
        return tuple(['^'.join(parents)] + [binarize((left + parents, right), h, v) for (left, right) in children])
    else:
        return (parents[0], children)
   
def flat_tree(node):
    
    result = '(' + node[0]
    
    for index in range(1, len(node)):
        if isinstance(node[index], tuple):
            result += ' ' + flat_tree(node[index])
        else:
            result += ' ' + node[index]

    return result + ')'

import sys, argparse

# Process command line arguments
parser = argparse.ArgumentParser(description='Tree parser', add_help=False)
parser.add_argument('-h', action='store', dest='h', type=int, required=False,
                    default=-1)
parser.add_argument('-v', action='store', dest='v', type=int, required=False,
                    default=-1)
parser.add_argument('-input', action='store', dest='input_file',
    type=argparse.FileType('r'), required=True)
parser.add_argument('-output', action='store', dest='output_file', 
    type=argparse.FileType('w'), required=True)
parameters = parser.parse_args(sys.argv[1:])

h = parameters.h
v = parameters.v

if v == 0:
    print 'Vertical markovization is not possible with order 0'
    exit(1)
    
input_file  = parameters.input_file
output_file = parameters.output_file

for line in input_file.readlines():
    
    if len(line) > 1:
        output_file.write(flat_tree(binarize(parse(line), h, v)))            
    else:
        output_file.write('\n')
    
output_file.write('\n')

input_file.close()
output_file.close()