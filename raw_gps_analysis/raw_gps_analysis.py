#!/usr/bin/env python
import math
import cmath
import struct
import argparse
import utm

def getLocalTime(line):
	return float(line.split(',')[0].strip())

def getGPSTime(line):
	return float(line.split(',')[3].strip())

def getGPSCoord(line):
	lat = float(line.split(',')[1].strip()) / 1e7
	lon = float(line.split(',')[2].strip()) / 1e7
	return (lat, lon)

def getGPS(GPS_filename, time):
	gps_file = open(GPS_filename, 'r')
	line = None
	pre_line = None
	while True:
		line = gps_file.readline()
		if getLocalTime(line) < time:
			pre_line = line
		if getLocalTime(line) >= time:
			break
	gps_file.close()
	pre_time = getLocalTime(pre_line)
	post_time = getLocalTime(line)
	timespan = post_time - pre_time
	fraction = (time - pre_time) / timespan
	
	pre_gps = getGPSCoord(pre_line)
	post_gps = getGPSCoord(line)
	x_dist = post_gps[0] - pre_gps[0]
	y_dist = post_gps[1] - pre_gps[1]
	x_offset = fraction * x_dist
	y_offset = fraction * y_dist
	x_final = pre_gps[0] + x_offset
	y_final = pre_gps[1] + y_offset
	
	pre_gps_time = getGPSTime(pre_line)
	post_gps_time = getGPSTime(line)
	time_dist = post_gps_time - pre_gps_time
	time_final = fraction * time_dist + pre_gps_time
	retval = (time_final, x_final, y_final)
	return retval


def process(input_dir, output_dir, run_num, col_num, tar_alt):
	# Configure variables
	signal_file = '/RUN_%06d_%06d.raw' % (run_num, col_num)
	gps_file = '/GPS_%06d' % (run_num)
	meta_file = '/META_%06d' % (run_num)
	output_file = '/RUN_%06d_COL_%06d.csv' % (run_num, col_num)
	period = 1.5

	# Import META file
	meta_file_stream = open(input_dir + meta_file, 'r')
	# Get start time
	start_time = float(meta_file_stream.readline().strip().split(':')[1].strip())
	center_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
	fft_length = 4096
	sampling_freq = int(meta_file_stream.readline().strip().split(':')[1].strip()) / fft_length
	gain = float(meta_file_stream.readline().strip().split(':')[1].strip())

	# Initialize GPS stream
	gps_stream = open(input_dir + gps_file, 'r')

	# Initialize Signal stream
	signal_stream = open(input_dir + signal_file, 'rb')

	# Initialize output stream
	out_stream = open(output_dir + output_file, 'w')

	signal_index = 0
	done = False
	line_counter = 0

	line = gps_stream.readline()
	time_target = float(line.split(',')[0].strip()) - 0.5
	start_alt = float(line.split(',')[4].strip()) / 1000

	latitude = int(line.split(',')[1].strip())
	longitude = int(line.split(',')[2].strip())
	utm_coord = utm.from_latlon(latitude / 1e7, longitude / 1e7)
	startlon = utm_coord[0]
	startlat = utm_coord[1]

	while True:
		# Read in 1.6 seconds of data
		target_index = int(signal_index + 1.6 * sampling_freq)
		max_amplitude = 0
		rms_amplitude = 0
		count = 0
		max_idx = signal_index
		while signal_index < target_index:
			signal_raw = signal_stream.read(8)
			if signal_raw == "":
				done = True
				break
			sample_buffer = struct.unpack('ff', signal_raw)
			sample = sample_buffer[0] + sample_buffer[1] * 1j;
			sample_amp = abs(sample)
			if sample_amp > max_amplitude:
				max_amplitude = sample_amp
				max_idx = signal_index
			rms_amplitude += sample_amp ** 2
			signal_index += 1
			count += 1
		rms_amplitude /= count
		rms_amplitude = math.sqrt(rms_amplitude)
		if done:
			break
		max_amplitude = 10 * math.log10(max_amplitude)
		signal_time = signal_index / sampling_freq
		localtime = signal_time + start_time
		gps_data = getGPS(input_dir + gps_file, localtime)
		out_stream.write("%f,%d,%d,%f,%f\n" % (gps_data[0], gps_data[1]*1e7, gps_data[2]*1e7, max_amplitude, 0))
	
	# Close file
	print("Read %d samples, or %d bytes of signal data" % (signal_index, signal_index * 8))
	out_stream.close()
	signal_stream.close()
	gps_stream.close()
	meta_file_stream.close()

if __name__ == '__main__':
	# Get configuration
	parser = argparse.ArgumentParser(description='Combines the signal and gps data streams for the Radio Collar Tracker')
	parser.add_argument('-i', '--input', metavar='input_dir', dest='input_dir', required = True)
	parser.add_argument('-o', '--output', metavar = 'output_dir', dest = 'output_dir', required = True)
	parser.add_argument('-r', '--run', type=int, required = True, metavar = 'run_num', dest = 'run_num')
	parser.add_argument('-c', '--collar', type = int, required = True, metavar = 'collar', dest = 'collar')
	parser.add_argument('-a', '--altitude', type = int, required = True, metavar = 'altitude', dest = 'alt')

	args = parser.parse_args()

	# Set configuration
	input_dir = args.input_dir
	output_dir = args.output_dir
	run_num = args.run_num
	col_num = args.collar
	tar_alt = args.alt

	process(input_dir, output_dir, run_num, col_num, tar_alt)
