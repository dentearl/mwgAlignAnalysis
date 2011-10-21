#include ../include.mk
bin:= ./bin
src:= ./src
.PHONY:= all test clean

all: ${bin}/makefileEvalWrapper.sh
	cd ${src} && make all

${bin}/%.sh: ${src}/%.sh
	mkdir -p $(dir $@)
	cp ${src}/$*.sh $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

test:
	cd ${src} && make test

clean:
	cd ${src} && make clean

