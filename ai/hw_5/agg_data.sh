#!/bin/sh

# there's always at least one fold
for file in `ls eval/fold_1/*.results`;
do
    fname=`basename ${file}`
    ARGS=`find . -name ${fname} -mindepth 3`
    python compute_results.py ${ARGS} > eval/${fname}
done

