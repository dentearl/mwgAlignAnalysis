#/bin/bash
# makefileEvalWrapper.sh
# 19 Oct 2011
# dent earl, dearl (a) soe ucsc edu
#
# This script is called by the project Makefile when performing
# an analysis. This script calls a single evaluation on a single
# prediction and passes along all the proper variables.
# It also verifies that necessary files exist and fails if they 
# do not.
##########
set -e
set -o pipefail

program=$0

evalAndPred=$1
location=$(readlink -f $2)
if [ $3 == "registries/.reg.tab" ]; then
    echo ERROR, you forgot to specify the \'set\' variable. Valid \'set\' options are testSet primates mammals drosophila >&2
    exit 1
fi
registry=$(readlink -f $3)
tmpDir=$(readlink -f $4)
outDir=$(readlink -f $5)

if [ -z $location ]; then
    echo ERROR, specify 'location' >&2
    exit 1
fi
if [ ! -f $registry ]; then
    echo ERROR, "registry=$registry" not found! Valid \'set\' options are testSet primates mammals drosophila >&2
    exit 1
fi

eval=$(readlink -f evaluations/bin/$(dirname $evalAndPred | perl -ple 's/.*\/(.*?)\-.*/$1/')*)
pred=$location/$(dirname $evalAndPred | perl -ple 's/.*\-(.*)/$1/').maf

##############################
mkdir -p $(dirname $evalAndPred)

# call the evaluation
$eval $location $pred $registry $tmpDir $outDir

rm -rf $tempDir
exit 0
