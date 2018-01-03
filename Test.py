
import time
from MockAccelerometer import MockAccelerometer
from MockDisplay import MockDisplay
from FileController import FileController
from BinaryFileController import BinaryFileController
from AWSIOTController import AWSIOTController
from REST import RESTThread

USE_BINLOG = False
USE_TEXTLOG = False
USE_REST = False
USE_IOT = True


def init():
    rest = None
    if (USE_REST):
        print('Start REST server')
        rest = RESTThread()
        rest.start()
    
    bin = None
    if (USE_BINLOG):
        print('Start BinLogg server')
        bin = BinaryFileController(2)
        bin.start()

    acc = MockAccelerometer(0.250, bin)
    acc.start()

    log = None
    if (USE_TEXTLOG):
        print('Start TextLogg server')
        log = FileController(20)
        log.start()

    iot = None
    if (USE_IOT):
        print('Start IOT server')
        iot = AWSIOTController(5)
        iot.start()

    print('Start MockDisplay')
    dsp = MockDisplay(acc, log, rest, iot)
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

    if (USE_REST):
        rest.stopit()
        rest.join()
        print("REST server stopped")

    time.sleep(2)
    print("End")

if __name__ == '__main__':
    init()
