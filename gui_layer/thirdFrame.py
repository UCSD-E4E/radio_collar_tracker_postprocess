import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

class Application(tk.Frame):
    randValue = 20
    # fileNameListParent is the list that stores all the file paths and names
    #fileNameListParent = ['/home/nan/gui/test2/1.txt','/home/nan/gui/test2/2.txt']

    def __init__(self,master=None):
        tk.Frame.__init__(self,master,width = 500,height=300)
        self.grid()
        self.placeFrames()
        self.config(background="red")
        
    def beginCalculations(self):
        print("Wow this actually worked%d" %(self.randValue))
        print("TODO: add functionality")
        
    def placeFrames(self):
        print("TODO: add functionality")
        firstFrame = dirExportFiles(self)
        
        
        #for(int i = 0; i < fileNameList.length;i++):
        #    filecopy(data_dir + fileNameList[1],dataout_dir + fileNameList[1]);
        

class dirExportFiles(tk.Frame):
    
    def __init__(self,parent):
	self.fileNameList = []
	
        tk.Frame.__init__(self,parent)
        self.grid()
        #self.doCalculations = calculationHandler
        self.initializeWidgets()
        self.config(bg='beige')
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

    def updateList(self, newList):
	self.fileNameList[:] = newList
	if (len(self.fileNameList) != 0 ):
		self.exportButton.config(state='active')





top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()