bin := ../../bin
.PHONY := all test clean

comparators := comparatorWrapper.py comparatorGenesWrapper.py comparatorRepeatsWrapper.py comparatorNeutralWrapper.py

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

all: ${comparators:%=${bin}/%} ${bin}/lib/libComparator.py

test:

clean:
	rm -f $(bin)/comparatorWrapper.py
