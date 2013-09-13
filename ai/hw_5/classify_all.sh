#!/bin/sh

WEKAPATH=/afs/cs.pitt.edu/projects/nlp/PACKAGES/weka-3-4/weka.jar 
k=$1

i=1
while [ ${i} -le ${k} ];
do
    echo running fold ${i}...
    classify.sh eval/fold_${i}/train_pp.arff eval/fold_${i}/test_pp.arff eval/fold_${i}/
    i=`expr ${i} + 1`
done
echo done
