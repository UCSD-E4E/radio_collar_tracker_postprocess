#!/usr/bin/env python
import argparse
import os
import numpy as np
import math
import utm

def processRun(inputFile, outputFile, targetZone, targetEasting, targetNorthing, targetHemisphere, append):
	names = ['time', 'lat', 'lon', 'col', 'alt']
	data = np.genfromtxt(inputFile, delimiter=',', names=names)
	lat = [x / 1e7 for x in data['lat']]
	lon = [y / 1e7 for y in data['lon']]
	col = data['col']
	alt = data['alt']

	distances = np.zeros(len(col))

	if append:
		out_stream = open(outputFile, 'a')
	else:
		out_stream = open(outputFile, 'w')

	avgCol = np.average(col)
	avgAlt = np.average(alt)

	for i in range(len(data['lat'])):
		utm_coord = utm.from_latlon(lat[i], lon[i])
		lat[i] = utm_coord[0]
		lon[i] = utm_coord[1]
		zonenum = utm_coord[2]
		zone = utm_coord[3] < 'N'

		if col[i] < avgCol + 1.5:
			continue
		if np.abs(alt[i] - avgAlt) > 5:
			continue
		if col[i] < -43:
			continue

		if zonenum is targetZone and targetHemisphere is zone:
			distances[i] = math.sqrt(math.pow(lon[i] - targetNorthing, 2) + math.pow(lat[i] - targetEasting, 2))
		else:
			continue
		out_stream.write('%f,%f\n' % (col[i], distances[i]))
	out_stream.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog = "Model Generator", description = "Analyzes a run to generate the probability model for that run.")
	parser.add_argument('-i', '--input', type = str, help = "Input CSV file", metavar = "input_file", dest = "input", required = True)
	parser.add_argument('-o', '--output', type = str, help = 'Output filename', metavar = 'output_file', dest = 'output', required = True)
	parser.add_argument('-a', '--append', action = 'store_true', help = 'Append to existing output')
	parser.add_argument('utm_zone', type = int, help = 'UTM Zone')
	parser.add_argument('mgrs_grid', type = str, help = 'MGRS Grid')
	parser.add_argument('utm_easting', type = int, help = 'UTM Easting')
	parser.add_argument('utm_northing', type = int, help = 'UTM Northing')

	args = parser.parse_args()
	inputFile = args.input
	outputFile = args.output
	utm_zone = args.utm_zone
	targetHemisphere = args.mgrs_grid < 'N'
	utm_easting = args.utm_easting
	utm_northing = args.utm_northing
	append = args.append

	if not os.path.isfile(inputFile):
		print("Failed to find %s!" % (inputFile))
		exit(-1)
	filename, filext = os.path.splitext(inputFile)
	if not filext == '.csv':
		print("Invalid input file!  Must be a csv file!")
		exit(-1)

	processRun(inputFile, outputFile, utm_zone, utm_easting, utm_northing, targetHemisphere, append)
