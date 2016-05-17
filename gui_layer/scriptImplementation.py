#The responsibility of this file is to process and then possibly display
#data, the display may be handled by the gui files instead
import shutil
import os
import fileinput
#import sys
#lib_path = os.path.abspath(os.path.join('..', 'raw_gps_analysis'))
#sys.path.append(lib_path)
#lib_path = os.path.abspath(os.path.join('..', 'collarDisplay'))
#sys.path.append(lib_path)

import subprocess

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'raw_gps_analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'CLI_GUI'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'collarDisplay'))

from read_meta_file import read_meta_file
from cat_relevant import cat_relevant
from raw_gps_analysis import raw_gps_analysis
from display_data import display_data


import glob



def scriptImplementation(programPath,data_dir,config_dir,run,flt_alt,num_col,frequencyList=[],tempFolder=""):

    configCOLPath = config_dir + '/COL'
    SDRPath = config_dir + '/SDR.cfg'

    num_raw_files = glob.glob(data_dir+'/RAW_DATA_*')
    #num_collars = self.getNumCollars(ConfigCOLPath)
    raw_file = "%s/RUN_%06d.raw" % (data_dir,int(run))
    if(tempFolder !=""):
        collar_file_prefix = "%s/RUN_%06d_" % (tempFolder,int(run))
    else:
        collar_file_prefix = "%s/RUN_%06d_" % (data_dir,int(run)) 
    meta_file = "%s/META_%06d" % (data_dir,int(run))
    sdr_center_freq = read_meta_file(meta_file, 'center_freq')
    #print "sdr: \n"
    #print SDRPath
    sdr_ppm = read_meta_file(SDRPath, 'sdr_ppm')
    
    #if os.path.exists(raw_file):
    #   os.remove(raw_file)
    
    if(not os.path.isfile(raw_file)):
        print("Concatenating raw files")
        cat_relevant(data_dir,int(run)) 
    #UNCOMMENT
    
    curCol = 1
    while curCol <= num_col:
        #print("entering calculation pipeline: %d <= %d" % (curCol,num_col))
        if(len(frequencyList) == 0):
            
            frequency = read_meta_file(configCOLPath,str(curCol))
        else:
            frequency = frequencyList[curCol-1]
           #TODO: Nathan: I believe this is the errorCheck on line 117
            #TODO: strengthen this error check
        if frequency == "":
            return
        frequency = int(frequency)
 


            #TODO: Error checking
        beat_freq = getBeatFrequency(int(sdr_center_freq), int(frequency), int(sdr_ppm))
  
        
        GNU_RADIO_PIPELINE = programPath + '/../fft_detect/fft_detect'
        collarFile = "%s%06d.raw" % (collar_file_prefix, curCol)
        #print("collarFile: %s" %(collarFile))




        #os.execl(GNU_RADIO_PIPELINE,'fft_detect','-f',str(beat_freq),'-i',str(raw_file),'-o',str(collarFile))
        #print(raw_file)
        #print(GNU_RADIO_PIPELINE)
        argString = '-f ' + str(beat_freq) + ' -i ' + str(raw_file) + ' -o ' + str(collarFile)
        print("Generating raw file for collar %d"%(curCol))
        p = subprocess.call(GNU_RADIO_PIPELINE + ' ' + argString, shell=True)
        #UNCOMMENT
            
            #TODO: Error checking
        if(tempFolder == ""):
            raw_gps_analysis(data_dir,data_dir,int(run),int(curCol),int(flt_alt))
        else:
            raw_gps_analysis(data_dir,tempFolder,int(run),int(curCol),int(flt_alt),raw_dir=tempFolder)
        curCol = curCol + 1
     
    curCol = 1
    while curCol <= num_col:
        data_file = "%s/RUN_%06d_COL_%06d.csv" %(tempFolder,int(run), int(curCol))
        display_data(int(run),int(curCol),data_file,tempFolder,configCOLPath)
        curCol = curCol + 1
           
        
            
            
    #curCol = 1
    #while curCol <= num_collars:  
    #    print("entering display pipeline: %d <= %d" % (curCol,num_collars))
            #TODO: Error Checking
    #    data_file = "%s/RUN_%06d_COL_%06d.csv" % (data_dir,int(run),int(curCol))
            
    #    self.display_data(data_file,data_dir,int(run),curCol,ConfigCOLPath)
           #TODO: error Checking
            
    #    if signal_dist_outpt == 1:
    #        signal_distance_angle(data_file,data_dir,run,curCol,ConfigCOLPath)
    
    
def getBeatFrequency(center_freq,collar_freq,ppm):
    
        actual_center = int(center_freq) / 1.e6 * int(ppm) + int(center_freq)

        beat_freq = int(collar_freq) - int(actual_center)
        return(int(beat_freq))
    
