#!/usr/bin/env python
import Tkinter as tk
import json
import os
import read_meta_file
import argparse
import fileinput

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
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_directory', dest = 'run_dir')
	args = parser.parse_args()

	run_dir = args.run_dir
	oldColFilename = os.path.join(run_dir, 'COL')
	newColFilename = os.path.join(run_dir, 'COLJ')
	col_db = collarDB()
	if os.path.isfile(oldColFilename) and not os.path.isfile(newColFilename):
		freqs = []
		for line in fileinput.input(oldColFilename):
			freqs.append(int(line.strip().split(':')[1].strip()))
		fileinput.close()
		col_s = []
		freq_list = col_db.freqMap.values()
		for freq in freqs:
			if unicode(freq) not in freq_list:
				print("Error: frequency not in collar database - please remove manually!")
				return
			else:
				col_s.append(col_db.freqMap.keys()[freq_list.index(unicode(freq))])
		newCol = open(newColFilename, 'w+')
		newCol.write(json.dumps(col_s))
		newCol.write('\n')
		newCol.close()

if __name__ == '__main__':
	main()