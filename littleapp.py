#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import csvJSON
import os
import platform
from Tkinter import *
from ttk import Frame, Style, Button
from tkFileDialog import askopenfilename

class littleapp(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
    	self.parent = parent
    	self.initialise()

    def initialise(self):
        #self.grid()

        self.resizable(width=False, height=False)
        system = platform.system()
        try:
            if system == 'Windows':
                self.iconbitmap(default='jsonlogo.ico')
            else:
                #self.iconbitmap(default='jsonlogo.xbm')
				pass
        except TclError:
            print('cant load custom icon')
        self.style = Style()
        self.style.theme_use("clam")
        
        frame = Frame(self, relief=SUNKEN, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        framebottom = Frame(self, relief=SUNKEN, borderwidth=1)
        framebottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        label = Tkinter.Label(frame,
                              anchor="w",fg="black", text='Upload CSV/XLSX File for Conversion!:')
        label.pack()

        self.entry = Tkinter.Entry(frame)
        self.entry.insert(0, 'File Path')
        self.entry.pack(ipadx=100)
        
        #self.pack(fill=BOTH, expand=True)
        
        convertButton = Button(frame, text="Convert", command=self.onConvertClick)
        convertButton.pack(side=RIGHT, padx=5, pady=5)
        browseButton = Button(frame, text="Browse", command=self.onBrowseClick)
        browseButton.pack(side=LEFT, padx=5, pady=5)

        self.canvas = Canvas(framebottom, width=400, height=200, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack()
        self.update()
        x = self.winfo_width()
        y = self.winfo_height()
        self.ball = self.canvas.create_oval(x/3.15, y/15, x/3.15+150, y/15+150, fill='white')

        self.photo = Tkinter.PhotoImage(file = './jsonlogo.gif')
        
        self.logo = self.canvas.create_image(x/2, y/3, image=self.photo)
        #self.canvas.move(self.logo, 20, 40)
        self.animate(1)

    def onBrowseClick(self):        
        filename = askopenfilename() #opens file chooser
        print(filename)
        self.entry.delete(0, 'end')
        self.entry.insert(0, filename)
        self.canvas.itemconfig(self.ball, fill='white')

    def onConvertClick(self): #converts csv or xlsx
        ext = os.path.splitext(self.entry.get())[-1].lower()
    	print('This file is a %s' % (ext))
        if ext == '.csv' or ext == '.xlsx':
            csvJSON.csvJSON(self.entry.get(),ext)
            self.canvas.itemconfig(self.ball, fill='green') #if success then indicator is green
            self.entry.delete(0, 'end')
            self.entry.insert(0, 'success! check app directory for new json file')
        else:
            self.canvas.itemconfig(self.ball, fill='red') #if fail then indicator is red
            self.entry.delete(0, 'end')
            self.entry.insert(0, 'unsupported file format!')

    def animate(self, direction):  
        self.canvas.move(self.logo, direction*1, 0)
        self.canvas.move(self.ball, direction*1, 0)
        if self.canvas.coords(self.ball)[0] > 250 or self.canvas.coords(self.ball)[0] < 0:
            direction = direction*-1
        self.after(20, self.animate, direction)


if __name__ == '__main__':
	app = littleapp(None)
	app.title('CSV/XLSX to JSON')
	app.mainloop()