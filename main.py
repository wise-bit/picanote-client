import tkinter as tk  
from tkinter import ttk
from tkinter.ttk import Style
# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os


def imageOCR(filename):

	image = cv2.imread(filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# apply thresholding to preprocess the image
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# apply median blurring to remove noise
	# gray = cv2.medianBlur(gray, 3)

	filename = "temp.png"
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	# show the output images
	# cv2.imshow("Image", image)
	# cv2.imshow("Output", gray)
	# cv2.waitKey(0)
	print(text[:-1])
	return text[:-1] # return string after removing tesseract delimiter


def main():
	win = tk.Tk()
	win.title("Picanote") # App title

	style = Style()
	style.configure('TButton', font = ('Helvetica', 16, 'bold'), borderwidth = '4')
	# style.map('TButton', foreground = [('active', '! disabled', 'green')], background = [('active', 'black')])

	# lbl = ttk.Label(win, text = "Enter the name:").grid(column = 0, row = 0)# Click event  
	# Textbox widget  
	def submitTextnote():   
	    print(textnote.get())# Textbox widget 
	    textnote.set("")

	textnote = tk.StringVar()  
	textbox = ttk.Entry(win, width = 15, textvariable = textnote, font=('Helvetica', 16)).grid(column = 0, row = 0, columnspan = 2, sticky = tk.W+tk.E)
	button = ttk.Button(win, width = 15, text = "SUBMIT", command = submitTextnote).grid(column = 0, row = 1, columnspan = 2, sticky = tk.W+tk.E)
	# button = ttk.Button(win, width = 10, text = "Screenshot\nwith OCR", command = submitTextnote, relief=tk.GROOVE).grid(column = 0, row = 2)
	button = ttk.Button(win, width = 15, text = "Screenshot\nwith OCR", command = imageOCR("sample1.png")).grid(column = 0, row = 2)
	button = ttk.Button(win, width = 15, text = "Screenshot\nwithout OCR", command = submitTextnote).grid(column = 1, row = 2)
	win.mainloop()   


if __name__ == '__main__':
	filename = "sample1.png"
	# print(imageOCR(filename))
	main()
