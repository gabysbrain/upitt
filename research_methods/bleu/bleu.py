import sys
from math import log
from math import exp

def mylog(x):
    if x == 0: return float(-sys.maxint-1)
    else: return log(x)
    
def ngrams(sent, n):
    return [tuple(sent[i:i+n]) for i in range(len(sent)-n+1)]

def countcorrect(cand, refs):
    # count maxrefs and initialize match counts
    maxrefs = {}
    matches = {}
    for word in cand:
        if word not in maxrefs: maxrefs[word] = 0
        matches[word] = 0
        for ref in refs:
            maxrefs[word] = max(maxrefs[word], ref.count(word))

    for word in cand:
        ct = sum([ref.count(word) for ref in refs])
        matches[word] = max(matches[word], min(maxrefs[word], ct))
            
    return sum(matches.values())

def tokenize(strsent):
    return strsent.lower().split(" ")

def agglogbleu(cand, refs, N):
    aggnum = 0
    for n in range(1, N+1):
        ngcand = ngrams(cand, n)
        ngrefs = [ngrams(r, n) for r in refs]
        numcorrect = countcorrect(ngcand, ngrefs)
        aggnum += mylog(numcorrect / float(len(ngcand)))
    return aggnum / float(N)

def closest(num, candnums):
    mindist = abs(num-candnums[0])
    minnum = candnums[0]
    for cn in candnums[1:]:
        tmp = abs(num-cn)
        if tmp < mindist:
            mindist = tmp
            minnum = cn
    return minnum

def bleu(cand, refs, N):
    tmp = agglogbleu(cand, refs, N)
    candlen = len(cand)
    refslen = [len(r) for r in refs]
    sbp = min(1 - (closest(candlen, refslen) / float(candlen)), 0)
    return exp(sbp + tmp)

if __name__ == '__main__':
    N = int(sys.argv[1])
    f = open(sys.argv[2])

    sentid = None
    cand = None
    refs = [None] * 3
    linenum = 0
    for line in f:
        if line.strip() == "": continue

        if linenum == 0: 
            sentid = line.strip()
        elif linenum == 1:
            cand = tokenize(line.strip())
        else:
            refs[linenum-2] = tokenize(line.strip())
        linenum = (linenum + 1) % 5
        if linenum == 0:
            b = bleu(cand, refs, N)
            print sentid, b
    f.close()

