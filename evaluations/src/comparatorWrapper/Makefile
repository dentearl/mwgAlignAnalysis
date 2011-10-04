bin:=../../bin
.PHONY:= all test clean

$(bin)/comparatorWrapper.py: comparatorWrapper.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

all: $(bin)/comparatorWrapper.py

test:

clean:
	rm -f $(bin)/comparatorWrapper.py
