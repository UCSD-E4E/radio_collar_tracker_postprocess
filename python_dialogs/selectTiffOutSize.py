
import Tkinter as tk
import os
import PIL

import math


class overlayOutputsDialog(tk.Toplevel):
    exportFunc = 0
    boundsIV = 0


    tiffBoundingBoxRB=0
    dataBoundsRB=0
    visibleBoundsRB=0
    
    sizeTV = 0
    
    customSizeRB=0
    tiffResRB = 0
    latLongRatioRB=0
    xPixToMRB =0
    
    customSizeTBW = 0
    customSizeTBH = 0
    
    latLongRatioTB = 0
    xPixTpMTB = 0
    
    customSizeTVW = 0
    customSizeTVH = 0
    
    latLongRatioTV = 0
    xPixTpMTV = 0
    
    exportButton = 0
    
    outputSize = [0,0]
    outputBounds = [0,0,0,0]
    outResultsText = 0
    submitButton = 0
    
    def __init__(self,exportFunc=0,tiffPath="",csvPath="",custBoundingBox=[0,0,0,0],
                dataBoundingBox=[0,0,0,0],tiffBoundingBox=[0,0,0,0],tiffRes=[0,0]):
        
        tk.Toplevel.__init__(self,bg='#F0F0F0',bd=1,relief='sunken')
        self.title("Select Overlay Output")
        print("TODO: Build dialog")
        self.exportFunc = exportFunc
        self.custBoundingBox = custBoundingBox
        self.dataBoundingBox = dataBoundingBox
        self.tiffBoundingBox = tiffBoundingBox
        self.tiffRes = tiffRes
        self.tiffPath = tiffPath
        self.csvPath = csvPath
        
        
        self.initWidgets()
        
        
        
    def updateResult(self):
        boundsString = self.boundsTV.get()
        sizeString = self.sizeTV.get()
        if(boundsString == "visible"):
            if(self.custBoundingBox[0] != self.custBoundingBox[2] ):
                self.outputBounds = self.custBoundingBox
            else:
                self.outputBounds = self.dataBoundingBox
        elif(boundsString == "data"):
            if(self.dataBoundingBox[0] != self.dataBoundingBox[2]):
                self.outputBounds = self.dataBoundingBox
            else:
                self.outputBounds = self.dataBoundingBox
        elif(boundsString == "tiff"):
            if(self.tiffBoundingBox[0] != self.tiffBoundingBox[2]):
                self.outputBounds = self.tiffBoundingBox
            else:
                self.outputBounds = self.dataBoundingBox
        else:
            print("Issue with boundsTV")
            return
        custSizeW = self.customSizeTVW.get()
        custSizeH = self.customSizeTVH.get()
        lonLatRatio = self.latLongRatioTV.get()
        xPixTpMTV = self.xPixTpMTV.get()
        if(sizeString == "customSize"):
            try:
                valW = int(custSizeW)
            except ValueError:
                valW = 0
            try:
                valH = int(custSizeH)
            except ValueError:
                valH = 0
            
            self.outputSize = [valW,valH]
        elif(sizeString == "tiffRes"):
            x=10
            #NOTE: Because using the Tiff resolution requires the bounding box
            #This has been moved below
            if(self.tiffPath != ""):
                self.outputSize = self.calcTiffResSize(self.outputBounds)
            else:
                self.outputSize = [0,0]
        elif(sizeString == "latLongRatio"):
            x=1
            #NOTE: Because using the Tiff resolution requires the bounding box
            #This has been moved below
            
            try:
                val = float(lonLatRatio) * 10000
            except ValueError:
                val = 0
            latRange = self.outputBounds[2]-self.outputBounds[0]
            longRange = self.outputBounds[1]-self.outputBounds[3]
            self.outputSize = [val*latRange,val*longRange]
        elif(sizeString == "xPixToM"):
            try:
                val = float(xPixTpMTV)
            except ValueError:
                val=0
                 
            latRange = self.outputBounds[2]-self.outputBounds[0]
            longRange = self.outputBounds[1]-self.outputBounds[3]
            lat = self.outputBounds[2]
            long = self.outputBounds[1]
            
            #This is an estimate, should eb good enough for now
            if(val == 0):
                xMeters = 0
                yMeters = 0
            else:
                xMeters = (111111*math.cos(lat) * longRange) * val
                yMeters = (111111*latRange) * val
            self.outputSize=[xMeters,yMeters]
            print(self.outputSize)
        else:
            print("Issue with imageSize")
            self.outputSize = [0,0]
            return
            
        self.printProperties()
    def printProperties(self):
        OB = self.outputBounds
        OS = self.outputSize
        resultsString = "Image Size: [%d x %d]\n"%(OS[0],OS[1])
        resultsString = resultsString + "Image Bounds= [%.2f,%.2f,%.2f,%.2f]"%(OB[0],OB[1],OB[2],OB[3])
        self.updateText(self.outResultsText,resultsString)
    def outputStuff(self):
        size = self.outputSize
        bounds = self.outputBounds
        if(not(size[0] == 0 or size[1] == 0 or  bounds[0] ==0 or bounds[1] ==0 or bounds[2] == 0 or bounds[3] == 0)):
            size = [int(size[0]),int(size[1])]
            self.outputSize = size
            
            self.exportFunc(self.outputBounds,self.outputSize)
        self.destroy()
    def updateText(self,text,string):
        text.config(state="normal")
        text.delete(1.0,"end")
        text.insert("insert",string)
        text.config(state="disable")
    def calcTiffResSize(self,bounds):
        xRange = bounds[2] - bounds[0]
        yRange = bounds[1] - bounds[3]
        print(self.tiffRes)
        if(self.tiffRes[0] == 0):
            xSize = 0
        else:
            xSize = xRange / self.tiffRes[0]
        if(self.tiffRes[1] == 0):
            ySize = 0
        else:
            ySize = yRange / self.tiffRes[1]
        print(xSize,ySize)
        return [xSize,ySize]
    def initWidgets(self):
        self.boundsTV = tk.StringVar()
        self.boundsTV.set("visible")
        self.boundsTV.trace("w",lambda name, index, mode, boundsTV=self.boundsTV.get():self.updateResult())
        
        self.visibleBoundsRB = tk.Radiobutton(self,text="Use cropped bounds",variable=self.boundsTV,value="visible")
        self.dataBoundsRB = tk.Radiobutton(self,text="Use data bounds",variable=self.boundsTV,value="data")
        self.tiffBoundingBoxRB = tk.Radiobutton(self,text="Use Tiff bounds",variable=self.boundsTV,value="tiff")
        

        self.sizeTV = tk.StringVar()
        self.sizeTV.set("customSize")
        self.sizeTV.trace("w",lambda name, index, mode, sizeTV=self.sizeTV.get():self.updateResult())
        
        self.customSizeRB = tk.Radiobutton(self,text="Cust. Size",variable=self.sizeTV,value="customSize")
        self.tiffResRB = tk.Radiobutton(self,text="Keep Tiff Resolution",variable=self.sizeTV,value="tiffRes")
        self.latLongRatioRB = tk.Radiobutton(self,text="Lat/Long prop.",variable=self.sizeTV,value="latLongRatio")
        self.xPixToMRB = tk.Radiobutton(self,text="Cust. Size",variable=self.sizeTV,value="xPixToM")
        
        
        self.customSizeTVW = tk.StringVar()
        self.customSizeTVH = tk.StringVar()
        self.latLongRatioTV = tk.StringVar()
        self.xPixTpMTV = tk.StringVar()
        
        self.customSizeTVW.trace("w",lambda name, index, mode, customSizeTVW=self.customSizeTVW.get():self.updateResult())
        self.customSizeTVH.trace("w",lambda name, index, mode, customSizeTVH=self.customSizeTVH.get():self.updateResult())
        self.latLongRatioTV.trace("w",lambda name, index, mode, latLongRatioTV=self.latLongRatioTV.get():self.updateResult())
        self.xPixTpMTV.trace("w",lambda name, index, mode, xPixTpMTV=self.xPixTpMTV.get():self.updateResult())
        
        self.customSizeTBW = tk.Entry(self,textvariable=self.customSizeTVW,width=5)
        self.customSizeTBH = tk.Entry(self,textvariable=self.customSizeTVH,width=5)
        self.latLongRatioTB = tk.Entry(self,textvariable=self.latLongRatioTV,width=10)
        self.xPixTpMTB = tk.Entry(self,textvariable=self.xPixTpMTV,width=5)
        
        
        self.exportButton = tk.Button(self,text="Export",command=self.outputStuff)
        
        
        self.custSizeAText = tk.Text(self,width=2,height=1,bd=0,bg='#F0F0F0')
        self.custSizeBText = tk.Text(self,width=2,height=1,bd=0,bg='#F0F0F0')
        self.latLongRatioText = tk.Text(self,width=13,height=1,bd=0,bg='#F0F0F0')
        self.xPixTpMText = tk.Text(self,width=4,height=1,bd=0,bg='#F0F0F0')
        
        self.outResultsText = tk.Text(self,width=40,height=2,bd=0,bg='#F0F0F0')
        
        self.updateText(self.custSizeAText,"px")
        self.updateText(self.custSizeBText,"px")
        self.updateText(self.latLongRatioText,"10,000 px/lat")
        self.updateText(self.xPixTpMText,"px/m")
        self.updateText(self.outResultsText,"outputSize:\noutputBounds")
        
        self.customSizeRB.grid(row=3,column=0,sticky="w")
        self.visibleBoundsRB.grid(row=0,column=0,sticky="w")
        self.dataBoundsRB.grid(row=1,column=0,sticky="w")
        self.latLongRatioRB.grid(row=5,column=0,sticky="w")
        self.xPixToMRB.grid(row=6,column=0,sticky="w")
        
        self.customSizeTBW.grid(row=3,column=1,sticky="w")
        self.customSizeTBH.grid(row=3,column=3,sticky="w")
        self.latLongRatioTB.grid(row=5,column=1,columnspan=2,sticky="w")
        self.xPixTpMTB.grid(row=6,column=1,sticky="w")
        
        self.exportButton.grid(row=8,columnspan=100)
        
        self.custSizeAText.grid(row=3,column=2)
        self.custSizeBText.grid(row=3,column=4)
        self.latLongRatioText.grid(row=5,column=3,columnspan=2)
        self.xPixTpMText.grid(row=6,column=2)
        self.outResultsText.grid(row=7)
        
        if(self.tiffPath != ""):
            self.tiffBoundingBoxRB.grid(row=2,column=0,sticky="w")
        
        if(self.tiffPath != ""):
            self.tiffResRB.grid(row=4,column=0,sticky="w")