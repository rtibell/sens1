import web
import json
from multiprocessing import Queue
from threading import Thread
import math

BUFF_SIZE = 50
buffer = [None] * BUFF_SIZE
idx = 0
global buffer, idx

class RESTThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dorun = True
        self.urls = ('/', 'HelloWorld')
        globs = globals()
        globs.update({'RESTself':self})
        self.app = web.application(self.urls, globs, autoreload=True)
        global buffer, idx
        
    def run(self):
        while (self.dorun):
            self.app.run()
        self.app.stop()

    def stopit(self):
        self.dorun = False    
        
    def putNext(self, entry):
        global buffer, idx
        buffer[idx] = entry
        idx = (idx+1) % BUFF_SIZE
        print(idx)
        
    
    
class HelloWorld:
       
    def GET(self):
        global buffer, idx
        retbuff = buffer[idx:-1] + buffer[0:idx] 
        #print(retbuff)
        labels = map(lambda x: x[0][9:], retbuff)
        series = ["Acc max", "Acc avg", "Acc min"]
        datamax = map(lambda x: x[1]['max'], retbuff)
        dataavg = map(lambda x: x[1]['avg'], retbuff)
        datamin = map(lambda x: x[1]['min'], retbuff)
        print(" max={}\n avg={}\n min={}".format(datamax, dataavg, datamin))
        #return json.dumps({"labels": ["January", "February", "March", "April", "May", "June", "July"],
        #        "series": ["Series A", "Series B"],
        #        "data": [[65, 18, 80, 81, 56, 55, 40],
        #                 [28, 29, 40, 19, 86, 27, 90]]})
        return json.dumps({"labels": labels,
                "series": series,
                "data": [datamax,
                         dataavg,
                         datamin]})


