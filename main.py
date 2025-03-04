import tkinter as tk  
from tkinter import ttk
from tkinter.ttk import Style
from PIL import Image
import pytesseract
import cv2
import os
import ss
import base64
import json
import requests
import pyautogui as pag


filename = "tempImage.png"
request_body = {}

auth_string = ""
url = 'https://us-central1-uottahj.cloudfunctions.net/app/picture'


class Text(tk.Text):
	@property
	def text(self) -> str:
		return self.get('1.0', 'end-1c')
		
	@text.setter
	def text(self, value) -> None:
		self.replace('1.0', 'end-1c', value)
		
	def __init__(self, master, **kwargs):
		tk.Text.__init__(self, master, **kwargs)


def postAndDeleteImage(hasImage):
	global auth_string
	global url

	if request_body["image"] == '' and request_body["text"] == '':
		pag.alert(text="No data was found ;-; please try again", title="Uh oh")
		return

	# header
	headers = {'nanoid': auth_string}

	# Make request
	requestpost = requests.post(url, data = request_body, headers = headers)

	print(url)
	print(request_body)
	print(requestpost.text)
	print(headers)

	try:
		response_data = requestpost.json()
		success = response_data["success"]
		if not success:
			pag.alert(text="Request error [404]", title="Uh oh")
	except:
		pag.alert(text="Request error [404]", title="Uh oh")

	if hasImage:
		os.remove(filename)

	return


def postText():
	return


def imageOCRtoText(filename):

	image = cv2.imread(filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# apply thresholding to preprocess the image
	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# apply median blurring to remove noise
	# gray = cv2.medianBlur(gray, 3)

	tempFilename = "temp" + filename

	cv2.imwrite(tempFilename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	
	# MODIFY THIS TO YOUR TESSERACT INSTALLATION
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

	text = pytesseract.image_to_string(Image.open(tempFilename))
	os.remove(tempFilename)	
	# show the output images
	# cv2.imshow("Image", image)
	# cv2.imshow("Output", gray)
	# cv2.waitKey(0)
	# print(text[:-1])
	return text[:-1] # return string after removing tesseract delimiter


def main():
	win = tk.Tk()
	win.iconbitmap(False, "icon.ico")
	win.minsize(200, 20)
	win.title("Picanote") # App title


	# def move_window(event):
	#	 win.geometry('+{0}+{1}'.format(event.x_win, event.y_win))

	# win.overrideredirect(True) # turns off title bar, geometry
	# win.geometry('400x100+200+200') # set new geometry

	# # make a frame for the title bar
	# title_bar = tk.Frame(win, bg='white', relief='raised', bd=2)

	# # put a close button on the title bar
	# close_button = tk.Button(title_bar, text='X', command=win.destroy)

	# # a canvas for the main area of the window
	# window = tk.Canvas(win, bg='black')

	# # pack the widgets
	# title_bar.pack(expand=1, fill=tk.X)
	# close_button.pack(side=RIGHT)
	# window.pack(expand=1, fill=BOTH)

	# # bind title bar motion to the move window function
	# title_bar.bind('<B1-Motion>', move_window)




	style = Style().configure('TButton', font = ('Helvetica', 12))
	# style.map('TButton', foreground = [('active', '! disabled', 'green')], background = [('active', 'black')])

	textnote = tk.StringVar()  
	# textbox = ttk.Entry(win, width = win.winfo_width(), textvariable = textnote, font=('Helvetica', 12))
	textbox = tk.Text(win, width = win.winfo_width(), height = 10, font=('Helvetica', 12), fg='#a36c31', bg='#fff3e6', highlightcolor="#ffd4a6", highlightbackground="#ffd4a6", highlightthickness=8)

	textbox.grid(column = 0, row = 0, columnspan = 2, sticky = tk.W+tk.E)
	# textbox.config(wrap=WORD)

	# lbl = ttk.Label(win, text = "Enter the name:").grid(column = 0, row = 0)# Click event  
	# Textbox widget  
	def submitTextnote():
		global request_body

		textBody = textbox.get("1.0","end")
		request_body = {
			"image": "",
			"text": textBody
		}

		postAndDeleteImage(False)
		# print(textBody)# Textbox widget 
		textbox.delete(1.0,"end")


	textbutton = tk.Button(win, width = 15, text = "SAVE NOTE", command = submitTextnote, bg='#ffd4a6', fg='#a36c31', font = ('Helvetica', 10, 'bold'), highlightthickness=10)
	textbutton.grid(column = 0, row = 1, columnspan = 2, sticky = tk.W+tk.E)


	def takeScreenshot(isOCR):
		global request_body
		# Screenshotting function goes here

		os.system('python3 ss.py')

		if isOCR:
			textBody = imageOCRtoText(filename)
			# Will send text
			request_body = {
				"image": "",
				"text": textBody
			}
			# print(textBody)
		else:
			with open(filename, "rb") as image_file:
				data = "data:image/png;base64," + str(base64.b64encode(image_file.read()), 'utf-8')
				# Will send image
				request_body = {
					"image": data,
					"text": ""
				}
				# print(data)
		
		# Will send image
		postAndDeleteImage(True)

		print("function is complete")


	# button = ttk.Button(win, width = 10, text = "Screenshot\nwith OCR", command = submitTextnote, relief=tk.GROOVE).grid(column = 0, row = 2)
	OCRbutton = tk.Button(win, width = 15, text = "SCREENSHOT\n(TO TEXT)", command = lambda : takeScreenshot(True), bg='#ffd4a6', fg='#a36c31', font = ('Helvetica', 10, 'bold'), highlightcolor="#e39846", highlightbackground="#e39846", highlightthickness=10)
	OCRbutton.grid(column = 0, row = 2)
	noOCRbutton = tk.Button(win, width = 15, text = "SCREENSHOT\n(TO IMAGE)", command = lambda : takeScreenshot(False), bg='#ffd4a6', fg='#a36c31', font = ('Helvetica', 10, 'bold'), highlightthickness=10)
	noOCRbutton.grid(column = 1, row = 2)

	def submitAuthstring():
		global auth_string

		auth_string = authstring.get()

		# print(authstring.get())

		# TODO: Check
		valid = True
		if valid:
			authbox.configure({"background": "#cdff94"})
		else:
			authbox.configure({"background": "#ffb0b0"})

	authstring = tk.StringVar()  
	authbox = tk.Entry(win, width = 15, textvariable = authstring, font=('Helvetica', 16, 'bold'), fg = "#237699", bg = "#d4effa", highlightcolor="#a7e2fa", highlightbackground="#a7e2fa", highlightthickness=8, show="*")
	authbox.grid(column = 0, row = 3, columnspan = 2, sticky = tk.W+tk.E)

	authbutton = tk.Button(win, width = 15, text = "AUTHORIZE", command = submitAuthstring, bg='#a7e2fa', fg='#237699', font = ('Helvetica', 10, 'bold'), highlightbackground="#a7e2fa", highlightthickness=5)
	authbutton.grid(column = 0, row = 4, columnspan = 2, sticky = tk.W+tk.E)

	win.update_idletasks()
	win.mainloop()   


if __name__ == '__main__':
	# print(imageOCRtoText(filename))
	main()
