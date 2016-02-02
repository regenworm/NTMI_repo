"""
NTMI - Assignment A step 1

NAMES:       Alex Khawalid
STUDENT IDs: 10634207
"""

# Parse ngrams
class CorpusParser():

    # set variables and 
    def __init__(self,corpus_path,n,m):
        self.f = corpus_path
        self.m = m
        self.n = n
        self.ngramtable = {}

    # parse ngrams
    def start(self):
        if self.n == 1:
            self.read_uni()
        elif self.n > 1:
            self.read_multi()
        elif self.n < 1:
            print "n should be larger than 0"

        self.get_most_frequent()

    def print_most_frequent(self):
        i = 1
        for ngram in self.most_frequent:
            print "%i.\t" % (i),
            print "ngram: " + ngram[0],
            print "\tfrequency: %i" %(ngram[1])
            i+=1

    # read unigrams from file, put in table
    def read_uni(self):
        with open(self.f, 'r') as f:
            for line in f:
                for words in line.split():
                    if words in self.ngramtable:
                        self.ngramtable[words] += 1
                    else:
                        self.ngramtable[words] = 1


    def read_multi(self):
        # read ngrams bigger than unigrams

        # i: the number of words in an ngram
        # linenumber: the number of current line (show progress)
        ngramkey = ""
        i = 0
        linenumber = 1

        # read all lines into words
        with open(self.f, 'r') as f:
            lines = f.readlines()
            totallines = len(lines)
            for line in lines:
                print "%i out of %i" % (linenumber,totallines)
                sys.stdout.write("\033[F")

                splitlines = line.split()
                for words in splitlines:
                    # if ngram has less than n words
                    if i < self.n:
                        if i == 0:
                            ngramkey = words
                        else:
                            ngramkey = ngramkey + " " + words
                        i += 1
                    if i == self.n:
                        # increment occurences of ngram
                        if ngramkey in self.ngramtable:
                            self.ngramtable[ngramkey] += 1
                            i = self.n-1
                            ngramkey = ngramkey.split(' ', 1)[1]
                        # if new ngram add to table
                        else:
                            self.ngramtable[ngramkey] = 1
                            i = self.n-1
                            ngramkey = ngramkey.split(' ', 1)[1]
                linenumber += 1


    # get most frequent ngrams
    def get_most_frequent(self):
        print "Getting most frequent ngrams"
        sys.stdout.write("\033[F")

        # sort ngrams
        top =  sorted(self.ngramtable.iteritems(), key=lambda (k,v):(v,k), reverse=True)
        
        # get the top m results from the sorted ngrams
        most_frequent = []
        i = 0
        while i < self.m:
            most_frequent.append(top[i])
            i += 1

        self.most_frequent = most_frequent

        # erase line
        print "\x1b[2K"



# main function
def step1(corpus,n,m):

    print "========== NTMI Assignment A step 1, n=%i ==========" % (n)
    print "Corpus:\t%s" % (corpus)
    print "n:\t%i" % (n)
    print "m:\t%i" % (m)
    parser = CorpusParser(corpus,n,m)
    parser.start()

    print "Most frequent ngrams and their frequencies respectively:"
    parser.print_most_frequent()


    # print sum of all frequencies for a number n
    print "The sum of all frequencies is %i" % (sum(parser.ngramtable.values()))
    print "==================================================="

def main(args):

    if args.do_all:
        step1('austen.txt',1,10)
        step1('austen.txt',2,10)
        step1('austen.txt',3,10)
    else:
        corpus = args.corpus
        n = args.n
        m = args.m
        # if arguments were not specified
        if not args.corpus:
            corpus = 'austen.txt'
        if not args.n:
            n = 3
        if not args.m:
            m = 10
        step1(corpus,n,m)




if __name__ == '__main__':

    import sys
    import argparse

    p = argparse.ArgumentParser("Parse ngrams from corpus")
    p.add_argument('-corpus', help='corpus path')
    p.add_argument('-n', help='length of ngrams', type=int)
    p.add_argument('-m', help='get top m most frequent words in descending order', type=int)
    p.add_argument('-do_all', help='set this to True to run for n=1,n=2 and n=3')

    args = p.parse_args(sys.argv[1:])
    main(args)
