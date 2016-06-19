from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue
import datetime as dt

ACC_SCALE = 8
RUCK_SCALE = 64

R = [255, 0, 0]  # Red
O = [255, 127, 0] # Orange
Y = [255, 255, 0] # Yellow
G = [0, 255, 0]   # Green
B = [0, 0, 255]   # Blue
I = [75, 0, 130]
V = [159, 0, 255]
E = [0, 0, 0]  # Black

WHI = [255, 255, 255]  # White
INIT_DSP = [
            E,E,E,Y,Y,E,E,E,
            E,E,Y,G,G,Y,E,E,
            E,Y,G,O,O,G,Y,E,
            Y,G,O,V,V,O,G,Y,
            Y,G,O,V,V,O,G,Y,
            E,Y,G,O,O,G,Y,E,
            E,E,Y,G,G,Y,E,E,
            E,E,E,Y,Y,E,E,E]

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
            buff[i] = [(255*i)/size, (255*(size-i))/size, 0]
        return buff
    
    def dsp(self):
        self.Sense.set_pixels(self.DSPbuff)
        
    def scaleAcc(self, value):
        v = value
        if (value > 8):
            v = 8
        return v
    
    def scaleRuck(self, value):
        v = value*64/(128)
        if (v > 63):
            v = 63
        return v
    
    def setValue(self, acc_value, ruck_value):
        """ setValue in last column of the display. Acceleration as bar hight and ruck as colors.
                acc_value - Acceleration number between 0 and 7
                ruck_value - Ruck value between 0 and 63
        """
        #print("a={} r={}".format(acc_value, ruck_value))
        if (acc_value == 0 & ruck_value == 0):
            return
        c = 7
        for r in range(7-acc_value+1,8):
            #print("c={} r={}".format(c,r))
            #print( self.color_scale[ruck_value])
            self.DSPbuff[c+8*r] = self.color_scale[ruck_value]
        
    def shiftL(self):
        for c in range(0,7):
            for r in range(0,8):
                #print("r={} c={}".format(r,c))
                self.DSPbuff[c+8*r] = self.DSPbuff[(c+1)+8*r]
        self.clrColumn(7)
                
    def clrColumn(self, c):
        for r in range(0,8):
            self.DSPbuff[c+8*r] = E
        
    def run(self):
        print("Running Cons")
        self.dsp()
        while (self.dorun):
            next = self.prod.getNext()
            if (next == None):
                 self.dorun = False
            else:
                print('{} {}'.format(dt.datetime.now(), next))
                acc_max = next[0]['max']
                ruck = next[1]['max']
                self.shiftL()
                self.setValue(int(self.scaleAcc(acc_max)), int(self.scaleRuck(ruck)))
                self.dsp()
        print("Stopping Cons")
        
    def stopit(self):
        self.dorun = False