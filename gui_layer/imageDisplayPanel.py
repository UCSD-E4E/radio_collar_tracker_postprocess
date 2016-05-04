import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

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
    imageList = [];
    buttonList = [];
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=210,height=HEIGHT,bg='#F0F0F0')

        number = 0


        
        self.frames = {}
        
        self.imageCanvas = interactiveImage(self)
        self.imageCanvas.grid(row=1,column=0,columnspan=100)
        
        self.addTiffButton = tk.Button(self,text="Add Tiff File")
        self.addTiffButton.grid(row=2,sticky="s")

    def newImages(self,numImages,imageIN_dir,imageNames):
        #self.imageCanvas.delete("all")
        self.image_dir = imageIN_dir;
    
    #this loop deletes all buttons
        while len(self.buttonList) > 0:
            self.buttonList[0].destroy()
            del self.buttonList[0]
        
        while len(self.imageList) > 0:
            del self.imageList[0]
            
        length = len(self.buttonList)
        print("len ButtonList = %d"%(length))    
            
            
        i = 0
        buttonOffset = 0;
        #buttonWidth = 25 / numImages; #Width / numImages
        while i < numImages:
            number = str(i)
            newButton = tk.Button(self,text=number,command=lambda i=i:self.changeImage(i))
            self.buttonList.append(newButton);
            newButton.grid(row=0,column=i)
            self.update()
            buttonOffset+=newButton.winfo_height();
            
            self.imageList.append(imageNames[i])
            i = i+1;
            
        self.numImages = numImages    
        if(numImages > 0):
            self.changeImage(0)
        
        #if self.numImages >0:
            #self.enlargeImageButton.lift()
        #else:
            #self.enlargeImageButton.lower()
            
            
    def changeImage(self,number):
        self.imageID = number
        imagePath = "%s%s" %(self.image_dir,self.imageList[number])
        self.imageCanvas.changeImage(imagePath)
        
        
        i =0
        while i < self.numImages:
            self.buttonList[i].grid(row=0,column=i)
            i=i+1
        
        
        return;
        
