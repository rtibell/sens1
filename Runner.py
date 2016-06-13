
import time
from Accelerometer import Accelerometer

def init():
    print('at init')
    acc = Accelerometer()
    print('at start')
    acc.start()
    for dat in acc.read_queue():
        print dat
    print('at sleep')
    time.sleep(15)
    for dat in acc.read_queue():
        print dat
    print('at sleep')
    time.sleep(30)

if __name__ == '__main__':
    init()
