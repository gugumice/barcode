#!/usr/bin/env python
from queue import Queuequeue.LifoQueue
from threading import Thread, Event
from time import sleep
from random import randint
# A thread that produces data
def producer(out_q):
    while True:
        data=randint(1,51)
        print(data)
        sleep(.2)
        # Make an (data, event) pair and hand it to the consumer
        if data == 5:
            print('data sent {}'.format(data))
            evt = Event()
            out_q.put((data, evt))
            # Wait for the consumer to process the item
            evt.wait()
# A thread that consumes data
def consumer(in_q):
    print('consumer waiting')
    while True:
        # Get some data
        data, evt = in_q.get()
        # Process the data
        
        print('Data received {}'.format(data))
        sleep(5)
        # Indicate completion
        evt.set()
def main():
    #q = Queue.LifoQueue(maxsize=1)
    q = Queue.LifoQueue()
    t1 = Thread(target=consumer, args=(q,))
    t2 = Thread(target=producer, args=(q,))
    t1.start()
    t2.start()
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
