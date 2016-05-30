#!/usr/bin/env python

import os
import shapefile
import numpy as np
import zipfile
import platform
from StringIO import StringIO
import argparse

def create_shapefile(csv, output):
	csv = csv.replace("\\", os.sep)
	csv = csv.replace("/", os.sep)
	output = output.replace("\\", os.sep)
	output = output.replace("/", os.sep)

	if not os.path.isfile(csv):
		print("File was not valid: %s" % (csv))
		return

	if output == "":
		print ("File was not valid: %s" % "")
		return

	if '.shp' in output or '.shx' in output or '.dbx' in output or '.prj' in output:
		output = os.path.splitext(output)[0]


	# Read CSV
	names = ['time', 'lat', 'lon', 'col']
	data = np.genfromtxt(csv, delimiter=',', names=names)
	# Modify values
	lat = [x / 1e7 for x in data['lat']]
	lon = [y / 1e7 for y in data['lon']]
	col = data['col']
	#print(col)


	w = shapefile.Writer(shapefile.POINT)
	w.autoBalance = 1
	w.field("lat", "F", 20, 18)
	w.field("lon", "F", 20, 18)
	w.field("alt", "F", 18, 18)
	w.field("measurement", "F", 18, 18)

	length = len(lat)
	i = 0
	while i < length:
		#Latitude, longitude, elevation, measurement
		w.point(lon[i], lat[i], 0, col[i])
		w.record(lon[i], lat[i], 0, col[i])
		i += 1

	#w.record('First','Point')

	w.save(output)
	prj = open('%s.prj' % output, "w")
	epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
	prj.write(epsg)
	prj.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input', action = "store", default = None, required = True, help = "Input CSV file")
	parser.add_argument('-o', '--output', action = 'store', default = '.', required = False, help = "Output Name")

	args = parser.parse_args()
	csvPath = os.path.realpath(args.input)
	output = os.path.realpath(args.output)
	create_shapefile(csvPath, output)
