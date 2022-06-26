import tkinter as tk
from tkinter import *
import tkinter.messagebox
import face
from tkinter import *
import os

def delete():
	path='data/face_image/user.jpg'
	os.remove(path)
	
win=tkinter.Tk()
win.title('wind')
win.geometry('800x600+300+100')

b1 = tk.Button(win, text='face', width=15,
              height=2, command=face.main)

b2 = tk.Button(win, text='delete', width=15,
              height=2, command=delete)
              

b2.pack(padx=60,pady=80)
b1.pack(padx=60,pady=80)

win.mainloop()
