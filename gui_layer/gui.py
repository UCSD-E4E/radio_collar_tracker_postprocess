#!/usr/local/bin/python


#running on python 3.5.1

import os.path

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from shutil import copyfile

import fileinput
import argparse

class Application(tk.Frame):


    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        
        self.SDOBool = tk.IntVar()
        self.recordBool = tk.IntVar()
        self.cleanBool = tk.IntVar() 

        self.createConfigButtons()
        self.createActionButtons()
        
    def beginCalculations(self):
        run = 0
        flt_alt = 0
    
    
    
        signal_dist_outpt = self.SDOBool.get()
        record = self.recordBool.get()
        clean_run = self.cleanBool.get()
        print('Do the maths here')
        print('signal_dist_outpt= ')
        print(signal_dist_outpt)
        print('record= ')
        print(record)
        print('clean_run=')
        print(clean_run)
        
        data_dir = self.runFileChooser()
        print("data_dir = ")
        print(data_dir)
        if data_dir == "":
            print("Directory not found, quitting calculations")
            return 1
        
        RUNPath = data_dir + '/RUN'
        ALTPath = data_dir + '/ALT'
        COLPath = data_dir + '/COL'
        
        
        if clean_run == 1:
            self.cleanRunProtocol(data_dir)
            return 0
            
        if os.path.exists(RUNPath):
            run = self.META_FILE_READER(RUNPATH, 'run_num')
        else:
            run = self.RUN_NUM_CHOOSER()
        
        if run == "":
            print("run not found, quitting calculations")
            return 1
            
        if os.path.exists(ALTPath):
            flt_alt =  self.META_FILE_READER(ALTPath, 'flt_alt')
        else:
            flt_alt = self.getFLTALT()
            if flt_alt == "":
                print("alt not found, quitting calculations")
                return 1;
                
        
        if record == 1:
            with open(ALTPath,'a') as altFile:
                altFile.write("flt_alt: "+str(flt_alt))
            print("flt alt:")
            print(flt_alt)
            
            
        ConfigCOLPath = 'CONFIG_DIR/COL' 
        if os.path.exists(COLPath):
            copyfile(COLPath,ConfigCOLPath)
        #else:
          #TODO  ${COLLAR_CHOOSER} > ${CONFIG_DIR}/COL
          #  col_res=$?
         # if ! [[ $col_res == 0 ]]
          #  exit 1
          #  fi
          
        #if record == 1:
            #TODO cp ${CONFIG_DIR}/COL ${data_dir}/COL

        #TODO: continue adapting code from line 93
        
    def createConfigButtons(self):
        self.sdoBox = tk.Checkbutton(self,text='signal_dist_output',variable=self.SDOBool)
        self.record = tk.Checkbutton(self,text='record',variable=self.recordBool)
        self.cleanRun = tk.Checkbutton(self,text='clean_run',variable=self.cleanBool)
        
        self.sdoBox.grid()
        self.record.grid()
        self.cleanRun.grid()
        
    def createActionButtons(self):
        self.doStuffButton = tk.Button(self,text='doMath',command=self.beginCalculations)
        
        self.doStuffButton.grid()
        
    
            
            
    def runFileChooser(self):
        root = tk.Tk()
        root.withdraw()
        root.grid()
        return filedialog.askdirectory()
         
    def cleanRunProtocol(self, data_dir):
        runPath = data_dir + "/RUN"
        altPath = data_dir + "/ALT"
        colPath = data_dir + "/COL"
        
        print(runPath)
        print(altPath)
        print(colPath)
        
        if os.path.exists(runPath):
            os.remove(runPath)
            print("removed RUN file")
            
        if os.path.exists(altPath):
            os.remove(altPath)
            print("removed ALT file")
            
        if os.path.exists(colPath):
            os.remove(colPath)
            print("removed COL file")
        
        
        
    def META_FILE_READER(self, path, tagVal):
        for line in fileinput.input(path):
            if tagVal == line.strip().split(':')[0].strip():
                return line.strip().split(':')[1].strip()
                
    def RUN_NUM_CHOOSER(self):
        root = tk.Tk()
        root.withdraw()
        simpledialog.askinteger("RCT Post-Processing Pipeline", "Run Number:")
    
    def getFLTALT(self):
        root = tk.Tk()
        root.withdraw()
        return simpledialog.askinteger("RCT Post-Processing Pipeline", "Flight Altitude:")
        
        
           
        
top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()