import Tkinter as tk

import sys
import os

from PIL import Image, ImageTk
from glob import glob


class interactiveImage(tk.Canvas):
    imageFrame = 0
    IMSize = 190, 270

    def __init__(self,parent):
        tk.Canvas.__init__(self,parent,width=210,bg='#F0F0F0')
        
        
        
    def changeImage(self,imagePath):
        self.image = Image.open(imagePath)
        self.image = self.image.resize(self.IMSize, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        #try:
        self.create_image(1,1,image=self.image,anchor='nw')
        self.update()
        #self.imageCanvas.pack_forget(