#!/usr/bin/env python
import numpy as np
import utm
import math

def strToGPS(line):
	lat = float(line.split(',')[0].strip())
	lon = float(line.split(',')[1].strip())
	return utm.from_latlon(lat, lon)

def baseline_distance(utm1, utm2):
	return np.sqrt((utm1[0] - utm2[0]) ** 2 + (utm1[1] - utm2[1]) ** 2)

def baseline_bearing(utm1, utm2):
	dy = utm2[1] - utm1[1]
	dx = utm2[0] - utm1[0]
	return 90 - np.degrees(math.atan2(dy, dx))

def bearing_complement(bearing):
	retval = bearing - 180
	if retval <= 0:
		retval = bearing + 180
	return retval

def main():
	pass


if __name__ == '__main__':
	main()
print("Enter lat lon, done when done")
latlonstr1 = raw_input('Point 1: ')
bearing1 = float(raw_input('Bearing: '))
if latlonstr1.lower() == 'done':
	exit()
latlonstr2 = raw_input('Point 2: ')
bearing2 = float(raw_input('Bearing: '))
if latlonstr2.lower() == 'done':
	exit()
latlonstr3 = raw_input('Point 3: ')
utm1 = strToGPS(latlonstr1)
utm2 = strToGPS(latlonstr2)
if latlonstr3.lower() == 'done':
	# baseline_dist = baseline_distance(utm1, utm2)
	# baseline_brng = baseline_bearing(utm1, utm2)
	# alpha = baseline_brng - bearing1
	# beta = bearing_complement(baseline_brng) - bearing2
	# d = baseline_dist * (math.sin(math.radians(alpha)) * math.sin(math.radians(beta))) / (math.sin(math.radians(alpha + beta)))
	m1 = 1 / np.tan(math.radians(bearing1))
	m2 = 1 / np.tan(math.radians(bearing2))
	b1 = utm1[1] - m1 * utm1[0]
	b2 = utm2[1] - m2 * utm2[0]
	a = np.array([[1, -1 * m1],[1, -1 * m2]])
	b = np.array([b1, b2])
	x = np.linalg.solve(a, b)
	coord = utm.to_latlon(x[1], x[0], utm1[2], utm1[3])
	print(coord)
else:
	bearing3 = float(raw_input('Bearing:'))
	utm3 = strToGPS(latlonstr3)

