#!/usr/bin/env python

import shapefile
import utm
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('offset')
args = parser.parse_args()
filenum = int(args.file)
fileoffset = float(args.offset)

shp = shapefile.Reader('RUN_000059_COL_000001_est.shp')
geolocation = shp.records()[0]

utm_coords = utm.from_latlon(geolocation[1], geolocation[0])

meta_file = open('META_000059', 'r')
start_time = float(meta_file.readline().split(':')[1].strip())
file_size = 67108864
file_seconds = file_size / 4.0 / 2000000.0
time = file_seconds * filenum + fileoffset + start_time
meta_file.close()
gps_file = open('GPS_000059', 'r')
line = gps_file.readline()
def getLocalTime(line):
	return float(line.split(',')[0].strip())
while True:
	line = gps_file.readline()
	gps_time = getLocalTime(line)
	if gps_time >= time:
		break
def getGPSCoord(line):
	lat = float(line.split(',')[1].strip()) / 1e7
	lon = float(line.split(',')[2].strip()) / 1e7
	return (lat, lon)

myCoord = getGPSCoord(line)
myUTM = utm.from_latlon(myCoord[0], myCoord[1])
distance = math.sqrt((utm_coords[0] - myUTM[0]) ** 2 + (utm_coords[1] - myUTM[1]) ** 2)
print(distance)