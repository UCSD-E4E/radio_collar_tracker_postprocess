#!/usr/bin/env python

import sys
import os

import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import ttk

class GUI(tk.Toplevel):
	def __init__(self, parent=None):
		tk.Toplevel.__init__(self, parent, bg = '#F0F0F0', bd = 1, relief = 'sunken')
		self.mainFrame = mainFrame(self)
		self.mainFrame.grid(row = 0, column = 0, sticky = "nswe")

		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1)

		self.setupMenu()
	def setupMenu(self):
		

class mainFrame(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master, bg = "#F0F0F0")
		programDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp")

def quit(self):
	root.destroy()
	sys.exit()

if __name__ == '__main__':
	tempDir = ""
	root = tk.Tk()
	# root.withdraw()
	GUI = GUI(root)
	GUI.protocol("WM_DELETE_WINDOW", quit)
	root.bind('<Control-q>', quit)
	GUI.title("Radio Collar Tracker")

	root.mainloop()