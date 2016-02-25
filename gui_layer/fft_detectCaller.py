import os
import subprocess

exampleRawFile = 
exampleBeatFreq = 
exampleRawFile = 

programPath = os.path.dirname(os.path.realpath(__file__))
exePath = programPath + '\HW.exe'
print(exePath)

#GNU_RADIO_PIPELINE = programPath + '/testCompiled.o'
#os.execl(GNU_RADIO_PIPELINE,str(beat_freq),str(raw_file),str(collarFile))
subprocess.call([exePath]);