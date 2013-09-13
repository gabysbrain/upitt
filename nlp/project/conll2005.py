import re
import sys

SEARCHDIRS = {'ADJP': 'left',
              'ADVP': 'right',
              'CONJP': 'right',
              'FRAG': 'right',
              'INTJ': 'left',
              'LST': 'right',
              'NAC': 'left',
              'PP': 'right',
              'PRN': 'left',
              'PRT': 'right',
              'QP': 'left',
              'RRC': 'right',
              'S': 'left',
              'SBAR': 'left',
              'SBARQ': 'left',
              'SINV': 'left',
              'SQ': 'left',
              'UCP': 'right',
              'VP': 'left',
              'WHADJP': 'left',
              'WHADVP': 'right',
              'WHNP': 'left',
              'WHPP': 'right'}

SEARCHPRIS = {'ADJP': ['NNS', 'QP', 'NN', '$', 'ADVP', 'JJ', 'VBN', 'VBG', 
                       'ADJP', 'JJR', 'NP', 'JJS', 'DT', 'FW', 'RBR', 'RBS', 
                       'SBAR', 'RB'],
              'ADVP': ['RB', 'RBR', 'RBS', 'FW', 'ADVP', 'TO', 'CD', 'JJR',
                       'JJ', 'IN', 'NP', 'JJS', 'NN'],
              'CONJP': ['CC', 'RB', 'IN'],
              'FRAG': [],
              'INTJ': [],
              'LST': ['LS', ':'],
              'NAC': ['NN', 'NNS', 'NNP', 'NNPS', 'NP', 'NAC', 'EX', '$', 'CD',
                      'QP', 'PRP', 'VBG', 'JJ', 'JJS', 'JJR', 'ADJP', 'FW'],
              'PP': ['IN', 'TO', 'VBG', 'VBN', 'RP', 'FW'],
              'PRN': [],
              'PRT': ['RP'],
              'QP': ['$', 'IN', 'NNS', 'NN', 'JJ', 'RB', 'DT', 'CD', 'NCD',
                     'QP', 'JJR', 'JJS'],
              'RRC': ['VP', 'NP', 'ADVP', 'ADJP', 'PP'],
              'S': ['TO', 'IN', 'VP', 'S', 'SBAR', 'ADJP', 'UCP', 'NP'],
              'SBAR': ['WHNP', 'WHPP', 'WHADVP', 'WHADJP', 'IN', 'DT', 'S',
                       'SQ', 'SINV', 'SBAR', 'FRAG'],
              'SBARQ': ['SQ', 'S', 'SINV', 'SBARQ', 'FRAG'],
              'SINV': ['VBZ', 'VBD', 'VBP', 'VB', 'MD', 
                       'VP', 'S', 'SINV', 'ADJP', 'NP'],
              'SQ': ['VBZ', 'VBD', 'VBP', 'VB', 'MD', 'VP', 'SQ'],
              'UCP': [],
              'VP': ['TO', 'VBD', 'VBN', 'MD', 'VBZ', 'VB', 'VBG', 'VBP',
                     'VP', 'ADJP', 'NN', 'NNS', 'NP'],
              'WHADJP': ['CC', 'WRB', 'JJ', 'ADJP'],
              'WHADVP': ['CC', 'WRB'],
              'WHNP': ['WDT', 'WP', 'WP$', 'WHADJP', 'WHPP', 'WHNP'],
              'WHPP': ['IN', 'TO', 'FW']}

def reversed(x):
    if hasattr(x, 'keys'):
        raise ValueError("mappings do not support reverse iteration")
    i = len(x)
    while i > 0:
        i -= 1
        yield x[i]

class Sentence(object):
    def __init__(self, lines):
        self.words = [Word(lines[i], i) for i in range(len(lines))]
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
        self.position = None
        self.args = []

class Word(object):
    def __init__(self, line, position):
        self.word = line[0]
        self.position = position
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
            try:
                yield Sentence(lines)
            except Exception:
                pass # don't give the sentence, just reset and start over
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
    v.position = verb.position
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

    try:
        return eval(treeline, {'words': words})
    except:
        sys.stderr.write("'" + treeline + "'\n")
        raise Exception("bad tree")

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

############################################
# computation/filtering functions
############################################

# computes the span for a subtree
def spanify(tree):
    if type(tree) == Word: 
        return (tree, (tree.position, tree.position))
    spans = [spanify(t) for t in tree[1:]]
    minnode = spans[0]
    maxnode = spans[-1]
    if type(minnode) == tuple:
        minspan = minnode[1][0]
    else: 
        minspan = minnode[0][1][0]
    if type(maxnode) == tuple:
        maxspan = maxnode[1][1]
    else: 
        maxspan = maxnode[0][1][1]

    return [(tree[0], (minspan, maxspan))] + spans
    
