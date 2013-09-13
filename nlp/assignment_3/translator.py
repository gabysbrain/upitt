import sys

def parsent(nt):
    def varval(varstr):
        x = varstr.split("=")
        if len(x) == 1: return (x[0], None)
        else: return (x[0], x[1])
    # parse a non term in to (nonterm, [(variable, value)]) pairs
    tmp = nt.replace(']', '').split('[')
    return (tmp[0], [varval(x) for x in tmp[1:]])
    
def parserule(rule):
    lhs,rhs = rule
    if type(rhs) != list: rhs = [rhs]

    return (parsent(lhs), [parsent(nt) for nt in rhs])

def combinent(nt):
    def comb(var, val):
        if val: return "[%s=%s]" % (var, val)
        else: return "[%s=?]" % (var)
    vars = "".join([comb(t[0], t[1]) for t in nt[1]])
    return "%s%s" % (nt[0], vars)
    
def combinerule(rule):
    tmp = [combinent(nt) for nt in rule]
    return (tmp[0], tmp[1:])
    
def findvar(rule, var):
    for nt in rule:
        for v in nt[1]:
            if v[0] == var and not v[1]: return True
    return False

def setvar(var, val, rule):
    newrule = []
    for nt in rule:
        newvars = []
        for v in nt[1]:
            if v[0] == var and not v[1]:
                newvars.append((v[0], val))
            else:
                newvars.append(v)
        newrule.append((nt[0], newvars))
    return newrule
    
def instantiaterules(baserule, varmap):
    convrules = [baserule]
    for var in varmap.keys():
        newrules = []
        for rule in convrules:
            if findvar(rule, var):
                vals = varmap[var]
                newrules += [setvar(var, v, rule) for v in vals]
            else:
                newrules.append(rule)
        convrules = newrules
    return convrules
    
def convert(grammar):
    biggrammar = {}
    vars = {}

    for lhs in grammar.keys():
        for rhs in grammar[lhs]:
            varlhs, varrhs = parserule((lhs, rhs))
            # find variable instantiations and add them to the list
            for nt in [varlhs] + varrhs:
                for var in nt[1]:
                    if var[1]:
                        if var[0] not in vars: vars[var[0]] = []
                        if var[1] not in vars[var[0]]: 
                            vars[var[0]].append(var[1])
    for lhs in grammar.keys():
        for rhs in grammar[lhs]:
            varlhs, varrhs = parserule((lhs, rhs))
            # find uninstantiated variables and add every possible 
            # combination to the grammar
            for rule in instantiaterules([varlhs] + varrhs, vars):
                strrule = combinerule(rule)
                if strrule[0] not in biggrammar: biggrammar[strrule[0]] = []
                biggrammar[strrule[0]].append(strrule[1:])
    return biggrammar

if __name__=='__main__':
    grammar = {}
    gfile = file(sys.argv[1], 'r')
    for line in gfile:
        line = line.strip()
        if line != "":
            tmp = line.split()
            if tmp[0] not in grammar: grammar[tmp[0]] = []
            grammar[tmp[0]].append(tmp[2:])
    gfile.close()
    
    newgrammar = convert(grammar)
    for lhs in newgrammar.keys():
        rhss = newgrammar[lhs]
        for rhs in rhss:
            rhsstr = " ".join(rhs[0])
            print "%s -> %s" % (lhs, rhsstr)

