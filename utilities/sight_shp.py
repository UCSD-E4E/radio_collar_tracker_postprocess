#!/usr/bin/env python
import math
import shapefile

output_path = '.'

iguanaNum = int(raw_input("Iguana Number: "))
print("Enter lat lon (x.xxxx,y.yyyy)")
latlonstr1 = raw_input('Point: ')
lat = float(latlonstr1.split(',')[0].strip())
lon = float(latlonstr1.split(',')[1].strip())
maxErr = float(raw_input('GPS Error (m): '))

w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field("channel", 'N')

w.point(lon, lat)
w.record(iguanaNum)
w.save('%s/CH_%06d_est.shp' % (output_path, iguanaNum))

prj = open('%s/CH_%06d_est.prj' % (output_path, iguanaNum), "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()
rpt = open('%s/CH_%06d.rpt' % (output_path, iguanaNum), 'w+')
rpt.write('Iguana %d\n' % iguanaNum)
rpt.write('\t%.6f, %.6f\n' % (lon, lat))
rpt.write('\t+/- %d m\n' % (maxErr))
est_time = raw_input('Time: ')
rpt.write('\t%s Local\n' % est_time)
rpt.write('\tSight Tracking\n')
rpt.close()
