#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

def getRunNum():
	root = tk.Tk()
	root.withdraw()
	return tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Run Number:")

if __name__ == "__main__":
	print(getRunNum())
