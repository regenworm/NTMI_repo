#
#	Students	: Philip Bouman , Alex Khawalid
#	Studentnr	: 10668667		, 10634207
#	Assignment A: step 1 NTMI
#	Date		: 06-02-2015
#


import re
from optparse import OptionParser


# reads lines from file and splits into words
def readword(f):
    # expression used to split words
    exp = "[^$' '\n]*"
    words = []

    # read all lines into lines
    lines = f.readlines()

    # split all lines with exp
    for line in lines:
        v = re.findall(exp, line)

        # save every word in words
        words.extend(v)
    # remove empty list items
    words = filter(None, words)
    return words


# print highest frequency ngrams and their counts
def printhigh(ngramtable, m):
    # sort ngrams
    top = sorted(ngramtable.iteritems(), key=lambda (k, v): (v, k), reverse=True)

    # get the top m results from the sorted ngrams
    i = 0
    while i < m:
        print top[i]
        print "\n"
        i += 1


# print sum of all frequencies for a number n
def printsum(ngramtable):
    print "The sum of all frequencies is %i times" % (sum(ngramtable.values()))


##################
#    main code   #
##################


# read cmdline options
parser = OptionParser()
parser.add_option("-c", "--corpus", dest="file_in")
parser.add_option("-n", dest="nth")
parser.add_option("-m", dest="mth")

(options, args) = parser.parse_args()

# parameters manual editing
file_name = options.file_in
n = int(options.nth)
m = int(options.mth)

ngramtable = {}

# open file
f = open(file_name, "r")

##################################################

# parse file and close
words = readword(f)
f.close()

# depending on number n, ngrams need to be offset
# should work with n-1 instead conditional offset
# but it did not

if n == 1:
    offset = 0;
elif n == 2:
    offset = 1;
else:
    offset = 2;

# make ngrams and look up in dictionary
# j is used to make ngrams
# i is used to iterate through words
i = 0
ngram = ""
while i < len(words) - offset:
    j = n
    # while ngram != nth order ngram keep adding words
    while j != 0:
        ngram = ngram + " " + words[i + n - j]
        j = j - 1
    # once ngram is made check if already exists
    # if so increment count
    if ngram in ngramtable:
        ngramtable[ngram] += 1
    # else initiate with 1 as startvalue
    else:
        ngramtable[ngram] = 1
    # reset ngram and increment i
    ngram = ""
    i = i + 1
# part 1
printhigh(ngramtable, m)
# part 2
printsum(ngramtable)

# end
