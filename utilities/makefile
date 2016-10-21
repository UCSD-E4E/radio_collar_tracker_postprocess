CXX = g++
CC = gcc
LD = g++
LFLAGS = -O4
INC =
CPPFLAGS = -std=c++11 -c -Wall -g ${INC}
CFLAGS = -std=gnu99 -c -Wall -g ${INC}
.PHONY: clean all install_python build_python test

all: checkAmplitudes

clean:
	-rm -rf *.o
	-rm -rf checkAmplitudes

checkAmplitudes: checkAmplitudes.o
	${LD} $^ ${LFLAGS} -o checkAmplitudes

checkAmplitudes.o: checkAmplitudes.c
	${CC} $< ${CFLAGS}
