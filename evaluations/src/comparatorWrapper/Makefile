bin := ../../bin
util := ../../util
.PHONY := all test clean

wrappers := comparatorWrapper.py comparatorGenesWrapper.py comparatorRepeatsWrapper.py comparatorRepeatsComplementWrapper.py comparatorNeutralWrapper.py
utilities := comparatorSummarizer.py
binWrappers := $(foreach f,${wrappers},${bin}/$f)
utilUtilities := $(foreach f,${utilities},${util}/$f)

all: ${binWrappers} ${bin}/lib/libComparator.py ${utilUtilities}

test:

clean:
	rm -f ${binWrappers} ${utilUtilities}


$(bin)/%: %
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

${util}/%: %
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

$(bin)/lib/libComparator.py: libComparator.py
	mkdir -p $(dir $@)
	touch $(dir $@)__init__.py
	cp $< $@.tmp
	mv $@.tmp $@

