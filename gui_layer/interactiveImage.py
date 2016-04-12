import numpy as np
# USING utm 0.4.0 from https://pypi.python.org/pypi/utm
import utm
import matplotlib.pyplot as plot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


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
