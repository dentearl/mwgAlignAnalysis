bin:=../../bin
.PHONY:= all clean

$(bin)/comparatorWrapper.py: comparatorWrapper.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

all: $(bin)/comparatorWrapper.py

clean:
	rm -f $(bin)/comparatorWrapper.py
