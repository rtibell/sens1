from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue

class Display(Thread):
    def __init__(self, prod):
        Thread.__init__(self)
        self.daemon = True
        self.prod = prod
        self.dorun = True
        
    def run(self):
        print("Running Cons")
        while (self.dorun):
            print('{} {}'.format('Cons', self.prod.getNext()))
        print("Stopping Cons")
        
    def stopit(self):
        self.dorun = False