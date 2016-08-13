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

def normalProbability(x, mean, stdDev):
    a = 1 / (math.sqrt(2 * stdDev * stdDev * math.pi))
    b = -1 * (x - mean) * (x - mean)
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

def residuals(x, col, lat, lon):
    residual = np.zeros(len(col))
    for i in xrange(len(col)):
        if col[i] < -43:
            continue
        residual[i] = 10 ** (((x[0] * col[i] + x[1]) / 10.0)) - math.sqrt((lat[i] - x[2]) ** 2 + (lon[i] - x[3]) ** 2)
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
    names = ['time', 'lat', 'lon', 'col']

    # Read CSV
    data = np.genfromtxt(filename, delimiter=',', names=names)
    # Modify values
    lat = [x / 1e7 for x in data['lat']]
    lon = [y / 1e7 for y in data['lon']]
    col = data['col']

    # convert deg to utm
    zone = "X"
    zonenum = 60
    avgCol = np.average(col)
    finalCol = []
    finalLat = []
    finalLon = []
    for i in range(len(data['lat'])):
        if col[i] < -43:
            continue
        finalCol.append(col[i])
        utm_coord = utm.from_latlon(lat[i], lon[i])
        finalLat.append(utm_coord[0])
        finalLon.append(utm_coord[1])
        zonenum = utm_coord[2]
        zone = utm_coord[3]

    # Data Analysis
    x0 = [-0.715, -14.51, finalLat[0], finalLon[0]]
    res_x, res_cov_x, res_infodict, res_msg, res_ler = leastsq(residuals, x0, args=(finalCol, finalLat, finalLon), full_output=1)
    easting = res_x[2]
    northing = res_x[3]
    lat_lon = utm.to_latlon(easting, northing, zonenum, zone_letter=zone)
    s_sq = (residuals(res_x, finalCol, finalLat, finalLon) ** 2).sum() / (len(finalCol) - len(x0))
    pcov = res_cov_x * s_sq
    print(np.absolute(pcov[0][0])**0.5)
    print(np.absolute(pcov[1][1])**0.5)
    print(np.absolute(pcov[2][2])**0.5)
    print(np.absolute(pcov[3][3])**0.5)

def generateKML(run_num, num_col, filename, output_path, col_def):
    from PIL import Image
    fig = plot.figure()
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)
    fig.set_size_inches(8, 6)
    fig.set_dpi(72)
    curColMap = plot.cm.get_cmap('jet')
    sc = plot.scatter(lon, lat, c=coldata[i - 1], cmap=curColMap, vmin = minCol, vmax = maxCol)
    ax = plot.gca()
    ax.patch.set_facecolor('none')
    ax.set_aspect('equal')
    plot.axis('off')
    plot.savefig('tmp.png', bbox_inches = 'tight')
    print('Collar at %0.3f MHz: %s/RUN_%06d_COL_%0.3ftx.png' %
        (collars[i - 1] / 1000000.0, output_path, run_num,
        collars[i - 1] / 1000000.0))
    # plot.show(block=False)
    plot.close()

    image=Image.open('tmp.png')
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

    new_image = Image.fromarray(image_data_new)
    new_image.save('%s/RUN_%06d_COL%06dtx.png' % (output_path, run_num, num_col))
    os.remove('tmp.png')

    f = open('%s/RUN_%06d_COL%06d.kml' % (output_path, run_num, num_col), 'w')
    f.write("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
          <Folder>
            <name>Radio Collar Tracker</name>
            <description>Radio Collar Tracker, UCSD</description>
            <GroundOverlay>
              <name>RUN %d</name>
              <description>RUN %d, Collar at %0.3f MHz</description>
              <Icon>
                <href>%s</href>
              </Icon>
              <LatLonBox>
                <north>%f</north>
                <south>%f</south>
                <east>%f</east>
                <west>%f</west>
                <rotation>0</rotation>
              </LatLonBox>
            </GroundOverlay>
          </Folder>
        </kml>""" % (run_num, run_num, collars[i - 1] / 1000000.0, '%s/RUN_%06d_COL%0.3ftx.png' % (output_path, run_num, collars[i - 1] / 1000000.0),north, south, east, west))
    f.close()
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
