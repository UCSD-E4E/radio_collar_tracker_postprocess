# -*- coding: utf-8 -*-
"""
Test Signal

Generates a signal with noise to be used as a sample data set for DSP
"""
import numpy as np
#from scipy import signal as sg
import scipy.signal as sg
import matplotlib.pyplot as plt

pi = np.pi

def nan_helper(y): # (stackoverflow.com/questions/6518811)
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def rm_nans(y):
    nans, x = nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
    return y


fx = 172950873  # collar frequency (Hz)
fs = 2000000    # sampling frequency (Hz)
wx = 2*pi*fx    # angular freq (rad)
pT = 2.4        # pulse period (s)
pw = 0.3        # pulse width (s)

end_time = 20
t = np.linspace(0, end_time, end_time * fs, endpoint=False)

## Generate collar's pulsing signal
A_p = 2
#collar = np.cos(wx * t)
collar = np.sin(wx * t)
pulse = sg.square(2 * pi * (1/pT) * t, (pw/pT) * collar) + 1
pulse = rm_nans(pulse)
dpulse = A_p * np.exp((-1 / end_time) * t) * pulse           # decaying collar signal

#plt.plot(t,dpulse)
#plt.xlim(0,end_time)

## Generate noise
A_n = 0.5
noise = np.random.normal(0,A_n,len(t)) # UG Noise

#plt.plot(t,noise)
#plt.xlim(0,end_time)

## Create Sample
x = dpulse + noise

plt.figure(1)
plt.plot(t,x)
plt.plot(t,dpulse)
plt.xlim(0,end_time)
plt.title("Collar Pings with Noise")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend(['Noisey Signal','Original Signal'])
###############################################################################

"""
FFT

"""
import scipy.fftpack as fft

fft_length = 4096

## FFT of Sample
X = fft.fft(x)

## Frequencies of each sample
f = fft.fftfreq(len(X),1/fs)
#X = X[0:int(np.floor(len(X)/2))]

## Filter for FFT
def filter_rule(x,freq):
    band = 1000000
    if abs(freq)>fs+band or abs(freq)<fs-band:
        return 0
    else:
        return x

Xfilt = np.array([filter_rule(x,freq) for x,freq in zip(X,f)])

xfilt = fft.ifft(Xfilt)

err = [abs(s1-s2) for s1,s2 in zip(x,xfilt)]


### Power Spectral Density
#Xpsd = np.abs(X) ** 2

## Corresponding frequencies
#Xfreqs = sg.fftfreq(len(Xpsd), spacing)

#f = np.linspace(0,round(fs/2/fft_length),round((end_time*fs)/2))
#
#t2= t[0:int(np.floor(len(t)/2))]
#
#f2 = np.linspace(0,len(X)/round(fs/fft_length))

#f = np.linspace(0,len(X))

plt.figure(2)
plt.subplot(2,1,1)
plt.semilogy(f,abs(Xfilt),'or')
plt.semilogy(f,abs(X),'.')
plt.legend(['Filtered Spectrum','Measured Spectrum',])
plt.xlabel('frequency [Hz]')

plt.subplot(4,1,4)
plt.plot(t,xfilt,'r')
plt.plot(t,x,'b')
plt.legend(['Filtered Signal','Original Signal'])
plt.xlabel('time [s]')

