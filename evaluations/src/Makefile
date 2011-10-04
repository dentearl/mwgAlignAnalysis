bin:= ../bin

####################
# MAKE EDITS IN THIS BOX
# place the name of your directory at the end of
# the 'evaluations' list
evaluations := comparatorWrapper

# DO NOT EDIT BELOW THIS LINE
####################
.PHONY = all test clean %.all %.test clean.%
evalBins:= $(foreach f,$(shell find ${bin} -type f -perm -o+x), all.$(notdir $f))

all : ${bin}/lib/libCall.py ${evaluations:%=%.all}

%.all: %
	cd $* && make all

test : evals.tested ${evaluations:%=%.test}

evals.tested:
	python2.6 ./testEvaluationsSimple.py --evalsDir ${bin}

%.test: 
	cd $* && make test

$(bin)/lib/libCall.py: libCall.py
	mkdir -p $(dir $@)
	touch $(dir $@)/__init__.py
	cp $< $@.tmp
	mv $@.tmp $@

clean: ${evaluations:%=clean.%}
	rm -rf ${bin}

clean.%: %
	cd $* && make clean
