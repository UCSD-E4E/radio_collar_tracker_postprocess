#include <unistd.h>
#include <getopt.h>
#include <fftw3.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "fft_detect.h"
#include <string.h>

#ifdef _PYTHON
#include <Python.h>
#endif

#define FFT_LENGTH 1024

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

	fftw_complex *fft_buffer_in, *fft_buffer_out;
	fftw_plan p;
	// RAW IQ buffer
	uint8_t buffer[2];
	// Sample buffer
	float sbuf[2];
	// Average
	double mbuf[2];
	// Sample counter
	int counter = 0;
	int file_num = 0;

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

	mbuf[0] = 0;
	mbuf[1] = 0;
	while(!feof(in_file)){
		if(!(counter < FFT_LENGTH)){
			counter = 0;
			int i;
			for(i = 0; i < FFT_LENGTH; i++){
				fft_buffer_in[i][0] -= mbuf[0] / FFT_LENGTH;
				fft_buffer_in[i][1] -= mbuf[1] / FFT_LENGTH;
			}
			fftw_execute(p);
			sbuf[0] = (float)fft_buffer_out[freq_bin][0] / FFT_LENGTH;
			sbuf[1] = (float)fft_buffer_out[freq_bin][1] / FFT_LENGTH;
			fwrite(sbuf, sizeof(float), 2, out_file);
			mbuf[0] = 0;
			mbuf[1] = 0;
		}
		int num_bytes_read = fread((void*)buffer, sizeof(uint8_t), 2, in_file);
		if(num_bytes_read == 0 && feof(in_file)){
			sprintf(ifile, "%s/RAW_DATA_%06d_%06d", run_dir, run_num, ++file_num);
			fclose(in_file);
			in_file = fopen(ifile, "rb");
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
		mbuf[0] += fft_buffer_in[counter][0];
		fft_buffer_in[counter][1] = buffer[1] / 128.0 - 1.0;
		mbuf[1] += fft_buffer_in[counter][1];
		++counter;
	}
	fftw_destroy_plan(p);
	free(ifile);
	fclose(out_file);
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
