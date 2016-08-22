radio_collar_tracker
====================
Airborne Wildlife Radio Collar Tracker

Engineers for Exploration, UCSD Project

Installing the Post-Process Code
================================
1.	Install Dependencies:
	* fftw3 (http://fftw.org/)
	* make (build-essential)
	* python 2.7+ (https://www.python.org/)
	* tkinter (python-tk)
	* numpy (python-numpy)
	* matplotlib (python-matplotlib)
	* utm 0.4.0 (https://pypi.python.org/pypi/utm)
	* pyshp 1.2.3 (https://pypi.python.org/pypi/pyshp)
	* gdal 2.1.0 (http://download.osgeo.org/gdal/)
2.	Make and install rct_cas
	```sh
	make all
	sudo make install
	```

In all, a typical Ubuntu-based installation might look like this:
```sh
sudo apt-get install build-essential python-tk python-numpy python-matplotlib python-pip python-dev git
wget ftp://ftp.fftw.org/pub/fftw/fftw-3.3.4.tar.gz
wget https://pypi.python.org/packages/source/u/utm/utm-0.4.0.tar.gz
wget http://download.osgeo.org/gdal/2.1.0/gdal-2.1.0.tar.gz
tar -xzf fftw-3.3.4.tar.gz
cd fftw-3.3.4
./configure
make
sudo make install
cd ..
tar -xzf utm-0.4.0.tar.gz
cd utm-0.4.0
sudo pip install -e .
cd ..
tar -xzf gdal-2.1.0.tar.gz
cd gdal-2.1.0
./configure --with-python
make
sudo make install
cd ..
sudo ldconfig
git clone https://github.com/UCSD-E4E/radio_collar_tracker
cd radio_collar_tracker
make
sudo make install
```

Running the Post-Process Code
=============================
1.	Execute rct_cas.

<!-- 1. Make the make_bin.sh file executable by running `chmod +x make_bin.sh`
2. Move the file `bin/run.tar` to a working directory of your choice.
3. Extract the binaries from `run.tar` by running `tar -xf run.tar`
4. Run the post-process code using any of the run scripts.
	1. `run.sh` needs to have the raw data from the SD card in the same working directory.  Usage: `run.sh NUM_COLLARS ALT_AGL`
	2. `run2.sh` takes an additional argument for where the raw data is.  Usage: `run2.sh NUM_COLLARS ALT_AGL DATA_DIR`
	3. `runcli.sh` is an interactive shell script.  Usage: `runcli.sh`
5. Note: if you run the PostProcessC code without using the integration scripts, ensure that all paths are fixed paths.
 -->

# Output and Intermediate Data Format

## Concatenated IQ Data
The utility CLI_GUI/cat_relevant.py concatenates the relevant raw IQ data files
together, in order to reduce the amount of computation required by the
post-processing code.  The resultant file is named `RUN_[run_num].raw`, where
run_num is a six character field containing the run number, zero padded.  This
file contains the raw IQ data from the start of recording until the sample
recorded at the same time as the last GPS datapoint.  This data is stored as
pairs of 8-bit unsigned integers, with each pair representing the in-phase and
quadrature components of the recorded signal.  See
https://en.wikipedia.org/wiki/In-phase_and_quadrature_components for an overview
of IQ signal representation.

## Processed IQ Data
The utility fft_detect/fft_detect transforms the raw time-domain IQ data into
its frequency-domain representation, and isolates a single frequency from that.
It loads the concatenated IQ data, and performs an FFT on 1024 sample wide
windows.  From the resultant complex frequency spectrum, fft_detect records the
proper frequency bin.  This frequency bin amplitude is stored as a 32-bit IEEE
float.  The resultant signal has a sampling frequency of 2 kSps, and each sample
represents the amplitude of the signal at the requested frequency, that is, the
time-averaged amplitude of the real signal's frequency component at that
frequency over the duration of that sample.

This file is named `RUN_[run_num]_[col_num].raw`.  The collar number is
referenced in the local collar definitions file (usually `COL`), and is
represented as a six digit field, zero padded.  The run number is also a six
digit field, zero padded.

## Correlated GPS and Signal Data
The utility raw_gps_analysis/raw_gps_analysis.py correlates the recorded GPS
data and the processed IQ data to create a sequence of correlated GPS locations
and signal strengths.  This utility also does a simple altitude filter to
eliminate the takeoff and landing phases of flight by doing a +/- 20% threshold
on the relative altitude data.  Correlation is accomplished by taking the
maximum signal amplitude for the signal data prior to each GPS location, for at
most 1.5 seconds.  That is, each GPS location is associated with the highest
signal amplitude in the previous 1.5 seconds or since the last GPS position.
This information is stored as comma separated values as: local timestamp
(seconds since UTC), latitude (degrees * 1e7), longitude (degrees * 1e7), signal
amplitude (dB?).

This file is named `RUN_[run_num]_[col_num].csv`.  The collar number is
referenced in the local collar definitions file (usually `COL`), and is
represented as a six digit field, zero padded.  The run number is also a six
digit field, zero padded.
