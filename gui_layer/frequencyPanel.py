import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

class frequencyPanel(tk.Frame):
    bgcolor=0
    frequencyList = []
    def __init__(self,parent,width,color):
        self.bgcolor=color
        tk.Frame.__init__(self,parent,width=width,bg=color)
        self.mainframe = tk.Frame(self)
        self.mainframe.pack()
        self.currframe = tk.Frame(self)
        self.currframe.pack()
        self.botframe = tk.Frame(self)
        self.botframe.pack(side='bottom')
        self.initializeWidgets()


    def initializeWidgets(self):
        self.freq = tk.Entry(self.currframe, bg='beige')
        self.add = tk.Button(self.currframe, text="ADD", command=self.addEntry)
        self.dele = tk.Button(self.currframe, text="DELETE", command=lambda:self.delEntry())
        self.freq.pack(side='left')
        self.add.pack(side='left')
        self.dele.pack(side='left')


    #TODO!!!!!!
    def setNewFreqs(self, newList):
        #self.frequencyList[:] = newList
        length = len(newList)

        print self.frequencyList
        print "\nIMHERE 5\n"

        if length > 0:
            self.freq.insert(0,newList[0])
            self.addEntry()
            curPanel = self.newEntry
            i = 1
            while i < length:
                curPanel.freq.insert(0,newList[i])
                curPanel.addEntry()
                curPanel = self.newEntry
                i = i+1



    def clearList(self):
        self.frequencyList[:] = []

    def getCollarFrequencies(self):
        print self.frequencyList
        print "\nIMHERE 4\n"

        return self.frequencyList[:]

    def updateList(self, newList):
        self.frequencyList[:] = newList

    def getList(self):
        return self.frequencyList[:]

    def printList(self):
        freqNum = len(self.frequencyList)
        print "The total number of frequencies entered is: " + str(freqNum)
        for i in range(freqNum):
            print "Frequency " + str(i) + ": " + self.frequencyList[i]

    def addElem(self,elem):
        self.frequencyList.append(elem)

    def delElem(self,elem):
        self.frequencyList.remove(elem)

    def addEntry(self):
        freqVal = self.freq.get()
        temp = 0
        try:
            temp = int(freqVal)
        except ValueError:
            temp = 0
        if (temp==0):
            self.freq.config(bg='red')
        else:
            self.addElem(freqVal)
            self.freq.config(state='disabled')
            self.add.config(state='disabled')
            # create a new frequency entry below by calling the sub panel class
            self.newEntry = frequencySubPanel(self.botframe, self.addElem, self.delElem, self.getList)

    def delEntry(self):
        freqVal = self.freq.get()
        temp = 0
        try:
            temp = int(freqVal)
        except ValueError:
            temp = 0
        if (temp==0):
            self.freq.config(bg='red')
        else:
            if (freqVal in self.getList()):
                self.delElem(freqVal)
                self.currframe.destroy()


# create a sub panel down below for creating a new frequency entry, the benifit of doing this is that this is a independent frame
class frequencySubPanel(tk.Frame):
    addfunc = 0
    delfunc = 0
    getlistfunc = 0

    def __init__(self,parent,addElemFunc,delElemFunc,getListFunc):
        self.addfunc = addElemFunc
        self.delfunc = delElemFunc
        self.getlistfunc = getListFunc

        tk.Frame.__init__(self,parent)

        self.mainframe = tk.Frame(parent)
        self.mainframe.pack()
        self.currframe = tk.Frame(parent)
        self.currframe.pack()
        self.botframe = tk.Frame(parent)
        self.botframe.pack(side='bottom')

        self.initializeWidgets()

    def initializeWidgets(self):
        self.freq = tk.Entry(self.currframe, bg='beige')
        self.add = tk.Button(self.currframe, text="ADD", command=self.addEntry)
        self.dele = tk.Button(self.currframe, text="DELETE", command=lambda:self.delEntry())
        self.freq.pack(side='left')
        self.add.pack(side='left')
        self.dele.pack(side='left')

    def addElem(self,elem):
        self.addfunc(elem)

    def delElem(self,elem):
        self.delfunc(elem)

    def getList(self):
        return self.getlistfunc()

    def addEntry(self):
        freqVal = self.freq.get()
        temp = 0
        try:
            temp = int(freqVal)
        except ValueError:
            temp = 0
        if (temp==0):
            self.freq.config(bg='red')
        else:
            self.addElem(freqVal)
            self.freq.config(state='disabled')
            self.add.config(state='disabled')
            self.newEntry = frequencySubPanel(self.botframe, self.addElem, self.delElem, self.getList)

    def delEntry(self):
        freqVal = self.freq.get()
        temp = 0
        try:
            temp = int(freqVal)
        except ValueError:
            temp = 0
        if (temp==0):
            self.freq.config(bg='red')
        else:
            if (freqVal in self.getList()):
                self.delElem(freqVal)
                self.currframe.destroy()
