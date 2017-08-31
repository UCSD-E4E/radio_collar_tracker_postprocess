#!/usr/bin/env python

import getMappedCollars
import os
import glob
import argparse
import json

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("run_dir")
	args = parser.parse_args()
	data_dir = args.run_dir

	collars = []
	
	runFile = open(os.path.join(data_dir, 'RUN'), 'r')
	run = int(runFile.readline().split(':')[1].strip())

	col_db = getMappedCollars.collarDB()

	coljFile = open(os.path.join(data_dir, 'COLJ'), 'r')
	freq_arr = json.loads(coljFile.readline())

	for ch in freq_arr:
		collars.append(int(col_db[unicode(ch)]))
	numCollars = len(collars)

	for i in xrange(numCollars):
		print("Looking for collar %d" % (i + 1))
		files = glob.glob('RUN_%06d_COL_%06d*' % (run, i + 1))
		ch = int(freq_arr[i])
		print('CH %d is %d' % (ch, i + 1))
		new_prefix = 'RUN_%06d_CH_%06d' % (run, ch)
		for file in files:
			print("Rename %s to %s" % (file, new_prefix + file[21:]))
			os.rename(file, new_prefix + file[21:])
