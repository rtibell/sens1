#!/usr/bin/python

from math import pow, sqrt, floor
import numpy as np
import time
from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue

class Accelorometer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.Sense = SenseHat()
        self.Sense.set_imu_config(False, False, True)
        self.cnt = 0
        self.que = Queue(1024)
        self.dorun = True

    def run(self):
        while (self.dorun):
            self.Queue.put(self.read_acc())
            self.report()
            print(self.Queue.qsize())
#            time.sleep(0.1)
            time.sleep(5)

    def read_acc(self):
        a1 = self.Sense.get_accelerometer_raw()
        self.acc = a1
        return a1

    def get(self):
        return [self.get_x(), self.get_y(), self.get_z()] 

    def get_x(self):
        return self.acc['x']

    def get_y(self):
        return self.acc['y']

    def get_z(self):
        return self.acc['z']

    def get_len(self):
        self.Length = sqrt(pow(self.get_x(),2) + pow(self.get_y(),2) + pow(self.get_z(),2))
        return self.Length

    def report(self):
        print(self.get_x())
        print(self.get_y())
        print(self.get_z())
        print(self.get())
        print(self.get_len())

    def read_queue(self):
        yield self.Queue.get(True, None)





