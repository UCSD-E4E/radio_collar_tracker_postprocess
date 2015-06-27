#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot

X_labels = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
maxFreq = np.amax(X_labels)
minFreq = np.amin(X_labels)
data = np.genfromtxt("fftheader.txt", skip_header=1)
minFFT = data[1]
maxFFT = data[2]
numFiles = data[0]
# get first row

print("Got header\n")

for i in range(int(numFiles)):
# for i in range(1):
	print("Getting data from file %d..."%(i))
	outputfile = open("test%02d.txt"%(i), "r")
	print("done\n")
	for line in outputfile:
		print("Getting line...")
		time = line.strip().split(',')[0]
		fft = [float(data) for data in line.strip().split(',')[1:]]
		print("done\n")

		print("Plotting...")
		plot.cla()
		plt = plot.plot(X_labels, fft)
		ax = plot.gca()
		# ax.set_xlim(left=minFFT, right=maxFFT)
		ax.set_title("Time: %8d"%(int(time)))
		ax.get_xaxis().get_major_formatter().set_useOffset(False)
		plot.xticks(rotation='vertical')
		plot.savefig("output%08d.png"%(int(time)), bbox_inches='tight')
		# break
	outputfile.close()
