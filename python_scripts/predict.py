# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:52:55 2017

@author: anthony
"""

#%% Dependencies
import rct
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns; sns.set() # styling
import scipy.signal as sg
import peakutils as pu

#%% Run Variables
# original tests performed on run10 from canyon series
#run = '16';
#series = 'desert'
run = '31';
series = 'anechoic2'
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
raw_files   = raw_files[:3]


#%% FFT
# return the power spectrum (time domain)
Pxx = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
Px = sg.medfilt(Pxx,9)

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))

# find the peak sample (most likely to be a near pulse)
midx = np.argmax(Px)

pT0 = pT
pW0 = pW

pulses0  = rct.predictPulses(ft, Fsf, pT0, midx)
periods0 = rct.predictPeriods(ft, Fsf, pT0, midx)

pT1 = rct.findTruePeriod(Px,pW,pT,Fsf)
pW1 = rct.findTrueWidth(Px,pW,pT,Fsf)

pulses1  = rct.predictPulses(ft, Fsf, pT1, midx)
periods1 = rct.predictPeriods(ft, Fsf, pT1, midx)

import matplotlib.lines as mlines

plt.figure(1)
ax1 = plt.subplot(1,2,1)
plt.title('Predictions with Theoretical Collar Specs')
plt.plot(ft,Px)
plt.scatter(ft[midx],Px[midx],c='y')
rct.plotPeriods2(ft, periods0)
rct.plotPulses2(ft, pulses0)

blu_lin = mlines.Line2D([],[],c='b')
mag_lin = mlines.Line2D([],[],c='m',marker='X')
yel_lin = mlines.Line2D([],[],c='y',linestyle='--')
plt.legend([blu_lin,mag_lin,yel_lin],
           ['Signal','Expected Pulse','Expected Period'])

ax2 = plt.subplot(1,2,2, sharex=ax1, sharey=ax1)
plt.title('Predictions with Autocalculated Collar Specs')
plt.plot(ft,Px)
plt.scatter(ft[midx],Px[midx],c='y')
rct.plotPeriods2(ft, periods1)
rct.plotPulses2(ft, pulses1)

blu_lin = mlines.Line2D([],[],c='b')
mag_lin = mlines.Line2D([],[],c='m',marker='X')
yel_lin = mlines.Line2D([],[],c='y',linestyle='--')
plt.legend([blu_lin,mag_lin,yel_lin],
           ['Signal','Expected Pulse','Expected Period'])
