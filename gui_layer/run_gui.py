#This will be application level, and will have all non-gui functions
import sys
import os
import glob

import Tkinter as tk

from gui import GUI

from scriptImplementation import scriptImplementation
from gen_overlayed_image import generateMapImage
from create_shapefile import create_shapefile
from getFileName import *


class Application():
    tempDir = ""
    def __init__(self,master=None):
        
        self.root = tk.Tk()
        self.root.withdraw()
        self.GUI = GUI(self.root)
        self.GUI.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.GUI.title('Radio Collar Tracker')
        
        self.attachFunctions()
        
        
        self.generateProgramPath()
        self.generateTempDir()
        self.generateConfigDir()
        
        self.setupValues()
        
        self.root.mainloop()
        
    def attachFunctions(self):
        self.GUI.attachBeginCalculations(self.beginCalculations)
        self.GUI.attachPrepareConfigCol(self.prepareConfigCOLFile)
        self.GUI.attachGenerateMapImage(self.generateMapImage)
        self.GUI.attachGenerateShapeFiles(self.generateShapeFiles)

    def setupValues(self):
        self.GUI.setTempDataDir(self.getTempDir())
    
    def beginCalculations(self, data_dir, run_num, flt_alt, num_col, frequencyList):
        #print("run_num= %d, flt_alt= %d, num_col= %d" % (run_num,flt_alt,num_col))
        imageList = []
        csvList = []
        self.clearTempFolder()
        self.GUI.resetImageFrame()
        self.GUI.resetExportFrame()
        
        programPath = self.programPath
        CONFIGPath = self.configDir
        col = 0
        
        scriptImplementation(programPath,data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList,self.tempDirPath)
        
        i=1
        imageListFullPath = []
        csvListFullPath = []
        frequencyListINT = []
        while i <= num_col:
            fileName = "RUN_%06d_COL_%09d"%(run_num,frequencyList[i-1])
            print("run_gui: csvPath=%s"%(self.tempDirPath+fileName+".csv"))
            imageList.append(fileName+".png")
            csvList.append(fileName+".csv")
            imageListFullPath.append("%s/%s" %(self.tempDirPath,imageList[i-1]))
            csvListFullPath.append("%s/%s" %(self.tempDirPath,csvList[i-1]))
            frequencyListINT.append(int(frequencyList[i-1])/1000000.)
            i = i+1
            
        print("run_gui: %s"%(self.tempDirPath))
        self.GUI.updateImageDataSet(num_col,frequencyListINT,"%s/"%(self.tempDirPath),imageList,csvList)
        self.GUI.updateExportSources(imageListFullPath,csvListFullPath)
        
    def clearTempFolder(self=None):
        tempPath = self.tempDirPath
        print("Clearing Temp Folder")
        print(tempPath)
        if(not "guiTempData" in tempPath):
            print("temp folder appears to not have been set properly")
            return
        
        for file in glob.glob(tempPath + "/*.png"):
            print("Removing file %s"%(file))
            os.remove(file)
            
        for file in glob.glob(tempPath + "/*.csv"):
            print("Removing file %s"%(file))
            os.remove(file)
            
        for file in glob.glob(tempPath + "/*.raw"):
            print("Removing file %s"%(file))
            os.remove(file)
        
    def prepareConfigCOLFile(self,data_dir,updatedFrequencyList):
        COLPath = data_dir + '/COL'
        CONFIGPath = self.getConfigDir()
        ConfigCOLPath = CONFIGPath + '/COL'
        
        col = 0
        if(len(updatedFrequencyList) == 0):
            if os.path.exists(COLPath):
                shutil.copyfile(COLPath,ConfigCOLPath)
        else: #frequency list was updated, use these values
            with open(ConfigCOLPath,'w') as concolFile:
                print("len(self.updatedFrequencyList) = %d" %(len(updatedFrequencyList)))
                while col < len(updatedFrequencyList):
                    concolFile.write("%d: %s\n" %(col+1,updatedFrequencyList[col]))
                    col = col+1
    def generateMapImage(self,tiffPath="",csvPath="",outDir="",outName="temp.png",mapWidth=200,mapHeight=400):
        if(outDir == ""):
            outDir = self.tempDirPath
        if(csvPath != ""):
            lastIndex = csvPath.rindex('/')
            outName = csvPath[lastIndex+1:].replace(".csv",".png")
        elif(tiffPath):
            lastIndex = tiffPath.rindex('/')
            outName = tiffPath[lastIndex+1:].replace(".tif",".png")
    
        outImage = outDir+"/"+outName.replace(".png","_OVERLAY.png")
        boundingBox = generateMapImage(tiffPath=tiffPath,csvPath=csvPath,outImage=outImage,mapWidth=mapWidth,mapHeight=mapHeight)
        return [boundingBox,outImage]
    
    def generateShapeFiles(self=None,file="",outdir="",outname=""):
        create_shapefile(file=file,outdir=outdir,outname=outname)
                    
                    
                    
                    
#---------BEGIN SOURCE DIR / FILE GENERATION---------   
    def generateProgramPath(self):
        programPath = os.path.dirname(os.path.realpath(__file__))
        programPath = programPath.replace("\\","/")
        self.programPath = programPath
        print("Program dir is %s"%(programPath))
    def getProgramPath(self):
        return self.programPath
        
    def generateTempDir(self):
        #This is a temp dir that will hold generated images
        tempDir = self.programPath + '/guiTempData'
        if(not os.path.isdir(tempDir)):
            os.mkdir(tempDir)
        self.tempDirPath = tempDir
        print ("Tempdir is %s"%(tempDir))
    def getTempDir(self):
        return self.tempDirPath
        
    def generateConfigDir(self):  
        lastIndex = self.programPath.rindex('/')
        aboveDir = self.programPath[0:lastIndex]
        configDir = aboveDir+"/config"
        if(not os.path.isdir(configDir)):
            os.mkdir(configDir)
        self.configDir = configDir
        print ("configDir is %s"%(configDir))
        
    def getConfigDir(self):
        return self.configDir
    
    
    
    
app = Application()