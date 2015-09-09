#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plot
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
import os
import argparse

parser = argparse.ArgumentParser(description='Processes RUN_XXXXXX.csv files '
        'from the Radio Collar Tracker software to generate maps of radio collar '
        'signal strength')

filename = '/home/ntlhui/workspace/radio_collar_tracker_test/RUN_001078/GPS_001078'
output_path = '/home/ntlhui/workspace/radio_collar_tracker_test/RUN_001078/'
kml_output = True
run_num = 1078
num_col = 1

# make list of columns
names = ['time', 'lat', 'lon']

# Read CSV
data = np.genfromtxt(filename, delimiter=',', names=names)
# Modify values
lat = [x / 1e7 for x in data['lat']]
lon = [x / 1e7 for x in data['lon']]

north = np.amax(lat)
south = np.amin(lat)
west = np.amin(lon)
east = np.amax(lon)
# convert deg to utm
zone = "X"
zonenum = 60
for i in range(len(data['lat'])):
    utm_coord = utm.from_latlon(lat[i], lon[i])
    zonenum = utm_coord[2]
    zone = utm_coord[3]
    lon[i] = utm_coord[0]
    lat[i] = utm_coord[1]


fig = plot.figure(i)
fig.set_size_inches(8, 6)
fig.set_dpi(72)
sc = plot.scatter(lon, lat)
plot.grid()
ax = plot.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.get_yaxis().get_major_formatter().set_useOffset(False)
ax.set_xlabel('Easting')
ax.set_ylabel('Northing')
ax.set_title('Run %d\nUTM Zone: %d %s' % (run_num, zonenum, zone))
ax.set_aspect('equal')
plot.xticks(rotation='vertical')

plot.savefig('%s/RUN_%06d_COL_.png' % (output_path, run_num,
), bbox_inches = 'tight')
print('Collar at MHz: %s/RUN_%06d_COL_.png' %
    (output_path, run_num))
# plot.show(block=False)
plot.close()

if(kml_output):
    import Image
    i = 1
    fig = plot.figure(i)
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0)
    fig.set_size_inches(8, 6)
    fig.set_dpi(72)
    curColMap = plot.cm.get_cmap('jet')
    sc = plot.scatter(lon, lat)
    ax = plot.gca()
    ax.patch.set_facecolor('none')
    ax.set_aspect('equal')
    plot.axis('off')
    plot.savefig('tmp.png', bbox_inches = 'tight')
    print('Collar at %0.3f MHz: %s/RUN_%06d_COL_%0.3ftx.png' %
        (0, output_path, run_num,
        0))
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
    new_image.save('%s/RUN_%06d_COL%0.3ftx.png' % (output_path, run_num,
    0))
    os.remove('tmp.png')

    f = open('%s/RUN_%06d_COL%0.3f.kml' % (output_path, run_num,
    0), 'w')
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
</kml>""" % (run_num, run_num, 0, '%s/RUN_%06d_COL%0.3ftx.png' % (output_path, run_num, 0),north, south, east, west))
    f.close()
