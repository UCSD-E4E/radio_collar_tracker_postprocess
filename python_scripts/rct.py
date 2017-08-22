# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:04:21 2017

@author: anthony
"""
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt

class Pulse:
    PULSE_WIDTH     = 0.02   # seconds
    PULSE_PERIOD    = 1.6    # seconds
    pulseCount      = 0      # number of pulses accounted for
    
    fs = 2000000 / 4096 # TODO: make this dynamic or something
    pWidxs = int(np.floor(PULSE_WIDTH*fs))    # pulse width array indices
    pTidxs = int(np.floor(PULSE_PERIOD*fs))   # pulse period array indices
    
    
    def __init__(self,sample,offset=0):
        # TODO: add error checking here
        Pulse.pulseCount += 1
        self.data = sample
        self.definePulse(); self.defineNoise(); self.defineSNR();
        self.peaks = self.peaks + offset
        self.noise = self.noise + offset
                
        # TODO: make this work
    def __repr__(self):
        return str(self.peaks)
    
    def __add__(self,offset):
        # TODO: handle or prevent other data types
        return Pulse(np.copy(self.data), offset)
    
    def definePulse(self):
        self.peaks = []; data_copy = np.copy(self.data)
        for i in range(0,self.pWidxs):
            m_idx = np.argmax(data_copy)
            self.peaks.append(m_idx)
            data_copy[m_idx] = 0
        self.peaks = np.sort(self.peaks)
            
    def defineNoise(self):
        if len(self.peaks) is 0 : self.definePulse()
        l,r = np.arange(0,self.peaks[0]),np.arange(self.peaks[-1]+1,len(self.data))
        self.noise = np.concatenate([l,r])
        
    def defineSNR(self):
        # Calculates the SNR of the pulse as avg signal power - avg noise power
        if len(self.noise) is 0 : self.defineNoise()
        pow_n = np.mean(self.data[self.noise])
        pow_s = np.mean(self.data[self.peaks]) - pow_n
        self.snr = 10*np.log10(pow_s) - 10*np.log10(pow_n)
        
    def setPulseWidth(W):
        # Updates the pulse width by taking W in seconds
        Pulse.PULSE_WIDTH = W
        Pulse.pWidxs = int(np.floor(Pulse.PULSE_WIDTH*Pulse.fs))
        
    def setPulsePeriod(T):
        # Updates the pulse period by taking T in seconds
        Pulse.PULSE_PERIOD = T
        Pulse.pTidxs = int(np.floor(Pulse.PULSE_PERIOD*Pulse.fs))
    
    def setSamplingFrequency(fs):
        # Updates the sampling frequency of the data
        Pulse.fs = fs
        Pulse.pWidxs = int(np.floor(Pulse.PULSE_WIDTH*Pulse.fs))
        Pulse.pTidxs = int(np.floor(Pulse.PULSE_PERIOD*Pulse.fs))      
            
    def isWellDefined(self):
        # Returns TRUE if all peaks are arranged sequentially
        consecutive_peaks = np.arange(self.peaks[0],self.peaks[-1]+1,1)
        return np.array_equal(self.peaks,consecutive_peaks)
    
    def findPulses(power_spectrum):
        # Returns a list of Pulse objects for each period in power spectrum
        periods = range(0,len(power_spectrum),Pulse.pTidxs)
        pulses = [Pulse(power_spectrum[p:p+Pulse.pTidxs],p) for p in periods]
        return pulses
            

def raw2complex(file):
    data = np.fromfile(file,dtype=np.dtype(np.int16))
    i,q  = [data[::2],data[1::2]] 
    iq   = np.vectorize(complex)(i,q) / 4096.0 # 4096 for filetype
    return iq

def getfiles(run_folder,run_number):
    # returns a list of individiual run files and a meta file
    import glob
    folder = run_folder + 'RUN_' + run_number.zfill(6) + '/'
    files  = 'RAW_DATA_' + run_number.zfill(6) + '*'
  #  meta   = 'META_' + run_number.zfill(6)
    return glob.glob(folder + files)#, glob.glob(folder + meta)

#def processMetaFile(metafile):
#    start_time: 1501855851.174393
#    center_freq: 172500000
#    sampling_freq: 2000000
#    gain: 76.00000
#    np.loadtxt()
#def defineNoiseFloor(pulses,data):
#    noise_bin= []
#    for p in pulses:
#        if p.isWellDefined():
#            noise_bin.append(np.median(data[p.noise]))
#    return np.mean(noise_bin)
#            
#
#def isPulse(pos,pulses):
#    # Checks to see if there is a pulse at the provided index
#    
#
#def predictPulses(known_pulse_pos, pulse_period, t):
#    for i in range(0,len(t),pulse_period): # plot to the right of known pulse
#        
#    

#TODO fix precision on this
def plotPeriods(t,fs,T,midx=0,c='y',n=1):
    hp_idx = int(np.floor(T*fs/2))
    err = T*fs/2 - hp_idx
    #right
    i = 0 + midx ; diff = 0
    while ((i + hp_idx) < len(t)):
        diff += err ; #print(diff)
        if (diff >= 1) : i += 1 ; diff -=1
        plt.axvline(t[i+hp_idx], color=c, linestyle='--')
        plt.axvline(t[i], color='m',linewidth=int(0.02*fs),alpha=0.1)
        plt.scatter(t[i],0,c='m',marker='X')
        i += 2*hp_idx + int(np.ceil(4*err))
#        print('Moving right: '+str(i)+'indexes')
    #left
    i = 0 + midx ; diff = 0
    while ((i - hp_idx) >= 0):
        diff += err ; #print(diff)
        if (diff >= 1) :i -= 1 ; diff -=1
        plt.axvline(t[i-hp_idx], color=c, linestyle='--')
        plt.axvline(t[i], color='m',linewidth=int(0.02*fs),alpha=0.1)
        plt.scatter(t[i],0,c='m',marker='X')
        i -= 2*hp_idx - int(np.ceil(4*err)) - 1
#        print('Moving left: '+str(i)+'indexes')

def plotPeriods2(t, periods, color='y', linestyle='--'):
    for p in periods:
        plt.axvline(t[p],c=color,linestyle=linestyle)

def plotPulses2(t, pulses, color='m'):
    for p in pulses:
        plt.axvline(t[p], color=color,linewidth=3,alpha=0.1)
        plt.scatter(t[p],0,c=color,marker='X',vmin=0)

def predictPeriods(t,fs,pT,midx=0):
    mt = t[midx]
    rT = []; lT = []
    
    for i in range( 0, int( ( len(t[midx:]) / fs) / pT ) + 1):
        print('adding period at {0}'.format(mt + pT*(i + 0.5)))
        if (mt + pT*(i + 0.5)) <= t[-1]:
            rT.append(mt + pT*(i + 0.5))

    for i in range( 0, int( t[midx] / pT ) + 1):
        print('adding period at {0}'.format(mt - pT*(i + 0.5)))
        if (mt - pT*(i + 0.5)) >= t[0]:
            lT.append(mt - pT*(i + 0.5))
        
    lrT = np.concatenate((lT[::-1],rT))
    
    chunks = np.array_split(t,len(lrT))
    periods = [np.abs(chunks[0]-lrT[0]).argmin()]
    
    for i in range(1,len(lrT),1):
        periods.append((np.abs(chunks[i]-lrT[i]).argmin()) + i*len(chunks[i-1]))
    
    return periods

def predictPulses(t,fs,pT,midx=0):
    # Assuming that the provided max index is a pulse, finds the temporal 
    #   location of each pulse (nT). Then fits the time to the nearest index
    mt = t[midx]
    rP = []; lP = []

    # For how ever many full periods fit in the right half of the data            
    for i in range( 0, int( ( len(t[midx:]) / fs) / pT ) + 1):
        rP.append(mt + pT*i)  # Add the time that a pulse should occur
        print('adding pulse at {0}'.format(mt + pT*i))
        
    # For how ever many full periods fit in the left half of the data            
    for i in range( 0, int( ( len(t[:midx]) / fs) / pT ) + 1):
        lP.append(mt - pT*i)
        print('adding pulse at {0}'.format(mt - pT*i))

    lrP = np.concatenate((lP[::-1],rP[1:]))

    chunks = np.array_split(t,len(lrP))
    pulses =  [np.abs(chunks[0]-lrP[0]).argmin()]
    
    for i in range(1,len(lrP),1):
        pulses.append((np.abs(chunks[i]-lrP[i]).argmin()) + i*len(chunks[i-1]))

    return pulses

def plotPulses(pulses,t,xt):
    for pulse in pulses:
        if pulse.isWellDefined():
            med = (t[int(np.median(pulse.peaks))],
                         xt[int(np.max(pulse.peaks))])
            plt.scatter(t[pulse.peaks],xt[pulse.peaks],
                        c='red',marker='.',label='Detected Pulses')
            plt.annotate('SNR = '+str(int(round(pulse.snr))),
                         xy = med,
#                         xytext = (med[0]+0.1,med[1]+0.1),
#                         arrowprops=dict(facecolor='black',shrink=0.05,
#                                         width=1,headwidth=4,frac=0.2),
#                         bbox=dict(facecolor='white',edgecolor='black'),
                         label='SNR')
        else:
            plt.scatter(t[pulse.peaks],xt[pulse.peaks],
                        c='orange',marker='.',label='Possible Pulses')
#            plt.annotate(str(int(round(pulse.snr)))+'?',
#                         (t[int(np.median(pulse.peaks))],
#                         xt[int(np.median(pulse.peaks))]))


def trimmedMean(pW, pT, fs, data):
    trim = np.sort(data)
    nPeaks = int(np.ceil(pW*fs))
    nPulses = int(np.ceil(len(data)/(pT*fs)))
    trim = trim[:nPeaks+nPulses]
    return np.mean(trim)
    
def fftFromFiles(raw_files, fft_size, target_bin):
    # Returns the fft of the data in the target frequency bin over time

    fdata = []; extra = []; count = 0;
    for rf in raw_files :
        count += 1
        print('Processing File '+str(count)+'/'+str(len(raw_files)))
    
        data = extra; extra = []
        data.extend(raw2complex(rf))
        
        for d in range(0,len(data),fft_size):
            fft_in = np.array(data[d:d+fft_size])
            fft_out = np.fft.fft(fft_in) / fft_size; fft_in=[]
            fdata.append(fft_out[target_bin])
            if(d+fft_size > len(data)):
                print('Copying leftover '+str(len(data[d+fft_size+1:]))+' data points')
                extra = data[d+fft_size+1:] # THIS WAS MISINDENTED
    return np.array(fdata)

def fftFromFiles2(raw_files, fft_size, target_bin, fs, w='boxcar',ovlap=None):
    count = 0        
    fdata = []; extra = []
    for rf in raw_files:
        count += 1
        print('Processing File '+str(count)+'/'+str(len(raw_files)))
        data = extra; extra = []
        data.extend(raw2complex(rf))
        for d in range(0,len(data),fft_size):
            fft_in = np.array(data[d:d+fft_size])
            f,Pxx = sg.welch(fft_in,fs, nperseg=fft_size, window=w,
                             noverlap=ovlap, return_onesided=False)
            fdata.append(Pxx[target_bin])
            if(d+fft_size > len(data)):
                extra = data[d+fft_size+1:]
    return np.array(fdata)


def findTruePeriod(data, pW, pT, fs):
    m_idx = np.argmax(data)
    flat = sg.convolve(data,sg.flattop(49),mode='same')
    
    pW_idx, pT_idx = [int(pW*fs*2),int(pT*fs)]
    r_idx_a,r_idx_b = [m_idx+pW_idx,m_idx+pW_idx+int(pT_idx*1)]
    l_idx_a,l_idx_b = [m_idx-pW_idx-int(pT_idx*1),m_idx-pW_idx]
#    print(m_idx)
    
    if l_idx_a < 0 :
        m_idx_l = m_idx
        m_idx = 0
        m_idx = np.argmax(flat[r_idx_a:r_idx_b]) + r_idx_a
        
        r_idx_a,r_idx_b = [0,0]
        r_idx_a,r_idx_b = [m_idx+pW_idx, m_idx+pW_idx+int(pT_idx*1.5)]
#        print('Right is from: '+str(r_idx_a)+' to '+str(r_idx_b))
        m_idx_r = np.argmax(flat[r_idx_a:r_idx_b]) + r_idx_a

#        print('Moving right, L,M,R = '+str(m_idx_l)+','+str(m_idx)+','+str(m_idx_r))

    elif r_idx_b > len(data) :
        m_idx_r = m_idx
        m_idx = np.argmax(flat[l_idx_a:l_idx_b]) + l_idx_a
        
        l_idx_a,l_idx_b = [m_idx-pW_idx-int(pT_idx*1),m_idx-pW_idx]
        m_idx_l = np.argmax(flat[l_idx_a:l_idx_b]) + l_idx_a

#        print('Moving left, L,M,R = '+str(m_idx_l)+','+str(m_idx)+','+str(m_idx_r))

    else:
        m_idx_r = np.argmax(flat[r_idx_a:r_idx_b]) + r_idx_a
        m_idx_l = np.argmax(flat[l_idx_a:l_idx_b]) + l_idx_a
#        print('No need to move, L,M,R = '+str(m_idx_l)+','+str(m_idx)+','+str(m_idx_r))
        
        
#    print('LeftT: '+str((m_idx_r-m_idx)/fs)+', RightT: '+str((m_idx-m_idx_l)/fs))
    
#    # For plot testing
#    import matplotlib.pyplot as plt
#    t = np.linspace(1/fs,len(data)/fs,len(data))
#    plt.scatter(t[m_idx],data[m_idx],c='c')
#    plt.scatter(t[m_idx_l],data[m_idx_l],c='c')
#    plt.scatter(t[m_idx_r],data[m_idx_r],c='c')
#    
    return np.mean([(m_idx_r-m_idx),(m_idx-m_idx_l)])/fs

def findTrueWidth(data, pW, pT, fs):
    m_idx = np.argmax(data)
    hat = sg.convolve(data,sg.ricker(9,1),mode='same')
    
    lside = m_idx-int(pT*fs/2)
    rside = m_idx+int(pT*fs/2)
    print("left: {0}".format(lside))
    print("right: {0}".format(rside))
    lmin = int(np.argmin(hat[max(lside,0):m_idx]) + max(lside,0))
    rmin = int(np.argmin(hat[m_idx:min(rside,len(data))]) + m_idx)
    

    return (rmin-lmin)/fs
    

def readMetaFile(metafile):
    variables = []; values = [];
    with open(metafile) as file:
        for line in file:
            var,val = line.split(': ')
            variables.append(str(var))
            values.append(float(val))
    return dict( zip( variables, values ) )
    

    