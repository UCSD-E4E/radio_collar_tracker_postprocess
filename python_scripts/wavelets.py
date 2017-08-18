# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:05:19 2017

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
Pxx = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='flattop')
Px = sg.medfilt(Pxx,9)
flt = sg.convolve(Px,sg.flattop(49),mode='same')
hat = sg.convolve(Px,sg.ricker(9,1),mode='same')

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))

# find the peak sample (most likely to be a near pulse)
midx = np.argmax(Px)

pT = rct.findTruePeriod(Px,pW,pT,Fsf)
pW = rct.findTrueWidth(Px,pW,pT,Fsf)

pulses  = rct.predictPulses(ft, Fsf, pT, midx)


#%% Peak detection
#Px = sg.convolve(Px,sg.flattop(49),mode='same')
peaks = pu.indexes(sg.convolve(Px,sg.flattop(49),mode='same'), thres= 0, min_dist=(pT-pW)*Fsf)


plt.figure(1)
ax0 = plt.subplot(2,1,1)
plt.plot(ft,Pxx)

ax1 = plt.subplot(2,1,2, sharex=ax0, sharey=ax0)
plt.plot(ft,Px)

#ax2 = plt.subplot(3,2,3)
#plt.plot(ft,Px)
#
#plt.subplot(3,2,4, sharex=ax2)
#plt.plot(ft,flt)
#
#plt.subplot(3,2,5)
#plt.plot(ft,Px)
#
#plt.subplot(3,2,6, sharex=ax2)
#plt.plot(ft,hat)