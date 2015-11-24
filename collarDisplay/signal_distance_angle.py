#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plot
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
import os
import argparse
import fileinput
import math

def read_meta_file(filename, tag):
    for line in fileinput.input(filename):
        if tag == line.strip().split(':')[0].strip():
	    return line.strip().split(':')[1].strip()

kml_output = False
# TODO Fix test case
plot_height = 6
plot_width = 8
plot_dpi = 72

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

# Get collar frequency
col_freq = float(read_meta_file(col_def, str(num_col))) / 1.e6

# make list of columns
# Expects the csv to have the following columns: time, lat, lon, [collars]
names = ['time', 'lat', 'lon', 'col']

# Read CSV
data = np.genfromtxt(filename, delimiter=',', names=names)
# Modify values
lat = [x / 1e7 for x in data['lat']]
lon = [x / 1e7 for x in data['lon']]

# convert deg to utm
zone = "X"
zonenum = 60
for i in range(len(data['lat'])):
	utm_coord = utm.from_latlon(lat[i], lon[i])
	lon[i] = utm_coord[0]
	lat[i] = utm_coord[1]
	zonenum = utm_coord[2]
	zone = utm_coord[3]

## Custom Location
target_lon = 599679
target_lat = 3620338
distance = [None] * len(data['lat'])
angle = [None] * len(data['lat'])

# Calculate distance and angle per sample
prev_lat = lat[0]
prev_lon = lon[0] + 1
for i in range(len(data['lat'])):
	d_lat = - lat[i] + target_lat
	d_lon = - lon[i] + target_lon
	distance[i] = math.sqrt(d_lat * d_lat + d_lon * d_lon)
	head_lat = prev_lat - lat[i]
	head_lon = prev_lon - lon[i]
	angle[i] = math.acos(d_lat * head_lat + d_lon * head_lon) / math.pi * 180
	prev_lat = lat[i]
	prev_lon = lon[i]

# Configure plot
fig = plot.figure()
fig.set_size_inches(plot_width, plot_height)
fig.set_dpi(plot_dpi)
plot.grid()
ax = plot.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.get_yaxis().get_major_formatter().set_useOffset(False)
ax.set_xlabel('Angle')
ax.set_ylabel('Distance')
ax.set_title('Run %d, Collar %d at %3.3f MHz' % (run_num, num_col, col_freq))
plot.xticks(rotation='vertical')

# Calculate colorplot
maxCol = np.amax(data['col'])
minCol = np.amin(data['col'])
curColMap = plot.cm.get_cmap('jet')

# Plot data
sc = plot.scatter(angle, distance, c=data['col'], cmap=curColMap, vmin = minCol, vmax = maxCol)
colorbar = plot.colorbar(sc)
colorbar.set_label('Maximum Signal Amplitude')


# Save plot
plot.savefig('%s/RUN_%06d_COL_%06d.png' % (output_path, run_num, num_col), bbox_inches = 'tight')
print('Collar %d: %s/RUN_%06d_COL_%06d.png' %
	(num_col, output_path, run_num, num_col))
# plot.show(block=False)
plot.close()