# removes the span information from a tree
def despanify(tree):
    if type(tree) == tuple: 
        return tree[0]
    elif type(tree) == Word:
        return tree
    else: 
        if type(tree[0]) == tuple: head = tree[0][0]
        else: head = tree[0]
        return [head] + [despanify(t) for t in tree[1:]]
    
# returns the parse tree corresponding to the input span.  Will return None
# if no subtree exactly matches the input span.  Tree must be spanified
def findspan(tree, span):
    if type(tree) == tuple:
        if tree[1] == span: return tree
        else: return None
    elif tree[0][1] == span:
        return tree
    else:
        for subtree in tree[1:]:
            tmp = findspan(subtree, span)
            if tmp: return tmp
    return None

# binarizes the parse tree
def binarize(tree):
    if type(tree) == Word: return tree

    if len(tree) > 3:
        return [tree[0], binarize(tree[1])] + \
               [binarize([tree[0]+'.ext'] + tree[2:])]
    else:
        return [tree[0]] + [binarize(t) for t in tree[1:]]

# returns a tree made only of the nonterminal labels
def structurize(tree):
    if type(tree) == Word: return [tree.pos1]

    return [tree[0]] + [structurize(t) for t in tree[1:]]

# returns a tree structure as a list of integers
def integerize(tree, key={}):
    if 'maxid' not in key: key['maxid'] = 1
    if tree[0] not in key: 
        tmp = key['maxid']
        key[tree[0]] = tmp
        key['maxid'] = tmp + 1
    return [key[tree[0]]] + [integerize(t, key) for t in tree[1:]]

# returns the depth of a tree
def depth(tree):
    if tree == []: return 0
    else: return 1 + max([0] + [depth(t) for t in tree[1:]])

def nonterm(node):
    if type(node) == Word: return node.pos1
    elif type(node[0]) == tuple: return node[0][0]
    else: return node[0]

def lexhead(node):
    if type(node) == Word: return node.word
    else: 
        return node[0][1]

def lexnpsearch(node):
    if type(node[-1]) == Word: return node[-1].word
    for t in reversed(node):
        if nonterm(t) in ('NN', 'NNP', 'NNPS', 'NNS', 'NX', 'JJR') or \
           type(t) == Word:
            return lexhead(t)
    for t in node:
        if nonterm(t) == 'NP': return lexhead(t)
    for t in reversed(node):
        if nonterm(t) in ('$', 'ADJP', 'PRN'): return lexhead(t)
    for t in reversed(node):
        if nonterm(t) == 'CD': return lexhead(t)
    for t in reversed(node):
        if nonterm(t) in ('JJ', 'JJS', 'RB', 'QP'): return lexhead(t)
    return lexhead(node[-1])

def lexgensearch(nt, node):
    try:
        dir = SEARCHDIRS[nt]
        if dir == 'left': searchee = node
        else: searchee = reversed(node)
    
        for item in SEARCHPRIS[nt]:
            for i in searchee:
                if nt == item: return lexhead(i)

        # return the first item
        for t in searchee: return lexhead(t)

    except KeyError:
        pass

    # by default return the first child
    return lexhead(node[0])

# adds head words to the tree so that each non 
# terminal will now be a pair (nt, head)
def lexicalize(tree):
    if type(tree) == Word:
        return tree

    children = [lexicalize(t) for t in tree[1:]]

    if tree[0] == 'NP':
        head = lexnpsearch(children)
    else:
        head = lexgensearch(tree[0], children)

    return [(tree[0], head)] + children

if __name__ == '__main__':
    filename = sys.argv[1]
    s = [t for t in gensentences(filename)]
    for sentid in range(len(s)):
        #print spanify(s[sentid].parsetree)
        #print spanify(binarize(s[sentid].parsetree))
        print findspan(spanify(binarize(s[sentid].parsetree)), (0,2))
        #print findspan(binarize(s[sentid].parsetree), (0,2))
        #print findspan(s[sentid].parsetree, (0,2))
        #printsentence(s[sentid])
        # don't print black line at the end
        #if sentid != len(s)-1:
            #print # blank line between sentences
        tmp = findspan(spanify(binarize(s[sentid].parsetree)), (0,2))
        if tmp: 
            print despanify(tmp)
            tmp = structurize(despanify(tmp))
            print tmp
            print integerize(tmp)

