bin := ../../bin
util := ../../util
.PHONY := all test clean

wrappers := coverageCopyNumWrapper.py
utilities := 
utilLibs := libStem.py
binWrappers := $(foreach f,${wrappers},${bin}/$f)
utilUtilities := $(foreach f,${utilities},${util}/$f)
utilLibUtilities :=$(foreach f,${utilLibs},${util}/lib/$f)

all: ${binWrappers} ${utilUtilities} ${utilLibUtilities}

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

${util}/lib/%: %
	mkdir -p $(dir $@)
	touch ${util}/__init__.py
	touch ${util}/lib/__init__.py
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@
