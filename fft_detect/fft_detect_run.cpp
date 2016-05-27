#include <iostream>
#include <unistd.h>

extern "C"{
	#include "fft_detect.h"
}
#define FFT_LENGTH 4096

using namespace std;

/////////////////////////
// Function Prototypes //
/////////////////////////

int main(int argc, char** argv) {
	string input_file;
	string output_file;
	int beat_freq = 0;
	int run_num = 0;

	bool hasOutput = false;
	bool hasInput = false;
	bool hasFreq = false;
	bool hasRun = false;

	int opt;
	while((opt = getopt(argc, argv, "o:i:f:r:")) != -1){
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
			case 'r':
				run_num = atoi(optarg);
				hasRun = true;
				break;
			case '?':
			default:
				break;
		}
	}

	if(!(hasOutput && hasInput && hasFreq && hasRun)){
		cerr << "Not enough args!" << endl;
		return -1;
	}

	int fft_index = beat_freq * ((float)FFT_LENGTH / 2048000);
	if(fft_index < 0){
		fft_index = FFT_LENGTH + fft_index;
	}

    printf("Using %d bin\n", fft_index);
	return process(input_file.c_str(), output_file.c_str(), fft_index, run_num);

}
