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

UP_LABEL = "▲"
DOWN_LABEL = "▼"

class simulatorGui(object):
    def __init__(self, settings):
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
        self.queuesTable.setColumnWidth(0,30)
        self.queuesTable.setColumnWidth(3,30)

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
        self.progressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)

        self.quitBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quitBtn.sizePolicy().hasHeightForWidth())
        self.quitBtn.setSizePolicy(sizePolicy)
        self.quitBtn.setObjectName("runBtn")
        self.horizontalLayout.addWidget(self.quitBtn)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.mainWidget)

        self.retranslateUi()
        self.setupElevators()
        self.setupQueues()
        self.bindEvents()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


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


    def setupElevators(self):
        self.elevators = []

        for j in range(self.nc):
            el = uiElevator(self.MainWindow)
            self.elevators.append(el)
            self.shaftsTable.setCellWidget(self.nf-1, j, el)


    def setupQueues(self):
        self.queues = {
            'upgoing' : [],
            'downgoing' : []
        }
        self.assignements = {
            'up' : [],
            'down' : []
        }

        for i in range(self.nf):
            for q_dir in ['upgoing', 'downgoing']:
                queue = uiQueue(self.MainWindow)
                self.queues[q_dir].append(queue)
                self.queuesTable.setCellWidget(i, ['upgoing', 'downgoing'].index(q_dir)+1, queue)

        for i in range(self.nf):
            for j in [0,3]:
                dir_index = {0:'up',3:'down'}
                item = QtWidgets.QTableWidgetItem()
                item.setText("-1")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.queuesTable.setItem(i,j,item)
                self.assignements[dir_index[j]].append(item)


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
        self.queuesTable.horizontalHeaderItem(1).setText(_translate("MainWindow", "UpGoing Queues"))
        self.queuesTable.horizontalHeaderItem(2).setText(_translate("MainWindow", "DownGoing Queues"))
        self.queuesTable.horizontalHeaderItem(3).setText(_translate("MainWindow", "#"))

        self.timeStaticLabel.setText(_translate("MainWindow", "Time:"))
        self.timeVariableLabel.setText(_translate("MainWindow", "120 (sec)"))
        self.runOnceBtn.setText(_translate("MainWindow", "Run Once"))
        self.runBtn.setText(_translate("MainWindow", "►"))
        self.quitBtn.setText(_translate("MainWindow", "Quit"))


    def bindEvents(self):
        Model.SETTINGS = self.settings
        self.modelCloseEvent = Event()
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

        def closeEvent(event):
            self.modelCloseEvent.set()
            event.accept()

        self.MainWindow.closeEvent = closeEvent

        def quitProgram(i):
            if i == QtWidgets.QMessageBox.Ok:
                self.modelEvent.set()
                sys.exit()

        msg = QtWidgets.QMessageBox()
        #msg.setIcon(QtGui.QMessageBox.Information)
        msg.setWindowTitle("Exit alert")
        msg.setText("Click OK to quit the simulation")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.buttonClicked.connect(quitProgram)

        #self.quitBtn.clicked.connect(lambda: quitProgram(msg.exec_()))

        def tmp():
            self.setElevatorFloor(0,4,0)

        self.quitBtn.clicked.connect(lambda : tmp())

        self.model = Model.model(self)
        self.modelThread = Thread(target=self.model.start, args=(self.modelCloseEvent, self.modelRunEvent, self.modelRunOnceEvent))
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
            self.insertItem(0, icon + " " + action)

    def unloadPassenger(self, index):
        return self.takeItem(index+1)

    def unloadAllPassengers(self):
        unloaded = []
        for x in range(1, self.count()):
            unloaded.append(self.takeItem(1))
        return unloaded

    def unloadPassengers(self, indexArray):
        indexArray.sort()
        unloaded = []
        for x in range(1, len(indexArray)):
            p = indexArray[x]-x
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