import re
import sys
from math import sqrt

WORDRE = re.compile('[A-Za-z]+(-[A-Za-z]+])?')
#WORDRE = re.compile('[-A-Za-z]+')

# calculates the length of a word vector
def vectorlength(words):
    length = 0
    for count in words.values():
        length += count * count
    return sqrt(length)

# calculates the dot product of 2 word vectors
def dotprod(w1, w2):
    total = 0
    for word in w1.keys():
        if word in w2:
            total += w1[word] * w2[word]
    return total

# computes cosine similarity of 2 word vectors
def cossimilarity(w1, w2):
    return dotprod(w1, w2) / (vectorlength(w1) * vectorlength(w2))

# counts the words in the given input file
def countwords(file):
    wordcounts = {}
    for match in re.finditer(WORDRE, file.read()):
        word = match.group().lower()
        #word = match.group()
        wordcounts[word] = wordcounts.get(word, 0) + 1
    return wordcounts

if __name__ == '__main__':
    filename = sys.argv[1]
    f = file(filename, 'r')

    docnames = [t.strip() for t in f]

    # add each file mentioned in the input line to the corpus
    allcounts = [(docname, countwords(file(docname, 'r'))) 
                 for docname in docnames]

    # print the similarities for each pair of documents
    for c1 in allcounts:
        for c2 in allcounts:
            print "%s\t%s\t%s" % (c1[0], c2[0], cossimilarity(c1[1], c2[1]))

    f.close()

