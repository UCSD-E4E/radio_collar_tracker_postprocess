#!/usr/bin/env python
import math
import cmath
import struct
import argparse
import utm

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
	while line != "":
		# Extract time
		gps_time = float(line.split(',')[0].strip())
		gps_alt = float(line.split(',')[4].strip()) / 1000 - start_alt

		# Fast forward if less than 1.5 sec prior to previous
		if gps_time < time_target:
			line = gps_stream.readline()
			line_counter += 1
			continue
		time_target += period

		# Fast forward if no SDR data.
		if gps_time <= (float(signal_index) / sampling_freq) + start_time:
			line = gps_stream.readline()
			line_counter += 1
			continue

		# throw out if not within 20% of target altitude
		# if math.fabs(gps_alt - tar_alt) / tar_alt > 0.2:
		# 	line = gps_stream.readline()
		# 	line_counter += 1
		# 	continue

		# Extract position
		latitude = int(line.split(',')[1].strip())
		longitude = int(line.split(',')[2].strip())
		utm_coord = utm.from_latlon(latitude / 1e7, longitude / 1e7)
		lon = utm_coord[0]
		lat = utm_coord[1]
		if abs(lon - startlon) < 2:
			line = gps_stream.readline()
			line_counter += 1
			continue
		if abs(lat - startlat) < 2:
			line = gps_stream.readline()
			line_counter += 1
			continue

		# Samples prior to this gps point
		#signal_bring_forward = gps_time - ((float(signal_index) / sampling_freq) + start_time )
		#samples_bring_forward = int(signal_bring_forward * sampling_freq)

		# Get max of samples
		max_amplitude = 0
		avg_amplitude = 0
		count = 0
		while gps_time > (float(signal_index) / sampling_freq + start_time):
			# Get sample
			signal_raw = signal_stream.read(8)
			if signal_raw == "":
				done = True
				break
			sample_buffer = struct.unpack('ff', signal_raw)
			sample = sample_buffer[0] + sample_buffer[1] * 1j;
			# Get amplitude
			sample_amplitude = abs(sample)
			# Check max
			if sample_amplitude > max_amplitude:
				max_amplitude = sample_amplitude
			avg_amplitude += sample_amplitude
			# update index
			signal_index += 1
			count += 1
		# Output GPS and signal amplitude
		avg_amplitude /= count
		if done:
			break
		max_amplitude = 10 * math.log10(max_amplitude)
		out_stream.write("%f,%d,%d,%f,%f\n" % (gps_time, latitude, longitude, max_amplitude, gps_alt))
		line = gps_stream.readline()
		line_counter += 1

	# Close file
	print("Read %d lines of GPS data" % line_counter)
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
