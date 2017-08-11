# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:04:21 2017

@author: anthony
"""
import numpy as np

class Pulse:
    PULSE_WIDTH     = 0.02  # seconds
    PULSE_PERIOD    = 1.48   # seconds
    pulseCount      = 0     # number of pulses accounted for
    
    fs = 2000000 / 4096 # TODO: make this dynamic or something
    __pWidxs = int(np.floor(PULSE_WIDTH*fs))
    __pTidxs = int(np.floor(PULSE_PERIOD*fs))
    
    
    def __init__(self,sample,offset=0):
        # TODO: add error checking here
        Pulse.pulseCount += 1
#        Pulse.__pWidxs = int(np.floor(Pulse.PULSE_WIDTH*self.fs))
#        Pulse.__pTidxs = int(np.floor(Pulse.PULSE_PERIOD*self.fs))
#        self.peaks = peaks; self.noise = noise; self.snr = float()
        self.data = sample
        self.definePulse(); self.defineNoise(); self.defineSNR();
        self.peaks = self.peaks + offset
        self.noise = self.noise + offset
        

            
        # TODO: add class functions to constructor for simpler use.
    
        # TODO: make this work
    def __repr__(self):
        return str(self.peaks)
    
    def __add__(self,offset):
        # TODO: handle or prevent other data types
        return Pulse(np.copy(self.data), offset)
    
    def definePulse(self):
        self.peaks = []; data_copy = np.copy(self.data)
        for i in range(0,self.__pWidxs):
            m_idx = np.argmax(data_copy)
            self.peaks.append(m_idx)
            data_copy[m_idx] = 0
        self.peaks = np.sort(self.peaks)
            
    def defineNoise(self): # TODO does this need to force noise = [] ?
        if len(self.peaks) is 0 : self.definePulse()
        l,r = np.arange(0,self.peaks[0]),np.arange(self.peaks[-1]+1,len(self.data))
        self.noise = np.concatenate([l,r])
        
        
    def defineSNR(self):
        if len(self.noise) is 0 : self.defineNoise()
        pow_n = np.mean(self.data[self.noise])
        pow_s = np.mean(self.data[self.peaks]) - pow_n
        self.snr = 10*np.log10(pow_s) - 10*np.log10(pow_n)
        
            
    def isWellDefined(self):
        consecutive_peaks = np.arange(self.peaks[0],self.peaks[-1]+1,1)
        return np.array_equal(self.peaks,consecutive_peaks)
    
    def findPulses(power_spectrum):
        periods = range(0,len(power_spectrum),Pulse.__pTidxs)
        pulses = [Pulse(power_spectrum[p:p+Pulse.__pTidxs],p) for p in periods]
        return pulses
            

def raw2complex(file):
    data = np.fromfile(file,dtype=np.dtype(np.int16))
    i,q  = [data[::2],data[1::2]] 
    iq   = np.vectorize(complex)(i,q) / 4096.0 # 4096 for filetype
    return iq

def getfiles(run_folder,run_number):
    import glob
    folder = run_folder + 'RUN_' + run_number.zfill(6) + '/'
    files  = 'RAW_DATA_' + run_number.zfill(6) + '*'
    return glob.glob(folder + files)

#    
#def definePulse(sample,width,fs):
#    maxima = []; sample = np.copy(sample);
#    for i in range(0,int(np.floor(width*fs))) :
#        m_idx = np.argmax(sample)
#        maxima.append(m_idx)
#        sample[m_idx] = 0
#    return maxima
#
#def isWellDefined(pulse):
#    pulse = np.sort(pulse)
#    return np.array_equal(pulse,np.arange(pulse[0],pulse[-1]+1,1))
#
#def findPulses(data,period,width,fs):
#    pulses = []; T = int(np.floor(period*fs))
#    for i in range(0,len(data),T) :
#        pulses.extend(np.array(definePulse(data[i:i+T],width,fs))+i)
#    return pulses


def plotPeriods(t,fs,T):
    import matplotlib.pyplot as plt
    for i in range(0,len(t),int(np.floor(T*fs))):
        plt.axvline(t[i], color = 'y', linestyle = '--')

def plotPulses(pulses,t,xt):
    import matplotlib.pyplot as plt
    for pulse in pulses:
        if pulse.isWellDefined():
            plt.scatter(t[pulse.peaks],xt[pulse.peaks],
                        c='red',marker='.',label='Detected Pulses')
            plt.annotate(str(int(round(pulse.snr))),
                        (t[int(np.median(pulse.peaks))],
                         xt[int(np.max(pulse.peaks))]),
                         label='SNR')
        else:
            plt.scatter(t[pulse.peaks],xt[pulse.peaks],
                        c='orange',marker='.',label='Possible Pulses')
#            plt.annotate(str(int(round(pulse.snr)))+'?',
#                         (t[int(np.median(pulse.peaks))],
#                         xt[int(np.median(pulse.peaks))]))

