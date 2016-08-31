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
import shapefile
from read_meta_file import read_meta_file

def normalProbability(x, mean, stdDev):
    # stdDev = 100
    a = 1 / (math.sqrt(2 * (stdDev ** 2.0) * math.pi))
    b = -1 * (x - mean) ** 2.0
    b = b / (2 * (stdDev ** 2.0))
    retval = -4
    probability = a * math.pow(math.e, b)
    if x < mean:
        probability = a - (a - probability) / 2
    if probability > 0.0001:
        retval = math.log10(probability)
    return retval

def generateGraph(run_num, num_col, filename, output_path, col_def, alpha = -0.715, beta = -14.51, mean = 0.0306, sigma = 6, startLocation = None):
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
    finalRange = []
    finalAlt = []
    for i in xrange(len(col)):
        utm_coord = utm.from_latlon(lat[i], lon[i])
        lon[i] = utm_coord[0]
        lat[i] = utm_coord[1]
        zonenum = utm_coord[2]
        zone = utm_coord[3]

    # Generate histogram
    knownEmptyCollars = []
    medianCollars = []
    for i in xrange(len(col)):
        if startLocation is not None:
            rangeToMedian = math.sqrt((lon[i] - startLocation[0]) ** 2.0 + (lat[i] - startLocation[1]) ** 2.0)
            if rangeToMedian > startLocation[2] * 2:
                knownEmptyCollars.append(col[i])
            else:
                medianCollars.append(col[i])
    threshold = -43
    if len(medianCollars) > 0:
        threshold = np.amax(knownEmptyCollars)
    print("Collar %d: Using %f threshold" % (num_col, threshold))

    for i in range(len(data['lat'])):
        # if col[i] < avgCol + stdDevCol:
        if col[i] < threshold:
            continue
        if stdAlt < 5:
            if math.fabs(alt[i] - avgAlt) > stdAlt:
                continue
        else:
            if alt[i] < avgAlt - stdAlt:
                continue
        if startLocation is not None:
            rangeToMedian = math.sqrt((lon[i] - startLocation[0]) ** 2.0 + (lat[i] - startLocation[1]) ** 2.0)
            if rangeToMedian > startLocation[2] * 1.7:
                continue
        finalCol.append(col[i])
        finalEasting.append(lon[i])
        finalNorthing.append(lat[i])
        finalAlt.append(alt[i])
        finalRange.append(10 ** ((alpha * col[i] + beta) / 10.0))
    if len(finalCol) == 0:
        print("Collar %d: No heatmap matches!" % num_col)
        return

    # Calculate heatmap
    print("Collar %d: Building heatmap..." % num_col)
    margin = 50
    tiffXSize = int(max(finalEasting)) - int(min(finalEasting)) + margin * 2
    tiffYSize = int(max(finalNorthing)) - int(min(finalNorthing)) + margin * 2
    pixelSize = 1
    heatMapArea = np.zeros((tiffYSize, tiffXSize)) # [y, x]
    minY = min(finalNorthing) - margin
    refY = max(finalNorthing) + margin
    refX = min(finalEasting) - margin
    maxX = max(finalEasting) + margin
    # print("min northing: %f" % minY)
    # print("max northing: %f" % refY)
    # print("min easting: %f" % refX)
    # print("max easting: %f" % maxX)
    # Xgeo = refY + X
    # Ygeo = refX - Ypix

    # Plot data
    for x in xrange(tiffXSize):
        for y in xrange(tiffYSize):
            for i in xrange(len(finalCol)):
                posRange = math.sqrt((refX + x - finalEasting[i]) ** 2.0 + (refY - y - finalNorthing[i]) ** 2.0 + finalAlt[i] ** 2.0)
                heatMapArea[y][x] = heatMapArea[y][x] + normalProbability(posRange - finalRange[i], mean, 0.4 * finalRange[i])

    # Reshift up
    maxProbability = np.amax(heatMapArea)
    heatMapArea = heatMapArea - maxProbability
    heatMapArea = np.power(10, heatMapArea)

    # Save plot
    print("Collar %d: Saving heatmap..." % num_col)
    outputFileName = '%s/RUN_%06d_COL_%06d_heatmap.tiff' % (output_path, run_num, num_col)
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
        outputFileName,
        tiffXSize,
        tiffYSize,
        1,
        gdal.GDT_Float32, ['COMPRESS=LZW'])

    spatialReference = osr.SpatialReference()
    spatialReference.SetUTM(zonenum, zone >= 'N')
    spatialReference.SetWellKnownGeogCS('WGS84')
    wkt = spatialReference.ExportToWkt()
    retval = dataset.SetProjection(wkt)
    dataset.SetGeoTransform((
        refX,    # 3
        1,                      # 4
        0,
        refY,    # 0
        0,  # 1
        -1))                     # 2
    band = dataset.GetRasterBand(1)
    # band.SetNoDataValue(100)
    # print(tiffXSize)
    # print(tiffYSize)
    # print(np.amin(heatMapArea))
    # print(np.amax(heatMapArea))
    # print(np.mean(heatMapArea))
    # print(np.std(heatMapArea))
    # print((heatMapArea > -30).sum())
    band.WriteArray(heatMapArea)
    band.SetStatistics(np.amin(heatMapArea), np.amax(heatMapArea), np.mean(heatMapArea), np.std(heatMapArea))
    dataset.FlushCache()
    dataset = None

    # writer = shapefile.Writer(shapefile.POINT)
    # writer.autoBalance = 1
    # writer.field("lat", "F", 20, 18)
    # writer.field("lon", "F", 20, 18)
    # writer.field("measurement", "F", 18, 18)

    # for i in xrange(len(finalCol)):
    #     #Latitude, longitude, elevation, measurement
    #     lat, lon = utm.to_latlon(finalEasting[i], finalNorthing[i], zonenum, zone)
    #     writer.point(lon, lat, finalCol[i])
    #     writer.record(lon, lat, finalCol[i])


    # writer.save('%s/RUN_%06d_COL_%06d_hpos.shp' % (output_path, run_num, num_col))
    # proj = open('%s/RUN_%06d_COL_%06d_hpos.prj' % (output_path, run_num, num_col), "w")
    # epsg1 = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
    # proj.write(epsg1)
    # proj.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Processes RUN_XXXXXX.csv files '
            'from the Radio Collar Tracker software to generate maps of radio collar '
            'signal strength')

    parser.add_argument('-r', '--run', type = int, help = 'Run number for this data file', metavar = 'run_num', dest = 'run_num', default = 1075)
    parser.add_argument('-n', '--collar', type = int, help = 'Collar number for this data file', metavar = 'collar', dest = 'collar', default = 1)
    parser.add_argument('-i', '--input', help = 'Input file to be processed', metavar = 'data_file', dest = 'filename', required = True)
    parser.add_argument('-o', '--output_dir', help = 'Output directory', metavar = 'output_dir', dest = 'output_path', required = True)
    parser.add_argument('-c', '--definitions', help = "Collar Definitions", metavar = 'collar_definitions', dest = 'col_def', required = True)
    parser.add_argument('-a', '--alpha', help = "Alpha paramater", metavar = 'alpha', dest = 'alpha', required = False, type = float)
    parser.add_argument('-b', '--beta', help = "Beta paramater", metavar = 'beta', dest = 'beta', required = False, type = float)

    # Get configuration
    args = parser.parse_args()
    run_num = args.run_num
    num_col = args.collar
    filename = args.filename
    output_path = args.output_path
    col_def = args.col_def
    alpha = (args.alpha)
    beta = args.beta
    generateGraph(run_num, num_col, filename, output_path, col_def, alpha, beta)
