import os
import shapefile
import numpy as np

from StringIO import StringIO



def create_shapefile(self=None,file="",outfile=""):
    
    if(file == "" or not os.path.isfile(file)):
        print("File was not valid: %s"%(file))
    if(outfile==""):
        rindex = file.rfind(".")
        outdir=file[0:rindex].replace("\\","/")
        rindex= outdir.rfind("/")
        outname = outdir[rindex+1:]
        outdir = outdir
        outfile = outdir + "/" + outname
        if(not os.path.isdir(outdir)):
            os.mkdir(outdir)
        
    names = ['time', 'lat', 'lon', 'col']

    # Read CSV
    data = np.genfromtxt(file, delimiter=',', names=names)
    # Modify values
    lat = [x / 1e7 for x in data['lat']]
    lon = [x / 1e7 for x in data['lon']]
    col = data['col']
    print(col)
    
    
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    
    length = len(lat)
    i=0
    while i < length:
        #Latitude, longitude, elevation, measurement
        w.point(lat[i],lon[i],0,col[i])
        i=i+1
    w.save(outfile)
    
    
if __name__ == "__main__":
    file = "C:\Users\Work\Documents\Files\Projects\RadioCollar\SampleData\RCT_SAMPLE\RUN_002027\RUN_002027_COL_000001.csv"
    outfile = ""#"C:\Users\Work\Documents\Files\Projects\RadioCollar\SampleData\RCT_SAMPLE\RUN_002027\RUN_002027_COL_000001"
    create_shapefile(file=file,outfile=outfile)
    