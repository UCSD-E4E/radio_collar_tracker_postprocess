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

def read_meta_file(filename, tag):
    retval = None
    for line in fileinput.input(filename):
        if tag == line.strip().split(':')[0].strip():
            retval = line.strip().split(':')[1].strip()
            break
    fileinput.close()
    return retval

def generateGraph(run_num, num_col, filename, output_path, col_def):
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
        if math.fabs(alt[i] - avgAlt) > stdAlt:
            continue
        finalCol.append(col[i])
        utm_coord = utm.from_latlon(lat[i], lon[i])
        finalEasting.append(utm_coord[0])
        finalNorthing.append(utm_coord[1])
        zonenum = utm_coord[2]
        zone = utm_coord[3]

    # Calculate heatmap
    print("Collar %d: Building median map..." % num_col)
    margin = 0
    pixelSize = 30 # meters per pixel
    tiffXSize = (int((max(finalEasting)) - int(min(finalEasting)) + margin * 2) / pixelSize + 1)
    tiffYSize = (int((max(finalNorthing)) - int(min(finalNorthing)) + margin * 2) / pixelSize + 1)
    heatMapArea = np.zeros((tiffYSize, tiffXSize)) # [y, x]
    refNorthing = max(finalNorthing) + margin
    minNorthing = refNorthing - (tiffYSize) * pixelSize
    refEasting = min(finalEasting) - margin
    maxEasting = refEasting + tiffXSize * pixelSize
    # print("min northing: %f" % minNorthing)
    # print("max northing: %f" % refNorthing)
    # print("min easting: %f" % refEasting)
    # print("max easting: %f" % maxEasting)
    # Xgeo = refEasting + pixelSize / 2+ Xpix
    # Ygeo = refNorthing - pixelSize / 2- Ypix

    # Plot data
    detectionRadius = 45
    maxLocation = [0, 0, detectionRadius]
    maxA = -100
    for x in xrange(tiffXSize):
        for y in xrange(tiffYSize):
            xgeo = refEasting + pixelSize / 2.0 + x * pixelSize
            ygeo = refNorthing - pixelSize / 2.0 - y * pixelSize
            medianCol = []
            gridCol = []
            for i in xrange(len(finalCol)):
                # if math.fabs(finalEasting[i] - xgeo) < detectionRadius and math.fabs(finalNorthing[i] - ygeo) < detectionRadius:
                if math.fabs(finalEasting[i] - xgeo) < detectionRadius and math.fabs(finalNorthing[i] - ygeo) < detectionRadius:
                    medianCol.append(finalCol[i])
            if len(medianCol) > 15:
                heatMapArea[y][x] = np.median(medianCol)
                if heatMapArea[y][x] > maxA:
                    maxLocation = [xgeo, ygeo, detectionRadius]
                    maxA = heatMapArea[y][x]
            else:
                heatMapArea[y][x] = 100

    # Save plot
    print("Collar %d: Saving median map..." % num_col)
    outputFileName = '%s/RUN_%06d_COL_%06d_median.tiff' % (output_path, run_num, num_col)
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
        refEasting,    # 3
        pixelSize,                      # 4
        0,
        refNorthing,    # 0
        0,  # 1
        -pixelSize))                     # 2
    band = dataset.GetRasterBand(1)
    band.SetNoDataValue(100)
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
    if maxA > np.amin(heatMapArea):
        writer = shapefile.Writer(shapefile.POINT)
        writer.autoBalance = 1
        writer.field("lat", "F", 20, 18)
        writer.field("lon", "F", 20, 18)

        for i in xrange(len(finalCol)):
            if math.fabs(finalEasting[i] - maxLocation[0]) < maxLocation[2] and math.fabs(finalNorthing[i] - maxLocation[1]) < maxLocation[2]:
                lat, lon = utm.to_latlon(finalEasting[i], finalNorthing[i], zonenum, zone)
                writer.point(lon, lat)
                writer.record(lon, lat)


        writer.save('%s/RUN_%06d_COL_%06d_median_sel.shp' % (output_path, run_num, num_col))
        proj = open('%s/RUN_%06d_COL_%06d_median_sel.prj' % (output_path, run_num, num_col), "w")
        epsg1 = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        proj.write(epsg1)
        proj.close()
    print("Collar %d: Median Map Stddev: %f" % (num_col, np.std(heatMapArea)))
    if maxA > np.amin(heatMapArea) + 0.5:
        print("Collar %d: Estimated location is %f, %f within %.0f meters" % (num_col, maxLocation[0], maxLocation[1], maxLocation[2]))
        writer = shapefile.Writer(shapefile.POINT)
        writer.autoBalance = 1
        writer.field("lat", "F", 20, 18)
        writer.field("lon", "F", 20, 18)
        writer.field("radius", "F", 20, 18)

        lat, lon = utm.to_latlon(maxLocation[0], maxLocation[1], zonenum, zone)
        writer.point(lon, lat, maxLocation[2])
        writer.record(lon, lat, maxLocation[2])


        writer.save('%s/RUN_%06d_COL_%06d_median_pos.shp' % (output_path, run_num, num_col))
        proj = open('%s/RUN_%06d_COL_%06d_median_pos.prj' % (output_path, run_num, num_col), "w")
        epsg1 = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        proj.write(epsg1)
        proj.close()
        return maxLocation
    else:
        print("Collar %d: no estimated location available!" % (num_col))
        return None

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
    generateGraph(run_num, num_col, filename, output_path, col_def)
