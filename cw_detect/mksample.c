#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#define S_RATE	2048000
#define P_LEN	0.01
#define P_PER	1.5
#define S_FREQ	12000

int main(int argc, char** argv){
	FILE* out_file = fopen("sample.raw", "wb");
	if(argc != 2){
		fprintf(stderr, "ERROR: length not specified!");
	}
	int num_pulses = atoi(argv[1]);
	int pulse_length = P_LEN * S_RATE;
	int off_length = P_PER * S_RATE - pulse_length;
	uint8_t off_signal[2] = {128, 128};
	for(int j = 0; j < num_pulses; j++){
		// First half of signal
		for(int i = 0; i < off_length / 2; i++){
			fwrite(off_signal, sizeof(uint8_t), 2, out_file);
		}
		// Pulse
		uint8_t sample[2];
		for(int i = 0; i < pulse_length; i++){
			sample[0] = off_signal[0] + 127 * sin(i * S_FREQ);
			sample[1] = off_signal[1] + 127 * cos(i * S_FREQ);
			fwrite(sample, sizeof(uint8_t), 2, out_file);
		}
		// Second half of signal
		for(int i = 0; i < off_length / 2; i++){
			fwrite(off_signal, sizeof(uint8_t), 2, out_file);
		}
	}
	fclose(out_file);
}
