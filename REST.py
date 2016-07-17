import web
import json
from multiprocessing import Queue
from threading import Thread
import math

BUFF_SIZE = 100
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
        acc_series = ["Acc max", "Acc avg", "Acc min"]
        acc_datamax = map(lambda x: x[1]['max'], retbuff)
        acc_dataavg = map(lambda x: x[1]['avg'], retbuff)
        acc_datamin = map(lambda x: x[1]['min'], retbuff)
        ruck_series = ["Ruck max", "Ruck avg"]
        ruck_datamax = map(lambda x: x[2]['max'], retbuff)
        ruck_dataavg = map(lambda x: x[2]['avg'], retbuff)
        return json.dumps({"Acc": 
                                {"labels": labels,
                                  "series": acc_series,
                                  "data": [acc_datamax,
                                           acc_dataavg,
                                           acc_datamin]},
                           "Ruck":
                          
                                {"labels": labels,
                                 "series": ruck_series,
                                 "data": [ruck_datamax,
                                          ruck_dataavg]}
                           })
