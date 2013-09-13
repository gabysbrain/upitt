#!/bin/sh

WEKAPATH=/afs/cs.pitt.edu/projects/nlp/PACKAGES/weka-3-4/weka.jar
ATTRCLASS=weka.attributeSelection.ChiSquaredAttributeEval
ATTROPTS=-M
SEARCHCLASS=weka.attributeSelection.Ranker
SEARCHOPTS='-N 5'

echo combining data...
combine_data.sh > /tmp/joined.dat
hard_select_attrs.sh /tmp/joined.dat /tmp/joined_pp.dat
python csv2arff.py /tmp/joined_pp.dat > /tmp/joined_pp.arff
java -Xmx1G -cp ${WEKAPATH} weka.classifiers.trees.J48 -t /tmp/joined_pp.arff -d classifier.model
#classify_all.sh ${K}
#echo aggregating results...
#agg_data.sh

