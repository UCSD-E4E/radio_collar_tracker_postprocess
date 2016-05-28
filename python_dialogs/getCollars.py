#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

root = tk.Tk()
root.withdraw()
counter = 1
hasOutput = False
while True:
	frequency = tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
	if frequency is not None:
		print("%d: %d" % (counter, frequency - 1000))
		counter += 1
		print("%d: %d" % (counter, frequency - 500))
		counter += 1
		print("%d: %d" % (counter, frequency))
		counter += 1
		print("%d: %d" % (counter, frequency + 500))
		counter += 1
		print("%d: %d" % (counter, frequency + 1000))
		counter += 1
		hasOutput = True
	else:
		if not hasOutput:
			exit(1)
		else:
			exit()
