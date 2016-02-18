import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog


from META_FILE_READER import META_FILE_READER
from getNumCols import GET_NUM_COLLARS
import os

from glob import glob

class imageDisplayPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    imageLabel = 0
    VERTICLE_PADDING = 3;
    image_dir =""
    imageList = [];
    buttonList = [];
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=250,height=HEIGHT,bg='beige')
        #self.config(bg='blue')
        self.imageList.append("LING");
        number = 0
        newButton = tk.Button(self,text=number,command=lambda:self.changeImage(0))
        self.buttonList.append(newButton);
        self.imageLabel = tk.Label(justify='left')
        self.imageLabel.pack()
        self.imageLabel.place(anchor='nw',y=5)
        
    def newImages(self,numImages,imageIN_dir,imageNames):
        self.imageLabel.configure(image="")
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
        buttonWidth = 25 / numImages; #Width / numImages
        while i < numImages:
            number = str(i)
            print("I is: %d, number is: %s" %(i,number))
            newButton = tk.Button(self,text=number,command=lambda i=i:self.changeImage(i))
            self.buttonList.append(newButton);
            newButton.pack()
            newButton.place(anchor='nw',x=buttonOffset + 20);
            self.update()
            buttonOffset+=newButton.winfo_height();
            
            self.imageList.append(imageNames[i])
            i = i+1;
            
    
    def changeImage(self,number):
        imagePath = "%s%s" %(self.image_dir,self.imageList[number])
        print("Number is %d" %(number))
        print("image_dir is :%s" %(self.image_dir))
        print("Image path is: %s" %(imagePath))
        #image = Image.open(imagePath)
        #photo = ImageTk.PhotoImage(image)
        self.image = tk.PhotoImage(file=imagePath)
        self.imageLabel.configure(image=self.image)
        self.imageLabel.place(anchor='nw',y=30,x=260)
        return;