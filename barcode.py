#!/usr/bin/python
from zebra import zebra
from string import Template
import logging, sys, socket, time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Basic label design is saved to tile and can be customised.
LBL_FILE='lblTemplate.txt'
#Number of copies to print after each scan
COPIES=1
#Sets max length for barcode
MAXLEN=11

#class for barcode reader

class bcr(object):
        def __init__(self, device='/dev/ttyACM0'):
                self.bc=[]
                try:
                        self.fp=open(device, 'rb')
                except:
                        print('Canot open: {}'.format(device))
                        sys.exit(1)
        def readBC(self):
                self.bc=[]
                done=False
                while not done:
                        buffer=self.fp.read(2)
                        for c in buffer:
                                #print(c, ord(c))
                                if ord(c)==10:
                                        done=True
                                        buffer=''
                                        break;
                                else:
                                        if 32 <= ord(c) <= 127:
                                                self.bc += c
                return("".join( self.bc ))

#class for printing labels

class lbl(object):
        def __init__(self, queue=1):
                self.zebra=zebra()
                self.lblText=''
                try:
                        self.zebra.setqueue(self.zebra.getqueues()[queue])
                except:
                        logging.debug('Queue {} not found!'.format(queue))
                        sys.exit(1)
                try:
                        with open(LBL_FILE) as f:
                                self.lblText=f.read()
                        logging.debug('Reading from {}'.format(LBL_FILE))
                except:
                        logging.debug('Error reading from {}. Using defaults'.format(LBL_FILE))
                        self.lblText='''
^XA
^LH100,10^MTT,^BY2,3
^FO0,0
^AS
^FDEGL^FS
^FO0,35
^AQ
^FD$hostName ^FS
^FO0,65
^GB200,2,2
^FS
^FO0,70
^BCN,70,Y,N,N,D
^FD$barCode ^FS
^PQ$numCopies
^XZ
'''
                        self.lblSave()

        def lblSave(self):
                try:
                        with open(LBL_FILE,'w') as f:
                                f.write(self.lblText)
                except:
                        logging.debug('Cannot write to {}'.format(LBL_FILE))

        def lblPrint(self, barCode="12345678", numCopies=1):
                t=Template(self.lblText)
                #print(self.__cleanBc(barCode))
                lblStr=t.substitute(hostName=socket.gethostname(), barCode=self.__cleanBc(barCode), numCopies=numCopies)
                self.zebra.output(lblStr)
        #Allows only ASCII 32-127 and sets MAXLEN
        def __cleanBc(self, barCode):
                b=[]
                for s in barCode:
                        if 32 <= ord(s) <=127:
                                b += s
                return("".join(b)[:MAXLEN])

if __name__ == '__main__':
        z=zebra()
        zQueues=z.getqueues()
        q=0
        i=0
        #If more than one printer set up in CUPS - asks for target
        if(len(zQueues))==1:
                z.setqueue(zQueues[0])
                logging.debug('Printer: {}'.format(zQueues[0]))
        else:
                for q in zQueues:
                        i+=1
                        print('{}. {}'.format(i,q))
                try:
                        q=input('Select printer ({}):'.format(i))
                except:
                        q=i
                        if  not 0 <= q-1 <= i-1:
                                print('{} - invalid option'.format(q))
                                z=None
                                sys.exit(1)
        print('<{}> selected'.format(zQueues[q-1]))
        lb=lbl(q-1)
        bc=bcr()
        done = False
        try:
                while not done:
                        lb.lblPrint(bc.readBC(), COPIES)
                        time.sleep(1)
        except KeyboardInterrupt:
                print('Interrupted')
