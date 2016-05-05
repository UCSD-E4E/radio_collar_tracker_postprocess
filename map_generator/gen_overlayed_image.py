import gdal
import os
from gdalconst import *

from osgeo import ogr

import mapnik
from mapnik import Raster, Layer




def generateMapImage(tiffPath="",csvPath="",outImage="",mapWidth=600,mapHeight=600,PV_BUFFER_CONST=.1,PH_BUFFER_CONST=.1):

    #tiffPath           Absolute path to tiff file
    #csv path           Absolute path to csv
    #outImage           Absolute path to desired out image (Will overwrite)
    #outSHPDir          Output directory to hold SHP files (PLANNED)
    #mapWidth / height  Dimensions of rendered map
    #PV_BUFFER_CONST    Amount of verticle buffer space over collected point cloud
    #PH_BUFFER_CONST    Amount of horizontal buffer space over collected point cloud
    
    boundingBox =[0,0,0,0] #Give bound box a value in case neither csv, nor tiff are valid
    #create map
    map = mapnik.Map(mapWidth,mapHeight)
    map.background = mapnik.Color('#F0F0F0')
    
    if(os.path.isfile(tiffPath)):
        dataset = gdal.Open(tiffPath, GA_ReadOnly)
        if dataset is None:
            print 'Could not open file'
        else:
            print("Image loaded")
        
            #Get details of image
            cols = dataset.RasterXSize
            rows = dataset.RasterYSize
            bands = dataset.RasterCount
            transform = dataset.GetGeoTransform()
            #print("cols=[%d],rows=[%d],bands=[%d]"%(cols,rows,bands))
            
            #Manually get bounds of tiff file
            leftEdge = transform[0]
            pixelWidth = transform[1]
            topEdge = transform[3]
            pixelHeight = transform[5]
            rightEdge = leftEdge + pixelWidth* cols
            bottomEdge = topEdge + rows* pixelHeight
            Tiffbounds = [leftEdge,topEdge,rightEdge,bottomEdge]
            #print(Tiffbounds)

            #Create style for raster layer
            rasterStyle = mapnik.Style() 
            rasterRule = mapnik.Rule() 
            rasterSymbolizer = mapnik.RasterSymbolizer()
            rasterRule.symbols.append(rasterSymbolizer)
            rasterStyle.rules.append(rasterRule)
            map.append_style('Tiff Style', rasterStyle)
            
            #create and add layer to map
            #Bounds are needed, hence why they are pre-calculated
            tiffRaster = Raster(file=tiffPath,lox=leftEdge,loy=bottomEdge,hix=rightEdge,hiy=topEdge)
            tifflayer = Layer('Tiff Layer')
            tifflayer.datasource = tiffRaster
            tifflayer.styles.append('Tiff Style')
            
            map.layers.append(tifflayer)
            boundingBox = [leftEdge,topEdge,rightEdge,bottomEdge]

    if(os.path.isfile(csvPath)):
        #NOTE: Requires csv to have line 1 be "time,latitude,longitude,value"
        #Lat/Long must also be divided properly
        
        
        #Create style for point layer
        pointSymbolizer = mapnik.PointSymbolizer()
        pointRule = mapnik.Rule()
        pointRule.symbols.append(pointSymbolizer)
        pointStyle = mapnik.Style()
        pointStyle.rules.append(pointRule)
        map.append_style('Point Style',pointStyle)


        #Create point layer
        pointDataSource = mapnik.Datasource(type='csv',file=csvPath)
        pointLayer = mapnik.Layer('point layer')
        pointLayer.datasource = pointDataSource
        pointLayer.styles.append('Point Style')
        map.layers.append(pointLayer)

        #Gets point set transform
        pointTransform = pointLayer.envelope()
        pointsLeftEdge = pointTransform[0]
        pointsTopEdge = pointTransform[1]
        pointsRightEdge = pointTransform[2]
        pointsBottomEdge = pointTransform[3]
        #pointsPixelWidth = pointTransform[1]


        pointsVerticleBuffer = PV_BUFFER_CONST * (pointsTopEdge - pointsBottomEdge)
        pointsHorizontalBuffer = PH_BUFFER_CONST * (pointsRightEdge - pointsLeftEdge)

        pointsLeftEdgeBuffered = pointsLeftEdge - pointsHorizontalBuffer
        pointsRightEdgeBuffered = pointsRightEdge + pointsHorizontalBuffer
        pointsTopEdgeBuffered = pointsTopEdge + pointsVerticleBuffer
        pointsBottomEdgeBuffered = pointsBottomEdge - pointsVerticleBuffer

        #bufferedBounds = [leftEdgeBuffered,bottomEdgeBuffered,rightEdgeBuffered,topEdgeBuffered]
        #print(bufferedBounds)

        #print(pointsBufferedBounds)
        #NOTE: This will overwrite bounding box of tiff, this is intended
        boundingBox = [pointsLeftEdgeBuffered,pointsTopEdgeBuffered,pointsRightEdgeBuffered,pointsBottomEdgeBuffered]
    
    zoomBoundBox = mapnik.Box2d(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3])
    map.zoom_to_box(zoomBoundBox)
    
    if(outImage != ""):
        #TODO error checking
        outImage = outImage.replace("\\","/")
        print(outImage)
        mapnik.render_to_file(map,str(outImage), 'png')

    return boundingBox

if __name__ == "__main__":
    csvPath = os.path.dirname(os.path.realpath(__file__)) + '/run2070Edited.csv'
    tiffPath = os.path.dirname(os.path.realpath(__file__)) + '/run2070.tif'
    outImage = os.path.dirname(os.path.realpath(__file__)) + "/pointsOverlayed.png"
    
    
    generateMapImage(tiffPath=tiffPath,csvPath=csvPath,outImage=outImage)
