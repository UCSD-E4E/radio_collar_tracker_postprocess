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

#if defined (__unix__) || (__MACH__)
#include <dirent.h>
#endif

#define FFT_LENGTH 4096
#define SAMPLE_RATE 2000000
#define SIG_LENGTH (int)(0.06 * SAMPLE_RATE / FFT_LENGTH)

#define PROGRESS_BAR_LEN 50

#define BYTES_PER_SAMPLE	sizeof(int16_t) * 2

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

/**
 * Converts the raw IQ data to a complex floating point form.
 * @param  buffer    Raw byte data
 * @param  component 0 for I, 1 for Q
 * @return           Double-precision floating point representing the component
 */
double inline getSample(const void* buffer, const size_t component){
	return ((int16_t*) buffer)[component] / 4096.0;
}

int process(const char* run_dir, const char* ofile, const int num_freqs, const int* freq_bins, const int run_num){
	FILE* in_file;
	FILE** out_file = malloc(sizeof(FILE*) * num_freqs);
	int i;
	for(i = 0; i < num_freqs; ++i){
		char* filename = calloc(sizeof(char), 1024);
		sprintf(filename, "%s/RUN_%06d_%06d.raw", ofile, run_num, i + 1);
		out_file[i] = fopen(filename, "wb");
    	free(filename);
	}

#if defined (__unix__) || (__MACH__)
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
#endif

	fftw_complex *fft_buffer_in, *fft_buffer_out;
	fftw_plan p;
	// RAW IQ buffer
	void* buffer = malloc(BYTES_PER_SAMPLE);
	if(!buffer){
		fprintf(stderr, "Error: Failed to allocate raw IQ buffer");
	}
	// Sample buffer
	float sbuf[num_freqs][2];
	// Sample counter
	int counter = 0;
	int file_num = 0;

	// Initialize buffers
	double** history = (double**) malloc(sizeof(double*) * num_freqs);
	unsigned int history_idx[num_freqs];
	float convolution[num_freqs][2];
	for(i = 0; i < num_freqs; i++){
		history[i] = (double*) calloc(2 * sizeof(double), SIG_LENGTH);
		history_idx[i] = 0;
	}

	int convolution_row;
	for(convolution_row = 0; convolution_row < num_freqs; convolution_row++){
		convolution[convolution_row][0] = 0;
		convolution[convolution_row][1] = 0;
	}

	fftw_init_threads();

	fft_buffer_in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_LENGTH);
	fft_buffer_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_LENGTH);
	fftw_plan_with_nthreads(8);
	p = fftw_plan_dft_1d(FFT_LENGTH, fft_buffer_in, fft_buffer_out, FFTW_FORWARD,
		FFTW_ESTIMATE);

	// Generate filename
	char* in_file_name = (char*) malloc(sizeof(char) * (strlen(run_dir) + 256));
	sprintf(in_file_name, "%s/RAW_DATA_%06d_%06d", run_dir, run_num, ++file_num);
	in_file = fopen(in_file_name, "rb");

	if(!in_file || !out_file){
		fprintf(stderr, "Error: Failed to open file!\n");
		return -1;
	}


#if defined (__unix__) || (__MACH__)
	char* progress_bar = (char*) calloc(sizeof(char), PROGRESS_BAR_LEN + 1);
	char* format_string = malloc(sizeof(char) * 17);
	sprintf(format_string, "%s%d%s", "\r[%-", PROGRESS_BAR_LEN, "s]%3.0f%%");
	for(i = 0; i < (int)round((float)PROGRESS_BAR_LEN * file_num / num_files); ++i){
		progress_bar[i] = '#';
	}
	printf(format_string, progress_bar, 100.0 * (file_num - 1) / num_files);
	fflush(stdout);
#endif

	int collar;

	while(!feof(in_file)){
		if(!(counter < FFT_LENGTH)){
			counter = 0;
			fftw_execute(p);
			for(collar = 0; collar < num_freqs; collar++){
				sbuf[collar][0] = (float)fft_buffer_out[freq_bins[collar]][0] / FFT_LENGTH;
				sbuf[collar][1] = (float)fft_buffer_out[freq_bins[collar]][1] / FFT_LENGTH;
				history[collar][history_idx[collar] * 2] = sbuf[collar][0] * sbuf[collar][0];
				history[collar][history_idx[collar] * 2 + 1] = sbuf[collar][1] * sbuf[collar][1];
				convolution[collar][0] = 0;
				convolution[collar][1] = 0;
				for(i = 0; i < SIG_LENGTH; i++){
					convolution[collar][0] += history[collar][i * 2];
					convolution[collar][1] += history[collar][i * 2 + 1];
				}
				history_idx[collar] = (history_idx[collar] + 1) % SIG_LENGTH;
				fwrite(convolution[collar], sizeof(float), 2, out_file[collar]);
			}
		}
		int num_bytes_read = fread(buffer, BYTES_PER_SAMPLE, 1, in_file);
		if(num_bytes_read == 0 && feof(in_file)){
			sprintf(in_file_name, "%s/RAW_DATA_%06d_%06d", run_dir, run_num, ++file_num);
			fclose(in_file);
			in_file = fopen(in_file_name, "rb");
#if defined (__unix__) || (__MACH__)
			int j;
			for(j = 0; j < (int)round((float)PROGRESS_BAR_LEN * file_num / num_files); ++j){
				progress_bar[j] = '#';
			}
			printf(format_string, progress_bar, 100.0 * (file_num - 1) / num_files);
			fflush(stdout);
#endif

			if(!in_file){
				break;
			}
			continue;
		}
		if(num_bytes_read != BYTES_PER_SAMPLE){
			fprintf(stderr, "Error: Read partial sample! %d\n", num_bytes_read);
			fprintf(stderr, "Current counter: %d\n", counter);
			return -1;
		}
		// Normalize data
		fft_buffer_in[counter][0] = getSample(buffer, 0);
		fft_buffer_in[counter][1] = getSample(buffer, 1);
		++counter;
	}
	fftw_free(fft_buffer_in);
	fftw_free(fft_buffer_out);
	fftw_destroy_plan(p);
	fftw_cleanup();
	fftw_cleanup_threads();
	free(in_file_name);
	for(i = 0; i < num_freqs; ++i){
		fclose(out_file[i]);
		free(history[i]);
	}

	free(out_file);

	free(history);

#if defined (__unix__) || (__MACH__)
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
	int num_freqs;
	int* freq_bins;
	int run_num;
	int retval;
	if(!PyArg_ParseTuple(args, "ssii", &ifile_cstr, &ofile_cstr, &num_freqs, &freq_bins, &run_num)){
		return NULL;
	}
	retval = process(ifile_cstr, ofile_cstr,num_freqs, freq_bins, run_num);
	return Py_BuildValue("i", retval);
}
#endif
