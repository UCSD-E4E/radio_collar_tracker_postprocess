#!/usr/bin/env python
import struct
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import sys
import glob
import utm
import argparse
import getMappedCollars

from matplotlib.colors import LinearSegmentedColormap


def getCallback(iteration, total):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
	"""
	decimals = 1
	prefix = ''
	suffix = ''
	length = 30
	fill = '*'
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
	sys.stdout.flush()
	# Print New Line on Complete
	if iteration == total: 
		print()

def getLocalTime(line):
	return float(line.split(',')[0].strip())

def getGPSTime(line):
	return float(line.split(',')[3].strip())

def getGPSCoord(line):
	lat = float(line.split(',')[1].strip()) / 1e7
	lon = float(line.split(',')[2].strip()) / 1e7
	return (lat, lon)

def getGPS(run_dir, run_num, time):
	gps_file = open('%s/GPS_%06d' % (run_dir, run_num), 'r')
	line = None
	while True:
		line = gps_file.readline()
		# print(line)
		gps_time = getLocalTime(line)
		if gps_time >= time:
			break
	gps_file.close()
	return line

def fileOffsetToTime(run_dir, run_num, file_num, file_offset):
	meta_file = open('%s/META_%06d' % (run_dir, run_num), 'r')
	start_time = float(meta_file.readline().split(':')[1].strip())
	file_size = 67108864
	file_seconds = file_size / 4.0 / 2000000.0
	meta_file.close()
	return file_seconds * (file_num - 1) + file_offset + start_time

CENTER_FREQ = 172500000
fft_length = 4096
fig = plt.figure()
minFreq = 172.012 - 0.01
maxFreq = 172.012 + 0.01


median_fft = None
shifted_fft = None
num_samples = None
cm_data = [[0.2081, 0.1663, 0.5292], [0.2116238095, 0.1897809524, 0.5776761905], 
 [0.212252381, 0.2137714286, 0.6269714286], [0.2081, 0.2386, 0.6770857143], 
 [0.1959047619, 0.2644571429, 0.7279], [0.1707285714, 0.2919380952, 
  0.779247619], [0.1252714286, 0.3242428571, 0.8302714286], 
 [0.0591333333, 0.3598333333, 0.8683333333], [0.0116952381, 0.3875095238, 
  0.8819571429], [0.0059571429, 0.4086142857, 0.8828428571], 
 [0.0165142857, 0.4266, 0.8786333333], [0.032852381, 0.4430428571, 
  0.8719571429], [0.0498142857, 0.4585714286, 0.8640571429], 
 [0.0629333333, 0.4736904762, 0.8554380952], [0.0722666667, 0.4886666667, 
  0.8467], [0.0779428571, 0.5039857143, 0.8383714286], 
 [0.079347619, 0.5200238095, 0.8311809524], [0.0749428571, 0.5375428571, 
  0.8262714286], [0.0640571429, 0.5569857143, 0.8239571429], 
 [0.0487714286, 0.5772238095, 0.8228285714], [0.0343428571, 0.5965809524, 
  0.819852381], [0.0265, 0.6137, 0.8135], [0.0238904762, 0.6286619048, 
  0.8037619048], [0.0230904762, 0.6417857143, 0.7912666667], 
 [0.0227714286, 0.6534857143, 0.7767571429], [0.0266619048, 0.6641952381, 
  0.7607190476], [0.0383714286, 0.6742714286, 0.743552381], 
 [0.0589714286, 0.6837571429, 0.7253857143], 
 [0.0843, 0.6928333333, 0.7061666667], [0.1132952381, 0.7015, 0.6858571429], 
 [0.1452714286, 0.7097571429, 0.6646285714], [0.1801333333, 0.7176571429, 
  0.6424333333], [0.2178285714, 0.7250428571, 0.6192619048], 
 [0.2586428571, 0.7317142857, 0.5954285714], [0.3021714286, 0.7376047619, 
  0.5711857143], [0.3481666667, 0.7424333333, 0.5472666667], 
 [0.3952571429, 0.7459, 0.5244428571], [0.4420095238, 0.7480809524, 
  0.5033142857], [0.4871238095, 0.7490619048, 0.4839761905], 
 [0.5300285714, 0.7491142857, 0.4661142857], [0.5708571429, 0.7485190476, 
  0.4493904762], [0.609852381, 0.7473142857, 0.4336857143], 
 [0.6473, 0.7456, 0.4188], [0.6834190476, 0.7434761905, 0.4044333333], 
 [0.7184095238, 0.7411333333, 0.3904761905], 
 [0.7524857143, 0.7384, 0.3768142857], [0.7858428571, 0.7355666667, 
  0.3632714286], [0.8185047619, 0.7327333333, 0.3497904762], 
 [0.8506571429, 0.7299, 0.3360285714], [0.8824333333, 0.7274333333, 0.3217], 
 [0.9139333333, 0.7257857143, 0.3062761905], [0.9449571429, 0.7261142857, 
  0.2886428571], [0.9738952381, 0.7313952381, 0.266647619], 
 [0.9937714286, 0.7454571429, 0.240347619], [0.9990428571, 0.7653142857, 
  0.2164142857], [0.9955333333, 0.7860571429, 0.196652381], 
 [0.988, 0.8066, 0.1793666667], [0.9788571429, 0.8271428571, 0.1633142857], 
 [0.9697, 0.8481380952, 0.147452381], [0.9625857143, 0.8705142857, 0.1309], 
 [0.9588714286, 0.8949, 0.1132428571], [0.9598238095, 0.9218333333, 
  0.0948380952], [0.9661, 0.9514428571, 0.0755333333], 
 [0.9763, 0.9831, 0.0538]]

parula_map = LinearSegmentedColormap.from_list('parula', cm_data)
clims = None
def spectrogram(run_dir, run_num, fileno, fft_length, CENTER_FREQ, ax):
	global minFreq, maxFreq
	global shifted_fft, median_fft
	global num_samples
	global parula_map
	global clims
	rawfilename = os.path.join(run_dir, 'RAW_DATA_%06d_%06d' % (run_num, fileno))
	# rawfilename = '/home/ntlhui/fiona/field/radioCollarBackups/2017.08.Caymans/2017.08.20/RUN_000037/RAW_DATA_000037_000001'

	rawfile = open(rawfilename, 'rb')
	statinfo = os.stat(rawfilename)
	filesize = statinfo.st_size
	numCols = math.ceil(filesize / 4 / fft_length)
	num_samples = filesize / 4

	count = 0
	done = False
	fft_buffer_in = np.zeros((int(numCols), fft_length), dtype = np.complex64)
	column = 0
	while not done:
		for i in xrange(fft_length):
			signal_raw = rawfile.read(4)
			if signal_raw == "":
				done = True
				break
			sample_buffer = struct.unpack('hh', signal_raw)
			fft_buffer_in[column][i] = sample_buffer[0] / 4096.0 + sample_buffer[1] / 4096.0 * 1j
			count += 1
		column += 1
		if not done and column % 64 == 0:
			getCallback(count, num_samples + (numCols - 2) * (f_max_idx - f_min_idx))
	fft_buffer_out = np.fft.fft(fft_buffer_in)
	shifted_fft = np.transpose(10 * np.log10(np.abs(np.fft.fftshift(fft_buffer_out, axes=(1,)) / float(fft_length))))

	median_fft = np.zeros((fft_length, int(numCols)), dtype = np.float64)
	median_length = 15

	# Post-fft processing
	for f in xrange(f_min_idx - 20, f_max_idx + 20):
		for t in xrange(int(median_length / 2), len(shifted_fft[0]) - int(median_length / 2)):
			median_fft[f,t] = np.median(shifted_fft[f, t - int(median_length / 2):t+int(median_length / 2)])
			count += 1
		getCallback(count, num_samples + (numCols - median_length + 1) * (f_max_idx - f_min_idx + 40))


	y = [(CENTER_FREQ - 1e6) / 1e6, (CENTER_FREQ + 1e6) / 1e6];
	x = [0, num_samples / 2000000.0]

	clims = [np.mean(shifted_fft), np.max(shifted_fft)]
	ax.clear()
	img = ax.imshow(shifted_fft, extent=[x[0], x[1], y[1], y[0]], aspect='auto', cmap = parula_map, picker=5)
	img.set_clim(clims[0], clims[1])
	ax.set_ylim(maxFreq, minFreq)
	ax.set_title('%d of %d, FFT' % (fileno, num_files))

parser = argparse.ArgumentParser()
parser.add_argument('run_dir')
parser.add_argument('run_num')
parser.add_argument('chn_num')
args = parser.parse_args()

run_num = int(args.run_num)
run_dir = str(args.run_dir)
col_num = int(args.chn_num)

col_db = getMappedCollars.collarDB()
col_freq = float(col_db.freqMap[unicode(col_num)]) / 1e6

minFreq = col_freq - 0.01
maxFreq = col_freq + 0.01
f_min_idx = int((minFreq - (CENTER_FREQ - 1e6) / 1e6) / ((CENTER_FREQ + 1e6) / 1e6 - (CENTER_FREQ - 1e6) / 1e6) * fft_length)
f_max_idx = int((maxFreq - (CENTER_FREQ - 1e6) / 1e6) / ((CENTER_FREQ + 1e6) / 1e6 - (CENTER_FREQ - 1e6) / 1e6) * fft_length)

num_files = len(glob.glob(os.path.join(run_dir, 'RAW_DATA_*')))


csv_file = open(os.path.join(run_dir, 'RUN_%06d_CH_%06d_sel.csv' % (run_num, col_num)), 'w+')

fileno = 10
# run_num = 39
# run_dir = '/home/ntlhui/fiona/field/radioCollarBackups/2017.08.Caymans/2017.08.20/RUN_000039'
spectrogramAxes = fig.gca()
spectrogram(run_dir, run_num, fileno, fft_length, CENTER_FREQ, spectrogramAxes)


lastPickEvent = None
lastKeyEvent = None

def onclick(event):
	global lastPickEvent
	lastPickEvent = event
	if event.mouseevent.button == 1:
		# a = event.artist.get_cursor_data(event.mouseevent) 
		t = event.mouseevent.xdata
		fft_data = event.artist.get_array()
		extent = event.artist.get_extent()
		t_lower_idx = int(len(fft_data[0]) * (t - 0.06 - extent[0]) / extent[1])
		t_upper_idx = int(len(fft_data[0]) * (t + 0.06 - extent[0]) / extent[1])
		f = event.mouseevent.ydata
		f_lower_idx = int((f - 0.0025 - extent[3]) / (extent[2] - extent[3]) * len(fft_data))
		f_upper_idx = int((f + 0.0025 - extent[3]) / (extent[2] - extent[3]) * len(fft_data))

		if t_lower_idx <= 0:
			t_lower_idx = 0
		if t_upper_idx >= len(fft_data[0]):
			t_upper_idx = len(fft_data[0]) - 1
		if f_lower_idx <= 0:
			f_lower_idx = 0
		if f_upper_idx >= len(fft_data):
			f_upper_idx = len(fft_data) - 1

		a = np.max(fft_data.data[f_lower_idx:f_upper_idx, t_lower_idx:t_upper_idx])
		ax = event.artist.axes
		ax.set_xlim(t - 0.06, t + 0.06)
		ax.set_ylim(f + 0.005, f - 0.005)
		event.canvas.draw()

		print('t: %f, f: %f, a: %f' % (t, f, a))

		time = fileOffsetToTime(run_dir, run_num, fileno, t)
		line = getGPS(run_dir, run_num, time)
		coords = getGPSCoord(line)
		localTime = getLocalTime(line)
		csv_file.write('%f,%d,%d,%f,%f\n' % (localTime, coords[0] * 1e7, coords[1] * 1e7, a, 0))
		csv_file.flush()

	else:
		ax = event.artist.axes
		global CENTER_FREQ
		y = [(CENTER_FREQ - 1e6) / 1e6, (CENTER_FREQ + 1e6) / 1e6];
		count = event.artist.get_array().size
		x = [0, count / 2000000.0]
		ax.set_xlim(x[0], x[1])
		spectrogramAxes.set_ylim(maxFreq, minFreq)
		event.canvas.draw()
showMedian = True
def onNext(event):
	global lastKeyEvent
	global spectrogramAxes
	global fileno, num_files
	global run_num
	global run_dir
	global fft_length
	global CENTER_FREQ
	global num_samples
	global shifted_fft, median_fft
	global parula_map
	global showMedian
	lastKeyEvent = event
	raw_files = glob.glob(os.path.join(run_dir, 'RAW_DATA_*'))
	if event.key == 'n':
		if fileno < len(raw_files):
			# print('Next')
			fileno += 1
			spectrogram(run_dir, run_num, fileno, fft_length, CENTER_FREQ, spectrogramAxes)
			spectrogramAxes.set_ylim(maxFreq, minFreq)
			event.canvas.draw()
	elif event.key == 'b':
		if fileno > 1:
			# print('Back')
			fileno -= 1
			spectrogram(run_dir, run_num, fileno, fft_length, CENTER_FREQ, spectrogramAxes)
			spectrogramAxes.set_ylim(maxFreq, minFreq)
			event.canvas.draw()
	elif event.key == 'd':
		exit()
	elif event.key == 'm':
		if showMedian:
			spectrogramAxes.clear()
			y = [(CENTER_FREQ - 1e6) / 1e6, (CENTER_FREQ + 1e6) / 1e6];
			x = [0, num_samples / 2000000.0]
			img = spectrogramAxes.imshow(median_fft, extent=[x[0], x[1], y[1], y[0]], aspect='auto', cmap = parula_map, picker=5)
			img.set_clim(clims[0], clims[1])
			spectrogramAxes.set_ylim(maxFreq, minFreq)
			spectrogramAxes.set_title('%d of %d, Median' % (fileno, num_files))
			showMedian = False
			event.canvas.draw()
		else:
			spectrogramAxes.clear()
			y = [(CENTER_FREQ - 1e6) / 1e6, (CENTER_FREQ + 1e6) / 1e6];
			x = [0, num_samples / 2000000.0]
			img = spectrogramAxes.imshow(shifted_fft, extent=[x[0], x[1], y[1], y[0]], aspect='auto', cmap = parula_map, picker=5)
			img.set_clim(clims[0], clims[1])
			spectrogramAxes.set_ylim(maxFreq, minFreq)
			spectrogramAxes.set_title('%d of %d, FFT' % (fileno, num_files))
			showMedian = True
			event.canvas.draw()



cid = fig.canvas.mpl_connect('pick_event', onclick)
cid2 = fig.canvas.mpl_connect('key_press_event', onNext)
plt.show(block=True)
