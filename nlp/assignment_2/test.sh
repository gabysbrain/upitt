#!/bin/sh

#TRAINFILE=/afs/cs.pitt.edu/courses/2731/corpora/hw2/doclistfiles/docList.train.small
TRAINFILE=/afs/cs.pitt.edu/courses/2731/corpora/hw2/doclistfiles/docList.train.100-102
#TESTFILE=/afs/cs.pitt.edu/courses/2731/corpora/hw2/doclistfiles/docList.train.small
#TESTFILE=/afs/cs.pitt.edu/courses/2731/corpora/hw2/doclistfiles/docList.test.small
TESTFILE=/afs/cs.pitt.edu/courses/2731/corpora/hw2/doclistfiles/docList.train.100-102

python torsneyweirHW2.py ${TRAINFILE} ${TESTFILE}

