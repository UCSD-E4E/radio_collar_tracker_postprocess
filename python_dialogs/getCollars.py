#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

def getCollars():
	root = tk.Tk()
	root.withdraw()
	root.update()
	retval = []
	hasOutput = False
	while True:
		frequency = tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
		root.update()
		if frequency is not None:
			retval.append(frequency - 1000)
			retval.append(frequency - 500)
			retval.append(frequency)
			retval.append(frequency + 500)
			retval.append(frequency + 1000)
			hasOutput = True
		else:
			return retval

if __name__ == '__main__':
	collars = getCollars()
	for i in xrange(len(collars)):
		print("%d: %d" % (i + 1, collars[i]))
