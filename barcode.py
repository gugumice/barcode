
#!/usr/bin/python
from zebra import zebra
from string import Template
import logging, sys, socket
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

LBL_FILE='lblTemplate.txt'
COPIES=1

#class for barcode reader

class bcr(object):
        def __init__(self, device='/dev/ttyACM0'):
                self.bc=()
                try:
                        self.fp=open(device, 'rb')
                except:
                        print('Canot open: {}'.format(device))
                        sys.exit(1)
        def readBC(self):
                buffer=self.fp.readline()
                return(buffer.strip('\n'))

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
^LH20,10^MTT
^FO0,0
^AS
^FDEGL^FS
^FO0,35
^AQ
^FD$hostName ^FS
^FO30,150
^AS
^FD$barCode^FS
^FO0,65
^GB200,2,2
^FS
^BY2,3,105
^FT20,150
^BCN,80,N,N
^FD>;$barCode^FS
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

        def __cleanBc(self, barCode):
                b=[]
                for s in barCode:
                        if 32 <= ord(s) <=127:
                                b += s
                return("".join(b))

if __name__ == '__main__':
        z=zebra()
        zQueues=z.getqueues()
        q=0
        i=0
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
        lblPref=''
        lblStr=''
        try:
                while not done:
                        lblStr=(bc.readBC())
                        if len(lblStr)>0:
                                if lblStr[0]=="#":
                                        lblPref=lblStr[1:]
                                        lblStr=''
                                else:
                                        #print('{}'.format(pref+s))
                                        #print('{}, type-{}, len-{}'.format(s, type(s),len(s)))
                                        lb.lblPrint(lblPref+lblStr, COPIES)
                                        lblPref=''

        except KeyboardInterrupt:
                print('Interrupted')
