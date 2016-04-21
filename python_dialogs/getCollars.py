#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

import os
import shutil
import fileinput

def GET_NUM_COLLARS(COLPath):
    if os.path.exists(COLPath):
        return getNumCollars(COLPath)
    else: #manually collect collar frequencies and write to configDir/Col file
        collarList = getCollars();
        return len(collarList)


def getNewCollars(self=None):
    #root = tk.Tk()
    #root.withdraw()
    counter = 1
    hasOutput = False
    output = [];
    while True:
        frequency = tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
        if frequency is not None:
            output.append("%d: %d" % (counter, frequency))
            counter += 1
            hasOutput = True
        else:
            return output

def getFromFile(path):
    frequencyList = []
    lineCount = 0;
    with open(path) as infp:
        for line in infp:
            frequencyList.append(line)
            lineCount += 1
    infp.close()

    return frequencyList

def getNumCollars(path):
    lineCount = 0;
    with open(path) as infp:
        for line in infp:
            lineCount += 1

    return lineCount


def getNewCollarsClean(self=None):
    frequencyList = getNewCollars()
    outFreqList = []
    num_col = len(frequencyList);
    i = 0
    while i < num_col:
        frequencyList[i] = frequencyList[i].split(':')[1].strip()
        outFreqList.append(frequencyList[i])
        i = i+1

    return outFreqList

def getOldCollarsClean(path):
    frequencyList = getFromFile(path)
    outFreqList = []
    num_col = len(frequencyList);
    i = 0
    while i < num_col:
        frequencyList[i] = frequencyList[i].split(':')[1].strip()
        outFreqList.append(frequencyList[i])
        i = i+1

    return outFreqList

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    output = getNewCollars();
    if len(output) is 0:
        exit(1)
    for line in output:
        print(line)
    exit()

