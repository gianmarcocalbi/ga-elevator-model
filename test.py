from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from threading import Thread, Event
import traceback
from time import sleep
import numpy as np
import pylab

ga1 = []
ga2 = []
opt = []

pylab.figure(1)
pylab.title('Mean waiting time')
pylab.xlabel('Time (HMS)')
pylab.ylabel('Time (sec)')
pylab.plot(ga1, c='r')
pylab.plot(ga2,c='g')
pylab.plot(opt, c = 'b')

pylab.show()