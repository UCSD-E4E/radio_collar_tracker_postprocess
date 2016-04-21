CC = g++
LD = g++
LFLAGS = -lm -L./fftw-3.3.4-64 -llibfftw3-3
CFLAGS = -std=c++11 -c -Wall -g -O4
.PHONY: clean all

all: fft_detect

clean:
	-rm -rf fft_detect.o
	-rm -rf fft_detect

fft_detect.o: fft_detect.cpp
	${CC} ${CFLAGS} fft_detect.cpp -lm -L./fftw-3.3.4-64 -llibfftw3-3

fft_detect: fft_detect.o
	${LD} fft_detect.o -o fft_detect ${LFLAGS}