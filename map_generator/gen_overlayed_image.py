import gdal
import os
from gdalconst import *


import mapnik
from mapnik import Raster, Layer
import numpy as np




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
            x=1
            #print("Image loaded")
        
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
        
        #This section calculates the cutoffs for each image png
        array = np.genfromtxt(csvPath,delimiter=',',names=True)
        minVal = np.amin(array['value'])
        maxVal = np.amax(array['value'])
        cutOffResolution = (maxVal-minVal)/10
        cutoff0 = minVal
        cutoff1 = minVal + cutOffResolution
        cutoff2 = minVal + cutOffResolution *2
        cutoff3 = minVal + cutOffResolution *3
        cutoff4 = minVal + cutOffResolution *4
        cutoff5 = minVal + cutOffResolution *5
        cutoff6 = minVal + cutOffResolution *6
        cutoff7 = minVal + cutOffResolution *7
        cutoff8 = minVal + cutOffResolution *8
        cutoff9 = minVal + cutOffResolution *9
        cutoff10 = maxVal
        
        
        #Create style for each point color layer
        detection1 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector1.png"))
        detection2 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector2.png"))
        detection3 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector3.png"))
        detection4 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector4.png"))
        detection5 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector5.png"))
        detection6 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector6.png"))
        detection7 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector7.png"))
        detection8 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector8.png"))
        detection9 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector9.png"))
        detection10 = mapnik.PointSymbolizer(mapnik.PathExpression("pointImages/detector10.png"))
        
        pointFilter1 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff0,cutoff1))
        pointFilter2 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff1,cutoff2))
        pointFilter3 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff2,cutoff3))
        pointFilter4 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff3,cutoff4))
        pointFilter5 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff4,cutoff5))
        pointFilter6 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff5,cutoff6))
        pointFilter7 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff6,cutoff7))
        pointFilter8 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff7,cutoff8))
        pointFilter9 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff8,cutoff9))
        pointFilter10 = mapnik.Filter("[value] > %f and [value] < %f"%(cutoff9,cutoff10))
        
        pointRule1 = mapnik.Rule()
        pointRule2 = mapnik.Rule()
        pointRule3 = mapnik.Rule()
        pointRule4 = mapnik.Rule()
        pointRule5 = mapnik.Rule()
        pointRule6 = mapnik.Rule()
        pointRule7 = mapnik.Rule()
        pointRule8 = mapnik.Rule()
        pointRule9 = mapnik.Rule()
        pointRule10 = mapnik.Rule()
        
        pointRule1.symbols.append(detection1)
        pointRule2.symbols.append(detection2)
        pointRule3.symbols.append(detection3)
        pointRule4.symbols.append(detection4)
        pointRule5.symbols.append(detection5)
        pointRule6.symbols.append(detection6)
        pointRule7.symbols.append(detection7)
        pointRule8.symbols.append(detection8)
        pointRule9.symbols.append(detection9)
        pointRule10.symbols.append(detection10)
        
        pointRule1.filter = pointFilter1
        pointRule2.filter = pointFilter2
        pointRule3.filter = pointFilter3
        pointRule4.filter = pointFilter4
        pointRule5.filter = pointFilter5
        pointRule6.filter = pointFilter6
        pointRule7.filter = pointFilter7
        pointRule8.filter = pointFilter8
        pointRule9.filter = pointFilter9
        pointRule10.filter = pointFilter10
        
        
        
        
        
        #pointRule = mapnik.Rule()
        #pointRule.symbols.append(pointSymbolizer)
        pointStyle = mapnik.Style()
        pointStyle.rules.append(pointRule1)
        pointStyle.rules.append(pointRule2)
        pointStyle.rules.append(pointRule3)
        pointStyle.rules.append(pointRule4)
        pointStyle.rules.append(pointRule5)
        pointStyle.rules.append(pointRule6)
        pointStyle.rules.append(pointRule7)
        pointStyle.rules.append(pointRule8)
        pointStyle.rules.append(pointRule9)
        pointStyle.rules.append(pointRule10)
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
        #print(outImage)
        mapnik.render_to_file(map,str(outImage), 'png')

    return boundingBox

if __name__ == "__main__":
    csvPath = os.path.dirname(os.path.realpath(__file__)) + '/run2070Edited.csv'
    tiffPath = os.path.dirname(os.path.realpath(__file__)) + '/run2070.tif'
    outImage = os.path.dirname(os.path.realpath(__file__)) + "/pointsOverlayed.png"
    
    
    generateMapImage(tiffPath=tiffPath,csvPath=csvPath,outImage=outImage)
