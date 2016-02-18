import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

from dirSelectPanel import dirSelectPanel
from imageDisplayPanel import imageDisplayPanel
from auxiliaryOptionsPanel import auxiliaryOptionsPanel

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
        tk.Frame.__init__(self,master,width=750,height=self.HEIGHT)
        #self.grid_propagate('false')
        #self.pack_propagate('false')
        #self.place_propagate('false')
        self.grid()
        self.placeFrames()
        self.config(background="red")
        
        
    def beginCalculations(self,data_dir,run_num,flt_alt,num_col):
        print("run_num= %d,flt_alt= %d,num_col= %d" %(run_num,flt_alt,num_col))
        imageList = []
        i=0
        while i < num_col:
            imageList.append("RUN_%06d_COL_%06d.gif"%(run_num,i+1))
            i = i+1
        self.secondFrame.newImages(num_col,"%s/"%(data_dir),imageList);
        
        #TODO: Move script stuff here
        
    def placeFrames(self):
        panelX = 0;
        self.firstFrame = dirSelectPanel(self,self.HEIGHT,self.beginCalculations)
        self.firstFrame.pack()
        self.firstFrame.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + self.firstFrame.winfo_width();
        
        separatorFrame1 = separatorFrame(self,self.HEIGHT);
        separatorFrame1.pack()
        separatorFrame1.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + separatorFrame1.winfo_width();
        
        self.secondFrame =imageDisplayPanel(self,self.HEIGHT);
        self.secondFrame.pack()
        self.secondFrame.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + self.secondFrame.winfo_width();
        
        separatorFrame2 = separatorFrame(self,self.HEIGHT);
        separatorFrame2.pack()
        separatorFrame2.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + separatorFrame2.winfo_width();
        
        self.thirdFrame = auxiliaryOptionsPanel(self,self.HEIGHT)
        self.thirdFrame.pack()
        self.thirdFrame.place(anchor='nw',x=panelX)
        self.update()
        panelX = panelX + self.thirdFrame.winfo_width()
        
        #for(int i = 0; i < fileNameList.length;i++):
        #    filecopy(data_dir + fileNameList[1],dataout_dir + fileNameList[1]);

        
class separatorFrame(tk.Frame):
    def __init__(self,parent,HEIGHT):
        data_dir = tk.StringVar()
        tk.Frame.__init__(self,parent,width=3,height=HEIGHT,bg='black')

top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()