
#!/usr/bin/python3
import sys
from time import sleep
from threading import Thread

class FileLoaderThread(Thread):
   def __init__(self, fileName, encryptionType):
       # Call the Thread class's init function
       Thread.__init__(self)
       self.fileName = fileName
       self.encryptionType = encryptionType

   # Override the run() function of Thread class
   def run(self):
       print('Started loading contents from file : ', self.fileName)
       print('Encryption Type : ', self.encryptionType)
       for i in range(5):
           print('Loading ... ')
           sleep(1)
       print('Finished loading contents from file : ', self.fileName)

th = FileLoaderThread('users.csv','ABC')
th.start()

# print some logs in main thread
for i in range(5):
   print('Hi from Main Function')
   sleep(1)

# wait for thread to finish
th.join()

