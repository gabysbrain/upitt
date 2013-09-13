import sys
import random

N = 5

def arrayfile(filename):
    f = open(filename)
    arr = [line.strip for line in f]
    f.close()
    return arr

def chunk(data):
    newseq = []
    n = len(seq) / N    # min items per subsequence
    r = len(seq) % N    # remaindered items
    b,e = 0, n + min(1, r)  # first split
    for i in range(p):
    newseq.append(seq[b:e])
    r = max(0, r-1)  # use up remainders
    b,e = e, e + n + min(1, r)  # min(1,r) is always 0 or 1
    return newseq

def flatten(chunk):
    output = []
    for c in chunk:
        output += c
    return output

def writechunks(basename, chunks):
    for i in range(len(chunks)):
        testchunk = chunks[i]
        trainchunks = chunks[:0] + chunks(i+1:)
        writefile(basename + '.test.' + str(i), testchunk)
        writefile(basename + '.train.' + str(i), trainchunk)

def writefile(name, chunk):
    f = open(name, 'w')
    writelines(chunk)
    f.close()

if __name__ == '__main__':
    fname = sys.argv[1]
    data = arrayfile(fname)
    randdata = random.shuffle(data)
    chunkdata = chunk(randdata)
    writechunks(fname, chunkdata)

