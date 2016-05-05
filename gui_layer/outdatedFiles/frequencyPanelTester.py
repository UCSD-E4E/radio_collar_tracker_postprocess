import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

from frequencyPanel import frequencyPanel

class Application(tk.Frame):
    randValue = 20

    def __init__(self,master=None):
        tk.Frame.__init__(self,master,width = 500,height=300)
        self.pack()
        self.placeFrames()
        self.config(background="red")
        
    def beginCalculations(self):
        print("Wow this actually worked%d" %(self.randValue))
        print("TODO: add functionality")
        
    def placeFrames(self):
        print("TODO: add functionality")
        self.firstFrame = frequencyPanel(self)
             



top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()
top.firstFrame.printList()
