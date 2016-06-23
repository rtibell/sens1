#!/usr/bin/python

from math import pow, sqrt, floor, degrees, atan2, sin, cos, tan
import sys
import numpy as np
import time
import datetime as dt
from sense_hat import SenseHat
from threading import Thread
from multiprocessing import Queue

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
        self.acc_offset = 0
        self.acc_bias = [0.0, 0.0, 0.0]
        self.Rmtx = IDmtx
        self.bin_logger = bin_logger

    def run(self):
        print("Calibrating...")
        self.adjust()
        print("Calibration done! adjust={}".format(self.acc_bias))

        acc_first = self.read_acc()
        while (self.dorun):
            i = self.iters
            max = -1000000000.0
            min = 1000000000.0
            sum = 0.0
            acc_list = []
            while (i > 0):
                acc_list.extend(self.adjAcc([acc_first['x'], acc_first['y'], acc_first['z']]))
                time.sleep
                acc_first = self.read_acc()
            print(acc_list)
            return
#                rd = self.read_acc()
#                av = self.get_adj_len()
#                sum = sum + av
#                if (max < av):
#                    max = av
#                    acc_max = rd
#                    acc_max_i = (self.iters - i)
#                if (min > av):
#                    min = av
#                    acc_min = rd 
#                    acc_min_i = (self.iters - i)
#                i = i - 1
#                time.sleep
#            acc_last = self.read_acc()
#            ruck_avg = sqrt(pow(acc_first['x']-acc_last['x'], 2)+pow(acc_first['y']-acc_last['y'], 2)+pow(acc_first['z']-acc_last['z'], 2))/self.quantum
#            ruck_max = sqrt(pow(acc_max['x']-acc_min['x'], 2)+pow(acc_max['y']-acc_min['y'], 2)+pow(acc_max['z']-acc_min['z'], 2))/(abs(acc_min_i-acc_max_i)*self.period)
#            acc_dic = {'avg': (sum/float(self.iters)), 'min': min, 'max': max}
#            ruck_dic = {'avg': ruck_avg, 'max': ruck_max}
#            self.que.put([dt.datetime.now().strftime('%Y%m%d %H:%M.%S.%f'), 
#                          acc_dic, ruck_dic, acc_first, acc_last])
            time.sleep(self.period)

    def old_run(self):
        print("Calibrating...")
        self.adjust()
        print("Calibration done!")
        while (self.dorun):
            i = self.iters
            max = -1000000000.0
            min = 1000000000.0
            sum = 0.0
            acc_first = self.read_acc()
            while (i > 0):
                rd = self.read_acc()
                av = self.get_adj_len()
                sum = sum + av
                if (max < av):
                    max = av
                    acc_max = rd
                    acc_max_i = (self.iters - i)
                if (min > av):
                    min = av
                    acc_min = rd 
                    acc_min_i = (self.iters - i)
                i = i - 1
                time.sleep
            acc_last = self.read_acc()
            ruck_avg = sqrt(pow(acc_first['x']-acc_last['x'], 2)+pow(acc_first['y']-acc_last['y'], 2)+pow(acc_first['z']-acc_last['z'], 2))/self.quantum
            ruck_max = sqrt(pow(acc_max['x']-acc_min['x'], 2)+pow(acc_max['y']-acc_min['y'], 2)+pow(acc_max['z']-acc_min['z'], 2))/(abs(acc_min_i-acc_max_i)*self.period)
            acc_dic = {'avg': (sum/float(self.iters)), 'min': min, 'max': max}
            ruck_dic = {'avg': ruck_avg, 'max': ruck_max}
            self.que.put([dt.datetime.now().strftime('%Y%m%d %H:%M.%S.%f'), 
                          acc_dic, ruck_dic, acc_first, acc_last])
            time.sleep(self.period)

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
            av = self.get_len()
            ac += av
            time.sleep(0.001)
        self.acc_offset = ac/100.0
        self.acc_offset *= 1.02
        self.acc_bias = [x/100.0, y/100.0, z/100.0]
        

    def read_acc(self):
        a1 = self.Sense.get_accelerometer_raw()
        self.writeBinLog(a1)
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

    def calc_len(self, acc):
        return sqrt(pow(acc[0], 2) + pow(acc[1], 2) + pow(acc[2], 2))

    def get_len(self):
        self.Length = sqrt(pow(self.get_x(),2) + pow(self.get_y(),2) + pow(self.get_z(),2))
        return self.Length

    def get_adj_len(self):
        return self.get_len()-self.acc_offset

    def adjAcc(self, acc):
        return [acc[0]-self.acc_bias[0], acc[1]-self.acc_bias[1], acc[0]+(Gdelta-self.acc_bias[0])]

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





