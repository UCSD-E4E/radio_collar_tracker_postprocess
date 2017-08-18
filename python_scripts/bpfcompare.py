# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:50:12 2017

@author: anthony
"""

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
run = '16';
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

xbin        = int( np.round( (Fx - Fc) / Fsx * FFT_LENGTH ) ) - 1
fakebin     = int( np.round( (F_FAKE-Fc)/Fsx * FFT_LENGTH ) )
raw_files   = rct.getfiles(path,run)
raw_files   = raw_files[:1]


#%% FFT
# return the power spectrum (time domain)
Pxx0 = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
Px0 = sg.medfilt(Pxx0,9)
f0,p0 = sg.welch(rct.raw2complex(raw_files[0]),fs=Fsx,nperseg=FFT_LENGTH)


run = '19'
raw_files = rct.getfiles(path,run)
raw_files = raw_files[:1]

Pxx1 = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
Px1 = sg.medfilt(Pxx1,9)
f1,p1 = sg.welch(rct.raw2complex(raw_files[0]),fs=Fsx,nperseg=FFT_LENGTH)


run = '25';
series = 'canyon'
path = 'C:\\Users\\anthony\\Desktop\\e4e\\rct_runs\\'+series+'\\' 
raw_files = rct.getfiles(path,run)
raw_files = raw_files[:1]

Pxx2 = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
Px2 = sg.medfilt(Pxx2,9)
f2,p2 = sg.welch(rct.raw2complex(raw_files[0]),fs=Fsx,nperseg=FFT_LENGTH)


# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px0)/Fsf,len(Px0))

# find the peak sample (most likely to be a near pulse)
midx0 = np.argmax(Px0)
midx1 = np.argmax(Px1)
midx2 = np.argmax(Px2)


pT0 = rct.findTruePeriod(Px0,pW,pT,Fsf)
pW0 = rct.findTrueWidth(Px0,pW,pT,Fsf)

pT1 = rct.findTruePeriod(Px1,pW,pT,Fsf)
pW1 = rct.findTrueWidth(Px1,pW,pT,Fsf)

pT2 = rct.findTruePeriod(Px2,pW,pT,Fsf)
pW2 = rct.findTrueWidth(Px2,pW,pT,Fsf)

pulses0  = rct.predictPulses(ft, Fsf, pT, midx0)
pulses1  = rct.predictPulses(ft, Fsf, pT, midx1)
pulses2  = rct.predictPulses(ft, Fsf, pT, midx2)


#%% Peak detection
#Px = sg.convolve(Px,sg.flattop(49),mode='same')
peaks0 = pu.indexes(sg.convolve(Px0,sg.flattop(49),mode='same'), thres= 0, min_dist=(pT0-pW0)*Fsf)
peaks1 = pu.indexes(sg.convolve(Px1,sg.flattop(49),mode='same'), thres= 0, min_dist=(pT1-pW1)*Fsf)
peaks2 = pu.indexes(sg.convolve(Px2,sg.flattop(49),mode='same'), thres= 0, min_dist=(pT2-pW2)*Fsf)


plt.figure(1)
ax0 = plt.subplot(1,3,1)
plt.title('Frequency Spectrum - No BPF')
plt.axvline(f0[xbin],c='c',linestyle='--', alpha=0.4)
plt.axvline(f0[fakebin],c='m',linestyle='--', alpha=0.4)
plt.semilogy(f0,p0)
plt.legend(['Collar Frequency Bin', 'Reference Bin'])

ax1 = plt.subplot(1,3,2, sharex=ax0)
plt.title('Frequency Spectrum - With BPF')
plt.axvline(f1[xbin],c='c',linestyle='--', alpha=0.4)
plt.axvline(f1[fakebin],c='m',linestyle='--', alpha=0.4)
plt.semilogy(f1,p1)
plt.legend(['Collar Frequency Bin', 'Reference Bin'])

ax2 = plt.subplot(1,3,3, sharex=ax0)
plt.title('Frequency Spectrum - 25')
plt.axvline(f2[xbin],c='c',linestyle='--', alpha=0.4)
plt.axvline(f2[fakebin],c='m',linestyle='--', alpha=0.4)
plt.semilogy(f2,p2)
plt.legend(['Collar Frequency Bin', 'Reference Bin'])

plt.figure(2)
ax2 = plt.subplot(1,3,1)
plt.title('No BPF')
plt.plot(ft,Px0)

ax3 = plt.subplot(1,3,2, sharex=ax2)
plt.title('BPF')
plt.plot(ft,Px1)

ax4 = plt.subplot(1,3,3, sharex=ax2)
plt.title('25')
plt.plot(ft,Px2)