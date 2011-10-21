bin:=../../bin
.PHONY:= all test clean

toys := recorder.sh wordCountWrapper.sh
binToys := $(foreach f,${toys},${bin}/$f)

$(bin)/%.sh: %.sh
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

all: ${binToys}

test:

clean:
	rm -f ${binToys}
