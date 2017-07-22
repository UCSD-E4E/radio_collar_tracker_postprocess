#!/usr/bin/env python
import numpy as np
import argparse

parser = argparse.ArgumentParser('')
parser.add_argument('frequency')
args = parser.parse_args()

data = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
labels = [float(label) for label in data]
if labels[0] > int(args.frequency) or labels[len(labels) - 1] < int(args.frequency):
	print('Not Found!')
	exit(-1)
for i in range(len(labels)):
	if int(args.frequency) < labels[i]:
		print(i-1)
		exit(0)
