import Tkinter as tk

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'map_generator'))


from PIL import Image, ImageTk
from glob import glob



class interactiveImage(tk.Canvas):
    measurementRange = [0,0]
    boundingBox = [0,0,0,0]
    imageFrame = 0
    IMSize = [190, 270]
    tiffPath = ""
    csvPath = ""
    imagePath = ""
    imageDir = ""

    def __init__(self,parent):
        tk.Canvas.__init__(self,parent,width=210,bg='#F0F0F0')
        
        
        
    def changeDataset(self,csvPath=""):
        #TODO: set this so it passes the csv to create image, then load that image
        if(csvPath != ""):
            filename,extension = os.path.splitext(csvPath)
            if(extension == ".csv"):
                if(os.path.isfile(csvPath)):
                    self.csvPath = csvPath
                    self.imagePath = csvPath.replace(".csv",".png")
                    
        self.changeImage()
            
        
        
    def changeTiff(self,tiffPath):
        filename,extension = os.path.splitext(tiffPath)
        if(extension != ".tif"):
            print("File was not a .tif file")
            return
        if(not os.path.isfile(tiffPath)):
            print("Selection was not a file")
            return
        if(self.imagePath ==""):
            self.imagePath = ""
        self.tiffPath = tiffPath
        
        self.changeImage()
        
    
    def changeImage(self,event=None):
        #Event is none so it can be called by eventhandler
        self.IMSize[0] = self.winfo_width()
        self.IMSize[1] = self.winfo_height()
            
        [self.boundingBox,self.imagePath,self.measurementRange] = self.generateMapImage(tiffPath=self.tiffPath,csvPath=self.csvPath,mapWidth=self.IMSize[0],mapHeight=self.IMSize[1])
        
        self.photoimage = ImageTk.PhotoImage(file=self.imagePath)
        self.create_image(1, 1, image=self.photoimage,anchor="nw")
        
    def getBoundingBox(self):
        return self.boundingBox
    
    def getImageSize(self):
        
        return self.IMSize
    def getTiffPath(self):
        return self.tiffPath
    def getMeasurementRange(self):
        return self.measurementRange
    def setTempDataDir(self,imageDir):
        self.imageDir = imageDir
    def attachGenerateMapImage(self,func):
        self.generateMapImage = func
        
    def reset(self):
        #self.tiffPath = "" NOTE: I could clear the tiff, but I assume most runs will be in same area
        #There is no risk of multiple tiff files being loading
        self.csvPath=""
        self.imagePath=""
        self.photoimage = None
            
        
            
            