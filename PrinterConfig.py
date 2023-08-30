# PrinterConfig.py
# The main program must be restarted after changes

#Change printerOrientation if receipts are coming out of the wrong printer [TRUE BY DEFAULT]
printerOrientation = True


###holdReceiptText determines the text to search to determine a Sticky Receipt
holdReceiptText = "Hold"
#holdLine is the line that the above text is on, with 0 being the first line
holdLine = 1
#info used to decipher information from hold receipts
nameLine = 2
#line that stores the book title
titleLine = 9
#line that stores the author's name
authorLine = 10
#line that stores the barcode number of the item
barcodeLine = 11
#line that stores the dewey decimal identifier for the item
deweyLine = 12
