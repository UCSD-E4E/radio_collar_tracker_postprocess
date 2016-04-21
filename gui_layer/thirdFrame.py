import Tkinter as tk
import tkFileDialog as filedialog
import shutil
import os.path

class Application(tk.Frame):
    randValue = 20
    # fileNameListParent is the list that stores all the file paths and names
    fileNameListParent = ['/home/nan/gui/test2/1.txt','/home/nan/gui/test2/2.txt']

    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        #self.pack_propagate('false')
        #self.grid_propagate('false')
        self.grid()
        self.placeFrames()
        self.config(background="red")
        
        
    def beginCalculations(self):
        print("Wow this actually worked%d" %(self.randValue))
        print("TODO: add functionality")
        
    def placeFrames(self):
        print("TODO: add functionality")
        firstFrame = dirExportFiles(self,self.fileNameListParent)
        
        
        #for(int i = 0; i < fileNameList.length;i++):
        #    filecopy(data_dir + fileNameList[1],dataout_dir + fileNameList[1]);
        

class dirExportFiles(tk.Frame):
    
    fileNameList = ""
    
    def __init__(self,parent,fileNameListParent=[]):
        self.fileNameList = fileNameListParent
        tk.Frame.__init__(self,parent,bg='#F0F0F0',width=44,height=300)
        self.pack_propagate('false')
        self.grid_propagate('false')
        self.pack(side='left')
        #self.doCalculations = calculationHandler
        self.initializeWidgets()

        
    def initializeWidgets(self):
	#self.exportButton = tk.Button(self, text='Export', command=self.exportFunction(self.fileNameList))
	self.exportButton = tk.Button(self, text='Export', command=lambda:self.exportFunction(self.fileNameList))
	self.exportButton.grid()
        
        
    def exportFunction(self,fileList):
	# dest_path = filedialog.askdirectory()
	# check for existence of the file path if not ask for path again
	dest_path = filedialog.askdirectory()
	if os.path.exists(dest_path):
		for file in fileList:
			shutil.copy2(file, dest_path)
			#print 'here'






#top = Application()
#top.master.title('Radio Collar Tracker')
#top.mainloop()