import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

from dirExportPanel import dirExportPanel

class Application(tk.Frame):
    randValue = 20
    # fileNameListParent is the list that stores all the file paths and names
    #fileNameListParent = ['/home/nan/gui/test2/1.txt','/home/nan/gui/test2/2.txt']

    def __init__(self,master=None):
        tk.Frame.__init__(self,master,width = 500,height=300)
        self.grid()
        self.placeFrames()
        self.config(background="red")
        
    def beginCalculations(self):
        print("Wow this actually worked%d" %(self.randValue))
        print("TODO: add functionality")
        
    def placeFrames(self):
        print("TODO: add functionality")
        firstFrame = dirExportPanel(self)
        
        
        #for(int i = 0; i < fileNameList.length;i++):
        #    filecopy(data_dir + fileNameList[1],dataout_dir + fileNameList[1]);

top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()