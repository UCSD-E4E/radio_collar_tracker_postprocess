#!/usr/bin/env python

import shapefile
from osgeo import gdal
import osr

import utm
import numpy as np
import os
import time
import getMappedCollars
import json
import argparse

def fromPixel(gt, x, y):
	# Outputs UTM
	# Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
	# Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)	x_geo = gt[0] + x * gt[1] + y * gt[2]
	x_geo = gt[0] + x * gt[1] + y * gt[2]
	y_geo = gt[3] + x * gt[4] + y * gt[5]
	return (x_geo, y_geo)

def toPixel(gt, x, y):
	# Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
	# Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)	gt_arr = np.array([[gt[1], gt[2]], [gt[4], gt[5]]])
	gt_inv = np.linalg.pinv(gt_arr)
	gcoord = np.array([[x],[y]])
	gorig = np.array([[gt[0]],[gt[1]]])
	pcoord = gt_inv * (gcoord - gorig)
	return(int(pcoord[0]), int(pcoord[1]))

def getDistance(c1, c2):
	return np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

def getEstimation(est_shapefile):
	shpfile = shapefile.Reader(est_shapefile)
	lonlat = shpfile.records()[0]
	utm_coord = utm.from_latlon(float(lonlat[1]), float(lonlat[0]))
	return utm_coord

def getError(est_shapefile, tiff):
	utm_coord = getEstimation(est_shapefile)
	easting = utm_coord[0]
	northing = utm_coord[1]
	estimated_location = (easting, northing)
	gtif = gdal.Open(tiff)
	gtf = gtif.GetGeoTransform()
	band = gtif.GetRasterBand(1)
	dataset = band.ReadAsArray()
	err_dist = 0
	for row in xrange(len(dataset)):
		for col in xrange(len(dataset[row])):
			if dataset[row, col] > 0.05:
				geo_coord = fromPixel(gtf, col, row)
				distance = getDistance(geo_coord, estimated_location)
				if err_dist < distance:
					err_dist = distance
	return err_dist

def generateReport(run_dir, run_num):
	gps_filename = os.path.join(run_dir, 'GPS_%06d' % (run_num))
	col_filename = os.path.join(run_dir, 'COLJ')
	note_filename = os.path.join(run_dir, 'Notes')

	gps_file = open(gps_filename, 'r')
	line = gps_file.readline()
	utc_epoch = float(line.split(',')[3].strip())
	localtime = time.localtime(utc_epoch)
	timestr = time.strftime('%H:%M %Z', localtime)
	col_db = getMappedCollars.collarDB()
	col_file = open(col_filename, 'r')
	col_line = col_file.readline()
	col_arr = json.loads(col_line)
	note_file = open(note_filename, 'w+')
	col_num = 1
	for i in col_arr:
		note_file.write('Iguana %d\n' % (int(i)))

		est_shapefile = os.path.join(run_dir, 'RUN_%06d_COL_%06d_est.shp' % (run_num, col_num))
		if os.path.isfile(est_shapefile):
			est_loc = getEstimation(est_shapefile)
			latlon = utm.to_latlon(est_loc[0], est_loc[1], est_loc[2], zone_letter = est_loc[3])
			note_file.write('\t%f, %f\n' % (latlon[1], latlon[0]))

			tiff = os.path.join(run_dir, 'RUN_%06d_COL_%06d_heatmap.tiff' % (run_num, col_num))
			if os.path.isfile(tiff):
				err_dist = getError(est_shapefile, tiff)
				note_file.write('\t+/- %d m\n' % err_dist)
			else:
				note_file.write('\tError not calculable - check manually!\n')
				print('Collar %d: Error not calculable - check manually!' % col_num)
		else:
			note_file.write('\tIguana not detected!\n')
		note_file.write('\t%s\n' % timestr)
		col_num = col_num + 1

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_dir')
	parser.add_argument('-r', '--run_num')
	arg = parser.parse_args()
	generateReport(arg.input_dir, int(arg.run_num))