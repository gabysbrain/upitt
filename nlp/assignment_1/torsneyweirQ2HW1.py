import re
import sys

WORDRE = re.compile('[A-Za-z]+(-[A-Za-z]+])?')
#WORDRE = re.compile('[-A-Za-z]+')

# given a list of word count dictionaries, sum the word counts
def unioncounts(wordcounts):
    total = {}
    for count in wordcounts:
        for word in count:
            total[word] = total.get(word, 0) + count[word]
    return total

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

    # add each file mentioned in the input line to the corpus
    allcounts = [countwords(file(textname.strip(), 'r')) for textname in f]

    # combine all the counts
    totalcounts = unioncounts(allcounts).items()

    # Now there's a list of tuples (word, count) so sort them by count
    totalcounts.sort(lambda x, y: -cmp(x[1], y[1]))

    # print the words with their counts
    for count in totalcounts[:10]:
        print "%s\t%s" % (count[0], count[1])

    f.close()

