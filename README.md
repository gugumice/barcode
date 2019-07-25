# barcode
reads barcode from scanner (currently HT-300) and prints it on ZEBRA TLP-2824
This version tested on PiIII, RASPBIAN STRETCH LITE
Version:June 2018

Requires CUPS, ZEBRA (https://pypi.org/project/zebra/)

https://drupalista.net/blog/raspberry-pi-install-printer-raspbian-lite

$ sudo apt-get install
! Cups-bsd is IMPORTANT for lpr to function

CUPS printer setup:
- sudo cupsctl --remote-admin --remote-anyifconfig
- Choose ZEBRA
- Set Make to RAW

Auto run un startup:

- sudo cp barcode.service /etc/systemd/system/barcode.service
- sudo systemctl enable barcode.service

Disable auto run:
- sudo systemctl disable barcode.service

If more than one printer is configured in CUPS, script will ask which printer to use for labels.
