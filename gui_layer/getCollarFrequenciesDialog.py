import Tkinter as tk

class getCollarFreqsDialog:
    frequencyList = []
    newFreqTB = 0
    listBox = 0;
    addButton = 0
    removeButton = 0
    finishButton = 0
    bgcolor = '#F0F0F0'
    buttonColor = '#CCCCCC'
    
    def __init__(self,master=None,configColPath):
        tk.Frame.__init__(self,master,height=400,width=500)
        self.initializeWidgets()
        
        
    def initializeWidgets(self):
        tk.Text(self,height=1,width = 30,bd=0,bg=self.bgcolor)
        self.newFreqTB =  tk.Entry(self,width = 12)
        self.listBox = tk.ListBox(self)