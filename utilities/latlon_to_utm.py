#!/usr/bin/env python
import argparse
import utm

parser = argparse.ArgumentParser(description='Converts latlon to UTM')
parser.add_argument('deg_east')
parser.add_argument('deg_north')
args = parser.parse_args()

utm = utm.from_latlon(float(args.deg_east), float(args.deg_north))
print("%d%s %d %d" % (utm[2], utm[3], utm[0], utm[1]))

