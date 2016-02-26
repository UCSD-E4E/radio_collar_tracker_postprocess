#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

import os
import shutil
import fileinput
if __name__ == "__main__":
    #Consider trying to make this call one of the below functions
    root = tk.Tk()
    root.withdraw()
    counter = 1
    hasOutput = False
    while True:
        frequency = tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
        if frequency is not None:
            print("%d: %d" % (counter, frequency))
            counter += 1
            hasOutput = True
        else:
            if not hasOutput:
                exit(1)
            else:
                exit()

            
def GET_NUM_COLLARS(COLPath):

    
    if os.path.exists(COLPath):
        return getNumCollars(COLPath)
    else: #manually collect collar frequencies and write to configDir/Col file
        collarList = getCollars();
        return len(collarList)
            
            
def getCollars(self=None):
    root = tk.Tk()
    root.withdraw()
    counter = 1
    hasOutput = False
    output = [];
    while True:
        frequency = tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
        if frequency is not None:
            output.append("%d: %d\n" % (counter, frequency))
            counter += 1
            hasOutput = True
        else:
            return output
            
def getNumCollars(path):
    lineCount = 0;
    with open(path) as infp:
        for line in infp:
            lineCount += 1
                    
    return lineCount