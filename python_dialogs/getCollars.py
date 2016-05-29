#!/usr/bin/env python
import Tkinter as tk
import tkSimpleDialog

def getCollars():
	root = tk.Tk()
	root.withdraw()
	retval = []
	hasOutput = False
	while True:
		frequency = tkSimpleDialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
		if frequency is not None:
			retval.append(frequency)
			hasOutput = True
		else:
			return retval

if __name__ == '__main__':
	collars = getCollars()
	for i in xrange(len(collars)):
		print("%d: %d" % (i + 1, collars[i]))
