radio_collar_tracker
====================
Airborne Wildlife Radio Collar Tracker

Engineers for Exploration, UCSD Project


Running the Post-Process Code
=============================
1. Make the make_bin.sh file executable by running `chmod +x make_bin.sh`
2. Move the file `bin/run.tar` to a working directory of your choice.
3. Extract the binaries from `run.tar` by running `tar -xf run.tar`
4. Run the post-process code using any of the run scripts.
	1. `run.sh` needs to have the raw data from the SD card in the same working directory.  Usage: `run.sh NUM_COLLARS ALT_AGL`
	2. `run2.sh` takes an additional argument for where the raw data is.  Usage: `run2.sh NUM_COLLARS ALT_AGL DATA_DIR`
	3. `runcli.sh` is an interactive shell script.  Usage: `runcli.sh`
5. Note: if you run the PostProcessC code without using the integration scripts, ensure that all paths are fixed paths.
