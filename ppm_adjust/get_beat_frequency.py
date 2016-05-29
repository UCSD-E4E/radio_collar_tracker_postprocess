#!/usr/bin/env python
import argparse

def getBeatFreq(center_freq, collar_freq, ppm):
	actual_center = center_freq / 1.e6 * ppm + center_freq
	beat_freq = collar_freq - actual_center
	return int(beat_freq)

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description = 'Computes the proper beat frequency for a collar given the SDR center frequency, SDR PPM error, and the transmit frequency of the collar')

	parser.add_argument('-f', '--frequency', help = 'SDR center frequency', metavar = 'center_freq', dest = 'center_freq', type = int, required = True)
	parser.add_argument('-c', '--collar_freq', help = 'Collar transmit frequency', metavar = 'collar_freq', dest = 'collar_freq', type = int, required = True)
	parser.add_argument('-e', '--error', help = 'SDR PPM error', metavar = 'ppm', dest = 'ppm', type = int, required = True)
	args = parser.parse_args()

	center_freq = args.center_freq
	collar_freq = args.collar_freq
	ppm = args.ppm

	print(getBeatFreq(center_freq, collar_freq, ppm))
