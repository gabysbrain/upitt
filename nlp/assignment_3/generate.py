from random import choice
from string import *
import sys

argfile = open(sys.argv[1],'r')
line = argfile.readline()
grammar = {}
while line != "":
   x = line.split()
   if not grammar.has_key(x[0]):
      grammar[x[0]] = []
   if len(x[2:]) > 1:   
      grammar[x[0]].append(x[2:])
   else:
      grammar[x[0]].append(x[2])
   line = argfile.readline()
argfile.close()

# The grammar is now a dictionary.
#   The LHS of the rule is the key.
#   The RHS is a list.  Each element of this
#     list is an alternative.  Nested lists are
#     and-nodes (all components must be generated
#     if you choose that alternative)
# That is:
#     LHS --> alt1-1 alt1-2 
#     LHS --> alt2 
#     LHS --> alt3-1 alt3-2
# Becomes:  LHS: [[alt1-1,alt1-2], [alt2], [alt3-1, alt3-2]]

def generate(phrase):
   """ generate a phrase in the form of a list of words """
   # example: phrase=[NP,VP]
   if type(phrase) == type([]):
      return mappend(generate, phrase)
   # example:  phrase=S
   elif grammar.has_key(phrase): 
       return generate(choice(grammar[phrase]))
   # example: phrase=woman
   else: return [phrase]
                                                                     
def generateTree(phrase):
   """ generate a parse tree.  Must be called with a non-terminal of the grammar. """
   ch = choice(grammar[phrase])
   if not type(ch) == type([]):
      if grammar.has_key(ch):
         return [phrase,generateTree(ch)]
      else:
         return [phrase,ch]
   else:
      toreturn = [phrase]
      for c in ch:
         toreturn.append(generateTree(c))
      return toreturn

def mappend(fn,lst):
   """Append together the results of calling fn on each element of list."""
   new = []
   for i in lst:  new = new + fn(i)
   return new

def prettyPrint(lst,spaces=""):
   if lst == []:
      return []
   # no lists inside; just print the line
   elif not [1 for x in lst if type(x)==type([])]:
      print "%s%s" % (spaces,lst)
   elif not type(lst[0]) == type([]):
      toprint = spaces + "[" + lst[0] + " "
      print toprint
      for x in lst[1:]:
         prettyPrint(x,spaces + "   ")

print "===Sentences==="

for i in range(0,5):
   print join(generate('S'))

print "===Sentence Trees==="
for i in range(0,2):
  prettyPrint(generateTree('S'))


#print "===NP Trees==="
#for i in range(0,2):
  #prettyPrint(generateTree('NP'))

