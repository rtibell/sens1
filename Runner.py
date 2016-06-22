
import time
from Accelerometer import Accelerometer
from Display import Display
from FileController import FileController
from BinaryFileController import BinaryFileController

def init():

    bin = BinaryFileController(0.250)
    bin.start()

    acc = Accelerometer(0.250, bin)
    acc.start()

    log = FileController(20)
    log.start()

    dsp = Display(acc, log)
    dsp.start()
    
    print('at sleep')
    time.sleep(60*60)
    
    acc.stopit()
    acc.join()
    print("Accelorometer stopped")
        
    dsp.stopit()
    dsp.join()
    print("Display stopped")

    bin.stopit()
    bin.join()
    print("BinLogger stopped")

    log.stopit()
    log.join()
    print("FileController stopped")

    time.sleep(2)
    print("End")

if __name__ == '__main__':
    init()
