LFLAGS = -lfftw3_threads -lfftw3 -lm -lpthread
CFLAGS = -std=gnu99 -c -Wall -g
CPPFLAGS = -std=c++11 -c -Wall -g
.PHONY: clean all docs

all: Sample.o FileLoader.o BFO.o LPF.o

cw_detect.o: cw_detect.c cw_detect.h
	gcc $(CFLAGS) cw_detect.c

clean:
	-rm *.o
	-rm tester
	-rm -rf html
	-rm -rf latex
	-rm -rf top_block.py

tester.o: tester.c cw_detect.h
	gcc $(CFLAGS) tester.c

tester: tester.o cw_detect.o
	gcc tester.o cw_detect.o -o tester $(LFLAGS)

Sample.o: Sample.cpp Sample.hpp
	gcc Sample.cpp $(CPPFLAGS)

docs:
	doxygen Doxyfile

FileLoader.o: FileLoader.cpp
	gcc FileLoader.cpp $(CPPFLAGS)

BFO.o: BFO.cpp
	gcc BFO.cpp $(CPPFLAGS)

LPF.o: LPF.cpp
	gcc LPF.cpp $(CPPFLAGS)
