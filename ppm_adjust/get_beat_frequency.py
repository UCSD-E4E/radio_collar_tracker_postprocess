#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description = 'Computes the proper beat frequency for a collar given the SDR center frequency, SDR PPM error, and the transmit frequency of the collar')

parser.add_argument('-f', '--frequency', help = 'SDR center frequency', metavar = 'center_freq', dest = 'center_freq', type = int, required = True)
parser.add_argument('-c', '--collar_freq', help = 'Collar transmit frequency', metavar = 'collar_freq', dest = 'collar_freq', type = int, required = True)
parser.add_argument('-e', '--error', help = 'SDR PPM error', metavar = 'ppm', dest = 'ppm', type = int, required = True)
args = parser.parse_args()

center_freq = args.center_freq
collar_freq = args.collar_freq
ppm = args.ppm

actual_collar = collar_freq / 1.e6 * ppm + collar_freq
beat_freq = center_freq - actual_collar
print(int(beat_freq))
