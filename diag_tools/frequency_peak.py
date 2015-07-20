#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
from multiprocessing import Pool
import argparse
import sys
from Queue import PriorityQueue
import os.path


def procFile(i):
	# print("Getting data from file %d..."%(i))
	outputfile = open("output%02d.txt"%(int(i)), "r")
	filestream = open("fftpeak_%03d.txt"%(i), "w")
	peaks = [0] * length
	for line in outputfile:
		fft = [float(data) for data in line.strip().split(',')[1:]]
		time = float(line.strip().split(',')[0])
		if time > 8:
			for j in range(length):
				if fft[j] > peaks[j]:
					peaks[j] = fft[j]
	for j in range(length):
		filestream.write("%.9f\t" % (peaks[j]))
	outputfile.close()
	filestream.close()
	return

parser = argparse.ArgumentParser('')
parser.add_argument('start')
parser.add_argument('end')
args = parser.parse_args()
sf = int(args.start)
ef = int(args.end)

length = 0
freq_index = 0

X_labels = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
X_label = [float(label) for label in X_labels]

data = np.genfromtxt("fftheader.txt", skip_header=1)
minFFT = data[1]
maxFFT = data[2]
numFiles = data[0]
# numFiles = 1
length = len(X_label)

print("Got header")
if not os.path.isfile('peaks.csv'):
	print("Running processes...")
	p = Pool(8)

	p.map(procFile, range(int(numFiles)))
	# procFile(0)
	# for i in range(int(numFiles)):
	# 	procFile(i)

	# All files done
print("Plotting...")
plot.cla()
fig = plot.figure()
fig.set_size_inches(8, 6)
fig.set_dpi(72)
ax = plot.gca()
ax.set_xlim(left=sf, right=ef)

peaks = [0] * length

for i in range(int(numFiles)):
	datafile = open("fftpeak_%03d.txt"%(i), "r")
	line = datafile.next()
	fft = [float(data) for data in line.strip().split('\t')]
	for j in range(length):
		if fft[j] > peaks[j]:
			peaks[j] = fft[j]

plt = plot.plot(X_label, peaks)
ax.set_ylim(bottom=minFFT, top=np.amax(peaks))
xx, locs = plot.xticks()
ll = ['%.0f' % a for a in xx]
print len(ll)
plot.xticks(xx, ll)
plot.xticks(rotation='vertical')
plot.savefig("peaks.png", bbox_inches='tight')

if not os.path.isfile('peaks.csv'):
	csv = open("peaks.csv", 'w')
	for i in range(length):
		csv.write("%f, %f\n" % (float(X_label[i]), float(peaks[i])))
	csv.close()


