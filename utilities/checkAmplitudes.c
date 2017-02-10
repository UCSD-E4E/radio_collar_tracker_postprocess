#include <unistd.h>
#include <dirent.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <float.h>

#define SAMPLE_T	uint8_t
#define OFFSET		-1.0
#define SCALAR		1 / 128.0

int main(int argc, char** argv){
	// Set up variables
	// Options variable
	int opt;
	// Run number
	int run_num = 0;
	// Data directory
	char* run_dir = NULL;

	while((opt = getopt(argc, argv, "i:r:")) != -1){
		switch(opt){
			case 'i':
				run_dir = malloc(sizeof(char) * (strlen(optarg) + 1));
				strcpy(run_dir, optarg);
				break;
			case 'r':
				run_num = atoi(optarg);
				break;
			case '?':
			default:
				break;
		}
	}

	if(!run_num){
		return -1;
	}
	if(!run_dir){
		return -1;
	}

	int num_files = 0;
	DIR* dirp;
	struct dirent* entry;

	dirp = opendir(run_dir);
	while ((entry = readdir(dirp)) != NULL) {
		char* data_prefix = malloc(sizeof(char) * 16);
		sprintf(data_prefix, "RAW_DATA_%06d", run_num);
	    if (strncmp(entry->d_name, data_prefix, 15) == 0) {
         	num_files++;
    	}
    	free(data_prefix);
	}
	closedir(dirp);

	float max = FLT_MIN;
	float min = FLT_MAX;
	double avg = 0;
	double squared = 0;
	uint64_t counter = 0;
	SAMPLE_T next[2];

	for(int i = 1; i <= num_files; i++){
		char* filename = malloc(sizeof(char) * (strlen(run_dir) + 24));
		sprintf(filename, "%s/RAW_DATA_%06d_%06d", run_dir, run_num, i);
		FILE* file = fopen(filename, "rb");
		if(!file){
			printf("Error!\n");
			return -1;
		}
		while(fread(&next, sizeof(SAMPLE_T) * 2, 1, file)){
			float i = next[0] * (SCALAR) + (OFFSET);
			float q = next[1] * (SCALAR) + (OFFSET);
			float magnitude = sqrt(i * i + q * q);
			counter++;
			if(magnitude > max){
				max = magnitude;
			}
			if(magnitude < min){
				min = magnitude;
			}
			avg += magnitude;
			squared += magnitude * magnitude;
		}
		fclose(file);
		free(filename);
	}
	printf("Max amplitude:     %f\n", max);
	printf("Min amplitude:     %f\n", min);
	printf("Average amplitude: %f\n", avg / counter);
	double stddev = sqrt((squared - avg * avg / counter) / counter);
	printf("Stddev amplitude:  %f\n", stddev);
	free(run_dir);
}