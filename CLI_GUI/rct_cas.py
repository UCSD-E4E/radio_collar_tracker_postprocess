#!/usr/bin/env python
import argparse
import fileChooser
import os
import read_meta_file
import getRunNum
import shutil
import platform
import getMappedCollars
# import getCollars
import get_beat_frequency
import subprocess
import raw_gps_analysis
import display_data
import pos_estimator
import fileinput
import getFltAlt
import itertools
import csvToShp
import median_filter
import analyzeError
import glob

from multiprocessing import Pool

def processRaw(data_dir, run, alt, collarDefinitionFilename, i):
	raw_gps_analysis.process(data_dir, data_dir, run, i + 1, alt)
	data_file = '%s/RUN_%06d_COL_%06d.csv' % (data_dir, run, i + 1)
	csvToShp.create_shapefile(data_file, '%s/RUN_%06d_COL_%06d.shp' % (data_dir, run, i + 1))
	start_location = median_filter.generateGraph(run, i + 1, data_file, data_dir, collarDefinitionFilename)
	res_x = pos_estimator.generateGraph(run, i + 1, data_file, data_dir, collarDefinitionFilename, start_location)
	if res_x is None:
		return
	if res_x[6]:
		display_data.generateGraph(run, i + 1, data_file, data_dir, res_x[0], res_x[1], res_x[4], res_x[5], start_location)
	# else:
		# display_data.generateGraph(run, i + 1, data_file, data_dir, collarDefinitionFilename)

def processRawPool(args):
	processRaw(args[0], args[1], args[2], args[3], args[4])

if __name__ == '__main__':
	# Constants
	config_dir = ""
	fft_detect = ""
	if platform.system() == "Windows":
		config_dir = os.path.join("C:", os.sep, "Users", "e4e", ".rct", "")
		fft_detect = os.path.join("C:", os.sep, "Users", "e4e", "fft_detect", "fft_detect.exe")
	elif platform.system() == "Linux" or platform.system() == 'Darwin':
		config_dir = os.path.join(os.sep, "usr", "local", "etc", "rct", "")
		fft_detect = os.path.join(os.sep, "usr", "local", "bin", "fft_detect")

	parser = argparse.ArgumentParser(description='Processes Radio Collar Tracker Data')

	parser.add_argument('-s', '--signal-distance', action = 'store_true', default = False, help = 'Enables distance to signal plots', dest = 'signal_dist')
	parser.add_argument('-r', '--record', action = 'store_true', default = False, help = 'Records the current run configuration', dest = 'record')
	parser.add_argument('-c', '--clear', action = 'store_true', default = False, help = 'Clears the existing run configuration', dest = 'clear_run')
	parser.add_argument('-i', '--input', help = 'Input Directory', metavar = 'data_dir', dest = 'data_dir', default = None)
	parser.add_argument('-nf', '--no_fft', action = 'store_const', const = False, default = True, dest = 'fft_flag', help = 'This flag disables running the fft')
	parser.add_argument('-raw', '--leave_raws', action = 'store_const', const = False, default = True, dest = 'raw_flag', help = 'This flag leaves the concatenated raw files')
	parser.add_argument('-C', '--collar', action = 'append', type = int, help = 'Specific collar to run', default = None, dest = 'collars')

	args = parser.parse_args()
	signal_dist_output = args.signal_dist
	record = args.record
	clean_run = args.clear_run
	data_dir = ""
	fft_flag = args.fft_flag
	raw_flag = args.raw_flag
	collarList = args.collars
	if args.data_dir is None:
		data_dir = fileChooser.getFileName()
		if data_dir == "":
			exit()
	else:
		data_dir = args.data_dir

	runFileName = os.path.join(data_dir, 'RUN')
	altFileName = os.path.join(data_dir, 'ALT')
	colFileName = os.path.join(data_dir, 'COL')
	collarDefinitionFilename = os.path.join(data_dir, 'COLdef')

	# clear run if needed
	if clean_run is True:
		try:
			os.remove(runFileName)
		except Exception, e:
			pass
		try:
			os.remove(altFileName)
		except Exception, e:
			pass
		try:
			os.remove(colFileName)
		except Exception, e:
			pass
	for curFile in os.listdir(data_dir):
		if any(curFile.lower().endswith(ext) for ext in ['.csv', '.png', '.tif', '.tiff', '.shp', '.shx', '.prj', '.dbf', '.xml']):
			if os.path.splitext(curFile.lower())[0].endswith('_sel'):
				continue
			try:
				os.remove(os.path.join(data_dir, curFile))
			except Exception, e:
				pass
		if fft_flag and any(curFile.lower().endswith(ext) for ext in ['.raw']):
			try:
				os.remove(os.path.join(data_dir, curFile))
			except Exception, e:
				pass

	# Get collar definition
	run_retval = getMappedCollars.getCollars(data_dir)
	if run_retval is None:
		exit()
	run = run_retval['run']
	col_db = getMappedCollars.collarDB()
	collars = []
	for ch in run_retval['tx']:
		collars.append(int(col_db[ch]))
	COLdef = open(collarDefinitionFilename, 'w+')
	for i in xrange(len(collars)):
		COLdef.write("%d: %d\n" % (i + 1, collars[i]))
	COLdef.close()

	alt = run_retval['alt']

	fileList = os.listdir(data_dir)
	# Count the number of raw data files
	num_raw_files = 0
	for file in fileList:
		if "RAW_DATA_" in file:
			num_raw_files += 1
	# count the number of collars
	numCollars = len(collars)
	# Generate collar file prefix
	collar_file_prefix = "%s/RUN_%06d_" % (data_dir, run)
	# Find meta file and get data
	meta_file_name = "%s/META_%06d" % (data_dir, run)
	sdr_center_freq = int(read_meta_file.read_meta_file(meta_file_name, "center_freq"))
	sdr_ppm = 0

	# Generate fixed frequencies
	beat_frequencies = [get_beat_frequency.getBeatFreq(sdr_center_freq, freq, sdr_ppm) for freq in collars]

	# Generate raw files
	if fft_flag:
		args = ""
		args += " -i %s " % (data_dir)
		args += " -o %s " % (data_dir)
		args += " -r %d " % (run)
		args += " -- "
		for freq in beat_frequencies:
			args += " %s " % (freq)
		subprocess.call(fft_detect + args, shell=True)

	if collarList is None:
		if len(collars) == 1:
			processRaw(data_dir, run, alt, collarDefinitionFilename, 0)
		else:
			pool = Pool()
			iterArgs = zip(itertools.repeat(data_dir), itertools.repeat(run), itertools.repeat(alt), itertools.repeat(collarDefinitionFilename), xrange(len(collars)))
			pool.map(processRawPool, iterArgs)
	else:
		for i in xrange(len(collarList)):
			processRaw(data_dir, run, alt, collarDefinitionFilename, i - 1)
	os.remove(collarDefinitionFilename)

	# Clean up raw files
	if raw_flag and fft_flag:
		print("Cleaning raws")
		for i in range(1, numCollars + 1):
			os.remove("%s/RUN_%06d_%06d.raw" % (data_dir, run, i))
	
	# Generate report
	analyzeError.generateReport(data_dir, run)

	# Rename files
	for i in xrange(numCollars):
		files = glob.glob('RUN_%06d_COL_%06d*' % (run, i + 1))
		ch = int(run_retval['tx'][i])
		print('CH %d is %d' % (ch, i + 1))
		new_prefix = 'RUN_%06d_CH_%06d' % (run, ch)
		for file in files:
			print("Rename %s to %s" % (file, new_prefix + file[21:]))
			os.rename(file, new_prefix + file[21:])


