import Tkinter as tk
import tkFileDialog as filedialog

class Application(tk.Frame):
    randValue = 20
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
        firstFrame = dirSelectPanel(self,self.beginCalculations)
        
        
        #for(int i = 0; i < fileNameList.length;i++):
        #    filecopy(data_dir + fileNameList[1],dataout_dir + fileNameList[1]);
        

class dirSelectPanel(tk.Frame):
    doCalculations = 0
    dirText = 0; runTBText = 0; altTBText = 0; colTBText = 0
    dirTB = 0; runTB = 0; altTB = 0; colTB = 0
    def __init__(self,parent,calculationHandler):
        tk.Frame.__init__(self,parent)
        self.grid()
        self.doCalculations = calculationHandler
        self.initializeWidgets()
        self.config(bg='beige')
        
    def initializeWidgets(self):
        self.dirText = tk.Text(self,height=1,width = 30,bd=0,bg='beige',wrap='word')
        self.dirTB = tk.Entry(self)
        self.runText = tk.Text(self,height=2,width = 30,bd=0,bg='beige',wrap='word')
        self.runTB = tk.Entry(self)
        self.altText = tk.Text(self,height=2,width = 30,bd=0,bg='beige',wrap='word')
        self.altTB = tk.Entry(self)
        self.colText = tk.Text(self,height=2,width = 30,bd=0,bg='beige',wrap='word')
        self.colTB = tk.Entry(self)
        
        
        #INSERT = self.dirText.INSERT
        self.dirText.insert('insert',"Please select a data directory")
        self.runText.insert('insert',"If this box is red, please insert the number of runs below")
        self.altText.insert('insert',"If this box is red, please insert the working altitude")
        self.colText.insert('insert',"If this box is red, please insert the number of collars below")
        
        curHeight = 0
        self.dirText.grid()
        curHeight = curHeight + self.dirText.winfo_height();
        print(curHeight)
        self.dirTB.grid()
        self.runText.grid()
        self.runTB.grid()
        self.altText.grid()
        self.altTB.grid()
        self.colText.grid()
        self.colTB.grid()
        
        
        
        
        #curHeight = 0
        #self.dirText.place(anchor='nw')
        #self.update()
        #curHeight = curHeight + self.dirText.winfo_height();
        #print(curHeight)
        #self.dirTB.place(anchor='ne',x=-1)
        #self.update()
        #curHeight = curHeight + self.dirTB.winfo_height();
        #print(curHeight)
        #self.runText.place(anchor='nw',rely=curHeight)
        #self.update()
        #curHeight = curHeight + self.runText.winfo_height();
        #print(curHeight)
        #self.runTB.place(anchor='nw',x=1)
        #self.altText.place(anchor='nw')
        #self.altTB.place(anchor='nw')
        #self.colText.place(anchor='ne',x=-1)
        #self.colTB.place(anchor='se',x=200)
        
        self.doStuffButton = tk.Button(self,text='Calculate',command=self.prepareForCalc)
        
        self.doStuffButton.grid()
        
    

    def changeSize(self):
        self.width = 200;
        self.height = 300;
        
    def prepareForCalc(self):
        self.doCalculations();






top = Application()
top.master.title('Radio Collar Tracker')
top.mainloop()