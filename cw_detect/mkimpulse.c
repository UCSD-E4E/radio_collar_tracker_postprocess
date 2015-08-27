#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char** argv){
	FILE* out_file = fopen("impulse.raw", "wb");
	if(argc != 2){
		fprintf(stderr, "ERROR: length not specified!");
	}
	int num_samples = atoi(argv[1]);
	int sample_length = 0;
	uint8_t sample[2] = {128, 128};
	//sample_length += fwrite(sample, sizeof(uint8_t), 2, out_file);
	sample[0] = 255;
	sample_length += fwrite(sample, sizeof(uint8_t), 2, out_file);
	sample[0] = 128;
	for(int i = 0; i < num_samples - 1; i++){
		sample_length += fwrite(sample, sizeof(uint8_t), 2, out_file);
	}

	printf("Wrote %d samples\n", sample_length / 2);
	fclose(out_file);
}
