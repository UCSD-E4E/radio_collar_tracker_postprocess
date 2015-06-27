#!/usr/bin/env python
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
from multiprocessing import Pool
import argparse
import sys
from Queue import PriorityQueue

queue = PriorityQueue()
freq_index = 0

def procFile(i):
	print("Getting data from file %d..."%(i))
	outputfile = open("output%02d.txt"%(i), "r")
	for line in outputfile:
		print("Getting line...")
		time = float(line.strip().split(',')[0])
		print("Got time %.3f" % (time))
		fft = [float(data) for data in line.strip().split(',')[1:]]

		queue.put((time, fft[freq_index]))

		# break
	outputfile.close()
	return

# Parse arguments
parser = argparse.ArgumentParser(description='Extracts a specific frequency'
	' from the exported FFT data')
parser.add_argument('frequency', help='Frequency to extract')
args = parser.parse_args()


X_labels = np.genfromtxt("fftheader.txt", delimiter=',', skip_footer=3)
X_label = [float(label) for label in X_labels]

if float(args.frequency) < X_label[0] or float(args.frequency) > X_label[len(X_label) - 1]:
	print("Could not find frequency!  Exiting...")
	sys.exit(1)
while float(args.frequency) > X_label[freq_index]:
	freq_index += 1
print("Using frequency %.3f" % (X_label[freq_index]))
data = np.genfromtxt("fftheader.txt", skip_header=1)
minFFT = data[1]
maxFFT = data[2]
numFiles = data[0]

print("Got header")

print("Running processes...")
p = Pool(1)

p.map(procFile, range(int(0)))


print("Plotting...")
plot.cla()
fig = plot.figure()
fig.set_size_inches(8, 6)
fig.set_dpi(72)
ax = plot.gca()
ax.set_ylim(bottom=minFFT, top=maxFFT)
ax.set_title("Frequency: %f"%(X_label[freq_index]))

fft = []
time = []

while not queue.empty():
	data = queue.get()
	fft.append(data[1])
	time.append(data[0])

plt = plot.scatter(time, fft)
xx, locs = plot.xticks()
ll = ['%.0f' % a for a in xx]
plot.xticks(xx, ll)
plot.xticks(rotation='vertical')
plot.savefig("frequency_%09d.png"%(int(X_label[freq_index])), bbox_inches='tight')
