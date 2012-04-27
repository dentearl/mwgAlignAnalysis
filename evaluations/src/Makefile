bin:= ../bin

####################
# MAKE EDITS IN THIS BOX
# place the name of your directory at the end of
# the 'evaluations' list
evaluations := comparatorWrapper coverageCopyNumWrapper toyExamples
libraries := libWrapper.py

# DO NOT EDIT BELOW THIS LINE
####################
.PHONY = all test clean %.all %.test clean.%
evalBins:= $(foreach f,$(shell find ${bin} -type f -perm -o+x), all.$(notdir $f))

all : ${libraries:%=${bin}/lib/%} ${evaluations:%=%.all}

%.all: %
	cd $* && make all

test : evals.tested ${evaluations:%=%.test}

evals.tested:
	python2.6 ./test.evaluations.py -v

%.test: 
	cd $* && make test

$(bin)/lib/%: %
	mkdir -p $(dir $@)
	touch $(dir $@)/__init__.py
	cp $< $@.tmp
	mv $@.tmp $@

clean: ${evaluations:%=clean.%}
	rm -rf ${bin}

clean.%: %
	cd $* && make clean
