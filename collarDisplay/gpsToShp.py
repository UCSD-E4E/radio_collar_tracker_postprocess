#!/usr/bin/env python

import os
import shapefile
import numpy as np
import zipfile
import platform
from StringIO import StringIO
import argparse
import utm


def create_shapefile(csv, output):
    csv = csv.replace("\\", os.sep)
    csv = csv.replace("/", os.sep)
    output = output.replace("\\", os.sep)
    output = output.replace("/", os.sep)

    if not os.path.isfile(csv):
        print("File was not valid: %s" % (csv))
        return

    if output == "":
        output = os.path.splitext(csv)[0]

    if '.shp' in output or '.shx' in output or '.dbx' in output or '.prj' in output:
        output = os.path.splitext(output)[0]


    # Read CSV
    names = ['local_time', 'lat', 'lon', 'utc_time', 'alt', 'relalt', 'vx', 'vy', 'vz', 'hdg']
    data = np.genfromtxt(csv, delimiter=',', names=names)
    # Modify values
    lat = [x / 1e7 for x in data['lat']]
    lon = [y / 1e7 for y in data['lon']]
    alt = data['alt']
    #print(col)

    finalNorthing = []
    finalEasting = []

    for i in range(len(data['lat'])):
        utm_coord = utm.from_latlon(lat[i], lon[i])
        finalEasting.append(utm_coord[0])
        finalNorthing.append(utm_coord[1])
        zonenum = utm_coord[2]
        zone = utm_coord[3]

    minLat = min(finalNorthing)
    refLat = max(finalNorthing)
    refLon = min(finalEasting)
    maxLon = max(finalEasting)
    # print("min northing: %f" % minLat)
    # print("max northing: %f" % refLat)
    # print("min easting: %f" % refLon)
    # print("max easting: %f" % maxLon)

    firstNorthing = finalNorthing[0]
    firstEasting = finalEasting[0]

    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field("lat", "F", 20, 18)
    w.field("lon", "F", 20, 18)

    length = len(lat)
    i = 0
    while i < length:
        if abs(finalNorthing[i] - firstNorthing) < 2:
            i += 1
            continue
        if abs(finalEasting[i] - firstEasting) < 2:
            i += 1
            continue
        #Latitude, longitude, elevation, measurement
        w.point(lon[i], lat[i])
        w.record(lon[i], lat[i])
        i += 1

    #w.record('First','Point')

    w.save(output)
    prj = open('%s.prj' % output, "w")
    epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
    prj.write(epsg)
    prj.close()
    print("Saved %s.shp" % output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', action = "store", default = None, required = True, help = "Input CSV file")
    parser.add_argument('-o', '--output', action = 'store', default = None, required = False, help = "Output Name")

    args = parser.parse_args()
    csvPath = os.path.realpath(args.input)
    output = ""
    if not args.output is None:
        output = os.path.realpath(args.output)
    create_shapefile(csvPath, output)
