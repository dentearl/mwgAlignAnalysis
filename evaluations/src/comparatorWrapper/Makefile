bin := ../../bin
.PHONY := all test clean

wrappers := comparatorWrapper.py comparatorGenesWrapper.py comparatorRepeatsWrapper.py comparatorNeutralWrapper.py
binWrappers := $(foreach f,${wrappers},${bin}/$f)

$(bin)/%: %
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

$(bin)/lib/libComparator.py: libComparator.py
	mkdir -p $(dir $@)
	touch $(dir $@)__init__.py
	cp $< $@.tmp
	mv $@.tmp $@

all: ${binWrappers} ${bin}/lib/libComparator.py

test:

clean:
	rm -f ${binWrappers}
