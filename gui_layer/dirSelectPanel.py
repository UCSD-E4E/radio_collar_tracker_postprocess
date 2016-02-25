import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import re


from META_FILE_READER import META_FILE_READER
from getNumCols import *
import os
import fileinput
import shutil

class dirSelectPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    bgcolor = '#F0F0F0'
    buttonColor = '#CCCCCC'
    VERTICLE_PADDING = 3;
    doCalculations = 0
    dirText = 0; runTBText = 0; altTBText = 0; colTBText = 0
    dirTB = 0; runTB = 0; altTB = 0; colTB = 0
    updatedFrequencyList = []#["123", "444123123"]
    #to be used in tandem with getCollarFrequencies
    def __init__(self,parent,HEIGHT,calculationHandler):
        data_dir = tk.StringVar()
        tk.Frame.__init__(self,parent,width=250,height=HEIGHT)
        #self.grid_propagate('false')
        #self.pack_propagate('false')
        self.doCalculations = calculationHandler
        self.initializeWidgets()
        #TODO: decide where CONFIGCOLPath file is written to
        #Probably in toplevel

        self.config(bg=self.bgcolor)
        
    def initializeWidgets(self):
        self.dirText = tk.Text(self,height=1,width = 30,bd=0,bg=self.bgcolor)
        self.dirTB = tk.Entry(self,width = 30)
        self.setDirButton = tk.Button(self,text='...',command=self.initializeFields,width=3,bg=self.buttonColor)
        self.runText = tk.Text(self,height=2,width = 30,bd=0,bg=self.bgcolor)
        self.runTB = tk.Entry(self,width = 8)
        self.altText = tk.Text(self,height=2,width = 30,bd=0,bg=self.bgcolor)
        self.altTB = tk.Entry(self,width = 8)
        self.colText = tk.Text(self,height=2,width = 30,bd=0,bg=self.bgcolor)
        self.colTB = tk.Entry(self,width = 8)
        self.updateFreqButton = tk.Button(self,text='View Collar Frequencies',command=self.updateFrequencies,bg=self.buttonColor)
        
        self.calculateButton = tk.Button(self,text='Calculate',command=self.prepareForCalc,bg=self.buttonColor)
        
        
        
        #INSERT = self.dirText.INSERT
        self.dirText.insert('insert',"Please select a data directory")
        self.runText.insert('insert',"If this box is red, please insert the run number below")
        self.altText.insert('insert',"If this box is red, please insert the working altitude")
        self.colText.insert('insert',"If this box is red, please insert the number of collars below")
        
        #disables text boxes, text cannot be edited
        self.dirText.config(state='disabled',wrap='word')
        self.runText.config(state='disabled',wrap='word')
        self.altText.config(state='disabled',wrap='word')
        self.colText.config(state='disabled',wrap='word')
        
        #self.dirTB.config(state='disabled')
        #self.runTB.config(state='disabled')
        #self.altTB.config(state='disabled')
        #self.colTB.config(state='disabled')
        
        
        
        
        
        #curHeight = 0
        #self.dirText.grid()
        #curHeight = curHeight + self.dirText.winfo_height();
        #print(curHeight)
        #self.dirTB.grid()
        #self.runText.grid()
        #self.runTB.grid()
        #self.altText.grid()
        #self.altTB.grid()
        #self.colText.grid()
        #self.colTB.grid()
        
        self.dirText.pack()
        self.dirTB.pack()
        self.setDirButton.pack();
        self.runText.pack()
        self.runTB.pack()
        self.altText.pack()
        self.altTB.pack()
        self.colText.pack()
        self.colTB.pack()
        self.updateFreqButton.pack()
        self.calculateButton.pack()
        
        curHeight = 0
        self.dirText.place(y=curHeight)
        self.update()
        curHeight = curHeight + self.dirText.winfo_height();
        
        self.dirTB.place(y=curHeight)
        self.update()
        self.setDirButton.place(y=curHeight,x=self.dirTB.winfo_width() + 3)
        self.update()
        curHeight = curHeight + self.dirTB.winfo_height() + self.VERTICLE_PADDING;
        
        self.runText.place(y=curHeight)
        self.update()
        curHeight = curHeight + self.runText.winfo_height();
        
        self.runTB.place(y=curHeight)
        self.update()
        curHeight = curHeight + self.runText.winfo_height() + self.VERTICLE_PADDING;
        
        self.altText.place(y=curHeight)
        self.update()
        curHeight = curHeight + self.runText.winfo_height();
        
        self.altTB.place(y=curHeight)
        self.update()
        curHeight = curHeight + self.runText.winfo_height() + self.VERTICLE_PADDING;
        
        self.colText.place(y=curHeight)
        self.update()
        curHeight = curHeight + self.runText.winfo_height();
        
        self.colTB.place(y=curHeight)
        self.update()
        #delay updating curHeight so I can place the button
        self.updateFreqButton.place(y=curHeight,x=(self.runText.winfo_width() / 3 +2));
        self.update()
        
        curHeight = curHeight + self.runText.winfo_height() + self.VERTICLE_PADDING;
        
        self.calculateButton.place(y=curHeight,x=80)
        
        self.dirText.lift()
    

    def changeSize(self):
        self.width = 200;
        self.height = 300;
        
    def prepareForCalc(self):
        proceed = 1;
        dirTBPath = self.dirTB.get()
        print("dirTBPath is: %s" %(dirTBPath))
        if(os.path.isdir(dirTBPath) != 1):
            self.dirTB.config(bg='red');
            proceed=0
        else:
            self.dirTB.config(bg='white');
        
        inString = self.runTB.get() 
        runValue = 0        
        try:
            runValue = int(inString)
        except ValueError:
            runValue = 0

        if(runValue == 0):
            self.runTB.config(bg='red');
            proceed=0
        else:
            self.runTB.config(bg='white');
            
        inString = self.altTB.get()  
        altValue = 0     
        
        try:
            altValue = int(inString)
        except ValueError:
            altValue = 0
           

        if(altValue == 0):
            self.altTB.config(bg='red');
            proceed=0
        else:
            self.altTB.config(bg='white');
            
        inString = self.colTB.get()  
        colValue = 0        
        try:
            colValue = int(inString)
        except ValueError:
            colValue = 0
        if(colValue == 0):
            self.colTB.config(bg='red');
            proceed=0
        else:
            self.colTB.config(bg='white');
        

        
        

 
        if(proceed == 1):
            #prepares the config file for calculations
            self.prepareConfigCOLFile(dirTBPath)
            self.doCalculations(dirTBPath,runValue,altValue,colValue,self.updatedFrequencyList);

    def initializeFields(self):
        self.updatedFrequencyList = []
        root = tk.Tk()
        root.withdraw()
        root.grid()
        self.dirTB.config(state='normal')
        data_dir = filedialog.askdirectory()#'C:/Users/Work/Documents/Files/Projects/RadioCollar/SampleData/RCT_SAMPLE/RUN_002027-copy'
        self.dirTB.delete(0, 'end')
        self.dirTB.insert(0, data_dir)
        if(data_dir ==""):
            self.dirTB.config(state='normal')
        else:
            self.dirTB.config(state='disabled')
        
        #TODO: Move these out to their own .py files
        RUNPath = data_dir + '/RUN'
        ALTPath = data_dir + '/ALT'
        COLPath = data_dir + '/COL' 

        run = 0; alt = 0; col = 0;
        if os.path.exists(RUNPath):
            run = META_FILE_READER(RUNPath, 'run_num')
            
        if os.path.exists(ALTPath):
            alt =  META_FILE_READER(ALTPath, 'flt_alt')
            
        if os.path.exists(COLPath):
            col = GET_NUM_COLLARS(COLPath);

                       
        if run < 1:
            self.runTB.config(bg='red',state='normal')
            self.runTB.delete(0, 'end')
        else:
            self.runTB.config(state='normal')
            self.runTB.delete(0, 'end')
            self.runTB.insert(0,run)
            self.runTB.config(bg='white',state='disabled')
            
        if alt < 1:
            self.altTB.config(bg='red',state='normal')
            self.altTB.delete(0, 'end')
        else:
            self.altTB.config(state='normal')
            self.altTB.delete(0, 'end')
            self.altTB.insert(0,alt)
            #self.altTB.config(bg='white',state='disabled') Nathan said do not disable altitude
            
        if col < 1:
            self.colTB.config(bg='red',state='normal')
            self.colTB.delete(0, 'end')
        else:
            self.colTB.config(state='normal')
            self.colTB.delete(0, 'end')
            self.colTB.insert(0,col)
            self.colTB.config(bg='white',state='disabled')
            
            
    def updateFrequencies(self):
        num_col = 0
        self.updatedFrequencyList = []
        frequencyArray = getCollars()
        num_col = len(frequencyArray);
        i = 0
        while i < num_col:
            frequencyArray[i] = frequencyArray[i].translate(None,' \n')
            frequencyArray[i] =frequencyArray[i].split(':')[1]
            self.updatedFrequencyList.append(frequencyArray[i])
            print("updatedCollarFreq 1= %s" %(self.updatedFrequencyList[i]));
            i = i+1
            
        print(num_col)
            
        
        if num_col < 1:
            self.colTB.config(bg='red',state='normal')
            self.colTB.delete(0, 'end')
        else:
            self.colTB.config(state='normal')
            self.colTB.delete(0, 'end')
            self.colTB.insert(0,num_col)
            self.colTB.config(bg='white',state='disabled')
    def prepareConfigCOLFile(self,data_dir):
    
        COLPath = data_dir + '/COL'
        CONFIGPath = os.path.dirname(os.path.realpath(__file__))
        CONFIGPath = CONFIGPath.replace("\\","/")
        lastIndex = CONFIGPath.rindex('/')
        CONFIGPath = CONFIGPath[0:lastIndex]
        programPath = CONFIGPath
        CONFIGPath = CONFIGPath + '/config'
        ConfigCOLPath = CONFIGPath + '/COL'
        col = 0
        
        if(len(self.updatedFrequencyList) == 0):
            if os.path.exists(COLPath):
                shutil.copyfile(COLPath,ConfigCOLPath)
        else: #frequency list was updated, use these values
            with open(ConfigCOLPath,'w') as concolFile:
                print("len(self.updatedFrequencyList) = %d" %(len(self.updatedFrequencyList)))
                print(self.updatedFrequencyList[0])
                print(self.updatedFrequencyList[1])
                while col < len(self.updatedFrequencyList):
                    concolFile.write("%d: %s\n" %(col+1,self.updatedFrequencyList[col]))
                    col = col+1