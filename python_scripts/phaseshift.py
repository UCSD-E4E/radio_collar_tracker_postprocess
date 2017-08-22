#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:44:57 2017

@author: anthony
"""
import rct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set() # styling
import scipy.signal as sg
import peakutils as pu

run = '19';
series = 'desert'

path = '/home/anthony/e4e/rct_runs/'+series+'/' 
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

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))

#%% Adjustments to pulses and periods
midx = np.argmax(Px)# find the peak sample (most likely to be a near pulse)

pT = rct.findTruePeriod(Px,pW,pT,Fsf)
pW = rct.findTrueWidth(Px,pW,pT,Fsf)

pulses  = rct.predictPulses(ft, Fsf, pT, midx)
periods = rct.predictPeriods(ft, Fsf, pT, midx)

pTi = int(pT*Fsx)
pWi = int(pW*Fsx)
phi = int(periods[0]/Fsf*Fsx)

st = np.linspace(0,pTi,pTi)
square = sg.square(2*Fx*st,0.125)

win = np.concatenate((np.zeros(int((pTi-pWi)/2)),np.ones(pWi),np.zeros(int((pTi-pWi)/2))))
winoff = np.concatenate((np.zeros(phi),win[:-phi]))