#ifndef __CW_DETECT__
#define __CW_DETECT__
/**
 * This module provides functionality to identify CW pulses in a given sample.
 */

#include <complex.h>
#include <fftw3.h>

/**
 * Initializes the FFTW module.
 */
int init_fftw(fftw_complex* data, fftw_complex* result, int data_len);

/**
 * Generates the Discrete Fourier Transform of the given sample of data.
 */
void discrete_fourier_transform();

/**
 * Multiplies complex signal data by the complex frequency frequency. Data and
 * result may be identical, in which case data will be overwritten.
 */
void beat_frequency_multiply(fftw_complex* data, double frequency,
                             double sampling_rate, fftw_complex* result, int length);
#endif // __CW_DETECT
