import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))
from read_meta_file import read_meta_file
from getCollars import *
from simpleDialogs import getDir

import fileinput
import shutil

#from newFrequencyPanel import frequencyPanel


class dataEntryPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    buttonColor = "#CCCCCC"
    doCalculations = 0

    updatedFrequencyList = []
    #to be used in tandem with getCollarFrequencies
    def __init__(self, parent, width, color):
        self.bgcolor = color
        self.parent = parent
        data_dir = tk.StringVar()
        tk.Frame.__init__(self, parent, bg = self.bgcolor)
        self.width = width

        #pack frames in order
        self.curframe = tk.Frame(self)
        self.curframe.grid(row=0,column=0)

        self.initializeWidgets()
        #TODO: decide where CONFIGCOLPath file is written to
        #Probably in toplevel

        #self.config(bg=self.bgcolor)

        self.update()

    def initializeWidgets(self):
        self.dirFrame = directoryPanel(self.curframe, self.width, self.bgcolor, self.initializeFields)
        self.runFrame = runIDPanel(self.curframe, self.width, self.bgcolor)
        self.altFrame = altitudePanel(self.curframe, self.width, self.bgcolor)
        self.colFrame = frequencyPanel(self.curframe, self.width, self.bgcolor)
        self.calculateButton = tk.Button(self.curframe, text = 'Calculate', command = self.prepareForCalc, bg = self.buttonColor)


        self.dirFrame.grid(row=0,column=0,sticky="nw")
        self.runFrame.grid(row=1,column=0,sticky="nw")
        self.altFrame.grid(row=2,column=0,sticky="nw")
        self.colFrame.grid(row=3,column=0,sticky="nw")
        self.calculateButton.grid(row=4,column=0,sticky="w")


    def prepareForCalc(self):
        proceed = 1;
        dirTBPath = self.dirFrame.getDirectory()
        print("dirTBPath is: %s" %(dirTBPath))
        if(os.path.isdir(dirTBPath) != 1):
            proceed=0

        inString = self.runFrame.getRunID()
        runValue = 0
        try:
            runValue = int(inString)
        except ValueError:
            runValue = 0

        if(runValue == 0):
            proceed=0

        inString = self.altFrame.getAlt()
        altValue = 0

        try:
            altValue = int(inString)
        except ValueError:
            altValue = 0


        if(altValue == 0):
            proceed=0

        frequencyList = self.colFrame.getCollarFrequencies()

        self.updatedFrequencyList = frequencyList

        i = 0
        while i < len(frequencyList ):
            print(frequencyList[i])
            i = i+1

        colValue = 0
        try:
            colValue = len(frequencyList)
        except ValueError:
            colValue = 0

        if(colValue == 0):
            proceed=0

        if(proceed == 1):
            #prepares the config file for calculations
            self.prepareConfigCOLFile(dirTBPath,self.updatedFrequencyList)
            if(self.doCalculations != 0):
                self.doCalculations(dirTBPath,runValue,altValue,colValue,frequencyList);

    def initializeFields(self):
        #This function is called by the directoryPanel when a new directory is set
        self.updatedFrequencyList = []

        data_dir = self.dirFrame.getDirectory()

        #TODO: Move these out to their own .py files
        RUNPath = data_dir + '/RUN'
        ALTPath = data_dir + '/ALT'
        COLPath = data_dir + '/COL'

        run = 0; alt = 0; col = 0;
        if os.path.exists(RUNPath):
            run = read_meta_file(RUNPath, 'run_num')

        if os.path.exists(ALTPath):
            alt =  read_meta_file(ALTPath, 'flt_alt')

        if os.path.exists(COLPath):
            self.updatedFrequencyList = getOldCollarsClean(COLPath);


        self.runFrame.setRunID(run)
        self.altFrame.setAlt(alt)
        self.colFrame.setCollarFrequencies(self.updatedFrequencyList)

    def reset(self):
        self.dirFrame.updateDirectory("")
        self.colFrame.clearFrequencies()

    def attachPrepareConfigCol(self,func):
        self.prepareConfigCOLFile = func
    def attachCalculationHandler(self,func):
        self.doCalculations = func

#------------------------------------------------------------------------------      
#                       Directory Panel
#------------------------------------------------------------------------------

