#!/usr/bin/env python
import numpy as np
import utm
import math
import shapefile

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
	output_path = '.'
	iguanaNum = int(raw_input('Iguana Number: '))
	print("Enter lat lon (x.xxxx,y.yyyy), done when done")
	latlonstr1 = raw_input('Point 1: ')
	bearing1 = float(raw_input('Bearing: '))
	if latlonstr1.lower() == 'done':
		return
	latlonstr2 = raw_input('Point 2: ')
	bearing2 = float(raw_input('Bearing: '))
	if latlonstr2.lower() == 'done':
		return
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
		print('%.6f, %.6f' % (coord[0], coord[1]))
		rpt = open('%s/CH_%06d.rpt' % (output_path, iguanaNum), 'w+')
		rpt.write('Iguana %d\n' % iguanaNum)
		rpt.write('\t%.6f, %.6f\n' % (coord[0], coord[1]))
		rpt.write('\tUnknown Error - 2 measurements\n')
		est_time = raw_input('Time: ')
		rpt.write('\t%s Local\n' % est_time)
		rpt.close()
	else:
		bearing3 = float(raw_input('Bearing: '))
		utm3 = strToGPS(latlonstr3)
		m1 = 1 / np.tan(math.radians(bearing1))
		m2 = 1 / np.tan(math.radians(bearing2))
		m3 = 1 / np.tan(math.radians(bearing3))
		b1 = utm1[1] - m1 * utm1[0]
		b2 = utm2[1] - m2 * utm2[0]
		b3 = utm3[1] - m3 * utm3[0]
		a = np.array([[1, -1 * m1],[1, -1 * m2], [1, -1 * m3]])
		b = np.array([b1, b2, b3])
		x = np.linalg.lstsq(a, b)
		coord = utm.to_latlon(x[0][1], x[0][0], utm1[2], utm1[3])

		a = np.array([[1, -m1],[1,-m2]])
		b = np.array([b1, b2])
		x12 = np.linalg.solve(a, b)
		a = np.array([[1, -m1], [1, -m3]])
		b = np.array([b1, b3])
		x13 = np.linalg.solve(a, b)
		a = np.array([[1, -m2], [1, -m3]])
		b = np.array([b2, b3])
		x23 = np.linalg.solve(a, b)
		err1 = baseline_distance(x[0], x12)
		err2 = baseline_distance(x[0], x13)
		err3 = baseline_distance(x[0], x23)
		maxErr = max([err1, err2, err3])
		print('%.6f, %.6f +/- %d m' % (coord[0], coord[1], math.ceil(maxErr)))

		rpt = open('%s/CH_%06d.rpt' % (output_path, iguanaNum), 'w+')
		rpt.write('Iguana %d\n' % iguanaNum)
		rpt.write('\t%.6f, %.6f\n' % (coord[1], coord[0]))
		rpt.write('\t+/- %d m\n' % math.ceil(maxErr))
		est_time = raw_input('Time: ')
		rpt.write('\t%s Local\n' % est_time)
		rpt.write('\tTriangulation\n')
		rpt.close()

	w = shapefile.Writer(shapefile.POINT)
	w.autoBalance = 1
	w.field("channel", 'N')

	w.point(coord[1], coord[0])
	w.record(iguanaNum)
	w.save('%s/CH_%06d_est.shp' % (output_path, iguanaNum))

	prj = open('%s/CH_%06d_est.prj' % (output_path, iguanaNum), "w")
	epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
	prj.write(epsg)
	prj.close()


if __name__ == '__main__':
	main()
