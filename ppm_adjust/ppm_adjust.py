#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description = 'Calculator for generating the recorded frequency given a PPM error and the actual frequency entering the antenna')
parser.add_argument('-f', '--frequency', type = int, required = True, metavar = 'frequency', dest = 'freq', help = 'Signal frequency entering the antenna')
parser.add_argument('-e', '--error', type = int, required = True, metavar = 'error', dest = 'err', help = 'PPM error of the entire SDR')
args = parser.parse_args()
theoretical_frequency = args.freq
ppm = args.err

actual_freq = theoretical_frequency / 1.e6 * ppm + theoretical_frequency
print("%d" % int(actual_freq))
