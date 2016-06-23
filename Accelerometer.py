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
        self.l_min = lambda x,y: min(self.calc_len(x),self.calc_len(y))
        self.l_max = lambda x,y: max(self.calc_len(x),self.calc_len(y))
        self.l_sum = lambda x,y: self.calc_len(x) + self.calc_len(y)


    def run(self):
        print("Calibrating...")
        self.adjust()
        print("Calibration done! adjust={}".format(self.acc_bias))

        acc_first = self.read_acc()
        while (self.dorun):
            i = self.iters
            sum = 0.0
            acc_list = []
            while (i > 0):
                print(acc_first)
                adj = self.adjAcc([acc_first['x'], acc_first['y'], acc_first['z']])
                print(adj)
                acc_list.append(adj)
                print(acc_list)
                i = i - 1
                time.sleep(self.period)
                acc_first = self.read_acc()
            max = reduce(self.l_max, acc_list)
            min = reduce(self.l_min, acc_list)
            sum = reduce(self.l_sum, acc_list)
            print(sum)
            ruck_avg = sqrt(pow(acc_list[0][0]-acc_list[-1][0], 2)+pow(acc_list[0][1]-acc_list[-1][1], 2)+pow(acc_list[0][2]-acc_list[-1][2], 2))/self.quantum
#            ruck_max = sqrt(pow(acc_max['x']-acc_min['x'], 2)+pow(acc_max['y']-acc_min['y'], 2)+pow(acc_max['z']-acc_min['z'], 2))/(abs(acc_min_i-acc_max_i)*self.period)
            acc_dic = {'avg': (sum/float(len(acc_list))), 'min': min, 'max': max}
#            ruck_dic = {'avg': ruck_avg, 'max': ruck_max}
#            self.que.put([dt.datetime.now().strftime('%Y%m%d %H:%M.%S.%f'), 
#                          acc_dic, ruck_dic, acc_list[0], cc_list[-1]])
            

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
            x += rd['x']
            y += rd['y']
            z += rd['z']
            time.sleep(0.001)
        self.acc_bias = [x/100.0, y/100.0, z/100.0]
        

    def read_acc(self):
        a1 = self.Sense.get_accelerometer_raw()
        self.writeBinLog(a1)
        return a1

    def get(self):
        return [self.get_x(), self.get_y(), self.get_z()] 

    def calc_len(self, acc):
        return sqrt(pow(acc[0], 2) + pow(acc[1], 2) + pow(acc[2], 2))


    def adjAcc(self, acc):
        return [acc[0]-self.acc_bias[0], acc[1]-self.acc_bias[1], acc[0]+(Gdelta-self.acc_bias[0])]


    def stopit(self):
        self.dorun = False
        
    def getNext(self):
            try:
                return self.que.get(True, timeout=5)    
            except:
                print("Exception")

    def read_queue(self):
        yield self.que.get(True, None)





