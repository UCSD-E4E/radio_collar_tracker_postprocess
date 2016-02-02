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
2.	Make and install rct_cas
	```sh
	make all
	sudo make install
	```

In all, a typical Debian-based installation might look like this:
```sh
sudo apt-get install build-essential python-tk python-numpy python-matplotlib python-pip python-dev git
wget ftp://ftp.fftw.org/pub/fftw/fftw-3.3.4.tar.gz
wget https://pypi.python.org/packages/source/u/utm/utm-0.4.0.tar.gz
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
