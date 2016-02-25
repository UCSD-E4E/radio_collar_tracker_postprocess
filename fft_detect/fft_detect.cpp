#include <iostream>
#include <unistd.h>
#include <getopt.h>
#include <string>
#include <fstream>
#include <cstdint>
#include <complex>
#include <fftw3.h>
#include <cstring>
#include <cstdlib>


#define FFT_LENGTH 1024

using namespace std;

int main(int argc, char** argv) {
	string input_file;
	string output_file;
	int beat_freq;

	bool hasOutput = false;
	bool hasInput = false;
	bool hasFreq = false;

	int opt;
	while((opt = getopt(argc, argv, "o:i:f:")) != -1){
		switch(opt){
			case 'o':
				output_file = optarg;
				hasOutput = true;
				break;
			case 'i':
				input_file = optarg;
				hasInput = true;
				break;
			case 'f':
				beat_freq = atoi(optarg);
				hasFreq = true;
				break;
			case '?':
			default:
				break;
		}
	}

	if(!(hasOutput && hasInput && hasFreq)){
		cerr << "Not enough args!" << endl;
		return -1;
	}

	int fft_index = beat_freq * (1024.0 / 2048000);
	if(fft_index < 0){
		fft_index = FFT_LENGTH + fft_index;
	}

	cerr << "Index: " << fft_index << endl;

	ifstream in_file_stream;
	ofstream out_file_stream;
	fftw_complex *fft_buffer_in, *fft_buffer_out;
	fftw_plan p;
	uint8_t buffer[2];	// buffer for raw data
	float sbuf[2];
	double mbuf[2];
	int counter = 0;

	fft_buffer_in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_LENGTH);
	fft_buffer_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * FFT_LENGTH);
	p = fftw_plan_dft_1d(FFT_LENGTH, fft_buffer_in, fft_buffer_out, FFTW_FORWARD,
	                     FFTW_ESTIMATE);

	cerr << "Input: " << input_file << endl;
	in_file_stream.open(input_file, ios::in | ios::binary);
	cerr << "Output: " << output_file << endl;
	out_file_stream.open(output_file, ios::out | ios::binary);

	if (in_file_stream.fail() || out_file_stream.fail()) {
		cerr << "Error: Failed to open file!" << endl;
		return -1;
	}
	// Loop through all of the samples
	mbuf[0] = 0;
	mbuf[1] = 0;
	while (in_file_stream.peek() != EOF) {
		in_file_stream.read(reinterpret_cast <char*>(buffer), 2);
		fft_buffer_in[counter][0] = buffer[0] / 128.0 - 1.0;
		mbuf[0] += fft_buffer_in[counter][0];
		fft_buffer_in[counter][1] = buffer[1] / 128.0 - 1.0;
		mbuf[1] += fft_buffer_in[counter][1];
		if (counter >= FFT_LENGTH) {
			counter = -1;
			for (int i = 0; i < FFT_LENGTH; i++){
				fft_buffer_in[i][0] -= mbuf[0] / FFT_LENGTH;
				fft_buffer_in[i][1] -= mbuf[1] / FFT_LENGTH;
			}
			fftw_execute(p);
			sbuf[0] = (float)fft_buffer_out[fft_index][0] / FFT_LENGTH;
			sbuf[1] = (float)fft_buffer_out[fft_index][1] / FFT_LENGTH;
			out_file_stream.write(reinterpret_cast<char*>(sbuf), 2 * sizeof(float));
			mbuf[0] = 0;
			mbuf[1] = 0;
		}
		counter++;
	}
	//fftw_free(fft_buffer_in);
	//fftw_free(fft_buffer_out);
	fftw_destroy_plan(p);
	in_file_stream.close();
	out_file_stream.close();
	return 0;
}
