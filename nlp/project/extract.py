#! /usr/bin/python

import sys
import conll2005

COLNAMES = ["constituent", "nonterm", "lex_head", "bag_of_words", 
            "path", "target_verb", "arg_type"]

PRINTSEP = "|"

def printtree(tree):
    if type(tree) == conll2005.Word:
        return tree.pos1 + " " + tree.word + " 1," + \
               tree.word + " " + tree.word + " 0"

    numchildren = len(tree[1:])
    node = tree[0]
    mytxt = node[0] + " " + node[1] + " " + str(numchildren)
    for node in tree[1:]:
        mytxt += PRINTSEP + printtree(node)
    return mytxt
    
def subtreeitr(tree):
    # first print the whole tree
    yield tree

    # then yield a dfs of the subtrees
    if type(tree) != conll2005.Word:
        for st in tree[1:]:
            for tmp in subtreeitr(st): 
                yield tmp

def bagofwords(tree):
    if type(tree) == conll2005.Word:
        return [tree.word]

    # otherwise this is a tree
    l = []
    for t in tree[1:]:
        l += bagofwords(t)
    return l

def pathtoverb(tree, verb):
    # base case
    if type(tree) == conll2005.Word:
        if tree.position == verb.position: return [tree]
        else: return None

    for st in tree[1:]:
        tmp = pathtoverb(st, verb)
        if tmp: return [tree] + tmp
    return None

def pathtoconstit(tree, constit):
    # base case 1
    if tree == constit:
        return [tree]
    # base case 2
    if type(tree) == conll2005.Word:
        return None

    for st in tree[1:]:
        tmp = pathtoconstit(st, constit)
        if tmp: return [tree] + tmp
    return None

def unifypaths(p1, p2):
    # find the first difference in the paths 
    # the previous matching node is the root
    pathrem = 0
    for tmp in zip(p1, p2):
        if tmp[0] == tmp[1]: 
            head = tmp[0]
            pathrem += 1
        else:
            return (head, p1[pathrem:], p2[pathrem:])
    # it's possible we've fallen off the end but found the head
    return (head, p1[pathrem:], p2[pathrem:])

def extractnt(tree):
    if type(tree) == conll2005.Word: return tree.pos1
    else: return tree[0]

# returns path from constituent to the verb
def argpath(tree, constit, verb):
    vp = pathtoverb(tree, verb)
    cp = pathtoconstit(tree, constit)
    hd, vpp, cpp = unifypaths(vp, cp)
    ehd = extractnt(hd)
    evpp = [extractnt(t1) for t1 in vpp]
    ecpp = [extractnt(t2) for t2 in cpp]
    return " > ".join(evpp) + ehd + " < ".join(ecpp)

def printheader():
    print "\t".join(COLNAMES)

# main script here
printheader()
filename = sys.argv[1]
for sent in conll2005.gensentences(filename):
    for constit in subtreeitr(sent.parsetree):
        lexconstit = conll2005.lexicalize(constit)
        #print printtree(lexconstit)
        bow = bagofwords(constit)
        span_constit = conll2005.spanify(constit)
        if type(span_constit[0]) == conll2005.Word:
            topspan = span_constit[1]
        else:
            topspan = span_constit[0][1]
        for verb in sent.targetverbs:
            #print argpath(sent.parsetree, constit, verb)
            argspans = [(x[1].position, x[-1].position) for x in verb.args \
                         if type(x) == list]
            argtypes = [x[0] for x in verb.args if type(x)==list]
            try:
                argidx = argspans.index(topspan)
                argtype = argtypes[argidx]
            except ValueError:
                argtype = None
            if type(constit) == conll2005.Word:
                nonterm = constit.pos1
            else:
                nonterm = constit[0][0]
            print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                      (printtree(lexconstit), 
                       nonterm,
                       conll2005.lexhead(lexconstit),
                       bow,
                       argpath(sent.parsetree, constit, verb),
                       verb.target,
                       argtype)

