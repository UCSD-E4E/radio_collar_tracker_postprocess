#This file will be used to standardize the names of files across the program
import os

def getProcessedRawFile(self,data_dir,run,col):
    #Data_dir is a string, run and col are integers
    return "%s/RUN_%06d_COL_%06d.raw"%(data_dir,run,col)
    
def getCSVFile(self,data_dir,run,col):
    return "%s/RUN_%06d_COL_%06d.csv"%(data_dir,run,col)
    
def getMatlabDisplayedImage(self,data_dir,run,col):
    return "%s/RUN_%06d_COL_%06d.png"%(data_dir,run,col)
    
def getDataDir(program_dir):
    print(program_dir)
    program_dir = program_dir.replace("\\","/")
    rindex = program_dir.rfind("/")
    configdir = program_dir[0:rindex]+"/temp"
    print(configdir)
    return configdir