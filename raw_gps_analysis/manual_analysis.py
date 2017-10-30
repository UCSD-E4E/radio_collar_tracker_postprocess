#!/usr/bin/env python

import shapefile
import utm
import math
import argparse
import os

def getLocalTime(line):
	return float(line.split(',')[0].strip())

def getGPSTime(line):
	return float(line.split(',')[3].strip())

def getGPSCoord(line):
	lat = float(line.split(',')[1].strip()) / 1e7
	lon = float(line.split(',')[2].strip()) / 1e7
	return (lat, lon)

def getGPS(run_dir, run_num, time):
	gps_file = open('%s/GPS_%06d' % (run_dir, run_num), 'r')
	line = None
	while True:
		line = gps_file.readline()
		print(line)
		gps_time = getLocalTime(line)
		if gps_time >= time:
			break
	gps_file.close()
	return line

def fileOffsetToTime(run_dir, run_num, file_num, file_offset):
	meta_file = open('%s/META_%06d' % (run_dir, run_num), 'r')
	start_time = float(meta_file.readline().split(':')[1].strip())
	file_size = 67108864
	file_seconds = file_size / 4.0 / 2000000.0
	meta_file.close()
	return file_seconds * (file_num - 1) + file_offset + start_time

parser = argparse.ArgumentParser()
parser.add_argument('run_dir')
parser.add_argument('run_num')
parser.add_argument('chn_num')
args = parser.parse_args()

run_num = int(args.run_num)
run_dir = str(args.run_dir)
col_num = int(args.chn_num)

csv_file = open(os.path.join(run_dir, 'RUN_%06d_CH_%06d.csv' % (run_num, col_num)), 'w+')

while True:
	try:
		file = int(raw_input('File No: '))
		offset = float(raw_input('Offset: '))
		amplitude = float(raw_input('Amplitude: '))
	except ValueError, e:
		continue
	time = fileOffsetToTime(run_dir, run_num, file, offset)
	line = getGPS(run_dir, run_num, time)
	coords = getGPSCoord(line)
	localTime = getLocalTime(line)
	csv_file.write('%f,%d,%d,%f,%f\n' % (localTime, coords[0] * 1e7, coords[1] * 1e7, amplitude, 0))
	csv_file.flush()
	state = str(raw_input('Continue: '))
	if state == '':
		continue
	else:
		break