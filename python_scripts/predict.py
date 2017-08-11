# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:52:55 2017

@author: anthony
"""

#%%
import rct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set() # styling
import scipy.signal as sg
import peakutils as pu

#%% Run Variables
# original tests performed on run10 from canyon series
#run = '16';
#series = 'desert'
run = '47';
series = 'canyon2'
path = 'C:\\Users\\anthony\\Desktop\\e4e\\'+series+'\\' # Inside here should be a RUN_000## folder

# TODO: Use META_DATA file for literals and run variables
Fsx         = 2000000.0       # sampling frequency of input data
Fx          = 172950830.0
Fc          = 172500000.0
FFT_LENGTH  = 4096
Fsf         = Fsx/FFT_LENGTH # sampling frquency of fft

pW          = 0.02 # pulse width [seconds]
pT          = 1.6 # pulse period [seconds]

xbin        = int( np.round( (Fx - Fc) / Fsx * FFT_LENGTH ) )
raw_files, meta   = rct.getfiles(path,run)
raw_files   = raw_files[:1]


#%% FFT
# return the power spectrum (time domain)
Px = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))

# find the peak sample (most likely to be a near pulse)
midx = np.argmax(Px)