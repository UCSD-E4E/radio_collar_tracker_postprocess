#!/usr/bin/env python
from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time

api = local_connect()
v = api.get_vehicles()[0]

current_milli_time = lambda: int(round(time.time() * 1000))

logfile = open("gps.log", "w")

while True:
	if v.location.lat is not None and v.location.lon is not None:
		logfile.write("%.3f, %f, %f\n" % (current_milli_time() / 1000.0, float(v.location.lat), float(v.location.lon)))
	time.sleep(0.5)

