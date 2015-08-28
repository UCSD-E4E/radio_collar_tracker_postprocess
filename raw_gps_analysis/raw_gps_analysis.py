#!/usr/bin/env python
import math
import cmath
import struct

input_dir = '/home/ntlhui/workspace/radio_collar_tracker_test/RUN_VALIDATION/'
output_dir = '/home/ntlhui/workspace/radio_collar_tracker_test/RUN_VALIDATION/'

signal_file = '/RUN_000045.out'
gps_file = '/GPS_000045'
meta_file = '/META_000045'

# Import META file
meta_file_stream = open(input_dir + meta_file, 'r')
# Get start time
start_time = float(meta_file_stream.readline().strip().split(':')[1].strip())
center_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
sampling_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())/100
gain = float(meta_file_stream.readline().strip().split(':')[1].strip())

# Initialize GPS stream
gps_stream = open(input_dir + gps_file, 'r')

# INitialize Signal stream
signal_stream = open(input_dir + signal_file, 'rb')

# Initialize output stream
out_stream = open(output_dir + "/RUN_000045.csv", 'w')

line = gps_stream.readline()
signal_index = 0
done = False
line_counter = 0

while line != "":
    # Extract time
    gps_time = float(line.split(',')[0].strip())
    if gps_time < (signal_index / sampling_freq) + start_time:
        line = gps_stream.readline()
        line_counter += 1
        continue
    # Extract position
    latitude = int(line.split(',')[1].strip())
    longitude = int(line.split(',')[2].strip())

    # Throw out samples prior to this gps point
    signal_bring_forward = gps_time - ((signal_index / sampling_freq) + start_time )
    samples_bring_forward = int(signal_bring_forward * sampling_freq)
    signal_stream.read(8 * samples_bring_forward)
    signal_index += samples_bring_forward
    
    # Get next second
    max_amplitude = 0
    for x in range(sampling_freq):
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
        # update index
        signal_index += 1
    # Output GPS and signal amplitude
    if done:
        break
    out_stream.write("%f,%d,%d,%f\n" % (gps_time, latitude, longitude, max_amplitude))
    line = gps_stream.readline()
    line_counter += 1

# Close file
print("Read %d lines of GPS data" % line_counter)
print("Read %d samples, or %d bytes of signal data" % (signal_index, signal_index * 8))
out_stream.close()
signal_stream.close()
gps_stream.close()
meta_file_stream.close()
