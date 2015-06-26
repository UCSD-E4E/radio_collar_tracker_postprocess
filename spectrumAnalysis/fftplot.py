#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import axes3d

X = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
data = np.genfromtxt("fftheader.txt", delimiter=',', skip_header=1)
minFFT = data[1]
maxFFT = data[2]
numFiles = data[0]
# get first row

for i in range(int(numFiles)):
	data = np.genfromtxt("output%02d.txt"%(i), delimiter=',')
	Y = [row[0] for row in data]
	Z = [(row[1:]) for row in data]
	sc = plot.scatter(X, Y, Z, vmin = minFFT, vmax = maxFFT)
	plot.savefig("output%02d.png"%(i), bbox_inches='tight')
