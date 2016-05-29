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
	saveOptions = {}
	saveOptions['filetypes'] = [('SHP file', '.shp')]
	outputFile = tkFileDialog.asksaveasfilename(**saveOptions)
	outputDir = os.path.dirname(outputFile)
	outputName = os.path.basename(outputFile)
	create_shapefile(file = inputFile, outdir = outputDir, outname = outputName)
