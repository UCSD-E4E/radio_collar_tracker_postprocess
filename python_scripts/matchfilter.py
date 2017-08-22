#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 12:08:21 2017

@author: anthony
"""

import rct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set() # styling
import scipy.signal as sg
import peakutils as pu

#%%http://qingkaikong.blogspot.com/2016/03/shift-signal-in-frequency-domain.html
def nextpow2(i):
    '''
    Find the next power 2 number for FFT
    '''
    
    n = 1
    while n < i: n *= 2
    return n

def shift_signal_in_frequency_domain(datin, shift):
    '''
    This is function to shift a signal in frequency domain. 
    The idea is in the frequency domain, 
    we just multiply the signal with the phase shift. 
    '''
    Nin = len(datin) 
    
    # get the next power 2 number for fft
    N = nextpow2(Nin +np.max(np.abs(shift)))
    
    # do the fft
    fdatin = np.fft.fft(datin, N)
    
    # get the phase shift for the signal, shift here is D in the above explaination
    ik = np.array([2j*np.pi*k for k in range(0, N)]) / N 
    fshift = np.exp(-ik*shift)
        
    # multiple the signal with the shift and transform it back to time domain
    datout = np.real(np.fft.ifft(fshift * fdatin))
    
    # only get the data have the same length as the input signal
    datout = datout[0:Nin]
    
    return datout

#%% Run Variables
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

pT_fix = rct.findTruePeriod(Px,pW,pT,Fsf)
pW_fix = rct.findTrueWidth(Px,pW,pT,Fsf)

pulses  = rct.predictPulses(ft, Fsf, pT_fix, midx)
periods = rct.predictPeriods(ft, Fsf, pT_fix, midx)

pTi_x = int(pT_fix*Fsx)
pWi_x = int(pW_fix*Fsx)
phi_x = int(periods[0]/Fsf*Fsx)

shift = shift_signal_in_frequency_domain(Pxx,-(periods[0] + 1))
#
##%% Reference
#run = '31';
#series = 'anechoic2'
#path = '/home/anthony/e4e/rct_runs/'+series+'/' 
#
#xbin        = int( np.round( (Fx - Fc) / Fsx * FFT_LENGTH ) )
#raw_files   = rct.getfiles(path,run)
#raw_files   = raw_files[:1]
#
#Pxx_ref = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')
#Px_ref = sg.medfilt(Pxx_ref,9)
#midx_ref = np.argmax(Px_ref)# find the peak sample (most likely to be a near pulse)
#
#pT_ref = rct.findTruePeriod(Px_ref,pW,pT,Fsf)
#pW_ref = rct.findTrueWidth(Px_ref,pW,pT,Fsf)
#
#pulses_ref  = rct.predictPulses(ft, Fsf, pT_ref, midx_ref)
#periods_ref = rct.predictPeriods(ft, Fsf, pT_ref, midx_ref)
#
#shift_ref = shift_signal_in_frequency_domain(Pxx_ref, periods_ref[0])
##%%
#plt.plot(ft,Pxx)
#plt.plot(ft,shift)

## CONCLUSION: WONT WORK WITH ANECHOIC, NOT IN PHASE

# create one period reference pulse
ref = np.concatenate( (np.zeros(int((pT_fix-pW_fix)*Fsf/2)), 
                       np.ones(int(pW_fix*Fsf)), 
                       np.zeros(int((pT_fix-pW_fix)*Fsf/2))) )
# phase shift
ref = np.concatenate((np.zeros(periods[0] + 1),ref[:-(periods[0] + 1)]))

Pxx_ref = []
for i in range(0,int(len(Pxx)/len(ref)) + 1):
    Pxx_ref.extend(ref)
Pxx_ref = Pxx_ref[:len(Pxx)]

conv = sg.xcorr(Pxx,Pxx_ref,mode='same')


plt.figure(1)
plt.subplot(1,2,1)
plt.plot(ft,Pxx)
plt.plot(ft,np.array(Pxx_ref)/10000)
plt.subplot(1,2,2)
plt.plot(ft,Pxx_ref)

plt.figure(2)
plt.plot(ft,Pxx)
plt.plot(ft,conv)
