#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

def getGMTDialog():
    root = tk.Tk()
    root.withdraw()
    return tkSimpleDialog.askinteger("Radio Collar GUI", "GMT (-12,12):")
