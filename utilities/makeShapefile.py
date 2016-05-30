#!/usr/bin/env python
import Tkinter as tk
import tkFileDialog
import os
import csvToShp

if __name__ == '__main__':
	root = tk.Tk()
	root.withdraw()
	options = {}
	options['filetypes'] = [('CSV', '.csv')]
	inputFile = tkFileDialog.askopenfilename(**options)
	if inputFile == '':
		exit()
	saveOptions = {}
	saveOptions['filetypes'] = [('SHP file', '.shp')]
	outputFile = tkFileDialog.asksaveasfilename(**saveOptions)
	if outputFile == '':
		exit()
	csvToShp.create_shapefile(inputFile, outputFile)
