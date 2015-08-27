#include <cstdlib>
#include <cstdint>
#include <unistd.h>
#include <getopt.h>
#include <string>
#include <fstream>
#include <cmath>

using namespace std;

int main(int argc, char** argv){
	// Variables
	int opt;
	string output_dir = "./";
	int start_freq = 1000;
	int end_freq = 200000;
	int cycles_per_freq = 10;
	int freq_step = 100;
	int samp_freq = 2048000;

	while ((opt = getopt(argc, argv, "o:")) != -1){
		switch(opt){
			case 'o':
				output_dir = optarg;
				break;
		}
	}

	ofstream out_stream (output_dir + "sweep.raw", ios::out | ios::binary);
	uint8_t sample[2];
	uint8_t base_signal[2] = {128, 128};
	for(int f = start_freq; f < end_freq; f += freq_step){
		for(int c = 0; c < cycles_per_freq; c++){
			int num_samples = (float) cycles_per_freq / f * samp_freq;
			for(int i = 0; i < num_samples; i++){
				sample[0] = base_signal[0] + 127 * sin(i * samp_freq);
				sample[1] = base_signal[1] + 127 * cos(i * samp_freq);
				out_stream.write(reinterpret_cast <char*> (sample), sizeof(uint8_t) * 2);
			}
		}
	}
	out_stream.close();
}
