#!/usr/local/bin/python


#running on python 3.5.1

import os

import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import shutil

import fileinput

import glob

#for raw_gps_analysis
import math
import cmath
import struct

#for display_data
import sys
import numpy as np
import matplotlib.pyplot as plot
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
#import os
#import fileinput

#for signal_distance_angle
#import sys
#import numpy as np
#import matplotlib.pyplot as plot
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
#import utm
#import os
#import fileinput
#import math

class Application(tk.Frame):


    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.SDOBool = tk.IntVar()
        self.recordBool = tk.IntVar()
        self.cleanBool = tk.IntVar() 

        self.createConfigButtons()
        self.createActionButtons()
        
    def beginCalculations(self):
        run = 0
        flt_alt = 0
        
        CONFIGPath = os.path.dirname(os.path.realpath(__file__))
        CONFIGPath = CONFIGPath.replace("\\","/")
        lastIndex = CONFIGPath.rindex('/')
        CONFIGPath = CONFIGPath[0:lastIndex]
        programPath = CONFIGPath
        CONFIGPath = CONFIGPath + '/config'
        print(CONFIGPath)
    
    
    
        signal_dist_outpt = self.SDOBool.get()
        record = self.recordBool.get()
        clean_run = self.cleanBool.get()
        print('Do the maths here')
        print('signal_dist_outpt= ')
        print(signal_dist_outpt)
        print('record= ')
        print(record)
        print('clean_run=')
        print(clean_run)
        
        data_dir = "C:/Users/Work/Documents/Files/Projects/RadioCollar/SampleData/RCT_SAMPLE/RUN_002027"
        #data_dir = self.runFileChooser()
        print("data_dir = ")
        print(data_dir)
        if data_dir == "":
            print("Directory not found, quitting calculations")
            return 1
        
        RUNPath = data_dir + '/RUN'
        ALTPath = data_dir + '/ALT'
        COLPath = data_dir + '/COL'
        
        if clean_run == 1:
            self.cleanRunProtocol(data_dir)
            return 0
            
        if os.path.exists(RUNPath):
            run = self.META_FILE_READER(RUNPath, 'run_num')
        else:
            run = self.RUN_NUM_CHOOSER()
        
        if run == "":
            print("run not found, quitting calculations")
            return 1
            
        if os.path.exists(ALTPath):
            flt_alt =  self.META_FILE_READER(ALTPath, 'flt_alt')
        else:
            flt_alt = self.getFLTALT()
            if flt_alt == "":
                print("alt not found, quitting calculations")
                return 1;
                
        
        if record == 1:
            with open(ALTPath,'a') as altFile:
                altFile.write("flt_alt: "+str(flt_alt))
            print("flt alt:")
            print(flt_alt)
            
        ConfigCOLPath = CONFIGPath + '/COL' 
        if os.path.exists(COLPath):
            shutil.copyfile(COLPath,ConfigCOLPath)
        else: #manually collect collar frequencies and write to configDir/Col file
            collarList = self.getCollars();
            if len(collarList) == 0:
                print("No valid collar frequencies detected, quitting")
                return 0

            with open(ConfigCOLPath,'a') as concolFile:
                while len(collarList) > 0:
                    concolFile.write(collarList[0])
                    del collarList[0]
          
        if record == 1:
            shutil.copyfile(ConfigCOLPath,COLPath)
            #TODO cp ${CONFIG_DIR}/COL ${data_dir}/COL
        #This begins line 93 of cas2.sh
        num_raw_files = glob.glob(data_dir+'/RAW_DATA_*')
        num_collars = self.getNumCollars(ConfigCOLPath)
        raw_file = "%s/RUN_%06d" % (data_dir,int(run))
        collar_file_prefix = "%s/RUN_%06d_" % (data_dir,int(run))
        meta_file = "%s/META_%06d" % (data_dir,int(run))
        sdr_center_freq = self.META_FILE_READER(meta_file, 'center_freq')
        sdr_ppm = 5 #arbitrary made up, need to ask Nathan
        #TODO: Nathan: need example configdir, I placed a COL file, need SDR.cfg file
        #sdr_ppm =self.META_FILE_READER(CONFIGPath + '/SDR.cfg', 'sdr_ppm')
        
        #TODO: line 106, add functionality
        if os.path.exists(raw_file):
            os.remove(raw_file)
        
        print("Made it to before cat relevent")
        self.cat_relevent(data_dir,int(run))
        print("Made it to after cat relevent")
        #TODO: Error checking
        curCol = 1
        while curCol <= num_collars:
            print("entering calculation pipeline: %d <= %d" % (curCol,num_collars))
            frequency = self.META_FILE_READER(ConfigCOLPath,str(curCol))
            #TODO: Nathan: I believe this is the errorCheck on line 117
            #TODO: strengthen this error check
            if frequency == "":
                return
               
               
            #TODO: Error checking
            beat_freq = self.getBeatFrequency(int(sdr_center_freq), int(frequency), int(sdr_ppm))
            
            GNU_RADIO_PIPELINE = programPath + '/fft_detect/fft_detect'
            collarFile = "%s%06d.raw" % (collar_file_prefix, curCol)
            os.execl(GNU_RADIO_PIPELINE,str(beat_freq),str(raw_file),str(collarFile))
            
            #TODO: Error checking
            self.raw_gps_analysis(data_dir,data_dir,int(run),int(curCol),int(flt_alt))

            curCol = curCol + 1
            
            
        curCol = 1
        while curCol <= num_collars:  
            print("entering display pipeline: %d <= %d" % (curCol,num_collars))
            #TODO: Error Checking
            data_file = "%s/RUN_%06d_COL_%06d.csv" % (data_dir,int(run),int(curCol))
            
            self.display_data(data_file,data_dir,int(run),curCol,ConfigCOLPath)
            #TODO: error Checking
            
            if signal_dist_outpt == 1:
                signal_distance_angle(data_file,data_dir,run,curCol,ConfigCOLPath)
        
        print("Made it to the end of beginCalculations")
    def createConfigButtons(self):
        self.sdoBox = tk.Checkbutton(self,text='signal_dist_output',variable=self.SDOBool)
        self.record = tk.Checkbutton(self,text='record',variable=self.recordBool)
        self.cleanRun = tk.Checkbutton(self,text='clean_run',variable=self.cleanBool)
        
        self.sdoBox.grid()
        self.record.grid()
        self.cleanRun.grid()
        
    def createActionButtons(self):
        self.doStuffButton = tk.Button(self,text='doMath',command=self.beginCalculations)
        
        self.doStuffButton.grid()
               
    def runFileChooser(self):
        root = tk.Tk()
        root.withdraw()
        root.grid()
        return filedialog.askdirectory()
         
    def cleanRunProtocol(self, data_dir):
        runPath = data_dir + "/RUN"
        altPath = data_dir + "/ALT"
        colPath = data_dir + "/COL"
        
        print(runPath)
        print(altPath)
        print(colPath)
        
        if os.path.exists(runPath):
            os.remove(runPath)
            print("removed RUN file")
            
        if os.path.exists(altPath):
            os.remove(altPath)
            print("removed ALT file")
            
        if os.path.exists(colPath):
            os.remove(colPath)
            print("removed COL file")
           
    def META_FILE_READER(self, path, tagVal):
        for line in fileinput.input(path):
            if tagVal == line.strip().split(':')[0].strip():
                fileinput.close()
                return line.strip().split(':')[1].strip()
                
    def RUN_NUM_CHOOSER(self):
        root = tk.Tk()
        root.withdraw()
        simpledialog.askinteger("RCT Post-Processing Pipeline", "Run Number:")
    
    def getFLTALT(self):
        root = tk.Tk()
        root.withdraw()
        return simpledialog.askinteger("RCT Post-Processing Pipeline", "Flight Altitude:")
        
    def getCollars(self):
        root = tk.Tk()
        root.withdraw()
        counter = 1
        hasOutput = False
        output = [];
        while True:
            frequency = simpledialog.askinteger("RCT Post-Processing Pipeline", "Collar Frequency, press Cancel to finish:")
            if frequency is not None:
                output.append("%d: %d\n" % (counter, frequency))
                counter += 1
                hasOutput = True
            else:
                return output
                
    def getNumCollars(self,path):
        lineCount = 0;
        with open(path) as infp:
            for line in infp:
                    lineCount += 1
                    
        return lineCount
        
    def getBeatFrequency(self,center_freq,collar_freq,ppm):
        actual_center = int(center_freq) / 1.e6 * int(ppm) + int(center_freq)
        beat_freq = int(collar_freq) - int(actual_center)
        return(int(beat_freq))
        
    def raw_gps_analysis(self,input_dir,output_dir,run_num,col_num,tar_alt):
        # Configure variables
        signal_file = '/RUN_%06d_%06d.raw' % (run_num, col_num)
        gps_file = '/GPS_%06d' % (run_num)
        meta_file = '/META_%06d' % (run_num)
        output_file = '/RUN_%06d_COL_%06d.csv' % (run_num, col_num)
        period = 1.5

        # Import META file
        meta_file_stream = open(input_dir + meta_file, 'r')
        # Get start time
        start_time = float(meta_file_stream.readline().strip().split(':')[1].strip())
        center_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
        sampling_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())/1024
        gain = float(meta_file_stream.readline().strip().split(':')[1].strip())

        # Initialize GPS stream
        gps_stream = open(input_dir + gps_file, 'r')

        # Initialize Signal stream
        signal_stream = open(input_dir + signal_file, 'rb')

        # Initialize output stream
        out_stream = open(output_dir + output_file, 'w')

        signal_index = 0
        done = False
        line_counter = 0

        line = gps_stream.readline()
        time_target = float(line.split(',')[0].strip()) - 0.5
        start_alt = float(line.split(',')[4].strip()) / 1000

        while line != "":
            # Extract time
            gps_time = float(line.split(',')[0].strip())
            gps_alt = float(line.split(',')[4].strip()) / 1000 - start_alt

            # Fast forward if less than 1.5 sec prior to previous
            if gps_time < time_target:
                line = gps_stream.readline()
                line_counter += 1
                continue
            time_target += period

            # Fast forward if no SDR data.
            if gps_time < (float(signal_index) / sampling_freq) + start_time:
                line = gps_stream.readline()
                line_counter += 1
                continue

            # throw out if not within 20% of target altitude
            if math.fabs(gps_alt - tar_alt) / tar_alt > 0.2:
                line = gps_stream.readline()
                line_counter += 1
                continue

            # Extract position
            latitude = int(line.split(',')[1].strip())
            longitude = int(line.split(',')[2].strip())

            # Samples prior to this gps point
            #signal_bring_forward = gps_time - ((float(signal_index) / sampling_freq) + start_time )
            #samples_bring_forward = int(signal_bring_forward * sampling_freq)

            # Get max of samples
            max_amplitude = 0
            avg_amplitude = 0
            count = 0
            while gps_time > (float(signal_index) / sampling_freq + start_time):
                # Get sample
                signal_raw = signal_stream.read(8)
                if signal_raw == "":
                    done = True
                    break
                sample_buffer = struct.unpack('ff', signal_raw)
                sample = sample_buffer[0] + sample_buffer[1] * 1j;
                # Get amplitude
                sample_amplitude = abs(sample)
                # Check max
                if sample_amplitude > max_amplitude:
                    max_amplitude = sample_amplitude
                avg_amplitude += sample_amplitude
                # update index
                signal_index += 1
                count += 1
            # Output GPS and signal amplitude
            avg_amplitude /= count
            if done:
                break
            max_amplitude = 10 * math.log10(max_amplitude)
            out_stream.write("%f,%d,%d,%f\n" % (gps_time, latitude, longitude, max_amplitude))
            line = gps_stream.readline()
            line_counter += 1

        # Close file
        print("Read %d lines of GPS data" % line_counter)
        print("Read %d samples, or %d bytes of signal data" % (signal_index, signal_index * 8))
        out_stream.close()
        signal_stream.close()
        gps_stream.close()
        meta_file_stream.close()
        
    def display_data(self,filename,output_path,run_num,num_col,col_def):
        kml_output = False
        # TODO Fix test case
        plot_height = 6
        plot_width = 8
        plot_dpi = 72
        
        # Get collar frequency
        col_freq = float(read_meta_file(col_def, str(num_col))) / 1.e6

        # make list of columns
        # Expects the csv to have the following columns: time, lat, lon, [collars]
        names = ['time', 'lat', 'lon', 'col']

        # Read CSV
        data = np.genfromtxt(filename, delimiter=',', names=names)
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
        fig.set_size_inches(plot_width, plot_height)
        fig.set_dpi(plot_dpi)
        plot.grid()
        ax = plot.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')
        ax.set_title('Run %d, Collar %d at %3.3f MHz\nUTM Zone: %d %s' % (run_num, num_col, col_freq, zonenum, zone))
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

        # Save plot
        plot.savefig('%s/RUN_%06d_COL_%06d.png' % (output_path, run_num, num_col), bbox_inches = 'tight')
        print('Collar %d: %s/RUN_%06d_COL_%06d.png' %
            (num_col, output_path, run_num, num_col))
        # plot.show(block=False)
        plot.close()

        if(kml_output):
            from PIL import Image
            fig = plot.figure()
            fig.patch.set_facecolor('none')
            fig.patch.set_alpha(0)
            fig.set_size_inches(8, 6)
            fig.set_dpi(72)
            curColMap = plot.cm.get_cmap('jet')
            sc = plot.scatter(lon, lat, c=coldata[i - 1], cmap=curColMap, vmin = minCol, vmax = maxCol)
            ax = plot.gca()
            ax.patch.set_facecolor('none')
            ax.set_aspect('equal')
            plot.axis('off')
            plot.savefig('tmp.png', bbox_inches = 'tight')
            print('Collar at %0.3f MHz: %s/RUN_%06d_COL_%0.3ftx.png' %
                (collars[i - 1] / 1000000.0, output_path, run_num,
                collars[i - 1] / 1000000.0))
            # plot.show(block=False)
            plot.close()

            image=Image.open('tmp.png')
            image.load()
            image_data = np.asarray(image)
            image_data_bw = image_data.max(axis=2)
            non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
            non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
            cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

            image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

            new_image = Image.fromarray(image_data_new)
            new_image.save('%s/RUN_%06d_COL%06dtx.png' % (output_path, run_num, num_col))
            os.remove('tmp.png')

            f = open('%s/RUN_%06d_COL%06d.kml' % (output_path, run_num, num_col), 'w')
            f.write("""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
          <Folder>
            <name>Radio Collar Tracker</name>
            <description>Radio Collar Tracker, UCSD</description>
            <GroundOverlay>
              <name>RUN %d</name>
              <description>RUN %d, Collar at %0.3f MHz</description>
              <Icon>
                <href>%s</href>
              </Icon>
              <LatLonBox>
                <north>%f</north>
                <south>%f</south>
                <east>%f</east>
                <west>%f</west>
                <rotation>0</rotation>
              </LatLonBox>
            </GroundOverlay>
          </Folder>
        </kml>""" % (run_num, run_num, collars[i - 1] / 1000000.0, '%s/RUN_%06d_COL%0.3ftx.png' % (output_path, run_num, collars[i - 1] / 1000000.0),north, south, east, west))
            f.close()
        
    def signal_distance_angle(self,filename,output_path,run_num,num_col,col_def):
        ml_output = False
        # TODO Fix test case
        plot_height = 6
        plot_width = 8
        plot_dpi = 72

        # Get configuration

        # Get collar frequency
        col_freq = float(read_meta_file(col_def, str(num_col))) / 1.e6

        # make list of columns
        # Expects the csv to have the following columns: time, lat, lon, [collars]
        names = ['time', 'lat', 'lon', 'col']

        # Read CSV
        data = np.genfromtxt(filename, delimiter=',', names=names)
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

        ## Custom Location
        target_lon = 599679
        target_lat = 3620338
        distance = [None] * len(data['lat'])
        angle = [None] * len(data['lat'])

        # Calculate distance and angle per sample
        prev_lat = lat[0]
        prev_lon = lon[0] + 1
        for i in range(len(data['lat'])):
            d_lat = - lat[i] + target_lat
            d_lon = - lon[i] + target_lon
            distance[i] = math.sqrt(d_lat * d_lat + d_lon * d_lon)
            head_lat = prev_lat - lat[i]
            head_lon = prev_lon - lon[i]
            head_len = math.sqrt(head_lat * head_lat + head_lon * head_lon)
            angle[i] = math.acos(d_lat / distance[i] * head_lat / head_len + d_lon / distance[i] * head_lon / head_len) / math.pi * 180
            prev_lat = lat[i]
            prev_lon = lon[i]

        # Configure plot
        fig = plot.figure()
        fig.set_size_inches(plot_width, plot_height)
        fig.set_dpi(plot_dpi)
        plot.grid()
        ax = plot.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.set_xlabel('Angle')
        ax.set_ylabel('Distance')
        ax.set_title('Run %d, Collar %d at %3.3f MHz' % (run_num, num_col, col_freq))
        plot.xticks(rotation='vertical')

        # Calculate colorplot
        maxCol = np.amax(data['col'])
        minCol = np.amin(data['col'])
        curColMap = plot.cm.get_cmap('jet')

        # Plot data
        sc = plot.scatter(angle, distance, c=data['col'], cmap=curColMap, vmin = minCol, vmax = maxCol)
        colorbar = plot.colorbar(sc)
        colorbar.set_label('Maximum Signal Amplitude')


        # Save plot
        plot.savefig('%s/RUN_%06d_COL_%06d_signal_distance.png' % (output_path, run_num, num_col), bbox_inches = 'tight')
        print('Collar %d: %s/RUN_%06d_COL_%06d_signal_distance.png' %
            (num_col, output_path, run_num, num_col))
        # plot.show(block=False)
        plot.close()

    def cat_relevent(self,input_dir,run_num):
        gps_file = '/GPS_%06d' % (run_num)
        meta_file = '/META_%06d' % (run_num)
        output_file = '/RUN_%06d.raw' % (run_num)
        signal_file_prefix = '/RAW_DATA_%06d_' % (run_num)

        # Import META file
        meta_file_stream = open(input_dir + meta_file, 'r')
        # Get info
        start_time = float(meta_file_stream.readline().strip().split(':')[1].strip())
        center_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
        sampling_freq = int(meta_file_stream.readline().strip().split(':')[1].strip())
        gain = float(meta_file_stream.readline().strip().split(':')[1].strip())

        # Get GPS data
        gps_stream = open(input_dir + gps_file, 'r')
        start_gps_time = float(gps_stream.readline().split(',')[0].strip())

        # get last gps
        gps_line = ""
        while True:
            line_buffer = gps_stream.readline()
            if line_buffer == "":
                break
            gps_line = line_buffer
            

        last_gps_time = float(gps_line.split(',')[0].strip())

        # Get number of signal files
        dir_list = os.listdir(input_dir)
        filecount = 0
        for filename in dir_list:
            if filename.startswith("RAW_DATA"):
                filecount += 1

        # Calculate first signal file
        filesize = os.stat(input_dir + signal_file_prefix + "%06d" % (1)).st_size
        file_length = filesize / 2.0 / sampling_freq
        start_file = 0
        for i in range(1, filecount + 1):
            if (i - 1) * file_length + start_time < start_gps_time:
                start_file = i
            else:
                break

        # Calculate last signal file
        last_file = start_file
        for i in range(start_file, filecount + 1):
            last_file = i
            if (i - 1) * file_length + start_time > last_gps_time:
                break

        # concatenate files
        dest = open(input_dir + output_file, 'wb')
        for i in range(start_file, last_file):
            shutil.copyfileobj(open(input_dir + signal_file_prefix + "%06d" % (i), 'rb'), dest)

        dest.close()    

top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()