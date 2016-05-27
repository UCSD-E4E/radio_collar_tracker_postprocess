#include <fftw3.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "fft_detect.h"
#include <string.h>
#include <math.h>

#ifdef _PYTHON
#include <Python.h>
#endif

#include <dirent.h>

#define FFT_LENGTH 4096
#define SAMPLE_RATE 2048000
#define SIG_LENGTH (int)(0.06 * SAMPLE_RATE / FFT_LENGTH)

#define PROGRESS_BAR_LEN 50

////////////////////////////////
// Hidden Function Prototypes //
////////////////////////////////
#ifdef _PYTHON
static PyObject* fft_detect(PyObject* self, PyObject* args);
static PyMethodDef fft_detect_method[] = {
	{"fft_detect", fft_detect, METH_VARARGS, "FFT detection process"},
	{NULL, NULL, 0 ,NULL}
};
PyMODINIT_FUNC initfft_detect(void){
	(void) Py_InitModule("fft_detect", fft_detect_method);
}
#endif

int process(const char* run_dir, const char* ofile, const int freq_bin, const int run_num){
	FILE* in_file;
	FILE* out_file = fopen(ofile, "wb");

	if(freq_bin < 0 || freq_bin >= FFT_LENGTH){
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

	fftw_complex *fft_buffer_in, *fft_buffer_out;
	fftw_plan p;
	// RAW IQ buffer
	uint8_t buffer[2];
	// Sample buffer
	float sbuf[2];
	// Sample counter
	int counter = 0;
	int file_num = 0;

	double* history = (double*) calloc(2 * sizeof(double), SIG_LENGTH);
	unsigned int history_idx = 0;
	float convolution[2] = {0, 0};

	fft_buffer_in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_LENGTH);
	fft_buffer_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_LENGTH);
	p = fftw_plan_dft_1d(FFT_LENGTH, fft_buffer_in, fft_buffer_out, FFTW_FORWARD,
		FFTW_ESTIMATE);

	char* ifile = (char*) malloc(sizeof(char) * (strlen(run_dir) + 256));
	// Generate filename
	sprintf(ifile, "%s/RAW_DATA_%06d_%06d", run_dir, run_num, ++file_num);
	in_file = fopen(ifile, "rb");

	if(!in_file || !out_file){
		fprintf(stderr, "Error: Failed to open file!\n");
		return -1;
	}

	int i;

	char* progress_bar = (char*) calloc(sizeof(char), PROGRESS_BAR_LEN + 1);
	char* format_string = malloc(sizeof(char) * 17);
	sprintf(format_string, "%s%d%s", "\r[%-", PROGRESS_BAR_LEN, "s]%3.0f%%");
	for(i = 0; i < (int)round((float)PROGRESS_BAR_LEN * file_num / num_files); ++i){
		progress_bar[i] = '#';
	}
	printf(format_string, progress_bar, 100.0 * (file_num - 1) / num_files);
	fflush(stdout);

	while(!feof(in_file)){
		if(!(counter < FFT_LENGTH)){
			counter = 0;
			fftw_execute(p);
			sbuf[0] = (float)fft_buffer_out[freq_bin][0] / FFT_LENGTH;
			sbuf[1] = (float)fft_buffer_out[freq_bin][1] / FFT_LENGTH;
			history[history_idx * 2] = sbuf[0] * sbuf[0];
			history[history_idx * 2 + 1] = sbuf[1] * sbuf[1];
			convolution[0] = 0;
			convolution[1] = 0;
			for(i = 0; i < SIG_LENGTH; i++){
				convolution[0] += history[i * 2];
				convolution[1] += history[i * 2 + 1];
			}
			history_idx = (history_idx + 1) % SIG_LENGTH;
			fwrite(convolution, sizeof(float), 2, out_file);
		}
		int num_bytes_read = fread((void*)buffer, sizeof(uint8_t), 2, in_file);
		if(num_bytes_read == 0 && feof(in_file)){
			sprintf(ifile, "%s/RAW_DATA_%06d_%06d", run_dir, run_num, ++file_num);
			fclose(in_file);
			in_file = fopen(ifile, "rb");
            
            
			int j;
			for(j = 0; j < (int)round((float)PROGRESS_BAR_LEN * file_num / num_files); ++j){
				progress_bar[j] = '#';
			}
			printf(format_string, progress_bar, 100.0 * (file_num - 1) / num_files);
			fflush(stdout);

			if(!in_file){
				break;
			}
			continue;
		}
		if(num_bytes_read != 2){
			fprintf(stderr, "Error: Read partial sample! %d\n", num_bytes_read);
			fprintf(stderr, "Current counter: %d\n", counter);
			return -1;
		}
		fft_buffer_in[counter][0] = buffer[0] / 128.0 - 1.0;
		fft_buffer_in[counter][1] = buffer[1] / 128.0 - 1.0;
		++counter;
	}
	fftw_free(fft_buffer_in);
	fftw_free(fft_buffer_out);
	fftw_destroy_plan(p);
	fftw_cleanup();
	free(ifile);
	fclose(out_file);
#ifdef __unix__
	printf("\n");
	free(progress_bar);
	free(format_string);
#endif
	return 0;
}

#ifdef _PYTHON
static PyObject* fft_detect(PyObject* self, PyObject* args){
	char* ifile_cstr;
	char* ofile_cstr;
	int freq_bin;
	int run_num;
	int retval;
	if(!PyArg_ParseTuple(args, "ssii", &ifile_cstr, &ofile_cstr, &freq_bin, &run_num)){
		return NULL;
	}
	retval = process(ifile_cstr, ofile_cstr, freq_bin, run_num);
	return Py_BuildValue("i", retval);
}
#endif
