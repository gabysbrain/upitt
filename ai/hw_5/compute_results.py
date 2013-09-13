import sys

def readmatrix(file):
    rows = []
    readmatrix = False
    for line in file:
        if readmatrix and line.strip()=='': 
            yield rows
            readmatrix = False
            rows = []
        sl = line.strip().split()
        if readmatrix:
            end = sl.index("|")
            col = [int(x) for x in sl[:end]]
            rows.append(col)
        if len(sl) > 0 and sl[0] == 'a': readmatrix = True

def readmatrices(file):
    ms = [m for m in readmatrix(file)]
    return ms

def addmatrices(m1, m2):
    ma = [[c1+c2 for c1,c2 in zip(r1,r2)] for r1,r2 in zip(m1, m2)]
    return ma

def sumcols(m):
    return [sum(col) for col in m]

def sumrows(m):
    sums = [0 for x in range(len(m))]
    for row in m:
        for ci in range(len(row)):
            sums[ci] += row[ci]
    return sums

def numcorrect(m):
    return [m[i][i] for i in range(len(m))]

def precision(m):
    # assumes 2x2 matrix
    if m[0][0] + m[1][0] == 0: return 0.0
    else: return float(m[0][0]) / float(m[0][0] + m[1][0])

def recall(m):
    # assumes 2x2 matrix
    if m[0][0] + m[0][1] == 0: return 0.0
    else: return float(m[0][0]) / float(m[0][0] + m[0][1])

# prints basic statistics computed from a confusion matrix to stdout
def printstats(m):
    header = "size\tnum_right\tnum_wrong\taccuracy\tprecision\trecall\tfscore"
    print header

    samples = 0
    for r in m:
        for c in r:
            samples += c

    # num right is the diagonal
    numright = 0
    for i in range(len(m)):
        numright += m[i][i]

    a = float(numright) / float(samples)
    p = precision(m)
    r = recall(m)
    if p + r == 0: f = 0.0
    else: f = (2 * p * r) / (p + r)
    print ("\t".join(["%s"] * len(header.split("\t")))) % \
          (samples, numright, samples-numright, a, p, r, f)

if __name__ == '__main__':

    # we take a list of files and compute the final confusion matrix
    # which is just all the confusion matrices added together
    f = file(sys.argv[1])
    ms = readmatrices(f)
    f.close()

    for fname in sys.argv[2:]:
        f = file(fname)
        nm = readmatrices(f)
        f.close()
        ms = [addmatrices(m1, m2) for m1,m2 in zip(ms, nm)]

    for m in ms:
        printstats(m)

