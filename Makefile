SHELL := /bin/bash -e
export SHELLOPTS = pipefail

trueMaf := ./truth/ancestor.maf
tree := '((simCow:0.18908,simDog:0.16303)sCow-sDog:0.032898,(simHuman:0.144018,(simMouse:0.084509,simRat:0.091589)sMouse-sRat:0.271974)sH-sM-sR:0.020593);'
predictionsDir := predictions
predictions := $(wildcard ${predictionsDir}/*.maf)
evalBinDir := evaluations/bin
evals := $(shell for f in ${evalBinDir}/*; do if [ -x $$f ] && [ ! -d $$f ] ; then echo $$f;  fi; done;)
tempDir = $(shell mktemp -d)
cwd := $(shell pwd)

.PHONY: all clean analyses

all:
	cd evaluations && make all

analyses: $(foreach e,$(basename $(notdir ${evals})),$(foreach p,$(basename $(notdir ${predictions})),analyses/$e-$p/.done))

clean:
	cd evaluations && make clean

analyses/%:
	mkdir -p $$(dirname $@) 
	 $$(find ${evalBinDir} -name $$(dirname $@ | perl -ple 's/.*\/(.*?)\-.*/$$1/')*) \
		$(realpath ${trueMaf}) \
		${cwd}/${predictionsDir}/$$(dirname $@ | perl -ple 's/.*\-(.*)/$$1/').maf \
		${tree} \
		$(realpath ${tempDir}) \
		${cwd}/$$(dirname $@)
	rm -rf ${tempDir}
	touch $@
