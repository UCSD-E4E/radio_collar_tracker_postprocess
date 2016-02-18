import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog


from META_FILE_READER import META_FILE_READER
from getNumCols import GET_NUM_COLLARS
import os

class auxiliaryOptionsPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    VERTICLE_PADDING = 3;
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=250,height=HEIGHT)

        self.config(bg='blue')