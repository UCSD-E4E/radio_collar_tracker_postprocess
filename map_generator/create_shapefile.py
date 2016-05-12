import os
import shapefile
import numpy as np
import zipfile

from StringIO import StringIO



def create_shapefile(self=None,file="",outdir="",outname=""):
    file = file.replace("\\","/")
    outdir=outdir.replace("\\","/")
    
    if(file == "" or not os.path.isfile(file)):
        print("File was not valid: %s"%(file))
        return
        
    if(outdir==""):
        if(outname==""):
            rindex = file.rfind(".")
            rindex= outdir.rfind("/")
            outname = outdir[rindex+1:]
            outdir = outdir
            outfile = outdir + "/" + outname
            if(not os.path.isdir(outdir)):
                os.mkdir(outdir)
        else:
            rindex = file.rfind("/")
            outdir = file[0:rindex] + "/" + outname
            outfile = outdir + "/" + outname
            if(not os.path.isdir(outdir)):
                os.mkdir(outdir)
    else:
        if(not os.path.isdir(outdir)):
            os.mkdir(outdir)
            
        if(outname==""):
            rindex= outdir.rfind("/")
            outname = outdir[rindex+1:]
            outdir = outdir
            outfile = outdir + "/" + outname
        else:
            outfile = outdir + "/" + outname
            
    print(file)
    print(outdir)
    print(outname)
    print(outfile)
        

    # Read CSV
    data = np.genfromtxt(file, delimiter=',', names=True)
    # Modify values
    lat = data['latitude']
    lon = data['longitude']
    col = data['value']
    #print(col)
    
    
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1
    w.field("lat","F",11,18)
    w.field("long","F",11,18)
    w.field("altitude","F",18,18)
    w.field("measurement","F",18,18)
    
    length = len(lat)
    i=0
    print(length)
    while i < length:
        #Latitude, longitude, elevation, measurement
        w.point(lon[i],lat[i])
        w.record(lon[i],lat[i],0,col[i])
        i=i+1
        
    #w.record('First','Point')
     
    w.save(outfile)
    
    
if __name__ == "__main__":
    csvPath = os.path.dirname(os.path.realpath(__file__)) + '/run2070Edited.csv'
    outdir = os.path.dirname(os.path.realpath(__file__)) + '/run2070DataLol'
    create_shapefile(file=csvPath,outdir=outdir,outname="WatchmeNeyNey")#,outdir=outfile,outname="run2070Data")
    