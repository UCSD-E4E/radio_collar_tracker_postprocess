import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path



class dirExportFiles(tk.Frame):
    
    def __init__(self,parent):
	self.fileNameList = []
	
        tk.Frame.__init__(self,parent)
        self.grid()
        #self.doCalculations = calculationHandler
        self.initializeWidgets()
        self.config(bg='#F0F0F0')
        self.config(height='500')
        self.config(width='300')
        
    def initializeWidgets(self):
	#self.exportButton = tk.Button(self, text='Export', command=self.exportFunction(self.fileNameList))
        self.exportButton = tk.Button(self, text='Export', state='disabled', command=self.exportFunction)
        self.exportButton.grid()
        
        
    def exportFunction(self):
	# dest_path = filedialog.askdirectory()
	# check for existence of the file path if not ask for path again
	dest_path = filedialog.askdirectory()
	if os.path.exists(dest_path):
		for file in self.fileNameList:
			shutil.copy2(file, dest_path)
			#print 'here'
		
    def clearList(self):
        self.fileNameList[:] = []
        self.exportButton.config(state='disabled')

    def updateList(self, newList):
        self.fileNameList[:] = newList
        if (len(self.fileNameList) != 0 ):
            self.exportButton.config(state='normal')
        else:
            self.exportButton.config(state='disabled')