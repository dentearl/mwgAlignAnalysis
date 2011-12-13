SHELL := /bin/bash -e
export SHELLOPTS = pipefail
####################
# alignathon Makefile
# October 2011
# dent earl, dearl (a) soe ucsc edu
# 
# This makefile is used to build all evaluations
# as in 'make all', to test the evaluations as
# in 'make test', and to run evaluations on a set
# of predictions for a particular test set as in
# 'make analyses set=testSet location=../testPackage'
#
####################
dirLocation := ${location:%/=%}
predictionsDir := ${dirLocation}/predictions
predictions := $(wildcard ${predictionsDir}/*.maf)
evalBinDir := evaluations/bin
evals := $(shell find ${evalBinDir}/ -perm 755 -type f | grep -v makefileEvalWrapper)
tempDir = $(shell mktemp -d)
cwd := $(shell pwd)
####################

.PHONY: all clean analyses test

all:
	cd evaluations && make all

test:
	cd evaluations && make test

registries/%: registries/%.template
	cp $^ $@.tmp
	mv $@.tmp $@

analyses: registries/${set}.reg.tab $(foreach e,$(basename $(notdir ${evals})),$(foreach p,$(basename $(notdir ${predictions})),${dirLocation}/analyses/$e-$p/.done))
	@if [ -z ${dirLocation} ]; then echo "Error, specify variable 'location'" && exit 1; fi
	@if [ ! -e ${dirLocation} ]; then echo "Error, 'location=${dirLocation}' does not exist" && exit 1; fi
	@if [ ! -d ${dirLocation} ]; then echo "Error, 'location=${dirLocation}' is not a directory" && exit 1; fi

clean:
	cd evaluations && make clean

${dirLocation}/analyses/%:
	@mkdir -p ${dirLocation}/analyses
	${evalBinDir}/makefileEvalWrapper.sh \
		$@ \
		${dirLocation}/ \
		registries/${set}.reg.tab \
		$(realpath ${tempDir}) \
		${cwd}/$$(dirname $@)
	touch $@
