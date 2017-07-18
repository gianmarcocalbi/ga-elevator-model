# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './settings.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StartingSettings(object):
    def setupUi(self, StartingSettings):
        StartingSettings.setObjectName("StartingSettings")
        StartingSettings.setFixedSize(563, 371)
        StartingSettings.setMaximumSize(QtCore.QSize(563, 371))
        self.centralwidget = QtWidgets.QWidget(StartingSettings)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 541, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonStart = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonStart.setObjectName("buttonStart")
        self.gridLayout.addWidget(self.buttonStart, 2, 0, 1, 2)
        self.elevatorBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elevatorBox.sizePolicy().hasHeightForWidth())
        self.elevatorBox.setSizePolicy(sizePolicy)
        self.elevatorBox.setMaximumSize(QtCore.QSize(800, 800))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.elevatorBox.setFont(font)
        self.elevatorBox.setObjectName("elevatorBox")
        self.label_4 = QtWidgets.QLabel(self.elevatorBox)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 61, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.elevatorBox)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 70, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.elevatorBox)
        self.label_7.setGeometry(QtCore.QRect(40, 120, 81, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.elevatorBox)
        self.label_8.setGeometry(QtCore.QRect(40, 160, 91, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.elevatorBox)
        self.label_9.setGeometry(QtCore.QRect(40, 200, 91, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.elevatorBox)
        self.label_10.setGeometry(QtCore.QRect(40, 240, 61, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.elevatorBox)
        self.label_11.setGeometry(QtCore.QRect(40, 280, 71, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.spinCapacity = QtWidgets.QSpinBox(self.elevatorBox)
        self.spinCapacity.setGeometry(QtCore.QRect(160, 40, 51, 22))
        self.spinCapacity.setObjectName("spinCapacity")
        self.spinMoving = QtWidgets.QSpinBox(self.elevatorBox)
        self.spinMoving.setGeometry(QtCore.QRect(160, 120, 51, 22))
        self.spinMoving.setObjectName("spinMoving")
        self.spinMoveToStop = QtWidgets.QSpinBox(self.elevatorBox)
        self.spinMoveToStop.setGeometry(QtCore.QRect(160, 160, 51, 22))
        self.spinMoveToStop.setObjectName("spinMoveToStop")
        self.spinStopToMove = QtWidgets.QSpinBox(self.elevatorBox)
        self.spinStopToMove.setGeometry(QtCore.QRect(160, 200, 51, 22))
        self.spinStopToMove.setObjectName("spinStopToMove")
        self.spinLoading = QtWidgets.QSpinBox(self.elevatorBox)
        self.spinLoading.setGeometry(QtCore.QRect(160, 240, 51, 22))
        self.spinLoading.setObjectName("spinLoading")
        self.spinUnloading = QtWidgets.QSpinBox(self.elevatorBox)
        self.spinUnloading.setGeometry(QtCore.QRect(160, 280, 51, 22))
        self.spinUnloading.setObjectName("spinUnloading")
        self.gridLayout.addWidget(self.elevatorBox, 0, 0, 2, 1)
        self.passengerBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.passengerBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passengerBox.sizePolicy().hasHeightForWidth())
        self.passengerBox.setSizePolicy(sizePolicy)
        self.passengerBox.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.passengerBox.setFont(font)
        self.passengerBox.setObjectName("passengerBox")
        self.label_6 = QtWidgets.QLabel(self.passengerBox)
        self.label_6.setGeometry(QtCore.QRect(20, 30, 111, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.spinWaitingTime = QtWidgets.QSpinBox(self.passengerBox)
        self.spinWaitingTime.setGeometry(QtCore.QRect(160, 30, 51, 22))
        self.spinWaitingTime.setObjectName("spinWaitingTime")
        self.gridLayout.addWidget(self.passengerBox, 1, 1, 1, 1)
        self.generalBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.generalBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.generalBox.sizePolicy().hasHeightForWidth())
        self.generalBox.setSizePolicy(sizePolicy)
        self.generalBox.setMaximumSize(QtCore.QSize(400, 800))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.generalBox.setFont(font)
        self.generalBox.setMouseTracking(False)
        self.generalBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.generalBox.setAccessibleDescription("")
        self.generalBox.setFlat(False)
        self.generalBox.setCheckable(False)
        self.generalBox.setChecked(False)
        self.generalBox.setObjectName("generalBox")
        self.label = QtWidgets.QLabel(self.generalBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 91, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.generalBox)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 91, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.spinShaftsAmount = QtWidgets.QSpinBox(self.generalBox)
        self.spinShaftsAmount.setGeometry(QtCore.QRect(160, 40, 51, 22))
        self.spinShaftsAmount.setObjectName("spinShaftsAmount")
        self.spinFloorsAmount = QtWidgets.QSpinBox(self.generalBox)
        self.spinFloorsAmount.setGeometry(QtCore.QRect(160, 80, 51, 22))
        self.spinFloorsAmount.setObjectName("spinFloorsAmount")
        self.label.raise_()
        self.label_2.raise_()
        self.elevatorBox.raise_()
        self.elevatorBox.raise_()
        self.spinShaftsAmount.raise_()
        self.spinFloorsAmount.raise_()
        self.gridLayout.addWidget(self.generalBox, 0, 1, 1, 1)
        StartingSettings.setCentralWidget(self.centralwidget)

        #START of SETTINGS_CONSTRAINTS
        MAX_CAPACITY = self.spinCapacity.setMaximum(7)
        MIN_CAPACITY = self.spinCapacity.setMinimum(0)
        MAX_MOVING = self.spinMoving.setMaximum(10)
        MIN_MOVING = self.spinMoving.setMinimum(0)
        MAX_MOVETOSTOP = self.spinMoveToStop.setMaximum(6)
        MIN_MOVETOSTOP = self.spinMoveToStop.setMinimum(0)
        MAX_STOPTOMOVE = self.spinStopToMove.setMaximum(4)
        MIN_STOPTOMOVE = self.spinStopToMove.setMinimum(0)
        MAX_LOADING = self.spinLoading.setMaximum(8)
        MIN_LOADING = self.spinLoading.setMinimum(0)
        MAX_UNLOADING = self.spinUnloading.setMaximum(7)
        MIN_UNLOADING = self.spinUnloading.setMinimum(0)
        MAX_SHAFTSAMOUNT = self.spinShaftsAmount.setMaximum(3)
        MIN_SHAFTSAMOUNT = self.spinShaftsAmount.setMinimum(1)
        MAX_FLOORSAMOUNT = self.spinFloorsAmount.setMaximum(10)
        MIN_FLOORSAMOUNT = self.spinFloorsAmount.setMinimum(4)
        MAX_WAITINGTIME = self.spinWaitingTime.setMaximum(30)
        MIN_WAITINGTIME = self.spinWaitingTime.setMinimum(5)
        #END of SETTINGS_CONSTRAINTS

        self.retranslateUi(StartingSettings)
        QtCore.QMetaObject.connectSlotsByName(StartingSettings)

    def bindEvents(self):

        #Action of the "Start" button
        self.buttonStart.clicked.connect(lambda l : [setInitialParameters()])

        def setInitialParameters(self):

            SETTINGS = {
                "shafts_amount" : self.spinShaftsAmount.value(),
                "floors_amount" : self.spinFloorsAmount.value(),
                "elevator" : {
                    "capacity" : self.spinCapacity.value(),
                    "timing" : { # in seconds
                        # movimento da un piano ad un altro
                        'moving' : self.spinMoving.value(),
                
                         # decelerazione + apertura_porte
                        'move_to_stop' : self.spinMoveToStop.value(),
                
                        # chiusura_porte + accelerazione
                        'stop_to_move' : self.spinStopToMove.value(),
                
                        # caricamento_passeggeri + selezione_piano
                        'loading' : self.spinLoading.value(),
                
                        # scaricamento passeggeri
                        'unloading' : self.spinUnloading.value()
                    }
                },
                "passenger" : {
                    "waiting_time" : self.spinWaitingTime.value() # secondi
                }
            }

    def retranslateUi(self, StartingSettings):
        _translate = QtCore.QCoreApplication.translate
        StartingSettings.setWindowTitle(_translate("StartingSettings", "Start settings"))
        self.buttonStart.setText(_translate("StartingSettings", "Start"))
        self.elevatorBox.setTitle(_translate("StartingSettings", "Elevator"))
        self.label_4.setText(_translate("StartingSettings", "Capacity:"))
        self.label_5.setText(_translate("StartingSettings", "Timers (s):"))
        self.label_7.setText(_translate("StartingSettings", "Moving:"))
        self.label_8.setText(_translate("StartingSettings", "Move To Stop:"))
        self.label_9.setText(_translate("StartingSettings", "Stop To Move:"))
        self.label_10.setText(_translate("StartingSettings", "Loading:"))
        self.label_11.setText(_translate("StartingSettings", "Unloading"))
        self.passengerBox.setTitle(_translate("StartingSettings", "Passenger"))
        self.label_6.setText(_translate("StartingSettings", "Waiting Time (s):"))
        self.generalBox.setTitle(_translate("StartingSettings", "General"))
        self.label.setText(_translate("StartingSettings", "Shafts Amount:"))
        self.label_2.setText(_translate("StartingSettings", "Floors Amount:"))

#def on_click(self):
    #print("ciao")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StartingSettings = QtWidgets.QMainWindow()
    ui = Ui_StartingSettings()
    ui.setupUi(StartingSettings)
    StartingSettings.show()
    sys.exit(app.exec_())

