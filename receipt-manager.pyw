import tkinter as tk
from tkinter import messagebox
from subprocess import Popen
import shutil
import psutil
import os

# Check if pid.txt exists
if not os.path.exists("pid.txt"):
    # Create pid.txt
    with open("pid.txt", "w") as file:
        file.write("11111")

# Read the PID from pid.txt
with open("pid.txt", "r") as file:
    pid = int(file.read())

# Check if the process with the provided PID exists and is named "python.exe"
if psutil.pid_exists(pid):
    process = psutil.Process(pid)
    if process.name() == "pythonw.exe":
        messagebox.showerror('Error: Already Open', 'Receipt Manager is already open!')
        quit()

# Overwrite pid.txt with this process's own PID
current_pid = os.getpid()
with open("pid.txt", "w") as file:
    file.write(str(current_pid))

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
        process = psutil.Process(os.getpid())
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

def terminate_edge():
    for process in psutil.process_iter():
        try:
            # Check if the process name contains "msedge" or "msedgewebview2"
            while "msedge" in process.name().lower() or "msedgewebview2" in process.name().lower():
                # Terminate the process
                process.terminate()
                print("Microsoft Edge process terminated.")
                break  # Stop checking for more instances
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def bookdropBrowser():
    terminate_edge()
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    kiosk_printing_flag = "--kiosk-printing"
    url = "https://staff-rclstn.bywatersolutions.com/"
    Popen([edge_path, kiosk_printing_flag, url])


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
    bg="dark goldenrod",
    fg="white",
    command=print_last,
)
swapButton = tk.Button(
    text="Swap Printers",
    width=25,
    height=2,
    bg="goldenrod",
    fg="white",
    command=swap_printers,
)
bookdropButton = tk.Button(
    text="Open Bookdrop Browser",
    width=25,
    height=2,
    bg="NavajoWhite3",
    fg="white",
    command=bookdropBrowser,
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
bookdropButton.pack()
exitButton.pack()

window.protocol("WM_DELETE_WINDOW", quit_program)
window.mainloop()
