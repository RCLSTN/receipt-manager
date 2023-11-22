# RCLSTN Receipt Manager 
Python program for handling, formatting, and printing receipts

![Windows](https://img.shields.io/badge/OS-Windows-blue.svg)
![Ver](https://img.shields.io/badge/Version-2.2.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.6-blue.svg)

Contact information may be found in the directory on [our website](https://rclstn.org/directorylisting).
###### Currently developed specifically for use in the Rutherford County Library System
###### Designed for use with Epson TM-T88IV printers, including ReStick versions
###### Should be compatible with [ the printers in this database ](https://mike42.me/escpos-printer-db/#profiles) but hasn't been tested

### Dependencies:
- tkinter
- PIL
- modified version of [EscPos 2.2.0](https://github.com/RCLSTN/python-escpos)
- [Zadig](https://zadig.akeo.ie/) for USB driver installation
- Utilizes Generic Windows Text Only driver to convert print jobs to text (shown in printer_setup.png)

### Setup:
```
1. Install python

2. Run "pip install python-escpos" in cmd

3. Locate python-escpos folder and replace printer.py with the modified printer.py

4. Use zadig following instructions in zadig.png for one or both printers

5. Create folder "C:\queue\pcoxPrint" and place receipt-manager files within it

6. Use a shortcut to launch "receipt-manager.pyw" or use the provided shortcut
```


#### To-do:
- Add support for additional printers

