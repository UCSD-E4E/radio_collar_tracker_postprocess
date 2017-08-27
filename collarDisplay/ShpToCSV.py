#!/usr/bin/env python

import os
import shapefile
import argparse
import utm

def create_csv(shp, output):
	shp = shp.replace('\\', os.sep)
	shp = shp.replace('/', os.sep)
	output = output.replace('\\', os.sep)
	output = output.replace('/', os.sep)

	if not os.path.isfile(shp):
		print("File was not valid %s" % (shp))
		return
	if output == "":
		output = os.path.splitext(shp)[0]
		
	# Read SHP
	shpfile = shapefile.Reader(shp)
	names = shpfile.fields
	data = shpfile.records()

	# Convert data
	lat = []
	lon = []
	alt = []
	col = []
	time = []
	for i in xrange(len(data)):
		lat.append(int(float(data[i][1]) * 1e7))
		lon.append(int(float(data[i][0]) * 1e7))
		alt.append(float(data[i][2]))
		col.append(float(data[i][3]))
		time.append(i)
	
	csv_file = open(output, 'w+')
	for i in xrange(len(data)):
		csv_file.write("%d, %d, %d, %.6f, %f\n" % (time[i], lat[i], lon[i], col[i], alt[i]))
	csv_file.close()
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required = True)
	parser.add_argument('-o', '--output', required = False)
	arg = parser.parse_args()
	outfile = arg.output
	infile = arg.input
	if arg.output == None:
		outfile = os.path.splitext(infile)[0]
		outfile = '%s.csv' % outfile
	create_csv(infile, outfile)