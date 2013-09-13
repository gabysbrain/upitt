#!/bin/sh

WEKAPATH=/afs/cs.pitt.edu/projects/nlp/PACKAGES/weka-3-4/weka.jar 
datafile=$1
k=$2

rm -rf eval

i=1
while [ ${i} -le ${k} ];
do
    echo generating fold ${i}...
    mkdir -p eval/fold_${i}
    java -Xmx1G -cp ${WEKAPATH} weka.filters.supervised.instance.StratifiedRemoveFolds -i ${datafile} -o eval/fold_${i}/train.arff -N ${k} -F ${i} -V -S 1 -c last
    java -Xmx1G -cp ${WEKAPATH} weka.filters.supervised.instance.StratifiedRemoveFolds -i ${datafile} -o eval/fold_${i}/test.arff -N ${k} -F ${i} -S 1 -c last
    select_attrs.sh eval/fold_${i}/train.arff eval/fold_${i}/train_pp.arff eval/fold_${i}/test.arff eval/fold_${i}/test_pp.arff
    i=`expr $i + 1`
done

echo done

