import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from getCollars import GET_NUM_COLLARS


from PIL import Image, ImageTk
from glob import glob


#The responsibility of this file is to process and then possibly display
#data, the display may be handled by the gui files instead
import shutil
import fileinput

#import sys
#lib_path = os.path.abspath(os.path.join('..', 'raw_gps_analysis'))
#sys.path.append(lib_path)
#lib_path = os.path.abspath(os.path.join('..', 'collarDisplay'))
#sys.path.append(lib_path)


import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'raw_gps_analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'CLI_GUI'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'collarDisplay'))

from read_meta_file import read_meta_file
from cat_relevant import cat_relevant
from raw_gps_analysis import raw_gps_analysis
from display_data import display_data


import numpy as np
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
import matplotlib.pyplot as plot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class imageDisplayPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    numImages = 0
    imageID = 0
    #enlargeImageButton = 0
    imageCanvas = 0
    VERTICLE_PADDING = 3;
    IMSize = 190, 270
    image_dir =""
    imageList = [];
    buttonList = [];
    numcol=0
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=210,height=HEIGHT,bg='#F0F0F0')

        number = 0

        self.pack(side="top",fill="both",expand=True)
	self.top=tk.Frame(self)
	self.top.pack(side="top")

	self.container = tk.Frame(self,width=600,height=HEIGHT,bg='#F0F0F0')
	self.container.pack(side="top",fill="both",expand=True)
	self.container.grid_rowconfigure(0,weight=1)
	self.container.grid_columnconfigure(0,weight=1)
	
	self.frames = {}

	#for F in (1,2):
	    #frame = f1(container,F)
	    #self.frames[F]=frame
	    #frame.grid(row=0,column=0,sticky="nsew")
        
        #self.imageCanvas = tk.Canvas(self,width=190,height=HEIGHT,bg='#F0F0F0')
        #self.imageCanvas.pack(side='bottom',fill='both',expand=True)
        
    def show_frame(self,curr):

	frame = self.frames[curr]
	frame.tkraise()

    def newImages(self,numImages,imageIN_dir,imageNames):
        #self.imageCanvas.delete("all")
        self.image_dir = imageIN_dir;
    
    #this loop deletes all buttons
        while len(self.buttonList) > 0:
            self.buttonList[0].destroy()
            del self.buttonList[0]
        
        while len(self.imageList) > 0:
            del self.imageList[0]
            
        length = len(self.buttonList)
        print("len ButtonList = %d"%(length))    
            
            
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
            
        self.numImages = numImages    
        if(numImages > 0):
            self.changeImage(0)
            
        print("imageListLength = %d" %(len(self.imageList)))
        
        #if self.numImages >0:
            #self.enlargeImageButton.lift()
        #else:
            #self.enlargeImageButton.lower()
            
            
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
        #self.imageCanvas.create_image(1,1,image=self.image,anchor='nw')
        self.update()
        #self.imageCanvas.pack_forget()
        
        
        i =0
        while i < self.numImages:
            self.buttonList[i].pack(side='left')
            i=i+1
        
        
        return;
        

    def scriptImplementation(self,programPath,data_dir,config_dir,run,flt_alt,num_col,frequencyList=[]):
    
	while len(self.buttonList) > 0:
            self.buttonList[0].destroy()
            del self.buttonList[0]
	self.frames.clear()

        configCOLPath = config_dir + '/COL'
        SDRPath = config_dir + '/SDR.cfg'
	
        num_raw_files = glob(data_dir+'/RAW_DATA_*')
        #num_collars = self.getNumCollars(ConfigCOLPath)
        raw_file = "%s/RUN_%06d.raw" % (data_dir,int(run))
        collar_file_prefix = "%s/RUN_%06d_" % (data_dir,int(run))
        meta_file = "%s/META_%06d" % (data_dir,int(run))
        sdr_center_freq = read_meta_file(meta_file, 'center_freq')
    
        print "SDR path: %s"%(SDRPath)
        
        sdr_ppm = read_meta_file(SDRPath, 'sdr_ppm')
        
        #if os.path.exists(raw_file):
        #   os.remove(raw_file)
        
        cat_relevant(data_dir,int(run)) 
        #UNCOMMENT
        
        curCol = 1
        while curCol <= num_col:
            print("entering calculation pipeline: %d <= %d" % (curCol,num_col))
            if(len(frequencyList) == 0):
                
                frequency = read_meta_file(configCOLPath,str(curCol))
            else:
                frequency = frequencyList[curCol-1]
               #TODO: Nathan: I believe this is the errorCheck on line 117
                #TODO: strengthen this error check
            if frequency == "":
                return
            frequency = int(frequency)
     
    
    
                #TODO: Error checking
            beat_freq = self.getBeatFrequency(int(sdr_center_freq), int(frequency), int(sdr_ppm))
      
      
            GNU_RADIO_PIPELINE = programPath + '/fft_detect/fft_detect'
            collarFile = "%s%06d.raw" % (collar_file_prefix, curCol)
            print("collarFile: %s" %(collarFile))
    
    
            #os.execl(GNU_RADIO_PIPELINE,'fft_detect','-f',str(beat_freq),'-i',str(raw_file),'-o',str(collarFile))
    
            argString = '-f ' + str(beat_freq) + ' -i ' + str(raw_file) + ' -o ' + str(collarFile)
    
            p = subprocess.call(GNU_RADIO_PIPELINE + ' ' + argString, shell=True)
            #UNCOMMENT
                
                #TODO: Error checking
            raw_gps_analysis(data_dir,data_dir,int(run),int(curCol),int(flt_alt))
            curCol = curCol + 1
         


	
        curCol = 1
        while curCol <= num_col:
            data_file = "%s/RUN_%06d_COL_%06d.csv" %(data_dir,int(run), int(curCol))
            display_data(int(run),int(curCol),data_file,data_dir,configCOLPath)
	    

	    #CREATE INTERACTIVE IMAGE PANEL
	    #self.interactiveImage(int(run),int(curCol),data_file,data_dir,configCOLPath)
	    
	    # create class instance
	    frame = interactiveImage(self.container,int(run),int(curCol),data_file,data_dir,configCOLPath)
	    self.frames[curCol]=frame
	    frame.grid(row=0,column=0,sticky="nsew")

	    # create button
	    number = str(curCol)


            newButton = tk.Button(self.top,text=number,command=lambda curCol=curCol:self.show_frame(curCol))
            self.buttonList.append(newButton);
            newButton.pack(side='left')
            self.update()


            #subprocess.call(display_data(int(run),int(curCol),data_file,data_dir,configCOLPath))
            curCol = curCol + 1
               
            
                
                
        #curCol = 1
        #while curCol <= num_collars:  
        #    print("entering display pipeline: %d <= %d" % (curCol,num_collars))
                #TODO: Error Checking
        #    data_file = "%s/RUN_%06d_COL_%06d.csv" % (data_dir,int(run),int(curCol))
                
        #    self.display_data(data_file,data_dir,int(run),curCol,ConfigCOLPath)
               #TODO: error Checking
                
        #    if signal_dist_outpt == 1:
        #        signal_distance_angle(data_file,data_dir,run,curCol,ConfigCOLPath)
        
        
    def getBeatFrequency(self,center_freq,collar_freq,ppm):
        
        actual_center = int(center_freq) / 1.e6 * int(ppm) + int(center_freq)
    
        beat_freq = int(collar_freq) - int(actual_center)
        print('center_freq = %d, collar_freq = %d, ppm= %d, actual_center = %d, beat_freq = %d'%    ( center_freq,collar_freq,ppm,actual_center,beat_freq))
        return(int(beat_freq))

    #def interactiveImage(int(run),int(curCol),data_file,data_dir,configCOLPath)