class directoryPanel(tk.Frame):
    buttonColor = '#CCCCCC'
    data_dir = ""
    def __init__(self, parent, width, color, updateDirectoryFunction):
        self.bgcolor = color
        self.parent = parent;
        tk.Frame.__init__(self, parent, width = width, bg = color)
        self.updateDirFunc = updateDirectoryFunction
        self.initializeWidgets()

    def initializeWidgets(self):
        self.dirText = tk.Label(self, text = "Data Directory/Folder", bg = self.bgcolor)
        self.dirTB = tk.Entry(self, width = 29)
        self.selectDirButton = tk.Button(self, text = '...', command = self.updateDirectory, width = 3, bg = directoryPanel.buttonColor)

        self.dirText.grid(row=0,column=0,sticky="w")
        self.dirTB.grid(row=0,column=1,sticky="w")
        self.selectDirButton.grid(row=0,column=2,sticky="w")

    def updateDirectory(self,data_dir=""):
        #self.dirTB.config(state='normal')
        if(data_dir == ""):
            data_dir = getDir() #'C:/Users/Work/Documents/Files/Projects/RadioCollar/SampleData/RCT_SAMPLE/RUN_002027-copy'\
        #self.parent.parent.quitter()
        if(data_dir==""):
            return
        self.data_dir = data_dir
        self.dirTB.delete(0, 'end')
        self.dirTB.insert(0, self.data_dir)
        #Decided not to disable dirTB

        self.updateDirFunc()

    def getDirectory(self=None):
        return self.data_dir

        
#------------------------------------------------------------------------------      
#                       Run Panel
#------------------------------------------------------------------------------
class runIDPanel(tk.Frame):
    bgcolor = 0
    runID = 0
    runIDText = 0
    runIDTB = 0
    #errorText = 0
    def __init__(self,parent,width,color):
        self.bgcolor = color
        tk.Frame.__init__(self,parent,width=width,bg=color)
        self.initializeWidgets()

    def initializeWidgets(self):
        self.runID = tk.StringVar()
        self.runID.trace("w", lambda name, index, mode, runID = self.runID.get() : self.changeRunID())

        self.runIDText = tk.Label(self, text = "Run ID: ", width = 12, bg = self.bgcolor)
        self.runIDTB = tk.Entry(self,width = 23, textvariable = self.runID)

        #self.errorText = tk.Text(self,height=1,width = 23,bd=0,bg=self.bgcolor)
        #self.errorText.insert('insert','Please input an integer')
        #self.errorText.config(bg=self.bgcolor)
        #self.errorText.config(foreground=self.bgcolor)

        self.runIDText.grid(row=0,column=0,sticky="w")
        self.runIDTB.grid(row=0,column=1,sticky="w")
        #self.errorText.pack(side='left',padx=3)

    def setRunID(self,newID='-1'):
        #Changing this should call changeRunID automatically
        self.runID.set(newID)


    def changeRunID(self=None):
        run = -1
        try:
            run = int(self.runID.get())
        except ValueError:
            run = -1
        print('run = %d' %(run))
        if run < 0:
            #self.errorText.config(foreground='red')
            self.runIDTB.config(bg='red')
            #self.runID.set('-1')

        else:
            #self.runID.set(newID)
            self.runIDTB.config(bg='white')
            #self.errorText.config(foreground=self.bgcolor)


    def getRunID(self=None):
        return self.runID.get()

#------------------------------------------------------------------------------      
#                       Altitude Panel
#------------------------------------------------------------------------------  
        
class altitudePanel(tk.Frame):
    bgcolor = 0
    alt = 0
    altText = 0
    altTB = 0
    #errorText = 0
    def __init__(self,parent,width,color):
        self.bgcolor = color
        tk.Frame.__init__(self,parent,width=width,bg=color)
        self.initializeWidgets()

    def initializeWidgets(self):
        self.alt = tk.StringVar()
        self.alt.trace("w", lambda name, index, mode, alt=self.alt.get(): self.changeAlt())

        self.altText = tk.Label(self,text="Run altitude: ",width=12,bg=self.bgcolor)
        self.altTB = tk.Entry(self,width = 23,textvariable=self.alt)

        #self.errorText = tk.Text(self,height=1,width = 23,bd=0,bg=self.bgcolor)
        #self.errorText.insert('insert','Please input an integer')
        #self.errorText.config(bg=self.bgcolor)
        #self.errorText.config(foreground=self.bgcolor)

        self.altText.grid(row=0,column=0,sticky="w")
        self.altTB.grid(row=0,column=1,sticky="w")
        #self.errorText.pack(side='left',padx=3)

    def setAlt(self,newalt='-1'):
        #Changing this should call changeRunID automatically
        self.alt.set(str(newalt))


    def changeAlt(self=None):
        alt = -1
        try:
            alt = int(self.alt.get())
        except ValueError:
            alt = -1

        if alt < 0:
            #self.errorText.config(foreground='red')
            self.altTB.config(bg='red')
            #self.alt.set ('-1')

        else:
            #self.alt.set(newID)
            self.altTB.config(bg='white')
            #self.errorText.config(foreground=self.bgcolor)

    def getAlt(self=None):
        return self.alt.get()
        
        
        
