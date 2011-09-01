SHELL := /bin/bash -e
export SHELLOPTS = pipefail

trueMaf := ./truth/ancestor.maf
tree := '((simCow:0.18908,simDog:0.16303)sCow-sDog:0.032898,(simHuman:0.144018,(simMouse:0.084509,simRat:0.091589)sMouse-sRat:0.271974)sH-sM-sR:0.020593);'
predictionsDir := ./predictions
predictions := $(wildcard ${predictionsDir}/*.maf)
evalBinDir := evaluations/bin
#evals := $(shell for f in ${evalBinDir}/*; do if [ -x $$f ] && [ ! -d $$f ] ; then echo $$f;  fi; done;)
evals := $(wildcard ${evalBinDir}/*)

.PHONY: all clean analyses

all:
	cd evaluations && make all

analyses: $(foreach e,${evals},analyses/$e-$(foreach p,${predictions},$p))
	@echo 'analyses:'
	@mkdir -p analyses
	@echo 'all inputs: '$<
	@echo 'evals: ' ${evals}
	@echo 'predictions: ' ${predictions}

clean:
	cd evaluations && make clean

analyses/%:
	@echo 'analyses/%'
	mkdir -p $@
	echo $@
	echo $*
