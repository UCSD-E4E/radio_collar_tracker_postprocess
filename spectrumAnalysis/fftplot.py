#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import axes3d

X_labels = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
data = np.genfromtxt("fftheader.txt", delimiter=',', skip_header=1)
minFFT = data[1]
maxFFT = data[2]
numFiles = data[0]
# get first row

print("Got header\n")

for i in range(int(numFiles)):
	print("Getting data from file %d..."%(i))
	data = np.genfromtxt("output%02d.txt"%(i), delimiter=',')
	print("done\n")
	Y_labels = [row[0] for row in data]
	Z = [(row[1:]) for row in data]
	print("Converting axes...")
	X = [X_labels[x] for x in range(len(X_labels)) for y in range(len(Y_labels))]
	Y = [Y_labels[y] for x in range(len(X_labels)) for y in range(len(Y_labels))]
	print("done\n")
	print("Plotting...")
	sc = plot.scatter(X, Y, Z, vmin = minFFT, vmax = maxFFT)
	print("done\n")
	plot.savefig("output%02d.png"%(i), bbox_inches='tight')
