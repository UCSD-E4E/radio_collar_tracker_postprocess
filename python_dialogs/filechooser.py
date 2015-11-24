#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog

root = tk.Tk()
root.withdraw()
file_path = tkFileDialog.askdirectory()
if file_path == "":
	print "None"
	exit
else:
	print(file_path)
