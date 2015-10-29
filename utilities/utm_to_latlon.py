#!/usr/bin/env python
import argparse
import utm
parser = argparse.ArgumentParser(description='Converts UTM to Lat Lon')
parser.add_argument('zone_num')
parser.add_argument('zone_letter')
parser.add_argument('easting')
parser.add_argument('northing')
args = parser.parse_args()

latlon = utm.to_latlon(int(args.easting), int(args.northing), int(args.zone_num), args.zone_letter)

print("%f, %f" % (latlon[0], latlon[1]))

