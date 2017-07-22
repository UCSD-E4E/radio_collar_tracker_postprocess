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
			// case 'f':
			// 	beat_freq = atoi(optarg);
			// 	hasFreq = true;
			// 	break;
			case 'r':
				run_num = atoi(optarg);
				hasRun = true;
				break;
			case '?':
			default:
				break;
		}
	}

	if(optind == argc){
		cerr << "No frequencies found!" << endl;
		return -1;
	}else{
		hasFreq = true;
	}
	if(!(hasOutput && hasInput && hasFreq && hasRun)){
		cerr << "Not enough args!" << endl;
		return -1;
	}
	int* frequencies = (int*) malloc(sizeof(int) * (argc - optind));
	int numFrequencies = argc - optind;
	for(int i = optind; i < argc; ++i){
		beat_freq = atoi(argv[i]);
		frequencies[i - optind] = beat_freq * ((float)FFT_LENGTH / 2000000);
		if(frequencies[i - optind] < 0 && frequencies[i - optind] > -1 * FFT_LENGTH / 2){
			frequencies[i - optind] = FFT_LENGTH + frequencies[i - optind];
		}
		if(frequencies[i - optind] < 0 || frequencies[i - optind] > FFT_LENGTH){
			return -1;
		}
		printf("Using %d bin\n", frequencies[i - optind]);
	}




	return process(input_file.c_str(), output_file.c_str(), numFrequencies, frequencies, run_num);

}
