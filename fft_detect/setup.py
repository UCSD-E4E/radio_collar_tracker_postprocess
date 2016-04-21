#!/usr/bin/env  python
from distutils.core import setup, Extension

# the c++ extension module
extension_mod = Extension("fft_detect", sources = ["fft_detect.c",], libraries = ["fftw3"], define_macros = [('_PYTHON', '1')])

setup(name = "fft_detect", ext_modules=[extension_mod])
