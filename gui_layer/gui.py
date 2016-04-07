#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import ttk

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from read_meta_file import read_meta_file
from getCollars import GET_NUM_COLLARS

from imageDisplayPanel import imageDisplayPanel
from auxiliaryOptionsPanel import auxiliaryOptionsPanel
from dirExportPanel import dirExportPanel
from newDataEntryPanel import newDataEntryPanel

class Application(tk.Frame):
    record = 0
    SDO = 0
    clean = 0
    randValue = 20
    HEIGHT = 300
    def __init__(self, master = None):
        tk.Frame.__init__(self, master, bg = "#F0F0F0")
        self.grid()

        self.firstF = tk.Frame(self)
        self.firstF.grid(row=0,column=0)
        self.secondF = tk.Frame(self)
        self.secondF.grid(row=0,column=1)
        self.thirdF = tk.Frame(self)
        self.thirdF.grid(row=0,column=2)

        self.placeFrames()
        self.update()

    def beginCalculations(self, data_dir, run_num, flt_alt, num_col, frequencyList):
        print("run_num= %d, flt_alt= %d, num_col= %d" % (run_num,flt_alt,num_col))
        imageList = []

        COLPath = data_dir + '/COL'
        CONFIGPath = os.path.dirname(os.path.realpath(__file__))
        CONFIGPath = CONFIGPath.replace("\\","/")
        lastIndex = CONFIGPath.rindex('/')
        CONFIGPath = CONFIGPath[0:lastIndex]
        programPath = CONFIGPath
        CONFIGPath = CONFIGPath + '/config'
        ConfigCOLPath = CONFIGPath + '/COL'
        col = 0

        self.secondFrame.scriptImplementation(programPath,data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList)
        i=1
        imageListFullPath = []
        while i <= num_col:
            imageList.append("RUN_%06d_COL_%06d.png"%(run_num,i))
            imageListFullPath.append("%s/%s" %(data_dir,imageList[i-1]))
            i = i+1
        #self.secondFrame.newImages(num_col,"%s/"%(data_dir),imageList)

        #self.secondFrame.displayImage(data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList)

        self.thirdFrame.updateList(imageListFullPath)

        #TODO: Move script stuff here

    def placeFrames(self):
        self.firstFrame = newDataEntryPanel(self.firstF, 200, '#F0F0F0', self.beginCalculations)
        separatorFrame1 = separatorFrame(self.firstF, self.HEIGHT);
        self.secondFrame = imageDisplayPanel(self.secondF, self.HEIGHT);
        separatorFrame2 = separatorFrame(self.thirdF, self.HEIGHT);
        self.thirdFrame = dirExportPanel(self.thirdF)

        self.firstFrame.grid(row=0,column=0)
        separatorFrame1.grid(row=0,column=1)
        self.secondFrame.grid(row=0,column=2)
        separatorFrame2.grid(row=0,column=3)
        self.thirdFrame.grid(row=0,column=4)


        #self.firstFrame.lift()
    def quit(self=None):
        root.destroy()

    def quitter(self):
        quit()


class separatorFrame(tk.Frame):
    def __init__(self,parent,HEIGHT):
        data_dir = tk.StringVar()
        tk.Frame.__init__(self,parent,width=2,height=HEIGHT,bg='black')

top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()
