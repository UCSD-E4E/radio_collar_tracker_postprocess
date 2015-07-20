#!/usr/local/bin/python
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
parser.add_argument('filename', help='CSV file from the spectrumAnalysis code')
parser.add_argument('-d', '--directory', default=os.getcwd(),
	help='output directory for map files', metavar='<directory>')
parser.add_argument('--ignore-run-number', action='store_true',
	dest='run_num_mismatch',
	help='Ignore run number mistmatch between filename and configuration file')
parser.add_argument('-k', '--output_kml', action='store_true', dest='kml',
	help='Creates a kml containing points representing the locations and '
	'signal strengths of the radio collars are specific copter locations.')
args = parser.parse_args()

filename = args.filename
ignore_number_mismatch = args.run_num_mismatch
output_path = args.directory
kml_output = args.kml
## FIXME use length of file to get number of collars!
# Load config file
try:
	job_cfg = open('JOB', 'r')
except Exception, e:
	print("Unable to open JOB config file! Aborting...")
	sys.exit(1)
job_cfg.readline()	# toss data path
run_num = int(job_cfg.readline().rpartition(" ")[2])
freq_em = int(job_cfg.readline().rpartition(" ")[2])
pulse_ms = int(job_cfg.readline().rpartition(" ")[2])
lin_scale = int(job_cfg.readline().rpartition(" ")[2])
map_d = int(job_cfg.readline().rpartition(" ")[2])
alpha_c_thres = int(job_cfg.readline().rpartition(" ")[2])
num_col = int(job_cfg.readline().rpartition(" ")[2])
freq_drift = int(job_cfg.readline().rpartition(" ")[2])

## FIXME use length of file to get number of collars!
# Load collar file
try:
	col_cfg = open('COL', 'r')
except Exception, e:
	print("Unable to open collar definitions file! Aborting...")
	sys.exit(1)
collars = []
for i in range(num_col):
	try:
		collars.append(int(col_cfg.readline().strip()))
	except Exception, e:
		print("Error: Could not load collar definitions! Aborting...")
		sys.exit(1)

# Load data file
try:
	filenum = int(filename.partition("_")[2].rpartition(".")[0])
except Exception,e:
	run_num = -1
if not ignore_number_mismatch and run_num != filenum:
	print("Error: Filename does not match expected run number from config! Exiting...")
	sys.exit(1)


if filename.rpartition(".")[2] != "csv":
	print("Invalid file! Usage: display_data.py data_file")
	print("data_file   CSV file from the spectrumAnalysis code")
# make list of columns
names = ['lat', 'lon', 'alt', 'r1', 'r2']
for i in xrange(1, num_col + 1):
	names.append('col' + str(i))

# Read CSV
data = np.genfromtxt(filename, delimiter=',', names=names)
coldata = [[0 for x in range(len(data['lat']))] for x in range(num_col)]
# Modify values
lat = [x / 10000000.0 for x in data['lat']]
lon = [x / 10000000.0 for x in data['lon']]
alt = [x / 1000.0 for x in data['alt']]
for i in xrange(1, num_col + 1):
	colname = 'col' + str(i)
	coldata[i-1] = [x / 1000 for x in data[colname]]
north = np.amax(lat)
south = np.amin(lat)
east = np.amax(lon)
west = np.amin(lon)

# convert deg to utm
zone = "X"
zonenum = 60;
for i in range(len(data['lat'])):
	utm_coord = utm.from_latlon(lat[i], lon[i])
	zonenum = utm_coord[2]
	zone = utm_coord[3]
	lon[i] = utm_coord[0]
	lat[i] = utm_coord[1]

maxCol = np.amax(coldata)
minCol = np.amin(coldata)
for i in xrange(1, num_col + 1):
	fig = plot.figure(i)
	fig.set_size_inches(8, 6)
	fig.set_dpi(72)
	curColMap = plot.cm.get_cmap('jet')
	sc = plot.scatter(lon, lat, c=coldata[i - 1], cmap=curColMap, vmin = minCol, vmax = maxCol)
	colorbar = plot.colorbar(sc)
	colorbar.set_label('SNR')
	plot.grid()
	ax = plot.gca()
	ax.get_xaxis().get_major_formatter().set_useOffset(False)
	ax.get_yaxis().get_major_formatter().set_useOffset(False)
	ax.set_xlabel('Easting')
	ax.set_ylabel('Northing')
	ax.set_title('Run %d, Collar at %0.6f MHz\nUTM Zone: %d %s' % (run_num,
		collars[i - 1] / 1000000.0, zonenum, zone))
	ax.set_aspect('equal')
	plot.xticks(rotation='vertical')

	plot.savefig('%s/RUN_%06d_COL_%0.6f.png' % (output_path, run_num,
		collars[i - 1] / 1000000.0), bbox_inches = 'tight')
	print('Collar at %0.6f MHz: %s/RUN_%06d_COL_%0.6f.png' %
		(collars[i - 1] / 1000000.0, output_path, run_num,
		collars[i - 1] / 1000000.0))
	# plot.show(block=False)
	plot.close()

if(kml_output):
	import Image
	for i in xrange(1, num_col + 1):
		fig = plot.figure(i)
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
		new_image.save('%s/RUN_%06d_COL%0.3ftx.png' % (output_path, run_num,
			collars[i - 1] / 1000000.0))
		os.remove('tmp.png')

		f = open('%s/RUN_%06d_COL%0.3f.kml' % (output_path, run_num,
			collars[i - 1] / 1000000.0), 'w')
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
