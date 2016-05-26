fft_detect is the signal processing pipeline for the RCT processing software.

SYNOPSIS
========
**fft_detect** -i [run_dir] -o [output_file] -f [freq_offset] -r [run_num]

DESCRIPTION
===========
Uses a DFT to extract a specific frequency component from raw data.

**run_dir**  is the run data directory containing the raw files and run metafiles.

**output_file** is the output filename in the run data directory.

**freq_offset** is the offset in Hertz of the desired frequency component from the center frequency of the raw data.

**run_num** is the run id number.

PYTHON USE
==========
Run:

    python setup.py build_ext
or

    make build_python
The shared library will be placed in `build/lib.*/`.  Move the library to the desired working directory.

PYTHON INSTALLATION
===================
Run:

    python setup.py install
or

    make install_python
The shared library will be installed to the system python modules folder.  The `fft_detect` module is now available globally.

AUTHOR
======
Written by Nathan Hui
