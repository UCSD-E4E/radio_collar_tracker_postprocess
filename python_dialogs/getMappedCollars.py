#!/usr/bin/env python
import Tkinter as tk
import json
import os
import read_meta_file

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
		if type(key) == str or type(key) == unicode:
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
	def __init__(self, run_num, altitude, cols):
		tk.Tk.__init__(self)
		self.col_db = collarDB()
		self._selDict = {}
		self._freqDict = {}
		self._varDict = {}
		self._runVar = tk.IntVar()
		self._altVar = tk.IntVar()

		run_lbl = tk.Label(self, text="Run")
		run_lbl.grid(row = 0, column = 0)
		self._run_txt = tk.Entry(self)
		self._run_txt.grid(row = 0, column = 1)
		if run_num is not None:
			self._run_txt.insert(0, str(run_num))

		alt_lbl = tk.Label(self, text = "Alt")
		alt_lbl.grid(row = 1, column = 0)
		self._alt_txt = tk.Entry(self)
		self._alt_txt.grid(row = 1, column = 1)
		if altitude is not None:
			self._alt_txt.insert(0, str(altitude))

		for i in self.col_db.freqMap:
			var = tk.IntVar()
			lbl = tk.Checkbutton(self, text='%s' % (i), variable=var)
			if i in cols:
				var.set(1)
			lbl.grid(row = int(i) + 2, column = 0)
			txt = tk.Entry(self)
			txt.grid(row = int(i) + 2, column = 1)
			txt.insert(0, self.col_db.freqMap[i])
			self._selDict[i] = lbl
			self._freqDict[i] = txt
			self._varDict[i] = var
		self._addLabel = tk.Label(self, text='Add')
		self._addRow = len(self.col_db.freqMap) + 1
		self._addLabel.grid(row = self._addRow + 2, column = 0)
		self._addEntry = tk.Entry(self)
		self._addEntry.grid(row = self._addRow + 2, column = 1)
		self._updateBtn = tk.Button(self, text="Update", command=self.updateCallback)
		self._updateBtn.grid(row = self._addRow + 3, column = 0)
		self._selectBtn = tk.Button(self, text="Select", command=self.selectCallback)
		self._selectBtn.grid(row = self._addRow + 3, column = 1)
		self.select = None
	
	def selectCallback(self):
		if self._run_txt.get() == "":
			return
		if self._alt_txt.get() == "":
			return
		self.select = {}
		self.select['tx'] = []
		self.select['run'] = int(self._run_txt.get())
		self.select['alt'] = int(self._alt_txt.get())
		for i in self.col_db.freqMap:
			if self._varDict[i].get() == 1:
				self.select['tx'].append(i)
		self.close()

	def updateCallback(self):
		if self._addEntry.get() != '':
			self.col_db.freqMap['%d' % self._addRow] = int(self._addEntry.get())
			var = tk.IntVar()
			chkbx = tk.Checkbutton(self, text='%d' % (self._addRow), variable = var)
			chkbx.grid(row = self._addRow + 2, column = 0)
			self._selDict['%d' % self._addRow] = chkbx
			self._freqDict['%d' % self._addRow] = self._addEntry
			self._varDict['%d' % self._addRow] = var
			self._addLabel.grid(row=self._addRow + 3, column = 0)
			self._addEntry = tk.Entry(self)
			self._addEntry.grid(row = self._addRow + 3, column = 1)
			self._updateBtn.grid(row = self._addRow + 4)
			self._selectBtn.grid(row = self._addRow + 4)
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

def getCollars(run_dir):
	run_filename = os.path.join(run_dir, 'RUN')
	alt_filename = os.path.join(run_dir, 'ALT')
	col_filename = os.path.join(run_dir, 'COLJ')
	run_num = None
	alt = None
	col_s = set()
	if os.path.isfile(run_filename):
		runString = read_meta_file.read_meta_file(run_filename, 'run_num')
		if runString is not None:
			run_num = int(runString)
	if os.path.isfile(alt_filename):
		altString = read_meta_file.read_meta_file(alt_filename, 'flt_alt')
		if altString is not None:
			alt = int(altString)
	if os.path.isfile(col_filename):
		col_file = open(col_filename, 'r')
		col_line = col_file.readline()
		if col_line != "" and col_line is not None:
			col_a = json.loads(col_line)
			# col file should only contain channel indices as array
			for i in col_a:
				col_s.add(i)
		col_file.close()
	else:
		print('COLJ not found')
	app = collarWindow(run_num, alt, col_s)
	app.mainloop()
	if app.select is None:
		return None
	run_file = open(run_filename, 'w+')
	run_file.write('run_num: %d\n' % app.select['run'])
	run_file.close()
	alt_file = open(alt_filename, 'w+')
	alt_file.write('flt_alt: %d\n' % app.select['alt'])
	alt_file.close()
	col_file = open(col_filename, 'w+')
	col_str = json.dumps(app.select['tx'])
	col_file.write(col_str)
	col_file.write('\n')
	col_file.close()
	return app.select
