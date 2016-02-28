import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))
from read_meta_file import read_meta_file
from getCollars import GET_NUM_COLLARS


from PIL import Image, ImageTk
from glob import glob

class imageDisplayPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    numImages = 0
    imageID = 0
    enlargeImageFunction = 0
    enlargeImageButton = 0
    imageCanvas = 0
    VERTICLE_PADDING = 3;
    IMSize = 190, 270
    image_dir =""
    imageList = [];
    buttonList = [];
    def __init__(self,parent,HEIGHT,enlargeFunc):
        self.enlargeImageFunction = enlargeFunc
        tk.Frame.__init__(self,parent,width=210,height=HEIGHT,bg='#F0F0F0')
        #self.config(bg='blue')
        #self.pack_propagate('false')
        #self.imageList.append("LING");
        number = 0
        #newButton = tk.Button(self,text=number,command=lambda:self.changeImage(0))
        #self.buttonList.append(newButton);
        self.enlargeImageButton = tk.Button(self,text='Enlarge Image',command=self.enlargeImage)
        self.enlargeImageButton.pack(side='bottom')
        self.enlargeImageButton.lower()
        
        self.imageCanvas = tk.Canvas(self,width=190,height=HEIGHT-40,bg='#F0F0F0')
        self.imageCanvas.pack(side='bottom',padx=10)
        
    def newImages(self,numImages,imageIN_dir,imageNames):
        self.imageCanvas.delete("all")
        self.image_dir = imageIN_dir;
        length = len(self.buttonList)
        print("len ButtonList = %d"%(length))
    
    #this loop deletes all buttons
        while len(self.buttonList) > 0:
            self.buttonList[0].destroy()
            del self.buttonList[0]
        
        while len(self.imageList) > 0:
            del self.imageList[0]
            
            
            
            
        i = 0
        buttonOffset = 0;
        #buttonWidth = 25 / numImages; #Width / numImages
        while i < numImages:
            number = str(i)
            print("I is: %d, number is: %s" %(i,number))
            newButton = tk.Button(self,text=number,command=lambda i=i:self.changeImage(i))
            self.buttonList.append(newButton);
            newButton.pack(side='left')
            print("Made it here")
            self.update()
            print("But not here")
            buttonOffset+=newButton.winfo_height();
            
            self.imageList.append(imageNames[i])
            i = i+1;
            
        if(numImages > 0):
            self.changeImage(0)
            
        self.numImages = numImages
        
        
        if self.numImages >0:
            self.enlargeImageButton.lift()
        else:
            self.enlargeImageButton.lower()
            
            
    def changeImage(self,number):
        self.imageID = number
        imagePath = "%s%s" %(self.image_dir,self.imageList[number])
        print("Number is %d" %(number))
        print("image_dir is :%s" %(self.image_dir))
        print("Image path is: %s" %(imagePath))
        image = Image.open(imagePath)
        image = image.resize(self.IMSize, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        #try:
        self.image = photo
        self.imageCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.update()
        #self.imageCanvas.pack_forget()
        
        
        i =0
        while i < self.numImages:
            self.buttonList[i].pack(side='left')
            i=i+1
        
        
        
        #self.enlargeImageButton.pack(side='bottom')
        #self.imageCanvas.pack(side='bottom',padx=10)
        #self.imageCanvas.place(anchor='nw',y=30,x=260)
        #self.image = tk.PhotoImage(file=imagePath)
        #self.imageLabel.configure(image=self.image)
        #self.imageLabel.place(anchor='nw',y=30,x=260)
        #except tk.TclError:
        #    print("Caught TCLERROR")
        return;
        
        
    def enlargeImage(self):
        self.enlargeImageFunction(self.imageID)