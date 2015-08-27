LFLAGS = -pthread -lm -Wl,--no-as-needed
CFLAGS = -std=gnu99 -c -Wall -g
CPPFLAGS = -std=c++11 -c -Wall -g -pthread -Wl,--no-as-needed -O0
.PHONY: clean all docs test testFile

all: Starter

test: tester
	-rm -rf test
	mkdir test
	./Starter

tester: tester.o
	g++ tester.o $(LFLAGS) -o tester

tester.o: tester.cpp
	g++ tester.cpp $(CPPFLAGS)

cw_detect.o: cw_detect.c cw_detect.h
	gcc $(CFLAGS) cw_detect.c

clean:
	-rm *.o
	-rm -rf html
	-rm -rf latex
	-rm -rf top_block.py
	-rm -rf Starter
	-rm -rf test
	-rm -rf Compare
	-rm -rf iqdump
	-rm -rf magdump
	-rm -rf mkstep
	-rm -rf mkconstant
	-rm -rf FileTester
	-rm -rf BFOtester
	-rm -rf LPFTester
	-rm -rf mkimpulse
	-rm -rf mksample
	-rm -rf DecimatorTester
	-rm -rf *.raw

Sample.o: Sample.cpp Sample.hpp
	g++ Sample.cpp $(CPPFLAGS)

docs:
	doxygen Doxyfile

FileLoader.o: FileLoader.cpp Sample.hpp FileLoader.hpp
	g++ FileLoader.cpp $(CPPFLAGS)

BFO.o: BFO.cpp Sample.hpp BFO.hpp
	g++ BFO.cpp $(CPPFLAGS)

LPF.o: LPF.cpp Sample.hpp LPF.hpp 20480_LPF_TAPS.hpp
	g++ LPF.cpp $(CPPFLAGS) -O3

Decimator.o: Decimator.cpp Decimator.hpp Sample.hpp
	g++ Decimator.cpp $(CPPFLAGS)

FileWriter.o: FileWriter.cpp Sample.hpp FileWriter.hpp
	g++ FileWriter.cpp $(CPPFLAGS)

Starter.o: Starter.cpp Sample.hpp FileWriter.hpp FileLoader.hpp
	g++ Starter.cpp $(CPPFLAGS)

Compare.o: Compare.cpp Sample.hpp FileWriter.hpp FileLoader.hpp
	g++ Compare.cpp $(CPPFLAGS)

Starter: Starter.o FileLoader.o Sample.o FileWriter.o Decimator.o BFO.o LPF.o
	g++ Starter.o FileLoader.o Sample.o FileWriter.o Decimator.o BFO.o LPF.o $(LFLAGS) -o Starter

Compare: Compare.o FileLoader.o Sample.o FileWriter.o Decimator.o BFO.o LPF.o
	g++ Compare.o FileLoader.o Sample.o FileWriter.o Decimator.o BFO.o LPF.o $(LFLAGS) -o Compare

iqdump: iqdump.cpp
	g++ iqdump.cpp $(CPPFLAGS)
	g++ iqdump.o $(LFLAGS) -o iqdump

mkconstant: mkconstant.c
	gcc mkconstant.c $(CFLAGS)
	gcc mkconstant.o $(LFLAGS) -o mkconstant

testFile: FileTester.cpp constant.raw FileLoader.o FileWriter.o Sample.o
	g++ FileTester.cpp $(CPPFLAGS)
	g++ FileTester.o FileLoader.o FileWriter.o Sample.o $(LFLAGS) -o FileTester
	./FileTester

testBFO: BFOtester.cpp constant.raw FileLoader.o FileWriter.o Sample.o BFO.o
	g++ BFOtester.cpp $(CPPFLAGS)
	g++ BFOtester.o FileLoader.o FileWriter.o Sample.o BFO.o $(LFLAGS) -o BFOtester
	./BFOtester

mkstep: mkstep.c
	gcc mkstep.c $(CFLAGS)
	gcc mkstep.o $(LFLAGS) -o mkstep

testLPF: LPFTester.cpp impulse.raw FileLoader.o FileWriter.o Sample.o LPF.o
	g++ LPFTester.cpp $(CPPFLAGS)
	g++ LPFTester.o FileLoader.o FileWriter.o Sample.o LPF.o $(LFLAGS) -o LPFTester
	./LPFTester

mkimpulse: mkimpulse.c
	gcc mkimpulse.c $(CFLAGS)
	gcc mkimpulse.o $(LFLAGS) -o mkimpulse

magdump: magdump.cpp
	g++ magdump.cpp $(CPPFLAGS)
	g++ magdump.o $(LFLAGS) -o magdump

mksample: mksample.c
	gcc mksample.c $(CFLAGS)
	gcc mksample.o $(LFLAGS) -o mksample

testDecimator: DecimatorTester.cpp impulse.raw FileLoader.o FileWriter.o Sample.o Decimator.o
	g++ DecimatorTester.cpp $(CPPFLAGS)
	g++ DecimatorTester.o FileLoader.o FileWriter.o Sample.o Decimator.o $(LFLAGS) -o DecimatorTester
	./DecimatorTester


