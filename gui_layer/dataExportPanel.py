import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

from simpleDialogs import *

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
    def exportOverlays(self):
        length = len(self.csvFileNameList)
        if(length <= 0):
            return
        tiffPath = self.getTiffPath()
        dest_dir = getDir()
        if(dest_dir==""):
            return
        
        i=0
        while i < length:
            csvPath = self.csvFileNameList[i]
            #print(csvPath)
            self.generateMapImage(tiffPath=tiffPath,csvPath=csvPath,outDir=dest_dir,mapWidth=600,mapHeight=800)
            
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
    def attachGetTiffPath(self,func):
        self.getTiffPath = func
    def attachGenerateMapImage(self,func):
        self.generateMapImage=func
    def attachGenerateShapeFiles(self,func):
        self.generateShapeFiles=func
        
