#!/usr/bin/env python

import getMappedCollars
import os
import glob
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("run_dir")
	args = parser.parse_args()
	data_dir = args.run_dir
	run_retval = getMappedCollars.getCollars(data_dir)
	if run_retval is None:
		exit()
	run = run_retval['run']
	col_db = getMappedCollars.collarDB()
	collars = []
	for ch in run_retval['tx']:
		collars.append(int(col_db[ch]))
	numCollars = len(collars)

	for i in xrange(numCollars):
		files = glob.glob('RUN_%06d_COL_%06d*' % (run, i + 1))
		ch = int(run_retval['tx'][i])
		print('CH %d is %d' % (ch, i + 1))
		new_prefix = 'RUN_%06d_CH_%06d' % (run, ch)
		for file in files:
			print("Rename %s to %s" % (file, new_prefix + file[21:]))
			os.rename(file, new_prefix + file[21:])
