# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './advanced_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from threading import Thread, Event
import traceback
import model as Model
import pylab
import matplotlib.pyplot as plt


UP_LABEL = "▲"
DOWN_LABEL = "▼"

class simulatorGui(QtCore.QObject):

    setTimeSignal = QtCore.pyqtSignal(str)
    setHMSSignal = QtCore.pyqtSignal(str)
    setAssignmentSignal = QtCore.pyqtSignal(list)
    setElevatorFloorSignal = QtCore.pyqtSignal(int, int, int)
    setElevatorDestinationFloorSignal = QtCore.pyqtSignal(int, int, int)
    enqueueAtFloorSignal = QtCore.pyqtSignal(int, str, int, str)
    dequeueFromFloorSignal = QtCore.pyqtSignal(int, str, int)
    setElevatorHeaderSignal = QtCore.pyqtSignal(int, str, str)
    unloadPassengerFromElevatorSignal = QtCore.pyqtSignal(int, int)
    unloadPassengersFromElevatorSignal = QtCore.pyqtSignal(int, list)
    loadPassengerOnElevatorSignal = QtCore.pyqtSignal(int, str, int, str)
    plotSignal = QtCore.pyqtSignal(dict)

    def __init__(self, settings):
        QtCore.QObject.__init__(self)
        self.settings = settings
        self.nf = settings["floors_amount"]
        self.nc = settings["shafts_amount"]
        self.uiElevator = uiElevator

    def setupGui(self, MainWindow):
        ######################
        ## MAIN FORM WINDOW ##
        ######################
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)

        self.mainWidget = QtWidgets.QWidget(MainWindow)
        self.mainWidget.setObjectName("mainWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.mainWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.mainWidget)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 940, 700))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        ##################
        ## SHAFTS TABLE ##
        ##################
        self.shaftsTable = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.shaftsTable.setMinimumSize(QtCore.QSize(200, 0))
        self.shaftsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.shaftsTable.setDragDropOverwriteMode(False)
        self.shaftsTable.setAlternatingRowColors(True)
        self.shaftsTable.setObjectName("shaftsTable")
        self.shaftsTable.setSelectionMode(0)

        # Set column and row amount
        self.shaftsTable.setColumnCount(self.nc)
        self.shaftsTable.setRowCount(self.nf)

        for i in range(self.nf):
            item = QtWidgets.QTableWidgetItem()
            self.shaftsTable.setVerticalHeaderItem(i, item)

        for j in range(self.nc):
            item = QtWidgets.QTableWidgetItem()
            self.shaftsTable.setHorizontalHeaderItem(j, item)

        for i in range(self.nf):
            for j in range(self.nc):
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(200,200,200))
                self.shaftsTable.setItem(i,j,item)

        self.shaftsTable.horizontalHeader().setCascadingSectionResizes(False)
        self.shaftsTable.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.shaftsTable, 2, 2, 1, 1)

        # Auto fill horizontal width for queues columns
        #self.queuesTable.resizeColumnsToContents()
        self.shaftsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Set minimum column width for queues
        self.shaftsTable.horizontalHeader().setMinimumSectionSize(100)

        # Queues table rows fill table height
        self.shaftsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


        ##################
        ## QUEUES TABLE ##
        ##################
        self.queuesTable = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queuesTable.sizePolicy().hasHeightForWidth())
        self.queuesTable.setSizePolicy(sizePolicy)
        self.queuesTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.queuesTable.setDragDropOverwriteMode(False)
        self.queuesTable.setAlternatingRowColors(True)
        self.queuesTable.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.queuesTable.setObjectName("queuesTable")
        self.queuesTable.setSelectionMode(0)

        self.queuesTable.setColumnCount(4)
        self.queuesTable.setRowCount(self.nf)

        for i in range(self.nf):
            item = QtWidgets.QTableWidgetItem()
            self.queuesTable.setVerticalHeaderItem(i, item)

        for j in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.queuesTable.setHorizontalHeaderItem(j, item)

        self.queuesTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(180, 180, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        self.queuesTable.setItem(0, 1, item)
        self.queuesTable.horizontalHeader().setCascadingSectionResizes(False)
        self.queuesTable.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.queuesTable, 2, 3, 1, 1)

        # Floors queues columns sizes
        self.queuesTable.setColumnWidth(0,40)
        self.queuesTable.setColumnWidth(3,40)

        # Auto fill horizontal width for queues columns
        #self.queuesTable.resizeColumnsToContents()
        self.queuesTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.queuesTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # Set minimum column width for queues
        self.queuesTable.horizontalHeader().setMinimumSectionSize(100)

        # Queues table rows fill table height
        self.queuesTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        #########################
        ## SIMULATION CONTROLS ##
        #########################
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.runOnceBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runOnceBtn.sizePolicy().hasHeightForWidth())
        self.runOnceBtn.setSizePolicy(sizePolicy)
        self.runOnceBtn.setObjectName("runOnceLabel")
        self.horizontalLayout.addWidget(self.runOnceBtn)

        self.runBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runBtn.sizePolicy().hasHeightForWidth())
        self.runBtn.setSizePolicy(sizePolicy)
        self.runBtn.setObjectName("runBtn")
        self.horizontalLayout.addWidget(self.runBtn)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.timeStaticLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeStaticLabel.sizePolicy().hasHeightForWidth())
        self.timeStaticLabel.setSizePolicy(sizePolicy)
        self.timeStaticLabel.setObjectName("timeStaticLabel")
        self.horizontalLayout.addWidget(self.timeStaticLabel)

        self.timeVariableLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeVariableLabel.sizePolicy().hasHeightForWidth())
        self.timeVariableLabel.setSizePolicy(sizePolicy)
        self.timeVariableLabel.setObjectName("timeVariableLabel")

        self.horizontalLayout.addWidget(self.timeVariableLabel)

        spacerItemX = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItemX)
        self.simSpeedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.simSpeedLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.simSpeedLabel.setIndent(-1)
        self.simSpeedLabel.setObjectName("simSpeedLabel")
        self.horizontalLayout.addWidget(self.simSpeedLabel)

        self.HMSStaticLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HMSStaticLabel.sizePolicy().hasHeightForWidth())
        self.HMSStaticLabel.setSizePolicy(sizePolicy)
        self.HMSStaticLabel.setObjectName("HMSStaticLabel")
        self.horizontalLayout.addWidget(self.HMSStaticLabel)

        self.HMSVariableLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HMSVariableLabel.sizePolicy().hasHeightForWidth())
        self.HMSVariableLabel.setSizePolicy(sizePolicy)
        self.HMSVariableLabel.setObjectName("HMSVariableLabel")

        self.horizontalLayout.addWidget(self.HMSVariableLabel)

        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.simSpeedLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.simSpeedLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.simSpeedLabel.setIndent(-1)
        self.simSpeedLabel.setObjectName("simSpeedLabel")
        self.horizontalLayout.addWidget(self.simSpeedLabel)

        self.speedSlider = QtWidgets.QSlider(self.scrollAreaWidgetContents)
        self.speedSlider.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speedSlider.sizePolicy().hasHeightForWidth())
        self.speedSlider.setSizePolicy(sizePolicy)
        self.speedSlider.setBaseSize(QtCore.QSize(0, 0))
        self.speedSlider.setMaximum(99)
        self.speedSlider.setSingleStep(10)
        self.speedSlider.setPageStep(10)
        self.speedSlider.setTracking(True)
        self.speedSlider.setOrientation(QtCore.Qt.Horizontal)
        self.speedSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.speedSlider.setTickInterval(10)
        self.speedSlider.setObjectName("speedSlider")
        self.horizontalLayout.addWidget(self.speedSlider)

        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.plotBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotBtn.sizePolicy().hasHeightForWidth())
        self.plotBtn.setSizePolicy(sizePolicy)
        self.plotBtn.setObjectName("runBtn")
        self.horizontalLayout.addWidget(self.plotBtn)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.mainWidget)

        self.retranslateUi()
        self.setupElevators()
        self.setupQueues()
        self.bindEvents()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def setAssignment(self, assignment):
        ups = assignment[0:int(len(assignment)/2)]
        downs = assignment[int(len(assignment)/2):]

        for i in list(reversed(range(len(ups)))):
            self.assignments['up'][i].setText(str(ups[i]))
            self.assignments['down'][i+1].setText(str(downs[i]))


    def setElevatorFloor(self, curr_floor, new_floor, shaft):
        new_row = abs(new_floor-self.nf+1)
        curr_row = abs(curr_floor-self.nf+1)
        try:
            new_el = uiElevator(self.MainWindow)
            el = self.elevators[shaft]
            new_el.setHeader(el.direction, el.action)
            new_el.loadPassengersAsQListWidgetItemArray(el.unloadAllPassengers())
            self.shaftsTable.setCellWidget(curr_row, shaft, None)
            self.shaftsTable.setCellWidget(new_row, shaft, new_el)
            self.elevators[shaft] = new_el
            new_el.show()

        except Exception as e:
            print(e)
            traceback.print_exc()


    def setElevatorDestinationFloor(self, curr_destination, new_destination, shaft):
        new_row = abs(new_destination-self.nf+1)
        curr_row = abs(curr_destination-self.nf+1)
        self.shaftsTable.item(curr_row, shaft).setBackground(QtGui.QColor(200,200,200))
        self.shaftsTable.item(new_row, shaft).setBackground(QtGui.QColor(130,212,114))


    def setupElevators(self):
        self.elevators = []

        for j in range(self.nc):
            el = uiElevator(self.MainWindow)
            self.elevators.append(el)
            self.shaftsTable.setCellWidget(self.nf-1, j, el)


    def setupQueues(self):
        self.queues = {
            'up' : [],
            'down' : []
        }
        self.assignments = {
            'up' : [],
            'down' : []
        }

        for i in list(reversed(range(self.nf))):
            for q_dir in ['up', 'down']:
                queue = uiQueue(self.MainWindow)
                self.queues[q_dir].append(queue)
                self.queuesTable.setCellWidget(i, ['up', 'down'].index(q_dir)+1, queue)


        for i in list(reversed(range(self.nf))):
            for j in [0,3]:
                dir_index = {0:'up',3:'down'}
                item = QtWidgets.QTableWidgetItem()
                item.setText("-1")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.queuesTable.setItem(i,j,item)
                self.assignments[dir_index[j]].append(item)

        self.assignments['up'][self.nf-1].setText("-")
        self.assignments['down'][0].setText("-")

    def plot(self, stats):
        """
        STATS = {
            "waiting_time" : [],
            "riding_time" : [],
            "total_time" : [],
            "mean_waiting_time : []
        }
        """

        with open("./random.txt", "w") as f:
            f.write("MIN waiting time: " + str(min(stats["waiting_time"])))
            f.write("\n")
            f.write("MAX waiting time: " + str(max(stats["waiting_time"])))
            f.write("\n")
            f.write(str(stats["waiting_time"]))
            f.write("\n")
            f.write("\n")

            f.write("MIN riding time: " + str(min(stats["riding_time"])))
            f.write("\n")
            f.write("MAX riding time: " + str(max(stats["riding_time"])))
            f.write("\n")
            f.write(str(stats["riding_time"]))
            f.write("\n")
            f.write("\n")

            f.write("MIN total time: " + str(min(stats["total_time"])))
            f.write("\n")
            f.write("MAX total time: " + str(max(stats["total_time"])))
            f.write("\n")
            f.write(str(stats["total_time"]))
            f.write("\n")
            f.write("\n")

            f.write("MEAN waiting TIME:")
            f.write("\n")
            f.write(str(stats["mean_waiting_time"]))
            f.write("\n")
            f.write("\n")

            f.write("MEAN riding TIME:")
            f.write("\n")
            f.write(str(stats["mean_riding_time"]))
            f.write("\n")
            f.write("\n")

            f.write("MEAN totale TIME:")
            f.write("\n")
            f.write(str(stats["mean_total_time"]))
            f.write("\n")
            f.write("\n")

        print("MIN waiting time: " + str(min(stats["waiting_time"])))
        print("MAX waiting time: " + str(max(stats["waiting_time"])))

        print("MIN riding time: " + str(min(stats["riding_time"])))
        print("MAX riding time: " + str(max(stats["riding_time"])))

        print("MIN total time: " + str(min(stats["total_time"])))
        print("MAX total time: " + str(max(stats["total_time"])))

        pylab.figure(1)
        pylab.title('Mean waiting time')
        pylab.xlabel('Time (seconds)')
        pylab.ylabel('Waiting_Time (seconds)')
        #pylab.plot([i[0] for i in something], [j[1] for j in someother], marker='.', alpha=1, color='b')
        pylab.plot(stats["mean_waiting_time"])
        pylab.plot(stats["mean_riding_time"])
        pylab.plot(stats["mean_total_time"])

        pylab.figure(2)
        pylab.title('Mean waiting time')
        pylab.xlabel('Time (HMS)')
        pylab.ylabel('Waiting_Time (seconds)')
        pylab.scatter(stats["birth_time"], [0 for _ in stats["birth_time"]], marker='|', c='g', s=600)
        pylab.scatter(stats["birth_time_reverse"], [0 for _ in stats["birth_time_reverse"]], marker='|', c='r', s=600)

        pylab.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.shaftsTable.setSortingEnabled(True)

        for i in range(self.nf):
            item = self.shaftsTable.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", str((self.nf-1)-i)))

        for j in range(self.nc):
            item = self.shaftsTable.horizontalHeaderItem(j)
            item.setText(_translate("MainWindow", "Shaft #" + str(j)))

        self.queuesTable.setSortingEnabled(False)

        self.queuesTable.horizontalHeaderItem(0).setText(_translate("MainWindow", "#"))
        self.queuesTable.horizontalHeaderItem(1).setText(_translate("MainWindow", "Up Queues"))
        self.queuesTable.horizontalHeaderItem(2).setText(_translate("MainWindow", "Down Queues"))
        self.queuesTable.horizontalHeaderItem(3).setText(_translate("MainWindow", "#"))

        self.HMSStaticLabel.setText(_translate("MainWindow", "[h:m:s]:"))
        self.HMSVariableLabel.setText(_translate("MainWindow", "07:00"))
        self.timeStaticLabel.setText(_translate("MainWindow", "Time:"))
        self.timeVariableLabel.setText(_translate("MainWindow", "120 (sec)"))
        self.runOnceBtn.setText(_translate("MainWindow", "Run Once"))
        self.simSpeedLabel.setText(_translate("MainWindow", "Simulation Speed:"))
        self.runBtn.setText(_translate("MainWindow", "►"))
        self.plotBtn.setText(_translate("MainWindow", "Plot"))


    def bindEvents(self):
        Model.SETTINGS = self.settings
        self.modelCloseEvent = Event()
        self.modelPlotEvent = Event()
        self.modelRunOnceEvent = Event()
        self.modelRunEvent = Event()

        def run():
            if self.modelRunEvent.is_set():
                self.modelRunEvent.clear()
                self.runOnceBtn.setDisabled(False)
                self.runBtn.setText("►")
            else:
                self.modelRunEvent.set()
                self.runOnceBtn.setDisabled(True)
                self.runBtn.setText("❚❚")


        self.runBtn.clicked.connect(lambda: run())

        def runOnce():
            self.modelRunOnceEvent.set()

        self.runOnceBtn.clicked.connect(lambda: runOnce())

        def plotEvent():
            self.modelPlotEvent.set()

        self.plotBtn.clicked.connect(lambda : plotEvent())

        def closeEvent(event):
            self.modelCloseEvent.set()
            event.accept()

        self.MainWindow.closeEvent = closeEvent

        def changeSpeed():
            self.model.setSpeed(self.speedSlider.value())

        self.speedSlider.valueChanged.connect(changeSpeed)

        self.setAssignmentSignal.connect(self.setAssignment)
        self.setElevatorFloorSignal.connect(self.setElevatorFloor)
        self.setElevatorDestinationFloorSignal.connect(self.setElevatorDestinationFloor)
        self.plotSignal.connect(self.plot)

        self.setTimeSignal.connect(
            lambda time:
            self.timeVariableLabel.setText(str(time))
        )

        self.setHMSSignal.connect(
            lambda HMS:
            self.HMSVariableLabel.setText(str(HMS))
        )


        self.enqueueAtFloorSignal.connect(
            lambda queue_floor, passenger_direction, passenger_destination_floor, passenger_name:
            self.queues[passenger_direction][queue_floor].enqueue(passenger_direction, passenger_destination_floor, passenger_name)
        )

        self.dequeueFromFloorSignal.connect(
            lambda queue_floor, queue_direction, p_index:
            self.queues[queue_direction][queue_floor].dequeue(p_index)
        )

        self.setElevatorHeaderSignal.connect(
            lambda el_id, direction, action:
            self.elevators[el_id].setHeader(direction, action)
        )

        self.unloadPassengerFromElevatorSignal.connect(
            lambda el_id, p_index:
            self.elevators[el_id].unloadPassenger(p_index)
        )

        self.unloadPassengersFromElevatorSignal.connect(
            lambda el_id, indexArray:
            self.elevators[el_id].unloadPassengers(indexArray)
        )

        self.loadPassengerOnElevatorSignal.connect(
            lambda el_id, direction, destination_floor, name:
            self.elevators[el_id].loadPassenger(direction, destination_floor, name)
        )

        signalDict = {
            "plot" : self.plotSignal
            , "setHMS" : self.setHMSSignal
            , "setTime" : self.setTimeSignal
            , "setAssignment" : self.setAssignmentSignal
            , "setElevatorFloor" : self.setElevatorFloorSignal
            , "setElevatorDestinationFloor" : self.setElevatorDestinationFloorSignal
            , "enqueueAtFloor" : self.enqueueAtFloorSignal
            , "dequeueFromFloor" : self.dequeueFromFloorSignal
            , "setElevatorHeader" : self.setElevatorHeaderSignal
            , "unloadPassengerFromElevator" : self.unloadPassengerFromElevatorSignal
            , "unloadPassengersFromElevator" : self.unloadPassengersFromElevatorSignal
            , "loadPassengerOnElevator" : self.loadPassengerOnElevatorSignal
        }

        self.model = Model.model(self.modelPlotEvent, self.modelCloseEvent, self.modelRunEvent, self.modelRunOnceEvent, signalDict)
        self.modelThread = Thread(target=self.model.start)
        self.modelThread.start()


