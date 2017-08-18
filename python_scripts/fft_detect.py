# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:10:11 2017

@author: anthony
"""
#%%
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
run = '25';
series = 'canyon'
path = 'C:\\Users\\anthony\\Desktop\\e4e\\'+series+'\\' # Inside here should be a RUN_000## folder

# TODO: Use META_DATA file for literals and run variables
Fsx         = 2000000.0       # sampling frequency of input data
Fx          = 172950830.0
Fc          = 172500000.0
FFT_LENGTH  = 4096
Fsf         = Fsx/FFT_LENGTH # sampling frquency of fft

pW          = 0.02 # pulse width [seconds]
pT          = 1.6 # pulse period [seconds]
rct.Pulse.setPulsePeriod(pT)

xbin               = int( np.round( (Fx - Fc) / Fsx * FFT_LENGTH ) )
raw_files         = rct.getfiles(path,run)
raw_files   = raw_files[-3:]


#%% FFT
# return the power spectrum (time domain)
Px = rct.fftFromFiles2(raw_files,FFT_LENGTH,xbin,Fsx,w='boxcar')

# frequency time axis (length of fft)
ft = np.linspace(1/Fsf,len(Px)/Fsf,len(Px))

# find the peak sample (most likely to be a near pulse)
midx = np.argmax(Px)


truePeriod = rct.findTruePeriod(Px,pW,pT,Fsf)
trueWidth = rct.findTrueWidth(Px,pW,pT,Fsf)
print("TW adjust, pass 1:")
print("T,W: "+str(pT)+'-->'+str(truePeriod)+','+str(pW)+'-->'+str(trueWidth))

truePeriod = rct.findTruePeriod(Px,trueWidth,truePeriod,Fsf)
trueWidth = rct.findTrueWidth(Px,trueWidth,truePeriod,Fsf)
print("TW adjust, pass 2:")
print("T,W: "+str(truePeriod)+','+str(trueWidth))

truePeriod = rct.findTruePeriod(Px,trueWidth,truePeriod,Fsf)
trueWidth = rct.findTrueWidth(Px,trueWidth,truePeriod,Fsf)
print("TW adjust, pass 3:")
print("T,W: "+str(truePeriod)+','+str(trueWidth))

rct.Pulse.setPulsePeriod(truePeriod)
rct.Pulse.setPulseWidth(trueWidth)


#sample1 = Px[:int(pT*Fsf)]
#sample2 = Px[int(1*pT*Fsf):int(2*pT*Fsf)]
#sample3 = Px[int(2*pT*Fsf):int(3*pT*Fsf)]
#sample4 = Px[int(3*pT*Fsf):int(4*pT*Fsf)]
#sample = np.concatenate((sample1,sample2,sample3,sample4))
#t1 = np.linspace(1/Fsf,len(sample1)/Fsf,len(sample1))
#t2 = np.linspace(t1[-1] + len(sample2)/Fsf,len(sample2)/Fsf,len(sample2))
#t3 = np.linspace(t2[-1] + len(sample3)/Fsf,len(sample3)/Fsf,len(sample3))
#t4 = np.linspace(t3[-1] + len(sample4)/Fsf,len(sample4)/Fsf,len(sample4))
#t = np.concatenate((t1,t2,t3,t4))
#
#
#
#plt.figure(1)
#plt.subplot(1,4,1)
#plt.plot(t1,sample1)
#plt.subplot(1,4,2)
#plt.plot(t2,sample2)
#plt.subplot(1,4,3)
#plt.plot(t3,sample3)
#plt.subplot(1,4,4)
#plt.plot(t4,sample4)
 
#%% Plotting Fre quency Windows
#plt.figure(1) # plot frequency bin and adjacent bins
#plt.subplot(1,3,1)
#plt.plot(ft,abs(np.array(fdataL)))
#plt.title('Left of Target Bin')
#plt.ylabel("Amplitude")
#
#plt.subplot(1,3,2)
#plt.plot(ft,abs(fdata))
#plt.title('Target Bin')
#plt.xlabel("Time [s]")
#
#plt.subplot(1,3,3)
#plt.plot(ft,abs(np.array(fdataR)))
#plt.title('Right of Target Bin')

#%% Sample rct.Pulse Use
#sample = Px[:int(np.ceil(1.6*Fs_fdata))]
#potpulse = rct.Pulse(sample)


#%% Plot Pulses and Power Spectrum
plt.figure(1)
plt.plot(ft,Px,label='Power Spectrum with Pulse Prediction')
plt.title('Detected Pulses in Power Spectrum')

# TODO: find best two
pW = trueWidth
pT = truePeriod
#rct.Pulse.setPulsePeriod((np.median(pulses[1].peaks) - np.median(pulses[0].peaks))/Fsf)
rct.Pulse.setPulsePeriod(truePeriod)
pulses = rct.Pulse.findPulses(Px)
    

rct.plotPulses(pulses,ft,Px)
#rct.plotPeriods(ft,Fsf,rct.Pulse.PULSE_PERIOD,np.argmax(Px))

rct.plotPeriods(ft,Fsf,truePeriod,np.argmax(Px),'y')


import matplotlib.lines as mlines

blu_lin = mlines.Line2D([],[],c='b')
mag_lin = mlines.Line2D([],[],c='m',marker='X')
red_dot = plt.scatter([],[],c='r')
org_dot = plt.scatter([],[],c='orange')
plt.legend([blu_lin,mag_lin,red_dot,org_dot],
           ['Power Spectrum','Expected Pulse','Detected Pulse','Possible Pulse'])
plt.ylabel("Power")
#plt.xlabel("Time [s]")
#avgSNR = np.sum([p.snr for p in pulses])/ rct.Pulse.pulseCount
#plt.text(0.1,0.1,'Average SNR = '+str(round(avgSNR,2))+' dB'
#         ,transform=plt.gca().transAxes,
#         bbox=dict(facecolor='white',edgecolor='black'))
#plt.legend()

#%% smooth moves
#sPx = sg.medfilt(Px)
sPx9 = sg.medfilt(Px,9)
pW = rct.findTrueWidth(sPx9,pW,pT,Fsf)
#sPx49 = sg.medfilt(Px,49)
#sPx999 = sg.medfilt(Px,999)
#
#plt.figure(2)
#plt.subplot(3,2,1)
#plt.plot(ft,Px)
#plt.plot(ft,sPx)
#plt.title('Median Filter, N=3')
#plt.subplot(3,2,2)
#plt.plot(ft,Px)
#plt.plot(ft,sPx9)
#plt.title('Median Filter, N=9')
#plt.subplot(3,2,3)
#plt.plot(ft,Px)
#plt.plot(ft,sPx49)
#plt.title('Median Filter, N=49')
#plt.subplot(3,2,4)
#plt.plot(ft,Px)
#plt.plot(ft,sPx999)
#plt.title('Median Filter, N=999')
#plt.subplot(3,2,5)
#plt.plot(ft,sPx)
#plt.plot(ft,sg.medfilt(sPx,3))
#plt.plot(ft,sg.medfilt(sPx,9))
#plt.legend(['Pass1','Pass2, N=3', 'Pass2, N=9'])
#plt.title('Median Filter, N=3 (2nd Pass)')
#plt.subplot(3,2,6)
#plt.plot(ft,sPx9)
#plt.plot(ft,sg.medfilt(sPx9,3))
#plt.plot(ft,sg.medfilt(sPx9,9))
#plt.legend(['Pass1','Pass2, N=3', 'Pass2, N=9'])
#plt.title('Median Filter, N=9 (2nd Pass)')
###CONCLUSION: median filter with N = 9 is best

#%% TEST Flattop test for making well defined peaks
## CONCLUSION Flattop works. 49 good balance, more makes all peaks(noise) higher
#plt.figure(3)
#plt.plot(ft,sPx9)
smoothPeriod = rct.findTruePeriod(sPx9,pW,truePeriod,Fsf)
#rct.plotPeriods(ft,Fsf,smoothPeriod,np.argmax(sPx9))

#flt9 = sg.convolve(sPx9,sg.flattop(9),mode='same')
flt49 = sg.convolve(sPx9,sg.flattop(49),mode='same')
#flt99 = sg.convolve(sPx9,sg.flattop(99),mode='same')

plt.figure(2)
plt.plot(ft,flt49)
flatPeriod = rct.findTruePeriod(flt49,pW,smoothPeriod,Fsf)
rct.plotPeriods(ft,Fsf,flatPeriod,np.argmax(flt49))
adj = 4 # magic number?
peaks = pu.indexes(flt49,thres=0,min_dist=flatPeriod*Fsf - adj)
plt.scatter(ft[peaks],flt49[peaks],color='r')

#%% ricker wavelet for pulse width detection

###TEST 1 -- assumes squareish --- RESULT: pW = 0.006144 (way too thin)
#same = True; tops = []; top_val = test[np.argmax(test)];
#while(same):
#    top = np.argmax(test)
#    tops.append(top)
#    test[top] *= -1
#    if not np.allclose(abs(test[tops]),[top_val]):
#        same = False
#        test[tops] *= -1
#        tops = tops[:-1]

# 9,1 hat on sPx9 is best
#hat = sg.convolve(Px,sg.ricker(9,1), mode='same')
smoothhat = sg.convolve(sPx9,sg.ricker(9,1),mode='same')
#flathat = sg.convolve(flt49,sg.ricker(9,1),mode='same')
#plt.figure(5)
#plt.subplot(1,3,1)
#plt.plot(ft,Px)
#plt.plot(ft,hat)
#plt.subplot(1,3,2)
#plt.plot(ft,sPx9)
#plt.plot(ft,smoothhat)
#plt.subplot(1,3,3)
#plt.plot(ft,flt49)
#plt.plot(ft,flathat)

#%% Welch exp
#plt.figure(2)
#plt.subplot(2,1,1)
##plt.semilogy(ft,abs(fdata)/FFT_LENGTH)
#plt.title("Nathan's Method")
#plt.subplot(2,1,2)
#plt.semilogy(ft,fdata2)
#plt.title("SciPy's Welch Method")

midx = np.argmax(flt49)

per = rct.predictPeriods(ft, Fsx, pT, midx)
pul = rct.predictPulses(ft, Fsx, pT, midx)
plt.figure(6)
plt.plot(ft,flt49)
rct.plotPeriods2(ft,per)
rct.plotPulses2(ft,pul)
adj = .8 # magic number?
peaks = pu.indexes(flt49,thres=0,min_dist=flatPeriod*Fsf*adj)
plt.scatter(ft[peaks],flt49[peaks],color='r')
