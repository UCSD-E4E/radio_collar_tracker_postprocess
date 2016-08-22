#!/usr/bin/env python
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
import os
import argparse
import fileinput
from osgeo import gdal
import osr
import math
from scipy.optimize import leastsq
import shapefile


def normalProbability(d, mean, stdDev):
    a = 1 / (math.sqrt(2 * stdDev * stdDev * math.pi))
    b = -1 * (d - mean) * (d - mean)
    b = b / (2 * stdDev * stdDev)
    return a * math.pow(math.e, b)

def read_meta_file(filename, tag):
    retval = None
    for line in fileinput.input(filename):
        if tag == line.strip().split(':')[0].strip():
            retval = line.strip().split(':')[1].strip()
            break
    fileinput.close()
    return retval

def residuals(v, col, x, y):
    residual = np.zeros(len(col))
    for i in xrange(len(col)):
        if col[i] < -43:
            continue
        residual[i] = 10 ** (((v[0] * col[i] + v[1]) / 10.0)) - math.sqrt((x[i] - v[2]) ** 2 + (y[i] - v[3]) ** 2)
    return residual


def generateGraph(run_num, num_col, filename, output_path, col_def):
    kml_output = False
    # TODO Fix test case
    plot_height = 6
    plot_width = 8
    plot_dpi = 72


    # Get collar frequency
    col_freq = float(read_meta_file(col_def, str(num_col))) / 1.e6

    # make list of columns
    # Expects the csv to have the following columns: time, lat, lon, [collars]
    names = ['time', 'lat', 'lon', 'col', 'alt']

    # Read CSV
    data = np.genfromtxt(filename, delimiter=',', names=names)
    # Modify values
    lat = [x / 1e7 for x in data['lat']]
    lon = [y / 1e7 for y in data['lon']]
    col = data['col']
    alt = data['alt']

    # convert deg to utm
    zone = "X"
    zonenum = 60
    avgCol = np.average(col)
    stdDevCol = np.std(col)
    maxCol = np.amax(col)
    avgAlt = np.average(alt)
    stdAlt = np.std(alt)
    finalCol = []
    finalNorthing = []
    finalEasting = []
    for i in range(len(data['lat'])):
        # if col[i] < avgCol + stdDevCol:
        if col[i] < (avgCol + maxCol) / 2:
            continue
        if math.fabs(alt[i] - avgAlt) > stdAlt:
            continue
        finalCol.append(col[i])
        utm_coord = utm.from_latlon(lat[i], lon[i])
        finalEasting.append(utm_coord[0])
        finalNorthing.append(utm_coord[1])
        zonenum = utm_coord[2]
        zone = utm_coord[3]


    if len(finalCol) < 4:
        print("Collar %d: No collars detected!" % num_col)
        print("Collar %d: Only %d detections!" % (num_col, len(finalCol)))
        print("Collar %d: Average Collar Measurement: %d" % (num_col, avgCol))
        return

    writer = shapefile.Writer(shapefile.POINT)
    writer.autoBalance = 1
    writer.field("lat", "F", 20, 18)
    writer.field("lon", "F", 20, 18)
    writer.field("measurement", "F", 18, 18)

    for i in xrange(len(finalCol)):
        #Latitude, longitude, elevation, measurement
        lat, lon = utm.to_latlon(finalEasting[i], finalNorthing[i], zonenum, zone)
        writer.point(lon, lat, finalCol[i])
        writer.record(lon, lat, finalCol[i])


    writer.save('%s/RUN_%06d_%06d_pos.shp' % (output_path, run_num, num_col))
    proj = open('%s/RUN_%06d_%06d_pos.prj' % (output_path, run_num, num_col), "w")
    epsg1 = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
    proj.write(epsg1)
    proj.close()

    # Data Analysis
    print("Collar %d: running estimation..." % num_col)
    x0 = [-0.715, -14.51, finalEasting[0], finalNorthing[0]]
    res_x, res_cov_x, res_infodict, res_msg, res_ier = leastsq(residuals, x0, args=(finalCol, finalEasting, finalNorthing), full_output=1)
    easting = res_x[2]
    northing = res_x[3]
    # print("easting: %f" % easting)
    # print("northing: %f" % northing)
    lat_lon = utm.to_latlon(easting, northing, zonenum, zone_letter=zone)

    print("Collar %d: ier %d; %s" % (num_col, res_ier, res_msg))

    if res_ier == 4:
        print("Collar %d: No collar detected - falloff not found!" % (num_col))
        res_x = np.append(res_x, [0, 0, False])
        return res_x

    print("Collar %d: Saving estimation..." % num_col)
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field("lat", "F", 20, 18)
    w.field("lon", "F", 20, 18)
    w.point(lat_lon[1], lat_lon[0]) #x, y (lon, lat)
    w.record(lat_lon[1], lat_lon[0]) #x, y (lon, lat)
    w.save('%s/RUN_%06d_%06d.shp' % (output_path, run_num, num_col))

    prj = open('%s/RUN_%06d_%06d.prj' % (output_path, run_num, num_col), "w")
    epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
    prj.write(epsg)
    prj.close()

    if res_cov_x is None:
        print("Collar %d: Collar position indeterminate! %s" % (num_col, res_msg))
        res_x = np.append(res_x, [0, 0, True])
        return res_x
    s_sq = (residuals(res_x, finalCol, finalEasting, finalNorthing) ** 2).sum() / (len(finalCol) - len(x0))
    pcov = res_cov_x * s_sq


    # Sigma estimation
    alpha = res_x[0]
    beta = res_x[1]
    errors = []
    for i in xrange(len(finalCol)):
        rangeToEstimate = math.sqrt((finalEasting[i] - easting) ** 2.0 + (finalNorthing[i] - northing) ** 2.0)
        modelRange = 10 ** ((alpha * finalCol[i] + beta) / 10.0)
        errors.append(rangeToEstimate - modelRange)
    errorSigma = np.std(errors)
    errorMean = np.average(errors)
    res_x = np.append(res_x, [errorMean, errorSigma, True])
    return res_x

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processes RUN_XXXXXX.csv files '
            'from the Radio Collar Tracker software to generate maps of radio collar '
            'signal strength')

    parser.add_argument('-r', '--run', type = int, help = 'Run number for this data file', metavar = 'run_num', dest = 'run_num', default = 1075)
    parser.add_argument('-n', '--collar', type = int, help = 'Collar number for this data file', metavar = 'collar', dest = 'collar', default = 1)
    parser.add_argument('-i', '--input', help = 'Input file to be processed', metavar = 'data_file', dest = 'filename', required = True)
    parser.add_argument('-o', '--output_dir', help = 'Output directory', metavar = 'output_dir', dest = 'output_path', required = True)
    parser.add_argument('-c', '--definitions', help = "Collar Definitions", metavar = 'collar_definitions', dest = 'col_def', required = True)

    # Get configuration
    args = parser.parse_args()
    run_num = args.run_num
    num_col = args.collar
    filename = args.filename
    output_path = args.output_path
    col_def = args.col_def
    res_x = generateGraph(run_num, num_col, filename, output_path, col_def)
    print("alpha: %f" % res_x[0])
    print("beta: %f" % res_x[1])
    print("easting: %f" % res_x[2])
    print("northing: %f" % res_x[3])
    print("mean: %f" % res_x[4])
    print("sigma: %f" % res_x[5])
    print("success: %f" % res_x[6])
