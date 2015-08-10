/**
 * Module that provides functionality to identify CW pulses in a sample.
 */
#include <complex.h>
#include <fftw3.h>
#include <math.h>
#include "cw_detect.h"

// Using engineering notation:
#undef I
#define j _Complex_I

fftw_plan fft_plan;

int init_fftw(fftw_complex* data, fftw_complex* result, int data_len) {
	if (!fftw_init_threads()) {
		return -1;
	}
	fftw_plan_with_nthreads(4);
	fft_plan = fftw_plan_dft_1d(data_len, data, result, FFTW_FORWARD,
	                            FFTW_ESTIMATE);
	return 0;
}

void discrete_fourier_transform() {
	fftw_execute(fft_plan);
	fftw_destroy_plan(fft_plan);
}

void _frequency_multiply(fftw_complex* f1, fftw_complex* f2,
                         fftw_complex* result, int length) {
	for (int i = 0; i < length; i++) {
		result[i] = f1[i] * f2[i];
	}
}

void beat_frequency_multiply(fftw_complex* data, double frequency,
                             double sampling_rate, fftw_complex* result, int length) {
	fftw_complex* f2 = (fftw_complex*)fftw_alloc_complex(length);
	for (int i = 0; i < length; i++) {
		f2[i] = cos(frequency * i / sampling_rate) + j * sin(frequency * i /
		        sampling_rate);
	}
	_frequency_multiply(data, f2, result, length);
	fftw_free(f2);
}

