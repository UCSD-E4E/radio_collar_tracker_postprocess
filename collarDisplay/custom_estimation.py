#!/usr/bin/env python
# coding: utf-8
import sys
import numpy as np
import utm
import os
import fileinput
import math
from scipy.optimize import leastsq
import shapefile
import getMappedCollars
import display_data
import argparse
import glob
import ShpToCSV
import analyzeError

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input_dir', required = True)

args = parser.parse_args()
data_dir = args.input_dir

files = glob.glob('RUN_*_sel.shp')
cols = []
for file in files:
    cols.append(int(file.split('_')[3]))

runFile = open(os.path.join(data_dir, 'RUN'), 'r')
run_num = int(runFile.readline().split(':')[1].strip())
for num_col in cols:

    output_path = data_dir
    col_def = os.path.join(data_dir, 'COLdef')
    shpFilename = os.path.join(data_dir, 'RUN_%06d_CH_%06d_sel.shp' % (run_num, num_col))
    csvFilename = os.path.join(data_dir, 'RUN_%06d_CH_%06d_sel.csv' % (run_num, num_col))
    ShpToCSV.create_csv(shpFilename, csvFilename)
    startLocation = None
    
    # col_freq = int(collars[num_col - 1])

    names = ['time', 'lat', 'lon', 'col', 'alt']
    data = np.genfromtxt(csvFilename, delimiter=',', names=names)
    lat = [x / 1e7 for x in data['lat']]
    lon = [y / 1e7 for y in data['lon']]
    col = data['col']
    alt = data['alt']
    zone = ''
    zonenum = 0
    avgCol = np.average(col)
    stdDevCol = np.std(col)
    maxCol = np.amax(col)
    finalEasting = []
    finalCol = col
    finalNorthing = []
    for i in xrange(len(col)):
        utm_coord = utm.from_latlon(lat[i], lon[i])
        lon[i] = utm_coord[0]
        lat[i] = utm_coord[1]
        
    maxCol - (stdDevCol + avgCol)
    finalEasting = lon
    finalNorthing = lat
    x0 = [-0.715, -14.51, np.average(finalEasting[0]), np.average(finalNorthing[0])]
    def residuals(v, col, x, y, z):
        residual = np.zeros(len(col))
        for i in xrange(len(col)):
            if col[i] < -43:
                continue
            residual[i] = 10 ** (((v[0] * col[i] + v[1]) / 10.0)) - math.sqrt((x[i] - v[2]) ** 2 + (y[i] - v[3]) ** 2 + (z[i]) ** 2)
        return residual
    finalAlt = alt
    res_x, res_cov_x, res_infodict, res_msg, res_ier = leastsq(residuals, x0, args=(finalCol, finalEasting, finalNorthing, finalAlt), full_output=1)
    utm_coord = utm.from_latlon(data['lat'][0] / 1e7, data['lon'][0] / 1e7)
    zonenum = utm_coord[2]
    zone = utm_coord[3]
    easting = res_x[2]
    northing = res_x[3]
    lat_lon = utm.to_latlon(easting, northing, zonenum, zone_letter = zone)
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field('lat', 'f', 20, 18)
    w.field('lon', 'f', 20, 18)
    w.point(lat_lon[1], lat_lon[0])
    w.record(lat_lon[1], lat_lon[0])
    w.save('%s/RUN_%06d_CH_%06d_est.shp' % (output_path, run_num, num_col))
    proj = open('%s/RUN_%06d_CH_%06d_est.prj' % (output_path, run_num, num_col), 'w')
    epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
    proj.write(epsg)
    proj.close()
    alpha = res_x[0]
    beta = res_x[1]
    errors = []
    for i in xrange(len(finalCol)):
        rangeToEstimate = math.sqrt((finalEasting[i] - easting) ** 2.0 + (finalNorthing[i] - northing) ** 2.0 + finalAlt[i] ** 2.0)
        modelRange = 10 ** ((alpha * finalCol[i] + beta) / 10.0)
        errors.append(rangeToEstimate - modelRange)
    errorSigma = np.std(errors)
    errorMean = np.average(errors)
    res_x = np.append(res_x, [errorMean, errorSigma, True])



    display_data.generateGraph(run_num, num_col, csvFilename, data_dir, res_x[0], res_x[1], res_x[4], res_x[5], collarChannel = True)
analyzeError.generateReport(data_dir, run_num, True)