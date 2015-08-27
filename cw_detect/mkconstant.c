#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char** argv){
	FILE* out_file = fopen("constant.raw", "wb");
	if(argc != 2){
		fprintf(stderr, "ERROR: length not specified!");
	}
	int num_samples = atoi(argv[1]);
	uint8_t sample[2] = {255, 128};
	for(int i = 0; i < num_samples; i++){
		fwrite(sample, sizeof(uint8_t), 2, out_file);
	}
	fclose(out_file);
}
