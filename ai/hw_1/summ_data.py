import sys

ETA = 1e-9

def solve(low, high, func):
    flow = func(low)
    fhigh = func(high)

    if flow*fhigh > 0: return None
    if flow>fhigh: low,high=high,low

    guess = (low + high) / 2.0

    while abs(low-high) > ETA / 100:
        val = func(guess)
        if abs(val) < ETA: return guess

        if val < 0:
            # too low
            low = guess
        else:
            # too high
            high = guess
        guess = (low+high) / 2.0
    return guess

def effectiveBranch(nodes, depth):
    def costfunc(guess):
        sum = 0
        for ex in range(depth+1):
            sum += pow(guess,ex)
        return sum - (nodes+1)
    return solve(0,10,costfunc)

if __name__ == '__main__':
    datafile = sys.argv[1]

    summaryTmpl = {'puzzles': 0,
                   'visited': 0,
                   'expanded': 0,
                   'max depth':0,
                   'max fringe':0}

    SUMMARY = {}

    f = file(datafile)
    for line in f:
        tmp = line.split(" ")
        puzztype = tmp[0]
        visited = int(tmp[2])
        expanded = int(tmp[3])
        length = int(tmp[4])
        mxdepth = int(tmp[5])
        mxfringe = int(tmp[6])

        if length not in SUMMARY:
            SUMMARY[length] = {'i': summaryTmpl.copy(),
                               'm': summaryTmpl.copy(),
                               'e': summaryTmpl.copy()}
        sum = SUMMARY[length][puzztype]
        sum['puzzles'] += 1
        sum['visited'] += visited
        sum['expanded'] += expanded
        sum['max depth'] += mxdepth
        sum['max fringe'] += mxfringe
    f.close()

    # now print the summary
    header1 = " & " + ("ids" + " & "*5) + ("A* Manhattan" + " & "*5) + ("A* Euclidean" + " & "*5)
    header2 = "d" + (" & visited & expanded & max depth & max fringe & eff branch factor" * 3)
    print header1 + "\\\\"
    print header2 + "\\\\"

    for d,groups in SUMMARY.items():
        line = str(d)
        for tst in ['i','m','e']:
            summ = SUMMARY[d][tst]
            p = float(summ['puzzles'])
            if p != 0:
                v = int(float(summ['visited']) / p)
                e = int(float(summ['expanded']) / p)
                dp = int(float(summ['max depth']) / p)
                f = int(float(summ['max fringe']) / p)
                b = effectiveBranch(v, d)
            else:
                v = "-"
                e = "-"
                dp ="-"
                f = "-"
                b = "-"
            line += (" & %.5s" * 5) % (v,e,dp,f,b)
        print line + "\\\\"

