
import Tkinter as tk
import os
import PIL



class overlayOutputsDialog(tk.Toplevel):
    tiffBoundsCB=0
    dataBoundsCB=0
    visibleBoundsCB=0
    
    customSizeCB=0
    latLongRatioCB=0
    
    def __init__(self,exportFunc=0,tiffPath="",csvPath="",custBoundingBox=[-1,-1,-1,-1],
                dataBoundingBox=[-1,-1,-1,-1],tiffBounds=[-1,-1,-1,-1],tiffRes=[-1,-1]):
        print("TODO: Build dialog")