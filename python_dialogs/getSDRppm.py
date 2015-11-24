#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog
import sys

root = tk.Tk()
root.withdraw()
retval = tkSimpleDialog.askinteger("RCT Installer", "SDR PPM Error:")
if retval is None:
	sys.exit(1)
print(retval)
sys.exit(0)
