from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue
ACC_SCALE = 8
RUCK_SCALE = 64
BLK = [0, 0, 0]  # Black
RED = [255, 0, 0]  # Red
GRE = [0, 255, 0]   # Green
BLU = [0, 0, 255]   # Blue
WHI = [255, 255, 255]  # White
INIT_DSP = [
                        RED, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK,
                        BLK, BLK, BLK, BLK, BLK, BLK, BLK, WHI
                        ]

class Display(Thread):
    def __init__(self, prod):
        Thread.__init__(self)
        self.daemon = True
        self.prod = prod
        self.dorun = True
        self.Sense = SenseHat()
        self.Sense.clear()
        self.DSPbuff = INIT_DSP
        self.color_scale = self.colorScale(RUCK_SCALE)
        self.Sense.low_light = True
    
    def colorScale(self, size):
        buff = [None] * 64
        for i in range(0, size):
            buff[i] = [(255*i)/size, (255*(size-i))/size]
        return buff
    
    def dsp(self):
        self.Sense.set_pixels(self.DSPbuff)
        
    def setValue(self, acc_value, ruck_value):
        """ setValue in last column of the display. Acceleration as bar hight and ruck as colors.
                acc_value - Acceleration number between 0 and 7
                ruck_value - Ruck value between 0 and 63
        """
        c = 7
        for r in range(7-acc_value,8):
            self.DSPbuff[c+8*r] = self.color_scale[ruck_value]
        
    def shiftL(self):
        for c in range(0,7):
            for r in range(0,8):
                #print("r={} c={}".format(r,c))
                self.DSPbuff[c+8*r] = self.DSPbuff[(c+1)+8*r]
        self.clrColumn(7)
                
    def clrColumn(self, c):
        for r in range(0,8):
            self.DSPbuff[c+8*r] = BLK
        
    def run(self):
        print("Running Cons")
        self.dsp()
        while (self.dorun):
            next = self.prod.getNext()
            print('{} {}'.format('Cons', next))
            acc_max = next[0]['max']
            ruck = next[1]['max']
            self.shiftL()
            self.dsp()
        print("Stopping Cons")
        
    def stopit(self):
        self.dorun = False