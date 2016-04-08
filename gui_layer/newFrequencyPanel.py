import Tkinter as tk
import shutil
import os.path


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
        print("In setCollarFrequencies")
        print(newList)
        self.clearFrequencies()
        
        #This does not do checking for if integer or not
        for s in newList:
            print("adding entry%s" %(s))
            self.createEntry(s)
            
        self.updateNumEntries()
            
    def clearFrequencies(self):
        i = len(self.freqPanelList)-1
        while i > 0:
            self.deleteEntry(i)
            i=i-1
            
    def createEntry(self,newValue=""):
        newPanel = frequencySubPanel(self,self.updateNumEntries,newValue)
        self.freqPanelList.append(newPanel)
        newPanel.grid()
        
    def deleteEntry(self,ID):
        self.freqPanelList[ID].deleteSelf()
        #del self.frequencyList[ID]
        
    def clearFrequencies(self):
        i = len(self.freqPanelList)-1
        while i > 0:
            self.deleteEntry(i)
            i=i-1
            
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