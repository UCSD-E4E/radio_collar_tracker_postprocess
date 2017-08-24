#!/usr/bin/env python

from pymavlink import mavutil
import datetime
import pytz
def leap(date):
	"""
	Return the number of leap seconds since 6/Jan/1980
	:param date: datetime instance
	:return: leap seconds for the date (int)
	"""
	if date < datetime.datetime(1981, 6, 30, 23, 59, 59):
		return 0
	leap_list = [(1981, 6, 30), (1982, 6, 30), (1983, 6, 30),
				 (1985, 6, 30), (1987, 12, 31), (1989, 12, 31),
				 (1990, 12, 31), (1992, 6, 30), (1993, 6, 30),
				 (1994, 6, 30), (1995, 12, 31), (1997, 6, 30),
				 (1998, 12, 31), (2005, 12, 31), (2008, 12, 31),
				 (2012, 6, 30), (2015, 6, 30), (2016, 12, 31)]
	leap_dates = map(lambda x: datetime.datetime(x[0], x[1], x[2], 23, 59, 59),
					 leap_list)
	for j in xrange(len(leap_dates[:-1])):
		if leap_dates[j] < date < leap_dates[j + 1]:
			return j + 1
	return len(leap_dates)

binFilename = '/home/ntlhui/workspace/2017.08.CI_Deployment/2017.08.23/flight_logs/141.BIN'
gpsFilename = '/home/ntlhui/workspace/2017.08.CI_Deployment/2017.08.23/RUN_000077/GPS_000077'
newGPSFilename = '/home/ntlhui/workspace/2017.08.CI_Deployment/2017.08.23/RUN_000077/GPS_000077.new'

gps_file = open(gpsFilename, 'r')
local_gps_start = float(gps_file.readline().split(',')[0])
global_gps_start = float(gps_file.readline().split(',')[3])
mavmaster = mavutil.mavlink_connection(binFilename)
epoch = datetime.datetime.utcfromtimestamp(0)

newGPSFile = open(newGPSFilename, 'w+')
while True:
	msg = mavmaster.recv_match(blocking = False)
	if msg is None:
		break
	if msg.get_type() == 'GPS':
		lat = int(msg.to_dict()['Lat'] * 1e7)
		lon = int(msg.to_dict()['Lng'] * 1e7)
		gps_time = int(msg.to_dict()['TimeMS'])
		gps_week = int(msg.to_dict()['Week'])
		gps_epoch = datetime.datetime(1980, 1, 6, 0, 0, 0)
		date_before_leaps = (gps_epoch + datetime.timedelta(seconds = gps_week * 604800 + (gps_time) / 1e3))
		rawdate = (date_before_leaps - datetime.timedelta(seconds = leap(date_before_leaps)))
		gps_timestamp = (rawdate - epoch).total_seconds()
		offset = gps_timestamp - global_gps_start
		local_timestamp = offset + local_gps_start
		newGPSFile.write('%f, %d, %d, %f, 0, -1, 0, 0, -1, 999\n'% (local_timestamp, lat, lon, gps_timestamp))

newGPSFile.close()