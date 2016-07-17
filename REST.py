import web
import json
from multiprocessing import Queue
from threading import Thread

ring_buffer = []
buffer_idx = 0

class RESTThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dorun = True
        self.que = Queue(1024)
        self.urls = ('/', 'HelloWorld')
        self.app = web.application(self.urls, globals(), autoreload=True)
        
    def run(self):
        print("Start REST Server")
        while (self.dorun):
            self.app.run()
            print("REST app started")
            entry = self.getNext()
            print("Entry:")
            print(entry)
        self.app.stop()

    def stopit(self):
        self.dorun = False
        
    def getNext(self):
        try:
            return self.que.get(True, timeout=600)    
        except:
            print("Exception")

    def read_queue(self):
        yield self.que.get(True, None)
        
    def putNext(self, entry):
        self.que.put_nowait(entry)
    
    
class HelloWorld:
    def GET(self):
        return json.dumps({"labels": ["January", "February", "March", "April", "May", "June", "July"],
                "series": ["Series A", "Series B"],
                "data": [[65, 18, 80, 81, 56, 55, 40],
                         [28, 29, 40, 19, 86, 27, 90]]})


