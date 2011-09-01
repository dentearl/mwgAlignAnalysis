bin:= ../bin

# place the names of directories here:
evaluations := comparatorWrapper

.PHONY = all clean all.% clean.%

all : ${bin}/lib/libCall.py ${evaluations:%=all.%}

all.%: %
	cd $* && make all

$(bin)/lib/libCall.py: libCall.py
	mkdir -p $(dir $@)
	touch $(dir $@)/__init__.py
	cp $< $@.tmp
	mv $@.tmp $@

clean: ${evaluations:%=clean.%}
	rm -rf $(bin)

clean.%: %
	cd $* && make clean
