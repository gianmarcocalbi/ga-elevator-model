from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from threading import Thread, Event
import traceback
from time import sleep
import numpy as np
import pylab
TIME = 0
def setArrivalTime():
    global TIME

    # morning uppeak
    nf = 6
    people_amount = 200
    arrivals = {}

    dest_count = []
    for i in range(1, nf):
        dest_count.append(0)
        dest_count += [i] * int(people_amount / (nf-1))
    if (people_amount / (nf-1)) % 1 != 0:
        dest_count += [nf-1]

    for t in list(np.random.normal(30600, 1800, people_amount)):
        t = int(t)

        if len(dest_count) == 0:
            break

        rnd = np.random.randint(0,len(dest_count))
        dest = dest_count.pop(rnd)

        if t not in arrivals:
            arrivals[t] = []

        arrivals[t].append(dest)

    TIME = min(list(arrivals.keys()))
    if TIME < 0:
        TIME = 0


    return arrivals

print(len(setArrivalTime()))
print(TIME)
exit()

pylab.figure(1)
pylab.title('Results plot')
pylab.xlabel('Time (minutes)')
pylab.ylabel('Passenger arrived')
pylab.plot(setArrivalTime())
pylab.show()
