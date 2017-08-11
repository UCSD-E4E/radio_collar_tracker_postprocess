# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:53:48 2017

@author: anthony
"""

from pylab import *
import scipy.signal as sg
import numpy as np
 
# setup the problem
num_samples  = 1000 # number of samples
 
# generate an ideal signal
f_signal  = 6   # signal frequency  in Hz
dt = 0.01 # sample timing in sec
p  = 30   # 30 degrees of phase shift
a  = 1    # signal amplitude
t = np.linspace(0,dt*num_samples,num_samples)

s = [a*sin((2*pi)*f_signal*k*dt) for k in range(0,num_samples)]
#s = a*sin((2*pi)*f_signal*t)

#s = sg.square((2*pi)*(1/2.4)*t,(0.3/2.4)*s)
s_time = [k*dt for k in range(0,num_samples)]
 
# simulate measurement noise
from random import gauss
mu = 0
sigma = 2
n = [gauss(mu,sigma) for k in range(0,num_samples)]
 
# measured signal
s_measured = [ss+nn for ss,nn in zip(s,n)]
 
# take the fourier transform of the data
F = fft(s_measured)
     
# calculate the frequencies for each FFT sample
f = fftfreq(len(F),dt)  # get sample frequency in cycles/sec (Hz)
 
# filter the Fourier transform
def filter_rule(x,freq):
    band = 0.05
    if abs(freq)>f_signal+band or abs(freq)<f_signal-band:
        return 0
    else:
        return x
         
F_filtered = array([filter_rule(x,freq) for x,freq in zip(F,f)])
 
# reconstruct the filtered signal
s_filtered = ifft(F_filtered)
 
# get error
err = [abs(s1-s2) for s1,s2 in zip(s,s_filtered) ]
 
figure()
subplot(4,1,1)
plot(s_time,s)
ylabel('Original Signal')
xlabel('time [s]')
 
subplot(4,1,2)
plot(s_time,s_measured)
ylabel('Measured Signal')
xlabel('time [s]')
 
subplot(4,1,3)
semilogy(f,abs(F_filtered),'or')
semilogy(f,abs(F),'.')
legend(['Filtered Spectrum','Measured Spectrum',])
xlabel('frequency [Hz]')
 
subplot(4,1,4)
plot(s_time,s_filtered,'r')
plot(s_time,s,'b')
legend(['Filtered Signal','Original Signal'])
xlabel('time [s]')
 
 
show()