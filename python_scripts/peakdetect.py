# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 16:07:58 2017

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
raw_files   = raw_files[:6]


#%% FFT
# return the power spectrum (time domain)
Pxx = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
Px = sg.medfilt(Pxx,9)

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))
ft_l,ft_r = np.split(ft,2)

# find the peak sample (most likely to be a near pulse)
Px_l,Px_r = np.split(Px,2)

midx_l = np.argmax(Px_l)
midx_r = np.argmax(Px_r)

pT_l = rct.findTruePeriod(Px_l,pW,pT,Fsf)
pT_r = rct.findTruePeriod(Px_r,pW,pT,Fsf)

pW_l = rct.findTrueWidth(Px_l,pW,pT_l,Fsf)
pW_r = rct.findTrueWidth(Px_r,pW,pT_r,Fsf)

pulses_l = rct.predictPulses(ft_l, Fsf, pT_l, midx_l) 
pulses_r = rct.predictPulses(ft_r, Fsf, pT_r, midx_r)

pulses_l = np.array(pulses_l)
pulses_r = np.array(pulses_r) + len(Px_l)
#pulses_r = len(Px_l)

pulses = np.concatenate((pulses_l,pulses_r))
#%% Peak detection
#Px = sg.convolve(Px,sg.flattop(49),mode='same')
peaks = pu.indexes(sg.convolve(Px,sg.flattop(49),mode='same'), thres= 0, min_dist=(pT-pW)*Fsf)


plt.figure(2)
plt.title('Peak Detection')
plt.plot(ft,Px)
rct.plotPulses2(ft, pulses)
plt.scatter(ft[peaks],Px[peaks],color='r')


#%% Second Pass
# Figure out the detected peak separation
p0,p1 = peaks[:-1],peaks[1:]
pdiff = p1-p0
pmean,pstd = np.mean(pdiff), np.std(pdiff)
ptruth = [abs(p - pmean) < pstd for p in pdiff]
