#!/bin/sh

NUMRUNS=30
DATADIR=data

run=0
while [ ${run} -lt ${NUMRUNS} ] ; do
  echo -n running experiment ${run}...
  datafile=${DATADIR}/data_${run}.dat.gz
  python poker.py | gzip > ${datafile}
  echo done
  run=`expr ${run} + 1`
done

