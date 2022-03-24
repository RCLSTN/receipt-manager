import tkinter as tk
from subprocess import Popen
import shutil
#import tkMessageBox

def printer_enabled():
    print("Printers starting...")
    global process
    process = Popen("pythonw C:\queue\pcoxPrint\PCoxReceiptFormat.py")
    status['text'] = 'Printer status:\nSTARTED'
    status['bg'] = 'springgreen3'
    button['text'] = 'Stop Receipt Printers'
    button['bg'] = 'red'
    button['command'] = printer_disabled
    button.pack()

def printer_disabled():
    print("Printers stopping...")
    process.terminate()
    status['text'] = 'Printer status:\nSTOPPED'
    status['bg'] = 'orangered2'
    button['text'] = 'Start Receipt Printers'
    button['bg'] = 'green'
    button['command'] = printer_enabled
    button.pack()
    
def quit_program():
    if 'process' in globals():
        print("Stopping process")
        process.terminate()
    window.destroy()

def print_last():
    queuepath = (r"C:\queue\job.txt")
    lastprint = (r"C:\queue\last\job.txt")
    shutil.copyfile(lastprint, queuepath)

def swap_printers():
    if 'process' in globals():
        printer_disabled()
    printer_enabled()
    file = open("PrinterConfig.py", "r")
    replacement = ""
    for line in file:
        line = line.strip()
        if line == "printerOrientation = True":
            changes = line.replace("printerOrientation = True", "printerOrientation = False")
            replacement = replacement + changes + "\n"
        elif line == "printerOrientation = False":
            changes = line.replace("printerOrientation = False", "printerOrientation = True")
            replacement = replacement + changes + "\n"
        else:
            replacement = replacement + line + "\n"
    file.close()
    fout = open("PrinterConfig.py", "w")
    fout.write(replacement)
    fout.close()


window = tk.Tk()
window.title("RCLS Receipt Manager")
window.iconbitmap(r"receipt-printer.ico")
label = tk.Label(text="RCLS Receipt Manager v1.0")

status = tk.Label(
    text="Printer status:\nSTOPPED",
    fg="white",
    bg="orangered2",
    width=25,
    height=3
)

button = tk.Button(
    text="Start Receipt Printers",
    width=25,
    height=5,
    bg="green",
    fg="white",
    command=printer_enabled,
)
reprintButton = tk.Button(
    text="Reprint Last Receipt",
    width=25,
    height=2,
    bg="goldenrod",
    fg="white",
    command=print_last,
)
swapButton = tk.Button(
    text="Swap Printers",
    width=25,
    height=2,
    bg="slate gray",
    fg="white",
    command=swap_printers,
)
exitButton = tk.Button(
    text="Exit Receipt Manager",
    width=25,
    height=2,
    bg="slate gray",
    fg="white",
    command=quit_program,
)
label.pack()
status.pack()
button.pack()
reprintButton.pack()
swapButton.pack()
exitButton.pack()

window.protocol("WM_DELETE_WINDOW", quit_program)
window.mainloop()
