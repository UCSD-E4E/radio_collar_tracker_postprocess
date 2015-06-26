#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import axes3d

data = np.genfromtxt("/home/e4e/fiona/output00.txt", delimiter=',')

# get first row

X = data[0][1:]

Z = [(row[1:]) for row in data[1:]]
Y = [row[0] for row in data[1:]]

for i in range(20):
	data = np.genfromtxt("/home/e4e/fiona/output%2d" % i, delimiter=',')
	for row in data:
		Y.append(row[0])
		Z.append(row[1:])

X, Y = np.meshgrid(X, Y)

fig = plot.figure()
ax = fig.gca(projection='3d')

ax.plot_surface(X, Y, np.array(Z))

plot.savefig("fftout.png", bbox_inches='tight')
