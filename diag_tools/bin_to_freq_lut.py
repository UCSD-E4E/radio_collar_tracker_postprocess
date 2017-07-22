#!/usr/bin/env python
import numpy as np
import argparse

parser = argparse.ArgumentParser('')
parser.add_argument('bin')
args = parser.parse_args()

bin = int(args.bin)
data = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
labels = [float(label) for label in data]
if bin >= len(labels):
	print('Not Found!')
	exit(-1)
print("%d" % labels[bin])
exit(0)
