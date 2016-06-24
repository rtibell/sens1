#!/usr/bin/python

from math import pow, sqrt, floor, degrees, atan2, sin, cos, tan
import sys
import numpy as np
import time
import datetime as dt
from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue

#
# Lambdas
#
l_min = lambda x,y: min(x, y)
l_max = lambda x,y: max(x, y)
l_sum = lambda x,y: x + y

#
# Constants
#
Gsto = 9.82436
Gs = 9.80665
Gdelta = Gsto/Gs
IDmtx = [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]

class Accelerometer(Thread):

    def __init__(self, quantum, bin_logger):
        Thread.__init__(self)
        self.daemon = True
        self.Sense = SenseHat()
        self.Sense.set_imu_config(False, False, True)
        self.cnt = 0
        self.quantum = quantum
        self.period = 0.01
        self.iters = int(self.quantum / self.period)
        self.que = Queue(1024)
        self.dorun = True
        self.acc_bias = [0.0, 0.0, 0.0]
        self.Rmtx = IDmtx
        self.bin_logger = bin_logger
        #
        # Lambdas
        #
        self.l_len = lambda x: self.calcLen2d(x)

    def run(self):
        print("Calibrating...")
        self.adjust()
        print("Calibration done! adjust={}".format(self.acc_bias))
        print("quantum={} period={} iters={}".format(self.quantum, self.period, self.iters))
        acc_first = self.read_acc()
        while (self.dorun):
            i = self.iters
            sum = 0.0
            acc_list = []
            while (i > 0):
                adj = self.adjAcc(acc_first)
                acc_list.append(adj)
                i = i - 1
                time.sleep(self.period)
                acc_first = self.read_acc()
            acc_len_list = map(self.l_len, acc_list)
            max = reduce(l_max, acc_len_list)
            min = reduce(l_min, acc_len_list)
            sum = reduce(l_sum, acc_len_list)
            avg = sum/float(len(acc_list))
            ruc_len_list = map(lambda x,y: (x+y)/self.period,acc_len_list[1:], acc_len_list[:-1])
            ruck_max = reduce(l_max, ruc_len_list)
            ruck_min = reduce(l_min, ruc_len_list)
            ruck_sum = reduce(l_sum, ruc_len_list)
            ruck_avg = ruck_sum/float(len(ruc_len_list))
            print(sum)
            ruck_avg = sqrt(pow(acc_list[0][0]-acc_list[-1][0], 2)+pow(acc_list[0][1]-acc_list[-1][1], 2)+pow(acc_list[0][2]-acc_list[-1][2], 2))/self.quantum
            acc_dic = {'avg': avg, 'min': min, 'max': max}
            ruck_dic = {'avg': ruck_avg, 'max': ruck_max}
            self.que.put([dt.datetime.now().strftime('%Y%m%d %H:%M.%S.%f'), 
                          acc_dic, ruck_dic, acc_list[0], acc_list[-1]])
            

    def writeBinLog(self, entry):
        if (self.bin_logger == None):
            return
        else:
            self.bin_logger.putNext([dt.datetime.now().strftime('%Y%m%d %H:%M.%S.%f'), entry])

    def adjust(self):
        ac = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        for i in range(0,100):
            rd = self.read_acc()
            x += rd[0]
            y += rd[1]
            z += rd[2]
            time.sleep(0.001)
        self.acc_bias = [x/100.0, y/100.0, z/100.0]
        

    def read_acc(self):
        a1 = self.Sense.get_accelerometer_raw()
        self.writeBinLog(a1)
        return [a1['x'], a1['y'], a1['z']]

    def get(self):
        return [self.get_x(), self.get_y(), self.get_z()] 

    def calcLen(self, acc):
        return sqrt(pow(acc[0], 2) + pow(acc[1], 2) + pow(acc[2], 2))

    def calcLen2d(self, acc):
        return sqrt(pow(acc[0], 2) + pow(acc[1], 2))

    def adjAcc(self, acc):
        return [acc[0]-self.acc_bias[0], acc[1]-self.acc_bias[1], acc[0]+(Gdelta-self.acc_bias[0])]


    def stopit(self):
        self.dorun = False
        
    def getNext(self):
            try:
                return self.que.get(True, timeout=15)    
            except:
                print("Exception")

    def read_queue(self):
        yield self.que.get(True, None)





