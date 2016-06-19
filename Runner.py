
import time
from Accelerometer import Accelerometer
from Display import Display

def init():
    acc = Accelerometer(0.250)
    acc.start()

    dsp = Display(acc)
    dsp.start()

    print('at sleep')
    time.sleep(120)
    
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
