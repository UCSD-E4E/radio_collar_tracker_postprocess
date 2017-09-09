"""
@author: Anthony Koutroulis

Created as an extension to the E4E Radio Collar Tracker Project, partially 
    derived from source material by Nathan Hui
    
Created as a part of the 2017 Engineers For Exploration REU, funded by the 
    National Science Foundation
"""
"""
widgets.py

Widgets for use in the Jupyter Notebook to accompany the E4E Radio Collar Tracker Project
"""

import ipywidgets as widgets
import matplotlib.pyplot as plt
import scipy.signal as sg
import os

class FileWidget:
    # Interactive widget for specifying file-path, data series, and run variables
    # TODO: Better path entry, supress output        
    def __init__(self,defaults=[]):
        
        if len(defaults) is not 0:
            defaults[2] = 'RUN_' + defaults[2].zfill(6)
            defaults[3] = defaults[3][0]-1,defaults[3][1]-1
        
        self.defaults    = defaults
            
        self.path_wdgt   = widgets.Text(description='File Path:', 
                                        placeholder='--enter--')
        
        self.series_wdgt = widgets.Dropdown(description='Data Series:',
                                            options=['--select--'])
        
        self.run_wdgt    = widgets.Dropdown(description='Run Number:',
                                            options=['--select--'])
        
        self.range_wdgt  = widgets.SelectionRangeSlider(description='File Range:',
                                                        options=[0])
        
        self.files_wdgt  = widgets.interactive(self.printer,
                                               a=self.path_wdgt, 
                                               b=self.series_wdgt, 
                                               c=self.run_wdgt, 
                                               d=self.range_wdgt)
        
        self.valid = len(defaults) is not 0 and os.path.isdir(self.getPath(self.defaults))
        
    def getPath(self,d=[]):
        if len(d) is 0:
            d = [self.files_wdgt.children[0].value, 
                 self.files_wdgt.children[1].value, 
                 self.files_wdgt.children[2].value]
        return d[0]+d[1]+'/'+d[2]+'/'

    def printer(self, a, b, c, d):
        print(a, b, c, d)
    
    def update_path(self,path):
        self.path_wdgt.value=path
        self.update_series_vals('value')

    def update_series_vals(self,*args):
        self.series_wdgt.options = os.listdir(self.path_wdgt.value)
        if self.valid:
            self.series_wdgt.value = self.defaults[1]
        else:
            self.series_wdgt.value = self.series_wdgt.options[0]
        self.update_run_vals('value')

    def update_run_vals(self,*args):
        runfolders = os.listdir(self.path_wdgt.value+self.series_wdgt.value)
        for folder in runfolders:
            if not folder.startswith('RUN'):
                runfolders.remove(folder)
        self.run_wdgt.options = runfolders
        if self.valid:
            self.run_wdgt.value = self.defaults[2]
        else:
            self.run_wdgt.value = self.run_wdgt.options[0]
        self.update_range_vals('value')

    def update_range_vals(self,*args):
        runfiles = []
        for file in os.listdir(self.path_wdgt.value+self.series_wdgt.value+'/'+self.run_wdgt.value):
            if file.startswith('RAW'):
                runfiles.append(file)   
        self.range_wdgt.options = runfiles
        self.range_wdgt.options = tuple(zip([str(i) for i in range(1,len(runfiles)+1)],runfiles))
        if self.valid:
            self.range_wdgt.index = self.defaults[3]
        else:
            self.range_wdgt.index = (0,len(runfiles)-1)

    def display(self):
        display(self.files_wdgt)
        self.observe()

    def observe(self):
        if self.valid :
            self.update_path(self.defaults[0])
            self.valid = False
            #self.files_wdgt.children[0].value = self.defaults[0]
            #self.files_wdgt.children[1].value = self.defaults[1]
            #self.files_wdgt.children[2].value = self.defaults[2]
            #self.update_range_vals()
            #self.files_wdgt.children[3].index = self.defaults[3]
        else:
            self.update_path(self.path)
        self.path_wdgt.observe(self.update_series_vals, 'value')
        self.series_wdgt.observe(self.update_run_vals, 'value')
        self.run_wdgt.observe(self.update_range_vals, 'value')
    
    def getFiles(self):
        file_path = (self.files_wdgt.children[0].value + 
                     self.files_wdgt.children[1].value + '/' + 
                     self.files_wdgt.children[2].value + '/')
        trash,files = zip(*self.files_wdgt.children[3].options)
        files = files[files.index(self.files_wdgt.children[3].value[0]):
                      files.index(self.files_wdgt.children[3].value[1])+1]
        raw_files = [file_path + file for file in files]
        return raw_files

        
class FilterWidget:
    # Interactive widget for filtering the power data
    
    def __init__(self,x,y):
        self.x         = x
        self.y         = y
        self.avg_n     = 1
        self.fig       = plt.figure()
        self.mPy       = sg.medfilt(self.y,self.avg_n)
        self.filt_plot,= plt.plot(self.x,self.y)
        self.filt_wdgt = widgets.IntSlider(
            value=self.avg_n,
            min=1,
            max=101,
            step=2,
            description='Resolution:',
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        self.fig.show()
        
    def figure(self):
        return self.fig
        
    def update_filt(self,*args):
        self.mPy = sg.medfilt(self.y,self.filt_wdgt.value)
        self.draw()
        
    def observe(self):
        self.filt_wdgt.observe(self.update_filt,'value')
    
    def display(self):
        display(self.filt_wdgt)
        self.observe()
    
    def getResult(self):
        return self.mPy
    
    def draw(self):
        self.filt_plot.set_data(self.x,self.mPy)
        plt.draw()
        self.fig.show()
                
            
# Progress Bar from Widget https://github.com/alexanderkuk/log-progress        
def log_progress(sequence, every=None, size=None, name='Items'):
    # wraps an iterable list to produce a progress bar tracking each iteration
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )
        
