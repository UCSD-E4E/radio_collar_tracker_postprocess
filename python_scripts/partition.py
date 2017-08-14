# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:31:55 2017

@author: anthony
"""

#%% Dependencies
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
run = '19';
series = 'desert'
# Inside here should be a RUN_000## folder
path = 'C:\\Users\\anthony\\Desktop\\e4e\\rct_runs\\'+series+'\\' 
# TODO: Use META_DATA file for literals and run variables
Fsx         = 2000000.0       # sampling frequency of input data
F_REAL      = 172950830.0   # REAL COLLAR
F_FAKE      = 172600000.0   # FAKE COLLAR

Fx          = F_REAL        # target collar frequency
Fc          = 172500000.0
#FFT_LENGTH  = int(4096 / 1.6)
FFT_LENGTH  = 4096
Fsf         = Fsx/FFT_LENGTH # sampling frquency of fft

pW          = 0.02 # pulse width [seconds]
pT          = 1.6 # pulse period [seconds]

xbin        = int( np.round( (Fx - Fc) / Fsx * FFT_LENGTH ) ) -1
raw_files   = rct.getfiles(path,run)
raw_files   = raw_files[:1]


#%% FFT
# return the power spectrum (time domain)
Pxx = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
Px = sg.medfilt(Pxx,9)
Px = sg.convolve(Px, sg.flattop(49), mode='same')
#Px = Pxx

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))

# find the peak sample (most likely to be a near pulse)
midx = np.argmax(Px)
pT = rct.findTruePeriod(Px,pW,pT,Fsf)
pW = rct.findTrueWidth(Px,pW,pT,Fsf)

half_per = int(np.ceil(pT/2 * Fsf))
half_wid = int(np.ceil(pW/2 * Fsf))

lT, rT = [midx - half_per, midx + half_per]
lW, rW = [midx - half_wid, midx + half_wid]

sample = Px[min(lT,0) : min(rT,len(Px))]
sample_midx = np.argmax(sample)

plt.figure(1)
plt.plot(ft,Px)
plt.axvline(ft[lT],c='y',linestyle='--')
plt.axvline(ft[rT-1],c='y',linestyle='--')
plt.axvline(ft[lW],c='c',linestyle='--')
plt.axvline(ft[rW-1],c='c',linestyle='--')

#%% SNR

noise = np.concatenate((Px[lT:lW],Px[rW:rT]))
signal = Px[lW:rW]

Pn = np.mean(noise)
Ps = np.mean(signal) - Pn
SNR = 10*np.log10(Ps/Pn)

