#This will be application level, and will have all non-gui functions
import sys
import os


import Tkinter as tk

from gui import GUI

from scriptImplementation import scriptImplementation
from gen_overlayed_image import generateMapImage
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

    def setupValues(self):
        self.GUI.setTempDataDir(self.getTempDir())
    
    def beginCalculations(self, data_dir, run_num, flt_alt, num_col, frequencyList):
        #print("run_num= %d, flt_alt= %d, num_col= %d" % (run_num,flt_alt,num_col))
        imageList = []
        csvList = []

        programPath = self.programPath
        CONFIGPath = self.configDir
        col = 0
        
        scriptImplementation(programPath,data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList)
        
        i=1
        imageListFullPath = []
        csvListFullPath = []
        while i <= num_col:
            fileName = "RUN_%06d_COL_%06d"%(run_num,i)
            imageList.append(fileName+".png")
            csvList.append(fileName+".csv")
            imageListFullPath.append("%s/%s" %(data_dir,imageList[i-1]))
            csvListFullPath.append("%s/%s" %(data_dir,csvList[i-1]))
            i = i+1
            
        self.GUI.updateImageDataSet(num_col,"%s/"%(data_dir),imageList,csvList)
        self.GUI.updateExportSources(imageListFullPath,csvListFullPath)
        
        
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
    
        outImage = outDir+"/"+outName
        boundingBox = generateMapImage(tiffPath=tiffPath,csvPath=csvPath,outImage=outImage,mapWidth=mapWidth,mapHeight=mapHeight)
        return [boundingBox,outImage]
                    
                    
                    
                    
                    
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