import tkinter as tk  
from tkinter import ttk

win = tk.Tk()
win.title("App") 

textnote = tk.StringVar()  
textbox = ttk.Entry(win, textvariable = textnote).grid(column = 0, row = 0)

def submitTextnote():
	print(textbox.get())
	textbox.set("")

textbutton = tk.Button(win, text = "Save", command = submitTextnote).grid(column = 0, row = 1)

win.mainloop()  