#!/usr/bin/env python

num_frames_per_file = 4
data_frame_size = 6348800

fin = open('RAW_DATA_001149')
fout = open('iq', 'w')

for i in range(num_frames_per_file):
	data = fin.read(data_frame_size)
	gps = fin.read(12)
	gain = fin.read(1)

	fout.write(data)

fout.close()
fin.close()
