#!/usr/bin/env python
import argparse
import utm

parser = argparse.ArgumentParser(description='Creates a polygon shape around a given point')
parser.add_argument('zone_num', help='UTM Zone Number')
parser.add_argument('zone_letter', help='UTM Zone Letter')
parser.add_argument('easting', help='UTM Easting')
parser.add_argument('northing', help='UTM Northing')
parser.add_argument('x_size', help="East-west size")
parser.add_argument('y_size', help='North-south size')
parser.add_argument('file', help='Output file')
args = parser.parse_args()

zone_num = int(args.zone_num)
zone_letter = args.zone_letter
easting = int(args.easting)
northing = int(args.northing)
x_size = int(args.x_size)
y_size = int(args.y_size)
outputFile = open(args.file, "w")

ul = [easting - x_size / 2, northing + y_size / 2]
ur = [easting + x_size / 2, northing + y_size / 2]
ll = [easting - x_size / 2, northing - y_size / 2]
lr = [easting + x_size / 2, northing - y_size / 2]

ulll = utm.to_latlon(ul[0], ul[1], zone_num, zone_letter)
urll = utm.to_latlon(ur[0], ur[1], zone_num, zone_letter)
llll = utm.to_latlon(ll[0], ll[1], zone_num, zone_letter)
lrll = utm.to_latlon(lr[0], lr[1], zone_num, zone_letter)

outputFile.write("#saved by Mission Planner 1.3.30\n")
outputFile.write("%.13f %.13f\n" % (ulll[0], ulll[1]))
outputFile.write("%.13f %.13f\n" % (urll[0], urll[1]))
outputFile.write("%.13f %.13f\n" % (lrll[0], lrll[1]))
outputFile.write("%.13f %.13f\n" % (llll[0], llll[1]))