#------------------------------------------------------------------------------      
#                       Frequency Panel
#------------------------------------------------------------------------------   

class frequencyPanel(tk.Frame):
    def __init__(self,parent,width,color="#F0F0F0"):
        self.freqPanelList = []
        tk.Frame.__init__(self,parent,width=width, bg=color)
        self.initWidgets()
        
    def getCollarFrequencies(self):
        outList = []
        for panel in self.freqPanelList:
            entry = panel.getValue()
            try:
                val = int(entry)
                outList.append(val)#TODO: May be append entry, see if needs list of strings or ints
            except ValueError:
                print("%s is not an integer, not adding to frequency list"%(entry))
                
        return outList
        
    def setCollarFrequencies(self,newList):
        print(newList)
        self.clearFrequencies()
        
        #This does not do checking for if integer or not
        for s in newList:
            print("Adding [%s] to frequency list" %(s))
            self.createEntry(s)
            
        self.updateNumEntries()
            
    def clearFrequencies(self):
        i = len(self.freqPanelList)-1
        while i >= 0:
            self.deleteEntry(i)
            i=i-1
            
    def createEntry(self,newValue=""):
        newPanel = frequencySubPanel(self,self.updateNumEntries,newValue)
        self.freqPanelList.append(newPanel)
        newPanel.grid()
        
    def deleteEntry(self,ID):
        self.freqPanelList[ID].deleteSelf()
        #del self.frequencyList[ID]
            
    def updateNumEntries(self):
        count = 0
        for panel in self.freqPanelList:
            if panel.getValue() != "":
                count = count+1
                
        self.numColsTV.set(str(count))
    def initWidgets(self):
        self.numColsTV = tk.StringVar()
        self.numColsText = tk.Text(self,width=19,height=1,bg="#F0F0F0",bd=0)
        self.numColsTB = tk.Entry(self,state="disable",textvariable=self.numColsTV)
        self.numColsTB.config(disabledforeground="black",disabledbackground="white",width=3)
        self.addColFreqButton = tk.Button(self,text="Add Frequency",command=self.createEntry)
        #self.numSubPanels = 
        
        self.numColsText.grid(row=0,column=0,sticky="w")
        self.numColsTB.grid(row=0,column=1)
        self.addColFreqButton.grid(row=0,column=2)
        
        
        self.numColsText.insert("insert","Number of collars: ")
        self.numColsText.config(state="disabled")
            
class frequencySubPanel(tk.Frame):

    def __init__(self,parent,UF,value="",color="#F0F0F0"):
        tk.Frame.__init__(self,parent,bg=color)
        self.updateNumCount = UF
        
        
        
        self.initWidgets()
        self.freqValTV.set(value)
        
    def initWidgets(self):
        self.freqValTV = tk.StringVar()
        self.freqValTV.trace("w", lambda name, index, mode, freqValTV=self.freqValTV.get(): self.changeFreq())
        
        self.freqTB = tk.Entry(self,textvariable=self.freqValTV,width=10)
        
        self.delButton = tk.Button(self,command=self.deleteSelf,text="Delete")
        
        self.freqTB.grid(row=0,column=0)
        self.delButton.grid(row=0,column=1)
        
    def deleteSelf(self,event=None):
        #These two lines ensure number of collars is updated correctly
        self.freqValTV.set("")
        self.updateNumCount()
        
        self.destroy()
    def changeFreq(self):
        
        string = self.freqValTV.get()
        self.updateNumCount()
        try:
            val = int(string)
            self.freqTB.config(bg="white")
            
        except ValueError:
            if(string != ""):
                self.freqTB.config(bg="red")
    def getValue(self):
        string = self.freqValTV.get()
        try:
            val=int(string)
            return string
        except ValueError:
            return ""