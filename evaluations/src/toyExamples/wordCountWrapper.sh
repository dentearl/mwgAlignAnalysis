#!/bin/bash
set -e
set -o pipefail
####################
# Demo evaluation script

####################
# Variables
if [ $# -ne 5 ]; then
    echo 'Error, evaluations take exactly five arguments'
    exit 2
fi

evaluation=$(basename $0)
location=$1
predMaf=$2
registry=$3
tempDir=$4
outDir=$5
trueMaf=$location/truths/ancestor.maf

####################
# valid evaluations must check the registriy
# to see if they should run and if not they
# should exit normally.
run=$(grep $evaluation $registry -c || true)
if [ $run == "0" ]; then
    exit 0
fi

####################
# evaluation code
wc $trueMaf > $outDir/trueMafWordCount.txt
wc $predMaf > $outDir/predMafWordCount.txt
