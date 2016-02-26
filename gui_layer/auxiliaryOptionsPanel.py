import Tkinter as tk
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'meta_file_reader'))
sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'python_dialogs'))

from read_meta_file import read_meta_file
from getCollars import GET_NUM_COLLARS

class auxiliaryOptionsPanel(tk.Frame):
    #TODO: Need to add functionality for collecting collar frequencies
    VERTICLE_PADDING = 3;
    def __init__(self,parent,HEIGHT):
        tk.Frame.__init__(self,parent,width=250,height=HEIGHT)

        self.config(bg='blue')