bin := ../../bin
.PHONY := all test clean

wrappers := indelDistributionWrapper.py
binWrappers := $(foreach f,${wrappers},${bin}/$f)

$(bin)/%: %
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

all: ${binWrappers}

test:

clean: 
	rm -f ${binWrappers}
