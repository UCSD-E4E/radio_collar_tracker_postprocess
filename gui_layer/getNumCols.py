import os
import shutil
import fileinput

import Tkinter as tk
import tkSimpleDialog as simpledialog

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
        frequency = simpledialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
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