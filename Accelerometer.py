#!/usr/bin/python

from math import pow, sqrt, floor
import numpy as np
import time
from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue

class Accelerometer(Thread):
    def __init__(self, quantum):
        Thread.__init__(self)
        self.daemon = True
        self.Sense = SenseHat()
        self.Sense.set_imu_config(False, False, True)
        self.cnt = 0
        self.quantum = quantum
        self.period = 50
        self.iters = self.quantum / self.period
        self.que = Queue(1024)
        self.dorun = True

    def run(self):
        while (self.dorun):
            i = self.iters
            max = Integer.MIN_VALUE
            min = Integer.MAX_VALUE
            sum = 0
            while (i > 0):
                acc = self.read_acc()
                sum = sum + acc
                if (max < acc):
                    max = acc
                if (min > acc):
                    min = acc
                i = i + 1
            dic = {'avg': (sum/self.iters), 'min': min, 'max': max}
            self.que.put(dic)
            time.sleep(self.quantum)

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

    def stopit(self):
        self.dorun = False
        
    def getNext(self):
            try:
                return self.que.get(True, timeout=5)    
            except:
                print("Exception")

    def read_queue(self):
        yield self.que.get(True, None)





