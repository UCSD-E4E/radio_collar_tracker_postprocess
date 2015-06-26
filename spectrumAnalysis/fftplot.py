#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import axes3d

data = np.genfromtxt("fft.txt", delimiter=',')

# get first row

X = data[0][1:]

Z = [(row[1:]) for row in data[1:]]
Y = [row[0] for row in data[1:]]

X, Y = np.meshgrid(X, Y)

fig = plot.figure()
ax = fig.gca(projection='3d')

ax.plot_surface(X, Y, np.array(Z))

plot.savefig("fftout.png", bbox_inches='tight')
