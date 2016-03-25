CXX = g++
CC = gcc
LD = g++
LFLAGS = -lfftw3 -lm -O4
INC =
CPPFLAGS = -std=c++11 -c -Wall -g ${INC}
CFLAGS = -std=gnu99 -c -Wall -g ${INC}
PYTHON = python
.PHONY: clean all install_python build_python test

test: all
	./fft_detect -i /home/ntlhui/workspace/RUN_002070 -o /home/ntlhui/workspace/RUN_002070/RUN_002070_000004.raw -f 1000 -r 2070

all: fft_detect

clean:
	-rm -rf *.o
	-rm -rf fft_detect
	-rm -r build dist

fft_detect_run.o: fft_detect_run.cpp
	${CXX} ${CPPFLAGS} fft_detect_run.cpp

fft_detect: fft_detect_run.o fft_detect.o
	${LD} $^ ${LFLAGS} -o fft_detect

fft_detect.o: fft_detect.c fft_detect.h
	gcc $< -std=gnu99 -c -Wall -O4 ${INC}

install_python: setup.py fft_detect.c
	${PYTHON} setup.py install

build_python: setup.py fft_detect.c
	${PYTHON} setup.py build_ext
