from escpos import *
import os.path
import os
import time
from PIL import Image, ImageDraw, ImageFont
from PrinterConfig import *
from datetime import datetime, timedelta
import logging
LOG_FILENAME = './log.out'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """

#####################################################################################################################
#											  _____   _____ _       _____  											#
#											 |  __ \ / ____| |     / ____| 											#
#											 | |__) | |    | |    | (___   											#
#											 |  _  /| |    | |     \___ \  											#
#											 | | \ \| |____| |____ ____) | 											#
#											 |_|  \_\\_____|______|_____/ 											#
#											 							  											#
#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#
#  VERSION 2.2																										#
#  update notes:																									#
#   - added functionality to print without prompt via the "Start Bookdrop Browser" button in receipt-manager.pyw	#
#   - converted some hardcoded information into easily changeable variables within PrinterConfig.py					#
#   - added error logging																							#
#  HOTFIX (11/4/2023):																								#
#   - added checkblankreceipt() to avoid printing blank receipts													#
#####################################################################################################################

def main():
	while True:
		queuepath = (r"C:\queue\job.txt")
		lastprint = (r"C:\queue\last\job.txt")
		if not os.path.exists(lastprint):
			os.makedirs(lastprint[:-8])
			open(lastprint, 'w').close()
		while not os.path.exists(queuepath):
			time.sleep(1)

		if os.path.isfile(queuepath):
			if checkblankreceipt(queuepath) == True:
				remove_headers(queuepath)
				mainProc(queuepath)
			while os.path.isfile(queuepath):
				try:
					os.replace(queuepath, lastprint)
				except:
					pass
		else:
			raise ValueError("%s isn't a file!" % queuepath)


def mainProc(queuepath):
	with open(queuepath) as f:
		listpoint = 0
		infolist= [""]

		for lines in f:
			infolist[listpoint] = lines
			listpoint += 1
			infolist.append("")
		printer = recType(infolist)

		if printerOrientation == True:
			normalID = "0"
			stickID = "1"
		else:
			normalID = "1"
			stickID = "0"

		if printer == 1:
			normalRec(infolist, normalID)
		elif printer == 2:
			stickyRec(infolist, stickID)
	f.close()
	return()



def recType(infolist):
	try:
		holdcheck = infolist[holdLine].find(holdReceiptText)
	except:
		holdcheck = -1
	if holdcheck != -1:
		print("<<<<Sticky Receipt>>>>")
		print(holdcheck)
		return(2)
	else:
		print("((((Normal Receipt))))")
		print(holdcheck)
		return(1)


def normalRec(infolist, normalID):
	listpoint = 0
	p = printer.Usb(0x04b8,0x0202, normalID)
	p.set(align='center')
	p.image("logo.png")
	p.text("\n")
	while listpoint < len(infolist)-1:
		printline = str(infolist[listpoint])
		if printline.isspace() == False:
			p.text(printline)
			if listpoint <= 3:
				p.text("\n")
		listpoint+=1
	p.cut()
	printer.Usb.close(p)
	return()

def stickyRec(infolist, stickID):
	listpoint = 0
	p = printer.Usb(0x04b8,0x0202, stickID)
	p.set(align='center')
	print(infolist)
	testVar = 0
	current_date = datetime.now().date()	
	future_date = current_date + timedelta(days=4)	
	formatted_date = datetime.strftime(future_date, "%m/%d/%Y")	
	future_date = "\nHold expires: "+str(formatted_date)	
	p.text(future_date)
	while listpoint < len(infolist)-1:
		if testVar != -1:
			username = infolist[nameLine]
			username = username
			nameImage(username, p)
			p.text("\n\n\n")
			p.image("username.png")
			p.text("\n\n\n")
			testVar = -1
		elif listpoint == holdLine or listpoint == titleLine or listpoint == authorLine or listpoint == barcodeLine or listpoint == deweyLine:
			p.text(infolist[listpoint])
		listpoint+=1
	p.cut()
	printer.Usb.close(p)
	return()

def nameImage(name, p):
	# get an image
	base = Image.open('test.png').convert('RGBA')

	txt = Image.new('RGBA', base.size, (255,255,255,0))


	# get a drawing context
	d = ImageDraw.Draw(txt)


	W, H = (100,150)
	msglen = name.find(", ")
	if msglen <= 4:
		fnt = ImageFont.truetype("arialbd.ttf", 90)
		msg = name[0:msglen] + ", " + name[msglen+2:msglen+3]
	else:
		fnt = ImageFont.truetype("arialbd.ttf", 90)
		msg = name[0:4] + ", " + name[msglen+2:msglen+3]
	w, h = d.textsize(msg)

	# draw text, full opacity
	d.text(((W-w)/2,(H-h)/2), msg, font=fnt, fill="#000")

	out = Image.alpha_composite(base, txt)

	out.save('username.png')



def checkblankreceipt(filename):
	with open(filename, 'r') as file:
		for line in file:
			if line.strip():  # Check if the line has non-whitespace content
				return(True)
		return(False)

def remove_headers(queuepath):
	with open(queuepath, 'r') as f:
		lines = f.readlines()

	if len(lines) >= 2 and lines[1].startswith("http"):
		# If the second line starts with "http", remove the first two lines
		del lines[:2]

		# Write the modified content back to the file
		with open(queuepath, 'w') as f:
			f.writelines(lines)
	else:
		pass

try:
	main()
except:
	logging.exception(str(datetime.now()) + ' - Got exception on main handler, logging in log.out ')
	raise
