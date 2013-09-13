#!/bin/sh

WEKAPATH=/afs/cs.pitt.edu/projects/nlp/PACKAGES/weka-3-4/weka.jar 
STATSCMD="grep -A 5 Confusion"

java -Xmx1G -cp ${WEKAPATH} weka.classifiers.rules.ZeroR -t $1 -T $2 -i | ${STATSCMD} > $3/zeror.results
java -Xmx1G -cp ${WEKAPATH} weka.classifiers.bayes.NaiveBayes -t $1 -T $2 -i | ${STATSCMD} > $3/nb.results
java -Xmx1G -cp ${WEKAPATH} weka.classifiers.trees.J48 -t $1 -T $2 -i | ${STATSCMD} > $3/j48.results

