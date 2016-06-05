#!/usr/bin/python

from math import pow, sqrt, floor
import numpy as np
import time
import threading
from sense_hat import SenseHat

class Account():
    def transfer(self, target, amount):
        pass
    def __init__(self, holder, number, balance):
        self.Holder = holder
        self.Number = number
        self.Balance = balance
    
def init():
    a1 = Account('Rasmus', 123232, 200)
    print(a1.Holder)

if __name__ == '__main__':
    init()
