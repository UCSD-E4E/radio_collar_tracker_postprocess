#include <cstdlib>
#include <cstdint>
#include <unistd.h>
#include <getopt.h>
#include <string>
#include <fstream>
#include <cmath>

using namespace std;

#define S_RATE	2048000
#define P_LEN	0.01
#define P_PER	1.5
#define S_FREQ	12000

int main(int argc, char** argv){
	string output_dir = "./";
	int num_pulses= 1;
	int opt;

	while ((opt = getopt(argc, argv, "o:l:")) != -1){
		switch(opt){
			case 'o':
				output_dir = optarg;
				break;
			case 'l':
				num_pulses= atoi(optarg);
				break;
		}
	}

	ofstream out_stream (output_dir + "sample.raw", ios::out | ios::binary);


	int pulse_length = P_LEN * S_RATE;
	int off_length = P_PER * S_RATE - pulse_length;
	uint8_t off_signal[2] = {128, 128};
	for(int j = 0; j < num_pulses; j++){
		// First half of signal
		for(int i = 0; i < off_length / 2; i++){
			out_stream.write(reinterpret_cast <char*> (off_signal), sizeof(uint8_t) * 2);
		}
		// Pulse
		uint8_t sample[2];
		for(int i = 0; i < pulse_length; i++){
			sample[0] = off_signal[0] + 127 * sin(i * S_FREQ);
			sample[1] = off_signal[1] + 127 * cos(i * S_FREQ);
			out_stream.write(reinterpret_cast <char*> (sample), sizeof(uint8_t) * 2);
		}
		// Second half of signal
		for(int i = 0; i < off_length / 2; i++){
			out_stream.write(reinterpret_cast <char*> (off_signal), sizeof(uint8_t) * 2);
		}
	}
	out_stream.close();
}
