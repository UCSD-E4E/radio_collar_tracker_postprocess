#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

def getFltAlt():
	root = tk.Tk()
	root.withdraw()
	return tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Flight Altitude:")

if __name__ == "__main__":
	print(getFltAlt())
