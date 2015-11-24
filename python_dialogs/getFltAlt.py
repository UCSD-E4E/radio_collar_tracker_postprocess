#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

root = tk.Tk()
root.withdraw()
print(tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Flight Altitude:"))
