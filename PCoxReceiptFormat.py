from escpos import *
import os.path
import os
import time
from PIL import Image, ImageDraw, ImageFont
from PrinterConfig import *
""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """



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
			mainProc(queuepath)
			os.replace(queuepath, lastprint)
		else:
			raise ValueError("%s isn't a file!" % queuepath)


def mainProc(queuepath):
	with open(queuepath) as f:
		listpoint = 0
		infolist= [""]
		
		for lines in f:
			infloc=-1
			infloc = lines.find('c="')
			endterm = lines.find('</span>')
			if infloc != -1:
				infloc+=3
				infend = infloc + 1
				infchar = lines[infloc:infend]
				infolist[listpoint] = infolist[listpoint] + infchar
			elif endterm != -1:
				print("[" + str(listpoint) + "] " + infolist[listpoint])
				listpoint +=1
				infolist.append("")
		printer = recType(infolist)
		#UNTIL CONFIG FILE, THIS IS MANUALLY SET :: >>MUST DELETE AFTER<<
		#printerOrientation = True
		
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
	typevar = infolist[normalLine].find(normalReceiptText)
	billcheck = infolist[billLine].find(billReceiptText)
	if typevar != -1 or billcheck != -1:
		print("((((Normal Receipt))))")
		print(billcheck)
		return(1)
	else:
		print("<<<<Sticky Receipt>>>>")
		print(billcheck)
		return(2)


def normalRec(infolist, normalID):
	listpoint = 2
	p = printer.Usb(0x04b8,0x0202, normalID)
	p.set(align='center')
	p.image("logo.png")
	p.text("\n")
	while listpoint < len(infolist)-1:
		printline = str(infolist[listpoint])
		p.text(printline)
		p.text("\n")
		listpoint+=1
	p.cut()
	return()
	
def stickyRec(infolist, stickID):
	listpoint = 0
	p = printer.Usb(0x04b8,0x0202, stickID)
	p.set(align='center')
	while listpoint < len(infolist)-1:
		userfield = infolist[listpoint].find("User name")
		if userfield != -1:
			username = infolist[listpoint]
			username = username[userfield+11:len(username)]
			nameImage(username, p)
			p.text("\n\n\n")
			p.image("username.png")
			p.text("\n\n\n")
			middlename = infolist[listpoint+1].find("Phone number")
			if middlename == -1:
				listpoint+=1
		else:
			printline = str(infolist[listpoint])
			p.text(printline)
			p.text("\n")
		listpoint+=1
	p.cut()
	return()

def nameImage(name, p):
	# get an image
	base = Image.open('test.png').convert('RGBA')

	txt = Image.new('RGBA', base.size, (255,255,255,0))

	# get a font
	#fnt = ImageFont.truetype("arial.ttf", 100)
	# get a drawing context
	d = ImageDraw.Draw(txt)

	#LINE BELOW IS FOR TESTING, PLEASE DELETE
	#name="ReallyLongNameMan, Jacqueline"


	W, H = (100,150)
	msglen = name.find(", ")
	if msglen <= 6:
		fnt = ImageFont.truetype("arial.ttf", 90)
		msg = name[0:msglen] + ", " + name[msglen+2:msglen+4] 
	elif msglen > 6 and msglen < 12:
		fnt = ImageFont.truetype("arial.ttf", 75)
		msg = name[0:msglen] + ", " + name[msglen+2:msglen+4] 
	else:
		fnt = ImageFont.truetype("arial.ttf", 70)
		msg = name[0:12] + "., " + name[msglen+2:msglen+4]
	w, h = d.textsize(msg)

	# draw text, full opacity
	d.text(((W-w)/2,(H-h)/2), msg, font=fnt, fill="#000")

	out = Image.alpha_composite(base, txt)

	out.save('username.png')
	#line below enables printing of full name on hold slips
	#p.text(name)




main()
