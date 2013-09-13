import re
import sys

# Don't want to pick up capital letters in the middle of words
CAPRE = re.compile('\s[A-Z][-A-Za-z]+|^[A-Z][-A-Za-z]+')

# counts the capitalized words in the given input file
def countcaps(file):
    found = re.findall(CAPRE, file.read())
    return len(found)

if __name__ == '__main__':
    filename = sys.argv[1]
    f = file(filename, 'r')

    # add each file mentioned in the input line to the corpus
    totalcaps = 0
    for textname in f:
        docfile = file(textname.strip(), 'r')
        totalcaps += countcaps(docfile)
        docfile.close()

    # print the words with their counts
    print totalcaps

    f.close()

