#!/usr/bin/env python
import argparse
import os
import shutil

# Get configuration
parser = argparse.ArgumentParser(description='Concatenates the proper signal files together for the Radio Collar Tracker')
parser.add_argument('-i', '--input', metavar='input_dir', dest='input_dir', required = True)
parser.add_argument('-r', '--run', type=int, required = True, metavar = 'run_num', dest = 'run_num')
args = parser.parse_args()

# Set configuration
input_dir = args.input_dir
run_num = args.run_num

gps_file = '/GPS_%06d' % (run_num)
meta_file = '/META_%06d' % (run_num)
output_file = '/RUN_%06d.raw' % (run_num)
signal_file_prefix = '/RAW_DATA_%06d_' % (run_num)

# Import META file
meta_file_stream = open(input_dir + meta_file, 'r')
# Get info
start_time = float(meta_file_stream.readline().strip().split(':')[1].strip())
center_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
sampling_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
gain = float(meta_file_stream.readline().strip().split(':')[1].strip())

# Get GPS data
gps_stream = open(input_dir + gps_file, 'r')
start_gps_time = float(gps_stream.readline().split(',')[0].strip())

# get last gps
gps_line = ""
while True:
    line_buffer = gps_stream.readline()
    if line_buffer == "":
        break
    gps_line = line_buffer
	

last_gps_time = float(gps_line.split(',')[0].strip())

# Get number of signal files
dir_list = os.listdir(input_dir)
filecount = 0
for filename in dir_list:
    if filename.startswith("RAW_DATA"):
        filecount += 1

# Calculate first signal file
filesize = os.stat(input_dir + signal_file_prefix + "%06d" % (1)).st_size
file_length = filesize / 2.0 / sampling_freq
start_file = 0
for i in range(1, filecount + 1):
    if (i - 1) * file_length + start_time < start_gps_time:
        start_file = i
    else:
        break

# Calculate last signal file
last_file = start_file
for i in range(start_file, filecount + 1):
    last_file = i
    if (i - 1) * file_length + start_time > last_gps_time:
	break

# concatenate files
dest = open(input_dir + output_file, 'wb')
for i in range(start_file, last_file):
    shutil.copyfileobj(open(input_dir + signal_file_prefix + "%06d" % (i), 'rb'), dest)

dest.close()    
