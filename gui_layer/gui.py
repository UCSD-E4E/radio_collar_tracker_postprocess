#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import ttk

from osgeo import gdal,ogr
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from read_meta_file import read_meta_file
from getCollars import GET_NUM_COLLARS

from imageDisplayPanel import imageDisplayPanel
from auxiliaryOptionsPanel import auxiliaryOptionsPanel
from dataExportPanel import dataExportPanel
from dataEntryPanel import dataEntryPanel

from getFileName import *
from scriptImplementation import scriptImplementation


class GUI(tk.Toplevel):
    def __init__(self,parent=None):
        tk.Toplevel.__init__(self,parent,bg='#F0F0F0',bd=1,relief='sunken')
        self.mainFrame = mainFrame(self)
        self.mainFrame.grid(row=0,column=0,sticky="nswe")
        
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        
        self.setupMenu()
        
    def setupMenu(self):
        print("TODO: Setup Menus")
    def attachPrepareConfigCol(self,func):
        self.mainFrame.attachPrepareConfigCol(func)
    def attachBeginCalculations(self,func):
        self.mainFrame.attachBeginCalculations(func)
    def attachGenerateMapImage(self,func):
        self.mainFrame.attachGenerateMapImage(func)
    def attachGenerateShapeFiles(self,func):
        self.mainFrame.attachGenerateShapeFiles(func)
        
    def setTempDataDir(self,dataDir):
        self.mainFrame.setTempDataDir(dataDir)
    def updateImageDataSet(self,num_col,frequencyList,data_dir,imageList,csvList):
        self.mainFrame.updateImageDataSet(num_col,frequencyList,"%s"%(data_dir),imageList,csvList)
    def updateExportSources(self,imageListFullPath,csvListFullPath):
        self.mainFrame.updateExportSources(imageListFullPath,csvListFullPath)
        
    def resetImageFrame(self):
        self.mainFrame.resetImageFrame()
        
    def resetExportFrame(self):
        self.mainFrame.resetExportFrame()

class mainFrame(tk.Frame):
#-------Functions pertinent to mainframe-------------
    record = 0
    SDO = 0
    clean = 0
    randValue = 20
    HEIGHT = 300
    beginCalculations = 0
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = "#F0F0F0")

        self.placeFrames()
        self.update()
        self.programDataDir = getDataDir(os.path.dirname(os.path.realpath(__file__)))
        

        self.firstFrame = dataEntryPanel(self, 200, '#F0F0F0')
        separatorFrame1 = separatorFrame(self, self.HEIGHT);
        self.secondFrame = imageDisplayPanel(self, self.HEIGHT);
        separatorFrame2 = separatorFrame(self, self.HEIGHT);
        self.thirdFrame = dataExportPanel(self)
        
        self.rowconfigure(0,weight=1)
        self.columnconfigure(2,weight=1)
        
        top = self.winfo_toplevel()
        
        #top.rowconfigure(0,weight=1)
        #top.columnconfigure(0,weight=1)

        self.firstFrame.grid(row=0,column=0)
        separatorFrame1.grid(row=0,column=1,sticky="ns")
        self.secondFrame.grid(row=0,column=2,sticky="nsew")
        separatorFrame2.grid(row=0,column=3,sticky="ns")
        self.thirdFrame.grid(row=0,column=4,sticky="nse")
    def resetFrames(self):
        self.thirdFrame.reset()
    def resetImageFrame(self):
        self.secondFrame.reset()
    def resetExportFrame(self):
        self.thirdFrame.reset()
    def getTiffFile(self):
        return self.secondFrame.getTiffFile()
        
        
    def setTempDataDir(self,dataDir):
        self.secondFrame.setTempDataDir(dataDir)
#-------Functions to First Frame-------------
    def attachPrepareConfigCol(self,func):
        self.firstFrame.attachPrepareConfigCol(func)
    def attachBeginCalculations(self,func):
        self.firstFrame.attachCalculationHandler(func)
        
#-------Functions to Second Frame-------------
    def updateImageDataSet(self,num_col,frequencyList,data_dir,imageList,csvList):
        self.secondFrame.newDataSet(num_col,frequencyList,data_dir,imageList,csvList)
    def attachGenerateMapImage(self,func):
        self.secondFrame.attachGenerateMapImage(func)
        self.thirdFrame.attachGenerateMapImage(func)
        self.thirdFrame.attachGetTiffPath(self.getTiffFile)
        
        
#-------Functions to Third Frame-------------
    def updateExportSources(self,imageListFullPath,csvListFullPath):
        self.thirdFrame.updateImageList(imageListFullPath)
        self.thirdFrame.updateCSVList(csvListFullPath)
    def attachGenerateShapeFiles(self,func):
        self.thirdFrame.attachGenerateShapeFiles(func)

        
    def quit(self=None):
        root.destroy()

    def quitter(self):
        quit()


class separatorFrame(tk.Frame):
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=2,bg='black')

