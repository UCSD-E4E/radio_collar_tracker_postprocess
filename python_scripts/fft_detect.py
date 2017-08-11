# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:10:11 2017

@author: anthony
"""
import rct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set() # styling
import scipy.signal as sg


run = '10' #10
series = 'canyon' #canyon
path = 'C:\\Users\\anthony\\Desktop\\'+series+'\\'

Fs          = 2000000
Fx          = 172950830
Fc          = 172500000
FFT_LENGTH  = 4096
Fs_fdata    = Fs/FFT_LENGTH

pW          = 0.02 # pulse width [seconds]
pT          = 1.48 # pulse period [seconds]

xbin        = int(np.floor((Fx - Fc) / Fs * FFT_LENGTH))
raw_files   = rct.getfiles(path,run)

data    = []
fdata   = []
fdataL  = []
fdataR  = []
extra   = []

w = sg.get_window('flattop',FFT_LENGTH)

# OPTIONAL: Halfdata for speedup
#raw_files = raw_files[:int(np.ceil(len(raw_files)/2))]

for rf in raw_files :
    data = extra;extra=[]
    data.extend(rct.raw2complex(rf))
    for d in range(0,len(data),FFT_LENGTH):
        fft_in = (data[d:d+FFT_LENGTH] * w) / FFT_LENGTH
        fft_out = np.fft.fft(fft_in);fft_in=[]
        fdata.append(fft_out[xbin])
        fdataL.append(fft_out[xbin-1])
        fdataR.append(fft_out[xbin+1]);fft_out=[]
    extra = data[d+FFT_LENGTH+1:]  

fdata = np.array(fdata)

t = np.linspace(1/Fs, len(data)/Fs, len(data))
#ft = np.linspace(1/Fs,len(fdata)/Fs,len(fdata))
ft = np.linspace(1/Fs_fdata,len(fdata)/Fs_fdata,len(fdata))

plt.figure(1)
plt.subplot(1,3,1)
plt.plot(ft,abs(np.array(fdataL)))
plt.title('Left of Target Bin')
plt.ylabel("Amplitude")

plt.subplot(1,3,2)
plt.plot(ft,abs(fdata))
plt.title('Target Bin')
plt.xlabel("Time [s]")

plt.subplot(1,3,3)
plt.plot(ft,abs(np.array(fdataR)))
plt.title('Right of Target Bin')




Px = abs(fdata**2)
#pn = np.mean(Px[150:450])
#ps = np.sqrt(Px[:int(round(len(Px)/2))].max()) - pn
#SNR = 10*np.log10(ps/pn)
#print(SNR)
#
#sample = Px[:int(np.ceil(1.6*Fs_fdata))]
#potpulse = rct.Pulse(sample)



plt.figure(2)
plt.plot(ft,Px,label='Power Spectrum')
pulses = rct.Pulse.findPulses(Px)
rct.plotPulses(pulses,ft,Px)
rct.plotPeriods(ft,Fs_fdata,1.48)
#plt.legend()