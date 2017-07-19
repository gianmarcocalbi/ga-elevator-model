from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from threading import Thread, Event
import traceback
from time import sleep

boom = 0

def main():
    signal = QtCore.pyqtSignal()
    signal.connect(BOOM)

    thread = Thread(target=loop, args=())
    thread.start()

@pyqtSlot()
def BOOM():
    global boom
    print("KAAAAABOOOOOOOOOOOOOOOOOOOOM")
    boom += 1
    if boom == 3:
        print("MEEEEEEEEEEEEEEEEGAAAAAAAAAAAAAAAAAAAAA")
        print("BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM")
        sys.exit()

def loop():
    sec = 0
    while True:
        print("Sono passati " + str(sec) + " secondi")
        sleep(1)

