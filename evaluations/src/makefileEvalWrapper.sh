#/bin/bash
#
#
##########
set -e
set -o pipefail

evalAndPred=$1
location=$(readlink -f $2)
registry=$(readlink -f $3)
tmpDir=$(readlink -f $4)
outDir=$(readlink -f $5)

eval=$(readlink -f evaluations/bin/$(dirname $evalAndPred | perl -ple 's/.*\/(.*?)\-.*/$1/')*)
pred=$location/$(dirname $evalAndPred | perl -ple 's/.*\-(.*)/$1/').maf

mkdir -p $(dirname $evalAndPred)
echo eval $eval 
echo pred $pred 
echo location $location 
echo registry $registry 
echo tmpDir $tmpDir 
echo outDir $outDir
rm -rf $tempDir

exit 0
# if [ -z ${set} ]; then 
#     echo "Error, specify variable 'set'" && exit 1; 
# fi
# if [[ ${set} != "testSet" && ${set} != "primates" && ${set} != "mammals" && ${set} != "drosophila" ]]; then 
#     echo "Error, 'set' must be equal to one of 'testSet' 'primates' 'mammals' 'drosophila'" && exit 1; 
# fi
# if [ ! -e registries/${set}.reg.tab ]; then echo "Error, unable to find registry file 'registries/${set}.reg.tab'" && exit 1; fi
# if [ -z ${location} ]; then echo "Error, specify variable 'location'" && exit 1; fi
# if [ ! -d ${location} ]; then echo "Error, location=${location} does not appear to be a directory" && exit 1; fi
# mkdir -p $$(dirname $@) 
# $(find ${evalBinDir} -name $$(dirname $@ | perl -ple 's/.*\/(.*?)\-.*/$$1/')*) \
#     ${location}/$$(dirname $@ | perl -ple 's/.*\-(.*)/$$1/').maf \
#     registries/${set}.reg.tab
#    $(realpath ${tempDir}) \
# 	${cwd}/$$(dirname $@)
# rm -rf $tempDir
