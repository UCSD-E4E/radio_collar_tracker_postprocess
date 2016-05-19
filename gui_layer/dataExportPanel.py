import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

from simpleDialogs import *
from selectTiffOutSize import overlayOutputsDialog

import gdal #TODO: Move this to some other file, getTiffBoundsRes()

class dataExportPanel(tk.Frame):
    imageFileNameList = []
    csvFileNameList = []
    def __init__(self,parent):
        self.imageFileNameList = []
	
        tk.Frame.__init__(self,parent)
        #self.grid()
        #self.doCalculations = calculationHandler
        self.initializeWidgets()
        self.config(bg='#F0F0F0')

        
    def initializeWidgets(self):
	#self.exportButton = tk.Button(self, text='Export', command=self.exportFunction(self.imageFileNameList))
        self.exportButton = tk.Button(self, text='Export Plots', state='disabled', command=self.exportFunction)
        self.exportButton.grid(row=0,column=0)
        
        self.exportOverlayImagesButton =tk.Button(self, text='Export Overlays', state='disabled', command=self.exportOverlays)
        self.exportOverlayImagesButton.grid(row=1,column=0)
        
        self.exportShapeFilesButton = tk.Button(self, text='Export ShapeFiles', state='disabled', command=self.exportShapes)
        self.exportShapeFilesButton.grid(row=2,column=0)
        
    def exportFunction(self):
        # dest_path = filedialog.askdirectory()
        # check for existence of the file path if not ask for path again
        dest_path = filedialog.askdirectory()
        if(dest_path==""):
            return
        if os.path.exists(dest_path):
            for file in self.imageFileNameList:
                shutil.copy2(file, dest_path)
                #print 'here'
		
    def reset(self):
        self.updateImageList([])
        self.updateCSVList([])
    
    def updateCSVList(self,newList):
        self.csvFileNameList[:] = newList
        if (len(self.csvFileNameList) != 0 ):
            self.exportOverlayImagesButton.config(state='normal')
            self.exportShapeFilesButton.config(state='normal')
        else:
            self.exportOverlayImagesButton.config(state='disabled')
            self.exportShapeFilesButton.config(state='disabled')
    def updateImageList(self, newList):
        self.imageFileNameList[:] = newList
        if (len(self.imageFileNameList) != 0 ):
            self.exportButton.config(state='normal')
        else:
            self.exportButton.config(state='disabled')
    def exportOverlays(self,boundingBox = [0,0,0,0],outputSize=[0,0]):
        length = len(self.csvFileNameList)
        if(length <= 0):
            return
        
            
        
        tiffPath = self.getTiffPath()
        if(boundingBox == [0,0,0,0]):
            print("TODO: add dialog for sizing selections")
            custBoundingBox = self.getVisibleBoundingBox()
            dataBoundingBox = self.getDataBoundingBox()
            [tiffBounds,tiffRes] = self.getTiffBoundsRes(tiffPath)
            dialog=overlayOutputsDialog(self.exportOverlays,tiffPath,self.csvFileNameList[0],
                custBoundingBox,dataBoundingBox,tiffBounds,tiffRes)
        dest_dir = getDir()
        if(dest_dir==""):
            return
        
        i=0
        while i < length:
            csvPath = self.csvFileNameList[i]
            #print(csvPath)
            self.generateMapImage(tiffPath=tiffPath,csvPath=csvPath,outDir=dest_dir,mapWidth=2000,mapHeight=2000,includeLegend=True)
            i=i+1
    def exportShapes(self):
        length = len(self.csvFileNameList)
        if(length <= 0):
            return
        base_dir = getDir()
        if(base_dir==""):
            return
        i=0
        while i < length:
            csvPath = self.csvFileNameList[i]
            rindex = csvPath.rfind('/')
            outName=csvPath[rindex+1:].replace(".csv","")
            dest_dir=base_dir + '/' + outName
            self.generateShapeFiles(file=csvPath,outdir=dest_dir,outname=outName)
            i=i+1
            
            
    def getTiffBoundsRes(self,tiffPath):
        Tiffbounds = [0,0,0,0]
        TiffRes = [0,0]
        if(os.path.isfile(tiffPath)):
            dataset = gdal.Open(tiffPath, GA_ReadOnly)
            if dataset is None:
                print 'Could not open file'
            else:
                x=1
                #print("Image loaded")
            
                #Get details of image
                cols = dataset.RasterXSize
                rows = dataset.RasterYSize
                bands = dataset.RasterCount
                transform = dataset.GetGeoTransform()
                #print("cols=[%d],rows=[%d],bands=[%d]"%(cols,rows,bands))
                
                #Manually get bounds of tiff file
                leftEdge = transform[0]
                pixelWidth = transform[1]
                topEdge = transform[3]
                pixelHeight = transform[5]
                rightEdge = leftEdge + pixelWidth* cols
                bottomEdge = topEdge + rows* pixelHeight
                Tiffbounds = [leftEdge,topEdge,rightEdge,bottomEdge]
                TiffRes = [pixelWidth,pixelHeight]
        
        return [Tiffbounds,TiffRes]
    def attachGetTiffPath(self,func):
        self.getTiffPath = func
    def attachGenerateMapImage(self,func):
        self.generateMapImage=func
    def attachGenerateShapeFiles(self,func):
        self.generateShapeFiles=func
    def attachGetVisibleBoundingBox(self,func):
        self.getVisibleBoundingBox = func
    def attachGetDataBoundingBox(self,func):
        self.getDataBoundingBox = func    