class interactiveImage(tk.Frame):
    run_num=0
    num_col=0
    filename=0
    output_path=0
    col_def=0
    def __init__(self,parent,r,c,df,dd,cp):
        tk.Frame.__init__(self,parent)

	self.run_num=r
	self.num_col=c
	self.filename=df
	self.output_path=dd
	self.col_def=cp

	self.mid=tk.Canvas(self)
	self.mid.pack(side="top")
	self.bot=tk.Canvas(self)
	self.bot.pack(side="top",fill="both",expand=True)

        # Get collar frequency
        col_freq = float(read_meta_file(self.col_def, str(self.num_col))) / 1.e6

        # make list of columns
        # Expects the csv to have the following columns: time, lat, lon, [collars]
        names = ['time', 'lat', 'lon', 'col']

        # Read CSV
        data = np.genfromtxt(self.filename, delimiter=',', names=names)
        # Modify values
        lat = [x / 1e7 for x in data['lat']]
        lon = [x / 1e7 for x in data['lon']]

        # convert deg to utm
        zone = "X"
        zonenum = 60
        for i in range(len(data['lat'])):
            utm_coord = utm.from_latlon(lat[i], lon[i])
            lon[i] = utm_coord[0]
            lat[i] = utm_coord[1]
            zonenum = utm_coord[2]
            zone = utm_coord[3]
    
        # Configure plot
        fig = plot.figure()
        fig.set_size_inches(8, 6)
        fig.set_dpi(72)
        plot.grid()
        ax = plot.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')
        ax.set_title('Run %d, Collar %d at %3.3f MHz\nUTM Zone: %d %s' % (self.run_num, self.num_col, col_freq, zonenum,     zone))
        ax.set_aspect('equal')
        plot.xticks(rotation='vertical')
    
        # Calculate colorplot
        maxCol = np.amax(data['col'])
        minCol = np.amin(data['col'])
        curColMap = plot.cm.get_cmap('jet')
    
        # Plot data
        sc = plot.scatter(lon, lat, c=data['col'], cmap=curColMap, vmin = minCol, vmax = maxCol)
        colorbar = plot.colorbar(sc)
        colorbar.set_label('Maximum Signal Amplitude')
            	
	self.canvas = FigureCanvasTkAgg(fig, self.bot)
	self.canvas.show()
	self.canvas.get_tk_widget().pack(side="left",fill="both", expand=True)
	#self.update()
	self.toolbar = NavigationToolbar2TkAgg(self.canvas,self.mid)
	self.toolbar.update()
	self.canvas._tkcanvas.pack(side="left",fill="both", expand=True)
	#self.update()
