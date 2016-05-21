#!/usr/bin/python

import time
from threading import Timer
from sense_hat import SenseHat


def doit():
    sched = Timer(1, doit)
    sched.start()
    root()

def init():
    doit()
#    time.sleep(30)
    
def root():
    sense = SenseHat()
    temp1 = sense.get_temperature()   
    temp2 = sense.get_temperature_from_pressure() 
    pressure = sense.get_pressure()
    north = sense.get_compass()
    accel_only = sense.get_accelerometer()
    acc_raw = sense.get_accelerometer_raw()
    temp = "Temp {:10.4f}".format(temp1) + " {:10.4f}".format(temp2) 
    other = "Pres {:10.4f}".format(pressure) + " Compas {:10.4f}".format(north)
    acc1 = "p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only)
    acc2 = "x: {x}, y: {x}, z: {z}".format(**acc_raw)
    print temp + "\n" + other + "\n" + acc1 + "\n" + acc2 + "\n"


if __name__ == '__main__':
    init()
