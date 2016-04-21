<<<<<<< HEAD
import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

from dirSelectPanel import dirSelectPanel
from imageDisplayPanel import imageDisplayPanel
from auxiliaryOptionsPanel import auxiliaryOptionsPanel
from thirdFrame import dirExportFiles

from scriptImplementation import scriptImplementation

from META_FILE_READER import META_FILE_READER
from getNumCols import GET_NUM_COLLARS
import os

class Application(tk.Frame):
    record=0;SDO=0;clean=0;
    firstFrame = 0;
    secondFrame = 0;
    thirdFrame = 0;
    randValue = 20
    HEIGHT = 300
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        #self.minsize(
        #self.grid_propagate('false')
        #self.pack_propagate('false')
        #self.place_propagate('false')
        self.grid()
        self.placeFrames()
        self.config(background="red")
        self.update()
        
        
    def beginCalculations(self,data_dir,run_num,flt_alt,num_col,frequencyList):
        print("run_num= %d,flt_alt= %d,num_col= %d" %(run_num,flt_alt,num_col))
        imageList = []
        
=======
#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import ttk

from osgeo import gdal,ogr
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from read_meta_file import read_meta_file
from getCollars import GET_NUM_COLLARS

from newImageDisplayPanel import imageDisplayPanel
from auxiliaryOptionsPanel import auxiliaryOptionsPanel
from dirExportPanel import dirExportPanel
from newDataEntryPanel import newDataEntryPanel

class Application(tk.Frame):
    record = 0
    SDO = 0
    clean = 0
    randValue = 20
    HEIGHT = 300
    def __init__(self, master = None):
        tk.Frame.__init__(self, master, bg = "#F0F0F0")
        self.grid(sticky="nsew")

        self.placeFrames()
        self.update()

    def beginCalculations(self, data_dir, run_num, flt_alt, num_col, frequencyList):
        print("run_num= %d, flt_alt= %d, num_col= %d" % (run_num,flt_alt,num_col))
        imageList = []

>>>>>>> origin/gui_oldFFT
        COLPath = data_dir + '/COL'
        CONFIGPath = os.path.dirname(os.path.realpath(__file__))
        CONFIGPath = CONFIGPath.replace("\\","/")
        lastIndex = CONFIGPath.rindex('/')
        CONFIGPath = CONFIGPath[0:lastIndex]
        programPath = CONFIGPath
        CONFIGPath = CONFIGPath + '/config'
        ConfigCOLPath = CONFIGPath + '/COL'
        col = 0
<<<<<<< HEAD
        
        scriptImplementation(programPath,data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList)
        i=1
        while i <= num_col:
            imageList.append("RUN_%06d_COL_%06d.png"%(run_num,i))
            i = i+1
        self.secondFrame.newImages(num_col,"%s/"%(data_dir),imageList);
        
        #TODO: Move script stuff here
        
    def placeFrames(self):
        panelX = 0;
        self.firstFrame = dirSelectPanel(self,self.HEIGHT,self.beginCalculations)
        self.firstFrame.pack()
        #self.firstFrame.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + self.firstFrame.winfo_width();
        
        separatorFrame1 = separatorFrame(self,self.HEIGHT);
        separatorFrame1.pack()
        #separatorFrame1.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + separatorFrame1.winfo_width();
        
        self.secondFrame =imageDisplayPanel(self,self.HEIGHT);
        self.secondFrame.pack()
        #self.secondFrame.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + self.secondFrame.winfo_width();
        
        separatorFrame2 = separatorFrame(self,self.HEIGHT);
        separatorFrame2.pack()
        #separatorFrame2.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + separatorFrame2.winfo_width();
        
        self.thirdFrame = dirExportFiles(self,self.HEIGHT)
        self.thirdFrame.pack()
        self.update()
        #self.thirdFrame.place(anchor='nw',x=panelX)
        panelX = panelX + self.thirdFrame.winfo_width()
        
        #for(int i = 0; i < fileNameList.length;i++):
        #    filecopy(data_dir + fileNameList[1],dataout_dir + fileNameList[1]);
        self.firstFrame.pack(side='left')
        separatorFrame1.pack(side='left')
        self.secondFrame.pack(side='left')
        separatorFrame2.pack(side='left')
        self.thirdFrame.pack(side='left')
        
        self.firstFrame.lift()
    
        
class separatorFrame(tk.Frame):
    def __init__(self,parent,HEIGHT):
        data_dir = tk.StringVar()
        tk.Frame.__init__(self,parent,width=3,height=HEIGHT,bg='black')

top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()
=======

        self.secondFrame.scriptImplementation(programPath,data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList)
        i=1
        imageListFullPath = []
        while i <= num_col:
            imageList.append("RUN_%06d_COL_%06d.png"%(run_num,i))
            imageListFullPath.append("%s/%s" %(data_dir,imageList[i-1]))
            i = i+1
        #self.secondFrame.newImages(num_col,"%s/"%(data_dir),imageList)

        #self.secondFrame.displayImage(data_dir,CONFIGPath,run_num,flt_alt,num_col,frequencyList)

        self.thirdFrame.updateList(imageListFullPath)

        #TODO: Move script stuff here

    def placeFrames(self):
        self.firstFrame = newDataEntryPanel(self, 200, '#F0F0F0', self.beginCalculations)
        separatorFrame1 = separatorFrame(self, self.HEIGHT);
        self.secondFrame = imageDisplayPanel(self, self.HEIGHT);
        separatorFrame2 = separatorFrame(self, self.HEIGHT);
        self.thirdFrame = dirExportPanel(self)
        
        self.rowconfigure(0,weight=1)
        #self.columnconfigure(0,weight=1)
        #self.columnconfigure(1,weight=0)
        self.columnconfigure(2,weight=1)
        #self.columnconfigure(3,weight=0)
        #self.columnconfigure(4,weight=0)
        
        top = self.winfo_toplevel()
        
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        #top.columnconfigure(1,weight=0)
        #top.columnconfigure(2,weight=0)
        #top.columnconfigure(3,weight=0)
        #top.columnconfigure(4,weight=0)

        self.firstFrame.grid(row=0,column=0,sticky="nsw")
        separatorFrame1.grid(row=0,column=1,sticky="ns")
        self.secondFrame.grid(row=0,column=2,sticky="nsew")
        separatorFrame2.grid(row=0,column=3,sticky="ns")
        self.thirdFrame.grid(row=0,column=4,sticky="nse")
        


        #self.firstFrame.lift()
    def quit(self=None):
        root.destroy()

    def quitter(self):
        quit()


class separatorFrame(tk.Frame):
    def __init__(self,parent,HEIGHT):
        data_dir = tk.StringVar()
        tk.Frame.__init__(self,parent,width=2,bg='black')

top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()
>>>>>>> origin/gui_oldFFT
