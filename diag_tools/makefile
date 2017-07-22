.PHONY: clean

spectrumAnalysis_fft: spectrumAnalysis_fft.c
	gcc spectrumAnalysis_fft.c -Wall -o spectrumAnalysis_fft -lfftw3_threads -lfftw3 -lm -lpthread -std=c99 -g

newspectrumAnalysis: newSpectrumAnalysis.c
	gcc newSpectrumAnalysis.c -Wall -o newspectrumAnalysis -lfftw3_threads -lfftw3 -lm -lpthread -std=c99 -g

sa_exportgain: spectrumAnalysis_exportgain.c
	gcc spectrumAnalysis_exportgain.c -Wall -o sa_exportgain -lfftw3threads -lfftw3 -lm -lpthread -std=c99 -g
