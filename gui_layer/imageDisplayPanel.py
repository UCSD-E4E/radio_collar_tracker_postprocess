import Tkinter as tk

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from getCollars import GET_NUM_COLLARS



from PIL import Image, ImageTk
from glob import glob


#The responsibility of this file is to process and then possibly display
#data, the display may be handled by the gui files instead
import shutil
import fileinput

#import sys
#lib_path = os.path.abspath(os.path.join('..', 'raw_gps_analysis'))
#sys.path.append(lib_path)
#lib_path = os.path.abspath(os.path.join('..', 'collarDisplay'))
#sys.path.append(lib_path)


import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'raw_gps_analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'CLI_GUI'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'collarDisplay'))

from read_meta_file import read_meta_file
from cat_relevant import cat_relevant
from raw_gps_analysis import raw_gps_analysis
from display_data import display_data
from interactiveImage import interactiveImage
from simpleDialogs import *

import numpy as np
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
import matplotlib.pyplot as plot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class imageDisplayPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    numImages = 0
    VERTICLE_PADDING = 3;
    image_dir =""
    csv_dir = ""
    imageList = [];
    csvList = []
    buttonList = [];
    frequencyList = []
    locationText = ""
    changeTiffButton = 0
    def __init__(self,parent,HEIGHT,WIDTH=210):
        tk.Frame.__init__(self,parent,width=WIDTH,height=HEIGHT,bg='#F0F0F0')

        number = 0

        
        
        self.frames = {}
        
        self.locationText = tk.Text(self,height=4,state='disable',bg='#F0F0F0',bd=0,wrap='char',width=40)
        self.locationText.config(state='normal')
        self.locationText.delete(1.0, 'end')
        self.locationText.config(state='disable',fg='#F0F0F0')
        self.locationText.grid(row=1,columnspan=100)
        
        self.imageCanvas = interactiveImage(self)
        self.imageCanvas.grid(row=2,column=0,columnspan=100,sticky="nsew")
        self.imageCanvas.bind("<Motion>",self.mouseMoved)
        self.imageCanvas.bind("<Leave>",self.mouseLeft)
        self.imageCanvas.bind("<Configure>", self.imageCanvas.changeImage)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(2,weight=1)
        
        self.addTiffButton = tk.Button(self,text="Add Tiff File",command=self.updateTiff)
        self.addTiffButton.grid(row=3,columnspan=100,sticky="s")
        
        
    
    
    
    
    def newDataSet(self,numImages,frequencyList,imageIN_dir,imageNames,csvNames):
        #self.imageCanvas.delete("all")
        self.frequencyList = frequencyList
        self.curFrequency = 0
        self.image_dir = imageIN_dir;
    
    #this loop deletes all buttons
        while len(self.buttonList) > 0:
            self.buttonList[0].destroy()
            del self.buttonList[0]
        
        self.imageList=[]
        self.csvList=[]
                       
            
        i = 0
        buttonOffset = 0;
        #buttonWidth = 25 / numImages; #Width / numImages
        while i < numImages:
            number = str(i)
            textNumber = str(i+1)
            newButton = tk.Button(self,text=textNumber,command=lambda i=i:self.changeImage(i))
            self.buttonList.append(newButton);
            newButton.grid(row=0,column=i+1,sticky="w")
            self.update()
            buttonOffset+=newButton.winfo_height();
            
            self.imageList.append(imageNames[i])
            self.csvList.append(csvNames[i])
            i = i+1;
            
        self.numImages = numImages    
        if(numImages > 0):
            self.changeImage(0)
        
        #if self.numImages >0:
            #self.enlargeImageButton.lift()
        #else:
            #self.enlargeImageButton.lower()
            
    def updateTiff(self):
        tiffFile = getFile()
        self.imageCanvas.changeTiff(tiffFile)
    def changeImage(self,number):
        #Make this find the correct CSV
        self.imageID = number
        csvPath = "%s%s" %(self.image_dir,self.csvList[number])
        self.imageCanvas.changeDataset(csvPath)
        self.curFrequency = number
        #This is called to update the text box
        self.mouseLeft(2)#2 is filler for event
        
        
        i =0
        while i < self.numImages:
            #self.buttonList[i].grid(row=0,column=i)
            i=i+1
        
        
        return;
    def mouseMoved(self,event):
        x = event.x
        y = event.y
        
        boundingBox = self.imageCanvas.getBoundingBox() #This is the geographic size    [left,top,right,bottom]
        imageSize = self.imageCanvas.getImageSize()     #This is the image's size       [width,height]
        
        if(boundingBox[0] == boundingBox[1] and boundingBox[0] == 0):
            #assume if BB,(0,0) there is nothing loaded
            return
        
        xResolution = (boundingBox[2] - boundingBox[0]) / imageSize[0]
        yResolution = (boundingBox[3] - boundingBox[1]) / imageSize[1]
        
        Xpos = boundingBox[0] + x * xResolution
        Ypos = boundingBox[3] - y * yResolution
        measurementRange = self.imageCanvas.getMeasurementRange()
        
        #textString = "longitude: %f\nLatitude: %f"%(Xpos,Ypos)
        textString = "%.3f MHz\nMeasurementRange: [%.2f <-> %.2f]\nLatitude: %f\nLongitude: %f"%(self.frequencyList[self.curFrequency],measurementRange[0],measurementRange[1],Ypos,Xpos)
        
        self.locationText.config(state='normal')
        self.locationText.delete(1.0, 'end')
        self.locationText.insert('insert',textString)
        self.locationText.config(state='disable',fg='black')
        
    def mouseLeft(self,event):
        if(len(self.frequencyList) !=0):
            self.locationText.config(state='normal')
            self.locationText.delete(1.0, 'end')
            measurementRange = self.imageCanvas.getMeasurementRange()
            self.locationText.insert('insert',"%f MHz\nMeasurementRange: [%04f <-> %04f]\n"%(self.frequencyList[self.curFrequency],measurementRange[0],measurementRange[1]))
            self.locationText.config(state='disable')
        
    def getTiffFile(self):
        return self.imageCanvas.getTiffPath()
    def setTempDataDir(self,data_dir):
        self.imageCanvas.setTempDataDir(data_dir)
    def attachGenerateMapImage(self,func):
        self.imageCanvas.attachGenerateMapImage(func)
    def reset(self):
        #numImages,frequencyList,imageIN_dir,imageNames,csvNames)
        self.newDataSet(0,[],"",[],[])
        self.imageCanvas.reset()
        
