# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 11:15:58 2017

@author: anthony
"""
#%%
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt
import scipy.fftpack as fft

#%% Initialize Environmnet Variables
pi = np.pi

fx = 172950873      # collar frequency (Hz)
fc = 172500000      # center frequency (Hz)
fs = 2000000        # sampling frequency (Hz)
fft_size = 4096     # fft length
N_bins = fft_size / 2 # number of frequency bins
fr = fx / N_bins    # frequency resolution

wx = 2*pi*fx        # angular freq (rad)
pT = 1.5            # pulse period (s)
pw = 0.02           # pulse width (s)

end_time = 4
t = np.linspace(0, end_time, end_time * fs, endpoint=False)
dt = t[1] - t[0]

#%% Create On/Off Amplitude function

A_t = np.zeros(len(t))                      # Initialize array to zero
slices = int(np.ceil(len(t) / (pT/dt)))     # How many periods of ON/OFF

for k in range(slices) :
    k = k*(pT/dt)                           # For every period...
    A_t[int(k):int(k+(pw/dt)-1)] = 1        # For pulse width, set to 1

A_x = 2
x = A_t * A_x * np.sin(wx * t)              # Amplitdue modulate sine wave

#%% Decay the pulse

A_p = 2
dpulse = A_p * np.exp((-1 / end_time) * t) * x

#%% Generate noise

A_n = 0.5
noise = np.random.normal(0,A_n,len(t)) # UG Noise

#%% Create Sample

x = dpulse + noise


#%% Calculate FFT

#fft_length = len(t)
fft_size = len(t)
## FFT of Sample
X = fft.fft(x,fft_size)

## Frequencies of each sample
f = fft.fftfreq(len(X),1/fs)
#X = X[0:int(np.floor(len(X)/2))]

#%%
## Filter for FFT
bw = 50000 # bandwidth from peak of signal to recover

def filter_rule(x,freq,band): 
    if abs(freq)>fs/2+band or abs(freq)<fs/2-band:
        return 0
    else:
        return x

Xfilt = np.array([filter_rule(x,freq,bw) for x,freq in zip(X,f)])
xfilt = fft.ifft(Xfilt)

err = [abs(s1-s2) for s1,s2 in zip(x,xfilt)]

#%% Gather SNRs

def snr_db(s_samp,n_samp):
    p_n = (1/len(n_samp))*np.sum(abs(n_samp)**2)
    p_s = (1/len(s_samp))*np.sum(abs(s_samp)**2)
    return 10*np.log10((p_s-p_n)/p_n)

s_idx,n_idx = [np.where(A_t != 0)[0],np.where(A_t == 0)[0]]

x_SNR       = snr_db(x[s_idx], x[n_idx])
xfilt_SNR   = snr_db(xfilt[s_idx], xfilt[n_idx])

#%% Plot
plt.figure(1)
plt.plot(t,x)
plt.plot(t,dpulse)
plt.xlim(0,end_time)
plt.title("Collar Pings with Noise")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.legend(['Noisey Signal','Ideal Signal'])
plt.text(0.1,0.1,'SNR = '+str(round(x_SNR,2))+' dB',
         transform=plt.gca().transAxes,
         bbox=dict(facecolor='white',edgecolor='black'))

# TODO: Label (Understand) the axis for the fourier transform
plt.figure(2)
plt.semilogy(f,abs(X),'.b')
plt.semilogy(f,abs(Xfilt),'or')
plt.title("Frequency Spectrum")
plt.xlabel('Frequency')
plt.legend(['Measured Spectrum','Filtered Spectrum'])

plt.figure(3)
plt.plot(t,x)
plt.plot(t[:fft_size],xfilt,'r')
plt.xlim(0,end_time)
plt.title("Filtered Signal")
plt.xlabel('Time [s]')
plt.legend(['Noisey Signal','Recovered Signal'])
plt.text(0.1,0.1,'SNR = '+str(round(xfilt_SNR,2))+' dB'
         ,transform=plt.gca().transAxes,
         bbox=dict(facecolor='white',edgecolor='black'))






























