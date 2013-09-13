import sys
import re
import math

class HMM(object):
    STARTTAG = "start"
    ENDTAG = "."
    def __init__(self):
        self.tagcounts = {}
        self.wordcounts = {}
        self.wordtagcounts = {}
        self.tagtagcounts = {}
        self.lasttag = self.STARTTAG

    def train(self, word, tag):
        # the first tag seen will also need the start tag incremented
        if self.lasttag==self.STARTTAG: 
            self.tagcounts[self.STARTTAG] = \
                    self.tagcounts.get(self.STARTTAG, 0) + 1
        # increment all relevent counts
        self.tagcounts[tag] = self.tagcounts.get(tag, 0) + 1
        self.wordcounts[word] = self.wordcounts.get(word, 0) + 1
        wt = (word, tag)
        tt = (tag, self.lasttag)
        self.wordtagcounts[wt] = self.wordtagcounts.get(wt, 0) + 1
        self.tagtagcounts[tt] = self.tagtagcounts.get(tt, 0) + 1

        # the end of sentence tag resets the previous tag
        if tag == self.ENDTAG: self.lasttag = self.STARTTAG
        else: self.lasttag = tag

    def wordtagprob(self, word, tag):
        tmp = self.wordcounts[word]
        wtp = self.wordtagcounts.get((word, tag),0) + 1
        tc = self.tagcounts[tag] + len(self.wordcounts)
        return float(wtp) / float(tc)

    def tagtagprob(self, tag1, tag2):
        """computes probability of tag1 given tag2"""
        ttp = self.tagtagcounts.get((tag1, tag2), 0) + 1
        tc = self.tagcounts[tag2] + len(self.tagcounts)
        return float(ttp) / float(tc)

    def missingwords(self, sentence):
        """returns a list of words that are not recognized by the hmm"""
        return [x for x in sentence if x not in self.wordcounts]
        
    def tag(self, sentence):
        """returns a sequence of (word, tag) pairs.  
           sentence is a list of words
        """
        # missing words will screw up the viterbi algorithm
        if len(self.missingwords(sentence)) > 0: 
            return None
        return viterbi(self, sentence)
    
def log2(x):
    return math.log(x) / math.log(2)

def viterbi(hmm, sentence):
    # lastcol and col store the i-1 and i probabilities and tag sequences
    # we don't need to keep the entire table in memory
    lastcol = {}
    tags = hmm.tagcounts.keys()

    for tag in tags:
        word = sentence[0]
        ttp = hmm.tagtagprob(tag, 'start')
        wtp = hmm.wordtagprob(word, tag)
        # compute start state tag probabilities
        lastcol[tag] = (log2(ttp) + log2(wtp), [tag])

    for word in sentence[1:]:
        col = {}
        for tag in tags:
            # comparisons of x > None are always True
            maxprob = None
            for lasttag in tags:
                ttp = hmm.tagtagprob(tag, lasttag)
                wtp = hmm.wordtagprob(word, tag)
                prevprob, prevseq = lastcol[lasttag]
                newprob = prevprob + log2(ttp) + log2(wtp)
                # logs of numbers < 1 are negative
                if newprob > maxprob:
                    maxprob = newprob
                    maxseq = prevseq + [tag]

            col[tag] = (maxprob, maxseq)
        lastcol = col

    # max will compare based on the first argument
    return max(lastcol.values())
    
def pairword(wordtagtxt):
    spt = wordtagtxt.split("/")
    # There may be backslashed slashes in the word so recombine them
    wordtxt = "/".join(spt[0:-1]).lower()
    tagtxt = spt[-1]
    return (wordtxt, tagtxt)

def splitsent(sentencetxt):
    """splits a sentence in the form of w1/t1 w2/t2 into (word, tag) pairs"""
    return [pairword(txt) for txt in re.split(" +", sentencetxt)]

def train(hmm, corpusfile):
    f = open(corpusfile)
    for line in f:
        c = open(line.strip())
        for sent in c:
            for word, tag in splitsent(sent.strip()): 
                hmm.train(word, tag)
        c.close()
    f.close()
    
def test(hmm, corpusfile):
    f = open(corpusfile)
    for line in f:
        c = open(line.strip())
        for sent in c:
            # tagger doesn't need pos information, that would be cheating
            words = [w for w,pos in splitsent(sent.strip())]
            tmp = hmm.tag(words)
            if tmp:
                score,tags = tmp
                # put the tag sequence with the words in the input format
                print " ".join([x+"/"+y for x,y in zip(words, tags)])
            else:
                print "No answer: the following were not in the train data", \
                      repr(hmm.missingwords(words))
            print
        c.close()
    f.close()
    
if __name__ == '__main__':
    # read a list of files in the corpus
    trainset = sys.argv[1]
    testset = sys.argv[2]

    hmm = HMM()
    train(hmm, trainset)
    test(hmm, testset)
    
