bin := ../../bin
util := ../../util
.PHONY := all test clean

wrappers := indelDistributionWrapper.py
utilities := indelDistributionSummarizer.py
binWrappers := $(foreach f,${wrappers},${bin}/$f)
utilUtilities := $(foreach f,${utilities},${util}/$f)

all: ${binWrappers} ${utilUtilities}

test:

clean: 
	rm -f ${binWrappers} ${utilUtilities}

${bin}/%: %
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

${util}/%: %
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@
