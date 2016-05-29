#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog

def getFileName():
	root = tk.Tk()
	root.withdraw()
	root.update()
	file_path = tkFileDialog.askdirectory(parent=root)
	return file_path

if __name__ == "__main__":
	file_path = getFileName()
	if file_path == "":
		print "None"
		exit
	else:
		print(file_path)
		exit
