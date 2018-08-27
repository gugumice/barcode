# barcode
reads barcode from scanner (currently HT-300) and prints it on ZEBRA TLP-2824
This version tested on PiIII, RASPBIAN STRETCH LITE
Version:June 2018

Requires CUPS, ZEBRA (https://pypi.org/project/zebra/)

https://drupalista.net/blog/raspberry-pi-install-printer-raspbian-lite

$ sudo apt-get install cups cups-bsd
cups-bsd IMPORTANT for lpr to function

CUPS printer setup:
Choose ZEBRA, set Make to RAW

If more than one printer is configured, programm asks which printer to use
