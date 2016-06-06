#!/usr/bin/python

from math import pow, sqrt, floor
import numpy as np
import time
import threading
from sense_hat import SenseHat

X = [255, 0, 0]  # Red
O = [255, 255, 255]  # White
cols = [
[128,128,128],
[0,255,0],
[64,255,0],
[128,255,0],
[192,255,0],
[255,255,0],
[255,192,0],
[255,128,0],
[255,64,0],
[255,0,0]
]

def doit():
    old = root()
    for i in range(0,64):
        acc = root()
        x = old['x'] - acc['x']
        y = old['y'] - acc['y']
        z = old['z'] - acc['z']
        len = sqrt(pow(x,2) + pow(y,2) + pow(z,2))
        abslen = int(floor(len*5))
        if abslen > 9:
            abslen = 9
            print "*** Over Flow ***"
        dsp_mtx[i] = cols[abslen]
        print i
        print "{:10.4f}".format(x) + " {:10.4f}".format(y) + " {:10.4f}".format(z) + " {:10.4f}".format(len) + "  --  "
        old = acc
	print avg()
        dsp()
        time.sleep(0.1)

def avg():
    arr = [None]*10
    for i in range(0,10):
        acc = root()
        x = acc['x']
        y = acc['y']
        z = acc['z']
        arr[i] = [x,y,z]
    print arr
    return np.average(arr)

def init():
    global dsp_mtx
    dsp_mtx = [
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
    [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] 
    ]
    sense = SenseHat()
    sense.set_imu_config(False, False, True)
    global sense
    tt = threading.Thread(target=doit)
    tt.daemon = True
    tt.start()
    print "start sleeping..."
    time.sleep(64)
    
def root():
    acc_raw = sense.get_accelerometer_raw()
    acc2 = "x: {x:10.4f}, y: {y:10.4f}, z: {z:10.4f}".format(**acc_raw)
    return acc_raw

def dsp():
    sense.set_pixels(dsp_mtx)
    

if __name__ == '__main__':
    init()
