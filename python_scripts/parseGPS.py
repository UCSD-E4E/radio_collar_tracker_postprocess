def parseGPS(gps_file):
  with open(gps_file) as file:
    for line in file:
      time,lat,lon,alt,ninety = []
      s = line.split(',')
      time.append(s[0])
      lat.append(s[1])
      lon.append(s[2])
      alt.append(s[3])
      ninety.append(s[4])
    keys = ['time','lat','lon','alt','ninety']
  return dict( zip( keys, s[:5] ) )
