#!/usr/bin/env python

import os
import argparse
from dateutil.parser import parse
from datetime import datetime

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Generates the daily CSV report for RTT runs')
	parser.add_argument('-i', '--input_directory', required = True, help = 'Directory containing all the day\'s runs and results')
	parser.add_argument('-d', '--date', required = False, help = 'Date of runs')
	args = parser.parse_args()

	directory = args.input_directory
	if args.date is None:
		date = datetime.today()
	else:
		date = parse(args.date)
	datestr = date.strftime('%d-%m-%Y')
	reportname = date.strftime('%Y.%m.%d')
	csv = open('%s.csv' % reportname, 'w+')

	csv.write('date,lat,lon,channel,time\n')
	for dirpath, dnames, fnames in os.walk(directory):
		for f in fnames:
			if f == 'Notes':
				rpt = open(os.path.join(dirpath, f), 'r')
				print(rpt)
				while True:
					iguanaline = rpt.readline()
					if iguanaline == '' or iguanaline is None:
						break
					iguana_num = int(iguanaline.split()[1])
					print(iguana_num)
					coordline = rpt.readline()
					try:
						lon = float(coordline.strip().split(',')[0].strip())
						lat = float(coordline.strip().split(',')[1].strip())
					except ValueError, e:
						timeline = rpt.readline()
						continue
					errline = rpt.readline()
					timeline = rpt.readline()
					time = timeline.strip().split(' ')[0]
					csv.write('%s,%.6f,%.6f,%d,%s\n' % (datestr,lat,lon,iguana_num,time))
				rpt.close()
			elif f.endswith('.rpt'):
				rpt = open(os.path.join(dirpath, f), 'r')
				print(rpt)
				iguanaline = rpt.readline()
				iguana_num = int(iguanaline.split()[1])
				print(iguana_num)
				coordline = rpt.readline()
				try:
					lon = float(coordline.strip().split(',')[0].strip())
					lat = float(coordline.strip().split(',')[1].strip())
				except ValueError, e:
					continue
				errline = rpt.readline()
				timeline = rpt.readline()
				time = timeline.strip().split(' ')[0]
				runtype = rpt.readline()
				rpt.close()
				csv.write('%s,%.6f,%.6f,%d,%s\n' % (datestr,lat,lon,iguana_num,time))
	csv.close()