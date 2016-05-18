CC = g++
LD = g++
LFLAGS = -lm -L/fftw-3.3.4-64 -I./fftw-3.3.4-64 -llibfftw3-3 -L.
CFLAGS = -std=c++11 -c -Wall -g -O4
.PHONY: clean all

all: fft_detect

clean:
	-rm -rf fft_detect.o
	-rm -rf fft_detect

fft_detect.o: fft_detect.cpp
	${CC} ${CFLAGS} ${LFLAGS} fft_detect.cpp

fft_detect: fft_detect.o
	${LD} fft_detect.o -o fft_detect ${LFLAGS}