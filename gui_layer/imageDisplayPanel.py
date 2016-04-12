import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from getCollars import GET_NUM_COLLARS

from interactiveImage import interactiveImage


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
    imageID = 0
    #enlargeImageButton = 0
    imageCanvas = 0
    VERTICLE_PADDING = 3;
    IMSize = 190, 270
    image_dir =""
    imageList = [];
    buttonList = [];
    numcol=0
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=210,height=HEIGHT,bg='#F0F0F0')

        number = 0

        self.pack(side="top",fill="both",expand=True)
	self.top=tk.Frame(self)
	self.top.pack(side="top")

	self.container = tk.Frame(self,width=600,height=HEIGHT,bg='#F0F0F0')
	self.container.pack(side="top",fill="both",expand=True)
	self.container.grid_rowconfigure(0,weight=1)
	self.container.grid_columnconfigure(0,weight=1)
	
	self.frames = {}

	#for F in (1,2):
	    #frame = f1(container,F)
	    #self.frames[F]=frame
	    #frame.grid(row=0,column=0,sticky="nsew")
        
        #self.imageCanvas = tk.Canvas(self,width=190,height=HEIGHT,bg='#F0F0F0')
        #self.imageCanvas.pack(side='bottom',fill='both',expand=True)
        
    def show_frame(self,curr):

	frame = self.frames[curr]
	frame.tkraise()

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
            print("I is: %d, number is: %s" %(i,number))
            newButton = tk.Button(self,text=number,command=lambda i=i:self.changeImage(i))
            self.buttonList.append(newButton);
            newButton.pack(side='left')
            print("Made it here")
            self.update()
            print("But not here")
            buttonOffset+=newButton.winfo_height();
            
            self.imageList.append(imageNames[i])
            i = i+1;
            
        self.numImages = numImages    
        if(numImages > 0):
            self.changeImage(0)
            
        print("imageListLength = %d" %(len(self.imageList)))
        
        #if self.numImages >0:
            #self.enlargeImageButton.lift()
        #else:
            #self.enlargeImageButton.lower()
            
            
    def changeImage(self,number):
        self.imageID = number
        imagePath = "%s%s" %(self.image_dir,self.imageList[number])
        print("Number is %d" %(number))
        print("image_dir is :%s" %(self.image_dir))
        print("Image path is: %s" %(imagePath))
        image = Image.open(imagePath)
        image = image.resize(self.IMSize, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        #try:
        self.image = photo
        #self.imageCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.update()
        #self.imageCanvas.pack_forget()
        
        
        i =0
        while i < self.numImages:
            self.buttonList[i].pack(side='left')
            i=i+1
        
        
        return;
        
