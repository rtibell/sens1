from threading import Thread
from multiprocessing import Queue
import datetime as dt
import time
import ssl
import os
import paho.mqtt.client as mqtt

awshost = "a19036sm3968bp.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "myThingName"
thingName = "myThingName"
caPath = "certs/VerisignClass3.crt"
certPath = "certs/0364cde5c9-certificate.pem.crt"
keyPath = "certs/0364cde5c9-private.pem.key"
connflag = False

class AWSIOTController(Thread):

    def on_connect_func(client, userdata, flags, rc):
        global connflag
        connflag = True
        print("Connection returned result: " + str(rc) )

    def on_message_func(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    def __init__(self, period):
        Thread.__init__(self)
        self.daemon = True
        self.cnt = 0
        self.period = period
        self.que = Queue(1024*8)
        self.dorun = True
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
            print('ssl patched')


    def run(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.on_connect_func
        self.mqttc.on_message = self.on_message_func
        self.mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        print("IOT connect")
        self.mqttc.connect(awshost, awsport, keepalive=60)
        print("IOT connected")
        self.mqttc.loop_start()
        print("at loop_start")
        while (self.dorun):
            time.sleep(self.period)
            tm = dt.datetime.now().strftime('%Y%m%d_%H.iot')
            while (self.que.empty() == False):
                entry = self.getNext()
                self.writeIOT(entry)

    def writeIOT(self, entry):
        print("{}\t{}\t{}\t{}\n".format(entry[0], entry[1]['x'], entry[1]['y'], entry[1]['z']))

    def stopit(self):
        self.dorun = False
        
    def getNext(self):
            try:
                return self.que.get(True, timeout=60)    
            except:
                print("Exception")

    def read_queue(self):
        yield self.que.get(True, None)
        
    def putNext(self, entry):
        self.que.put_nowait(entry)