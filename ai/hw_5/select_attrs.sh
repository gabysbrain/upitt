#!/bin/sh

WEKAPATH=/afs/cs.pitt.edu/projects/nlp/PACKAGES/weka-3-4/weka.jar 
ATTRCLASS=weka.attributeSelection.ChiSquaredAttributeEval
ATTROPTS=-M
SEARCHCLASS=weka.attributeSelection.Ranker
SEARCHOPTS='-N 5'

java -Xmx1G -cp ${WEKAPATH} weka.filters.supervised.attribute.AttributeSelection -S "${SEARCHCLASS} ${SEARCHOPTS}" -E "${ATTRCLASS} ${ATTROPTS}" -i $1 -o $2 -r $3 -s $4 -c last -b

