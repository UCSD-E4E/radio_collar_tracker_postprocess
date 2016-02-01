#!/usr/local/bin/python

import tkinter as tk;

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
		
    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',command=self.quit)
        self.quitButton.grid()
		
        self.textButton = tk.Button(self,text='makeSomeText',command=self.createWidgetsTwo)
        self.textButton.grid()
		
    def createWidgetsTwo(self):
        self.newButton = tk.Button(self,text='newButton')
        self.newButton.grid()
		
app = Application()

app.master.title('sampleApplication')
app.mainloop()




    