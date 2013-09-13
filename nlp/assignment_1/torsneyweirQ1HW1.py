import re
import sys

class Sentence(object):
    def __init__(self, lines):
        self.words = [Word(l) for l in lines]
        self.parsetree = createparsetree(self.words, lines)
        self.chunks = createchunks(self.words, lines)
        self.clauses = createclauses(self.words, lines)
        self.targetverbs = [createtvs(self.words, lines, colid) 
                            for colid in range(9, len(lines[0]))]

        setupnes(self.words, lines)

class Verb(object):
    def __init__(self):
        self.target = None
        self.sense = None
        self.args = []

class Word(object):
    def __init__(self, line):
        self.word = line[0]
        self.pos1 = line[1]
        self.pos2 = line[4]
        if line[8] != '-': self.targetverb = line[8]
        else: self.targetverb = None
        if line[7] != '-': self.verbsense = line[7]
        else: self.verbsense = None

        self.neclass = None
        self.netotal = None

############################################
# processing functions for the input
############################################

def gensentences(filename):
    f = file(filename, 'r')

    # process one sentence at a time
    lines = []
    for line in f:
        if line.strip() == '': 
            yield Sentence(lines)
            lines = []
        else:
            # some lines have spaces after them
            lines.append(re.split(' +', line.strip()))
    if len(lines) > 0:
        yield Sentence(lines) # don't forget the last sentence!
    f.close()

def createparsetree(words, lines):
    # need to remove the tuple created by createtree
    return createtree(words, lines, 5)[0]

def createchunks(words, lines):
    return list(createtree(words, lines, 2))

# The clauses have characters at the end which get picked 
# up here and screw everything up later
def filterclauses(clause):
    first = True
    newclause = []
    for node in clause:
        if type(node) == str and first: newclause.append(node)
        elif type(node) == Word: newclause.append(node)
        elif type(node) == list: newclause.append(filterclauses(node))
        first = False
    return newclause

def createclauses(words, lines):
    return filterclauses(list(createtree(words, lines, 3)))

def setupnes(words, lines):
    nes = [ne for ne in list(createtree(words, lines, 6)) if type(ne) == list]
    for negroup in nes:
        neclass = negroup[0]
        for word in negroup[1:]:
            word.neclass = neclass
            word.netotal = negroup[1:]

def createtvs(words, lines, colnum):
    #tv = [x for x in list(createtree(words, lines, colnum)) if type(x) == list]
    tv = [x for x in list(createtree(words, lines, colnum))]

    # find the verb.  We need some information from it
    for tmp in tv:
        if type(tmp) == list and tmp[0] == 'V': verb = tmp[1]
    
    v = Verb()
    v.target = verb.targetverb
    v.sense = verb.verbsense
    v.args = tv
    return v

def createtree(words, lines, colnum):
    wordindex = 0
    treeline = ''
    for line in lines:
        tmp = line[colnum].strip()
        # a bunch of transformations to get their tree format 
        # into python's list format
        tmp = re.sub(r'([^()*]+)', r'"""\1""", ', tmp)
        tmp = re.sub(r'\(', '[', tmp)
        tmp = re.sub(r'\)', '], ', tmp)
        tmp = re.sub(r'\*', 'words[%s], ' % (wordindex), tmp)
        treeline += tmp
        wordindex += 1
    return eval(treeline, {'words': words})

############################################
# output functions
############################################

# generator function to print a tree.  Using a generator so it maintains
# where we are in the tree in between calls so I can just write a normal
# tree traversal function and have it stop every time it hits a word like
# the input file format
def printtree(tree, printendnonterm=False):
    if type(tree) == Word: yield '*'
    else:
        nonterm = tree[0]
        prefix = '(' + nonterm
        if printendnonterm: suffix = nonterm + ')'
        else: suffix = ')'

        # need to use indexes so we can see when we've hit the last item
        for nodeid in range(1, len(tree)):
            node = tree[nodeid]
            subtreetxts = [x for x in printtree(node, printendnonterm)]
            for txtid in range(0, len(subtreetxts)):
                txt = subtreetxts[txtid]
                # if we're on the last item we need to print the closing parens
                if txtid == len(subtreetxts)-1 and \
                   nodeid==len(tree)-1: 
                    yield prefix + txt + suffix
                else: 
                    yield prefix + txt
                prefix = ''

# Things like chuncks and clauses are actually forests
def printforest(forest, printendnonterm=False):
    for tree in forest:
        for tmp in printtree(tree, printendnonterm):
            yield tmp

def printne(word):
    # figure out how to print the named entity column
    if word.neclass:
        wordidx = word.netotal.index(word)
        if len(word.netotal) == 1: netxt = '(' + word.neclass + '*)'
        elif wordidx == 0: netxt = '(' + word.neclass + '*'
        elif wordidx == len(word.netotal)-1: netxt = '*)'
        else: netxt = '*'
    else: netxt = '*'
    return netxt
    
def printsentence(sentence):
    chunkgen = printforest(sentence.chunks)
    clausegen = printforest(sentence.clauses, True)
    ptgen = printtree(sentence.parsetree)
    tvgens = [printforest(tv.args) for tv in sentence.targetverbs]
    for word in sentence.words:
        if word.targetverb:
            tgttxt = word.targetverb
            sensetxt = word.verbsense
        else:
            tgttxt = '-'
            sensetxt = '-'
        printtxt = "%s    %s    %s    %s    %s    %s    %s    %s    %s" + \
                   ("    %s" * len(sentence.targetverbs))
        printargs = [word.word, word.pos1, chunkgen.next(), clausegen.next(), \
                     word.pos2, ptgen.next(), printne(word), sensetxt, tgttxt]+\
                    [tvgen.next() for tvgen in tvgens]
        print printtxt % tuple(printargs)

if __name__ == '__main__':
    filename = sys.argv[1]
    s = [t for t in gensentences(filename)]
    for sentid in range(len(s)):
        printsentence(s[sentid])
        # don't print black line at the end
        if sentid != len(s)-1:
            print # blank line between sentences

