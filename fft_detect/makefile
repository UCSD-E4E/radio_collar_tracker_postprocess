CC = g++
LD = g++
LFLAGS = -lfftw3 -lm -pthread
CFLAGS = -std=c++11 -c -Wall -g
.PHONY: clean all

all: fft_detect

clean:
	-rm -rf fft_detect.o
	-rm -rf fft_detect

fft_detect.o: fft_detect.cpp
	${CC} ${CFLAGS} fft_detect.cpp

fft_detect: fft_detect.o
	${LD} fft_detect.o ${LFLAGS} -o fft_detect
