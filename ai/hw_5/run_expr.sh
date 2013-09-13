#!/bin/sh

K=20

echo combining data...
combine_data.sh > /tmp/joined.dat
python csv2arff.py /tmp/joined.dat > /tmp/joined.arff
create_folds.sh /tmp/joined.arff ${K}
classify_all.sh ${K}
echo aggregating results...
agg_data.sh

