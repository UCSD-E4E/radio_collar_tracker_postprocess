#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog

def getDir():
    #root = tk.Tk()
    #root.withdraw()
    file_path = tkFileDialog.askdirectory()
    print("filePath = %s" %(file_path))
    return file_path
