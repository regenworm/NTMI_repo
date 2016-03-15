'''
    NTMI - Project Exercises
    Part b, step 1: Binarization

    Authors:
        Alex Khawalid (10634207)
        Wessel Klijnsma (10172432)
        Winand Renkema (10643478)
'''


# returns a list containing lists with tuples (tag, word) for each level in the tree
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
            elif level > 1:
                buffer += '('
            level += 1
        elif character == ')':
            level -= 1
            if level == 1:
                buffer += ')'
                children.append(buffer)
                buffer = ''
            elif level > 1:
                buffer += ')'
        else:
            buffer += character

    if len(children) == 0:
        return tuple(buffer.split(' '))
    else:
        return (tag, [parse(child) for child in children])


# binarizes the tree and changes tags to allow for debinerization
def binarize((tag1, children)):
    if isinstance(children, list) and len(children) > 1:
        triples = []
        prefix = ''
        for index in range(0, len(children)):

            (tag2, children2) = children[index]
            triples.append((prefix, tag2, children2))

            if index == 0:
                prefix += '@' + tag1 + '->'

            prefix += '_' + tag2

        for index in range(len(triples) - 1, 0, -1):
            if index == len(triples) - 1:
                subtree = (triples[index][0], binarize(tuple(triples[index][1:])))
            else:
                subtree = (triples[index][0], binarize(tuple(triples[index][1:])), subtree)

        return (tag1, binarize(children[0]), subtree)

    elif isinstance(children, list):
        return tuple([tag1] + [binarize(child) for child in children])
    else:
        return (tag1, children)


# returns a string representation of the tree
def flat_tree(node):
    result = '(' + node[0]

    for index in range(1, len(node)):
        if isinstance(node[index], tuple):
            result += ' ' + flat_tree(node[index])
        else:
            result += ' ' + node[index]

    return result + ')'


import sys
import argparse

# Process command line arguments
parser = argparse.ArgumentParser(description='Tree parser')
parser.add_argument('-input', action='store', dest='input_file',
                    type=argparse.FileType('r'), required=True)
parser.add_argument('-output', action='store', dest='output_file',
                    type=argparse.FileType('w'), required=True)
parameters = parser.parse_args(sys.argv[1:])

input_file = parameters.input_file
output_file = parameters.output_file

for line in input_file.readlines():
    if len(line) > 1:
        output_file.write(flat_tree(binarize(parse(line))))
    else:
        output_file.write('\n')

output_file.write('\n')

input_file.close()
output_file.close()
