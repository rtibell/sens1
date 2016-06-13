
import time
from Accelerometer import Accelerometer
from Accelerometer import Accelerometer

def init():
    print('at init')
    acc = Accelerometer()
    print('at start')
    acc.start()

    dsp = Display(acc)
    acc.start

    print('at sleep')
    time.sleep(30)
    
    acc.stopit()
    acc.join()
    print("Accelorometer stopped")
    
    dsp.stopit()
    dsp.join()
    print("Display stopped")
    time.sleep(2)
    print("End")

if __name__ == '__main__':
    init()
