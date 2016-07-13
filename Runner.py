
import time
from Accelerometer import Accelerometer
from Display import Display
from FileController import FileController
from BinaryFileController import BinaryFileController
from REST import RESTThread

USE_BINLOG = False
USE_TEXTLOG = False


def init():
    print('Start REST server')
    rest = RESTThread()
    rest.start()
    
    bin = None
    if (USE_BINLOG):
        bin = BinaryFileController(2)
        bin.start()

    acc = Accelerometer(0.250, bin)
    acc.start()

    log = None
    if (USE_TEXTLOG):
        log = FileController(20)
        log.start()

    dsp = Display(acc, log)
    dsp.start()
    
    print('at sleep')
    time.sleep(60*30)
    
    acc.stopit()
    acc.join()
    print("Accelorometer stopped")
        
    dsp.stopit()
    dsp.join()
    print("Display stopped")

    if (USE_BINLOG):
        bin.stopit()
        bin.join()
        print("BinLogger stopped")

    if (USE_TEXTLOG):
        log.stopit()
        log.join()
    print("FileController stopped")

    rest.stopit()
    rest.join()
    print("REST server stopped")

    time.sleep(2)
    print("End")

if __name__ == '__main__':
    init()
