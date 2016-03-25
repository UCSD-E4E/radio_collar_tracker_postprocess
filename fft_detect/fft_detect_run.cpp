#include <iostream>
#include <unistd.h>
#include <getopt.h>
#include <string>
#include <fstream>
#include <cstdint>
#include <complex>
#include <fftw3.h>

extern "C"{
	#include "fft_detect.h"
}
#define FFT_LENGTH 1024

using namespace std;

/////////////////////////
// Function Prototypes //
/////////////////////////

int main(int argc, char** argv) {
	string input_file;
	string output_file;
	int beat_freq;

	bool hasOutput = false;
	bool hasInput = false;
	bool hasFreq = false;

	int opt;
	while((opt = getopt(argc, argv, "o:i:f:")) != -1){
		switch(opt){
			case 'o':
				output_file = optarg;
				hasOutput = true;
				break;
			case 'i':
				input_file = optarg;
				hasInput = true;
				break;
			case 'f':
				beat_freq = atoi(optarg);
				hasFreq = true;
				break;
			case '?':
			default:
				break;
		}
	}

	if(!(hasOutput && hasInput && hasFreq)){
		cerr << "Not enough args!" << endl;
		return -1;
	}

	int fft_index = beat_freq * (1024.0 / 2048000);
	if(fft_index < 0){
		fft_index = FFT_LENGTH + fft_index;
	}

	cerr << "Index: " << fft_index << endl;

	return process(input_file.c_str(), output_file.c_str(), fft_index);

}
