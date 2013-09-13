import re
import sys
from conll2005 import *

def arrayify(tree):
    queue = []
    array = []
    queue.append(tree)
    while len(queue) > 0:
        t = queue.pop(0)
        array.append(t[0])
        for tmp in t[1:]:
            queue.append(tmp)
    return array
    
if __name__ == '__main__':
    filename = sys.argv[1]
    s = [t for t in gensentences(filename)]
    argtrees = []
    keymap = {}
    for sent in s:
        for verb in sent.targetverbs:
            for arg in verb.args:
                if type(arg) ==list and arg[0] != 'V':
                    span = (arg[1].position, arg[-1].position)
                    #print span
                    tmp = findspan(spanify(binarize(sent.parsetree)), span)
                    if tmp: 
                        tmp = integerize(structurize(despanify(tmp)), keymap)
                        argtrees.append((arg[0], tmp))
                    else:
                        s = "%s %s\n" % \
                            (arg[0], repr([(w.word, w.pos1) for w in arg[1:]]))
                        sys.stderr.write(s)
    lists = [arrayify(tree) for at, tree in argtrees]

    sum = 0
    for t in argtrees:
        sum += depth(t[1])
    print sum / len(argtrees)

    maxtreelen = min(10, max([len(l) for l in lists]))

    # print ARFF file header
    #print "@RELATION trees"
    #for i in range(maxtreelen):
        #print "@ATTRIBUTE n%d NUMERIC" % (i)
    #print

    # ARFF file data section
    #print "@DATA"
    #for l in lists:
        #l = l[0:10]
        #padnum = maxtreelen - len(l)
        #padlist = l + ([0] * padnum)
        #print ",".join([str(t) for t in padlist])


