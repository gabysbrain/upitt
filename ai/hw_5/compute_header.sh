#!/bin/sh

# header for state file is not in the file
STATEHEADER='state	city	zipcode	occupation	name	date	amount	candidate'

# header for census file is the second line
CENSUSHEADER=`tail -n +2 data/census.txt | head -n 1`
#CENSUSHEADER=`tail -n +1 data/census.txt | head -n 1`

join_field=`echo "${STATEHEADER}" | cut -d '	' -f 3`
state_rest=`echo "${STATEHEADER}" | cut -d '	' -f 1-2,4-`
census_rest=`echo "${CENSUSHEADER}" | cut -d '	' -f 2-`

echo "${join_field}	${census_rest}	${state_rest}"

