#!/usr/bin/env python
import Tkinter as tk
import json
import os

class collarDB:
	def __init__(self):
		userHome = os.environ.data['HOME']
		self._freq_db_name = os.path.join(userHome, '.rct', 'rct_cas_col')
		if not os.path.isdir(os.path.join(userHome, '.rct')):
			os.mkdir(os.path.join(userHome, '.rct'))
		if os.path.isfile(self._freq_db_name):
			freqMapFile = open(self._freq_db_name, 'r')
			freqMapString = freqMapFile.readline()
			if freqMapString is None or freqMapString == '':
				freqMapString = '{}'
			freqMapFile.close()
		else:
			freqMapString = '{}'
		self.freqMap = json.loads(freqMapString)

	def __getitem__(self, key):
		if type(key) == str:
			return self.freqMap[key]
		else:
			return None

	def __setitem__(self, key, item):
		self.freqMap[key] = item

	def close(self):
		freqMapFile = open(self._freq_db_name, 'w+')
		freqMapString = json.dumps(self.freqMap)
		freqMapFile.write(freqMapString)
		freqMapFile.close()


class collarWindow(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.col_db = collarDB()
		self._selDict = {}
		self._freqDict = {}
		self._varDict = {}
		for i in self.col_db.freqMap:
			var = tk.IntVar()
			lbl = tk.Checkbutton(self, text='%s' % (i), variable=var)
			lbl.grid(row = i, column = 0)
			txt = tk.Entry(self)
			txt.grid(row = i, column = 1)
			txt.insert(0, self.col_db.freqMap[i])
			self._selDict[i] = lbl
			self._freqDict[i] = txt
			self._varDict[i] = var
		self._addLabel = tk.Label(self, text='Add')
		self._addRow = len(self.col_db.freqMap) + 1
		self._addLabel.grid(row = self._addRow, column = 0)
		self._addEntry = tk.Entry(self)
		self._addEntry.grid(row = self._addRow, column = 1)
		self._updateBtn = tk.Button(self, text="Update", command=self.updateCallback)
		self._updateBtn.grid(row = self._addRow + 1, column = 0)
		self._selectBtn = tk.Button(self, text="Select", command=self.selectCallback)
		self._selectBtn.grid(row = self._addRow + 1, column = 1)
		self.select = None
	
	def selectCallback(self):
		self.select = []
		for i in self.col_db.freqMap:
			if self._varDict[i].get() == 1:
				self.select.append(i)
		self.close()

	def updateCallback(self):
		if self._addEntry.get() != '':
			self.col_db.freqMap['%d' % self._addRow] = int(self._addEntry.get())
			var = tk.IntVar()
			chkbx = tk.Checkbutton(self, text='%d' % (self._addRow), variable = var)
			chkbx.grid(row = self._addRow, column = 0)
			self._selDict['%d' % self._addRow] = chkbx
			self._freqDict['%d' % self._addRow] = self._addEntry
			self._varDict['%d' % self._addRow] = var
			self._addLabel.grid(row=self._addRow + 1, column = 0)
			self._addEntry = tk.Entry(self)
			self._addEntry.grid(row = self._addRow + 1, column = 1)
			self._updateBtn.grid(row = self._addRow + 2)
			self._selectBtn.grid(row = self._addRow + 2)
			self._addRow = self._addRow + 1
		for i in self.col_db.freqMap:
			var = self._varDict[i]
			lbl = self._selDict[i]
			txt = self._freqDict[i]
			if txt.get() != self.col_db[i]:
				self.col_db[i] = txt.get()


	def close(self):
		self.col_db.close()
		self.destroy()

def getCollars():
	app = collarWindow()
	app.mainloop()
	retval = []
	for i in app.select:
		retval.append(int(app.col_db[str(i)]))
	return retval
