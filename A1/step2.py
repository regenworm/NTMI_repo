"""
NTMI - Assignment A step 2

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
        last_line = []
        self.ngramtable = {"START": 1, "STOP": 1}
        with open(self.f, 'r') as f:
            i=1
            for line in f:
                linesplit = line.split()

                for words in linesplit:
                    if words in self.ngramtable:
                        self.ngramtable[words] += 1
                    else:
                        self.ngramtable[words] = 1

                # add start and stop at at end of paragraph
                if linesplit == [] and not (last_line == "\n" or last_line == "" or last_line == " "):
                    self.ngramtable["STOP"] +=1
                    self.ngramtable["START"] +=1
                last_line = line


    def add_start_and_stop(self,ngramkey,word0,word1,i):
        # if ngram has less than n words
        if i < self.n:
            if i == 0:
                ngramkey = word0
            else:
                ngramkey = ngramkey + " " + word1
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
        
        return [i, ngramkey]
                

    def read_multi(self):
        # read ngrams bigger than unigrams

        # i: the number of words in an ngram
        # linenumber: the number of current line (show progress)
        ngramkey = "START"
        i = 1
        linenumber = 1

        # read all lines into words
        with open(self.f, 'r') as f:
            lines = f.readlines()
            totallines = len(lines)
            last_line = ""

            for line in lines:
                print "%i out of %i" % (linenumber,totallines)
                sys.stdout.write("\033[F")

                splitlines = line.split()

                # if last line empty and this one is not add start
                if (not splitlines == []) and last_line == "\n":
                   [i, ngramkey] = self.add_start_and_stop(ngramkey,"START","START",i)

                for word in splitlines:
                   [i, ngramkey] = self.add_start_and_stop(ngramkey,word,word,i)


                # if this line is empty and last line was not add stop
                if splitlines == [] and not (last_line == "\n" or last_line == "" or last_line == " "):
                    self.add_start_and_stop(ngramkey,"START","STOP",i)
                    ngramkey = ""
                    i = 0


                last_line = line
                linenumber += 1
        self.add_start_and_stop(ngramkey,"START","STOP",i)
   


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

    def get_ngrams_alphabetical(self):
        for key in sorted(parser.ngramtable.iterkeys()):
            print "%s: %s" % (key, parser.ngramtable[key])

    # get all ngrams that contain a certain word (case sensitive)
    def get_ngrams_containing(self, word):
        print "Searching ngramtable"
        sys.stdout.write("\033[F")
        print [(key,value) for key, value in self.ngramtable.items() if word in key]


# do step 2 assignment
def step2(corpus,n,m):
    print "========== NTMI Assignment A step 2, n=%i ==========" % (n)
    print "Corpus:\t%s" % (corpus)
    print "n:\t%i" % (n)
    print "m:\t%i" % (m)
    parser = CorpusParser(corpus,n,m)
    parser.start()

    print "Most frequent ngrams and their frequencies respectively:"
    parser.print_most_frequent()


    # print sum of all frequencies for a number n
    print "The sum of all frequencies is %i" % (sum(parser.ngramtable.values()))

    # parser.get_ngrams_containg("STOP")

    print "===================================================\n\n"

# parse args
def main(args):
    if args.do_all:
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
        step2(corpus,n,m)
        step2(corpus,n-1,m)





if __name__ == '__main__':

    import sys
    import argparse

    p = argparse.ArgumentParser("Parse ngrams from corpus")
    p.add_argument('-corpus', help='corpus path')
    p.add_argument('-n', help='length of ngrams', type=int)
    p.add_argument('-m', help='get top m most frequent words in descending order', type=int)
    p.add_argument('-conditional-prob-file', '--cpf', help='path to word sequence file to calculate probability of word sequence')
    p.add_argument('-do_all', help='Do everything')

    args = p.parse_args(sys.argv[1:])
    main(args)
