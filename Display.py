from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue

BLK = [0, 0, 0]  # Black
RED = [255, 0, 0]  # Red
GRE = [0, 255, 0]   # Green
BLU = [0, 0, 255]   # Blue
WHI = [255, 255, 255]  # White

class Display(Thread):
    def __init__(self, prod):
        Thread.__init__(self)
        self.daemon = True
        self.prod = prod
        self.dorun = True
        self.Sense = SenseHat()
        self.Sense.clear()
        self.DSPbuff = [
                        RED, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, WHI
                        ]
    
    def dsp(self):
        self.Sense.set_pixels(self.DSPbuff)
        
    def shiftL(self):
        for c in range(0,7):
            for r in range(0,8):
                print("r={} c={}".format(r,c))
                self.DSPbuff[c+8*r] = self.DSPbuff[(c+1)+8*r]
                
    def clrColumn(self, c):
        for r in range(0,8):
            self.DSPbuff[c+8*r] = BLK
        
    def run(self):
        print("Running Cons")
        self.dsp()
        while (self.dorun):
            print('{} {}'.format('Cons', self.prod.getNext()))
            self.shiftL()
            self.dsp()
        print("Stopping Cons")
        
    def stopit(self):
        self.dorun = False