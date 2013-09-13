#!/bin/sh

STATEFILES="data/NewYork.train data/Ohio.train"
CENSUSFILE=data/census.txt

# first sort the 2 files
tail -n +3 ${CENSUSFILE} | sort -t '	' -k 1,2 > /tmp/tmp1.tmp
sort -t '	' -k 3,4 ${STATEFILES} > /tmp/tmp2.tmp

./compute_header.sh
join -a 2 -t '	' -1 1 -2 3 /tmp/tmp1.tmp /tmp/tmp2.tmp