class uiQueue(QtWidgets.QListWidget):
    def __init__(self, Window):
        QtWidgets.QListWidget.__init__(self, Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setProperty("showDropIndicator", False)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setFlow(QtWidgets.QListView.TopToBottom)
        self.setProperty("isWrapping", False)
        self.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.setUniformItemSizes(False)
        self.setObjectName("queueWidget")

    def enqueue(self, direction, destination_floor, name):
        if direction == 'up':
            icon = UP_LABEL
        else:
            icon = DOWN_LABEL
        self.addItem(str.format("({0} {1}) {2}", icon, str(destination_floor), name))

    def dequeue(self, index):
        self.takeItem(index)


class uiElevator(QtWidgets.QListWidget):
    def __init__(self, Window):
        QtWidgets.QListWidget.__init__(self, Window)
        self.hide()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setProperty("showDropIndicator", False)
        self.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setFlow(QtWidgets.QListView.TopToBottom)
        self.setProperty("isWrapping", False)
        self.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.setUniformItemSizes(False)
        self.setObjectName("elevatorWidget")

        # Set default Header
        item = QtWidgets.QListWidgetItem("")
        brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setBackground(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.addItem(item)
        self.action = "Idle"
        self.setHeader("up", "Idle")

    def setHeader(self, direction, action=None):
        if action is None:
            action = self.action

        if direction == 'up':
            icon = UP_LABEL
        else:
            icon = DOWN_LABEL

        self.direction = direction
        self.action = action

        if self.item(0) != 0:
            self.item(0).setText(icon + " " + action)
        else:
            item = QtWidgets.QListWidgetItem("")
            brush = QtGui.QBrush(QtGui.QColor(85, 85, 85))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setBackground(brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setForeground(brush)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(icon + " " + action)
            self.insertItem(0, item)

    def unloadPassenger(self, index):
        return self.takeItem(index+1)

    def unloadAllPassengers(self):
        unloaded = []
        for x in range(self.count()-1):
            unloaded.append(self.takeItem(1))
        return unloaded

    def unloadPassengers(self, indexArray):
        indexArray.sort()
        indexArray = list(reversed(indexArray))
        unloaded = []
        for y in range(len(indexArray)):
            p = indexArray[y]+1
            unloaded.append(self.takeItem(p))
        return unloaded

    def loadPassenger(self, direction, destination_floor, name):
        if direction == 'up':
            icon = UP_LABEL
        else:
            icon = DOWN_LABEL
        self.addItem(str.format("({0} {1}) {2}", icon, str(destination_floor), name))

    def loadPassengersAsQListWidgetItemArray(self, QListWidgetItemArray):
        for i in range(len(QListWidgetItemArray)):
            self.addItem(QListWidgetItemArray[i])


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = simulatorGui(2,6)
    ui.setupGui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())