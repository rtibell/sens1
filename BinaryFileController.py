from threading import Thread
from multiprocessing import Queue
import datetime as dt
import time

class BinaryFileController(Thread):
    def __init__(self, period):
        Thread.__init__(self)
        self.daemon = True
        self.cnt = 0
        self.period = period
        self.que = Queue(1024*8)
        self.dorun = True

    def run(self):
        while (self.dorun):
            time.sleep(self.period)
            tm = dt.datetime.now().strftime('%Y%m%d_%H.bin')
            with open(tm, 'ab') as f:
                while (self.que.empty() == False):
                    entry = self.getNext()
                    self.writeFile(f, entry)
                    f.closed

    def writeFile(self, file, entry):
        file.write(entry)

    def stopit(self):
        self.dorun = False
        
    def getNext(self):
            try:
                return self.que.get(True, timeout=60)    
            except:
                print("Exception")

    def read_queue(self):
        yield self.que.get(True, None)
        
    def putNext(self, entry):
        self.que.put_nowait(entry)