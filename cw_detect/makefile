LFLAGS = -pthread -lm -Wl,--no-as-needed
CFLAGS = -std=gnu99 -c -Wall -g
CPPFLAGS = -std=c++11 -c -Wall -g -pthread -Wl,--no-as-needed
.PHONY: clean all docs test

all: Starter

test: Starter
	-rm -rf test
	mkdir test
	./Starter

cw_detect.o: cw_detect.c cw_detect.h
	gcc $(CFLAGS) cw_detect.c

clean:
	-rm *.o
	-rm -rf html
	-rm -rf latex
	-rm -rf top_block.py
	-rm -rf Starter
	-rm -rf test

Sample.o: Sample.cpp Sample.hpp
	g++ Sample.cpp $(CPPFLAGS)

docs:
	doxygen Doxyfile

FileLoader.o: FileLoader.cpp Sample.hpp FileLoader.hpp
	g++ FileLoader.cpp $(CPPFLAGS)

BFO.o: BFO.cpp Sample.hpp BFO.hpp
	g++ BFO.cpp $(CPPFLAGS)

LPF.o: LPF.cpp Sample.hpp LPF.hpp
	g++ LPF.cpp $(CPPFLAGS)

Decimator.o: Decimator.cpp Decimator.hpp Sample.hpp
	g++ Decimator.cpp $(CPPFLAGS)

FileWriter.o: FileWriter.cpp Sample.hpp FileWriter.hpp
	g++ FileWriter.cpp $(CPPFLAGS)

Starter.o: Starter.cpp Sample.hpp FileWriter.hpp FileLoader.hpp
	g++ Starter.cpp $(CPPFLAGS)

Starter: Starter.o FileLoader.o Sample.o FileWriter.o Decimator.o BFO.o LPF.o
	g++ Starter.o FileLoader.o Sample.o FileWriter.o Decimator.o BFO.o LPF.o $(LFLAGS) -o Starter
