# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './advanced_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class simulatorGui(object):
    def __init__(self, nc, nf):
        self.nf = nf
        self.nc = nc

    def setupGui(self, MainWindow):
        ######################
        ## MAIN FORM WINDOW ##
        ######################

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

        # Set column and row amount
        self.shaftsTable.setColumnCount(self.nc)
        self.shaftsTable.setRowCount(self.nf)

        for i in range(self.nf):
            item = QtWidgets.QTableWidgetItem()
            self.shaftsTable.setVerticalHeaderItem(i, item)

        for j in range(self.nc):
            item = QtWidgets.QTableWidgetItem()
            self.shaftsTable.setHorizontalHeaderItem(j, item)

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

        self.queuesTable.setColumnCount(4)
        self.queuesTable.setRowCount(self.nf)

        for i in range(self.nf):
            item = QtWidgets.QTableWidgetItem()
            self.queuesTable.setVerticalHeaderItem(i, item)

        for j in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.queuesTable.setHorizontalHeaderItem(j, item)

        item = QtWidgets.QTableWidgetItem()
        item.setBackground(QtGui.QColor(100,100,100))
        self.shaftsTable.setItem(1, 1, item)

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
        self.queuesTable.setColumnWidth(0,44)
        self.queuesTable.setColumnWidth(3,44)

        # Auto fill horizontal width for queues columns
        #self.queuesTable.resizeColumnsToContents()
        self.queuesTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.queuesTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # Set minimum column width for queues
        self.queuesTable.horizontalHeader().setMinimumSectionSize(100)

        # Queues table rows fill table height
        self.queuesTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        self.runOnceLabel = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runOnceLabel.sizePolicy().hasHeightForWidth())
        self.runOnceLabel.setSizePolicy(sizePolicy)
        self.runOnceLabel.setObjectName("runOnceLabel")
        self.horizontalLayout.addWidget(self.runOnceLabel)
        self.runBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runBtn.sizePolicy().hasHeightForWidth())
        self.runBtn.setSizePolicy(sizePolicy)
        self.runBtn.setObjectName("runBtn")
        self.horizontalLayout.addWidget(self.runBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 2, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.mainWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        self.runOnceLabel.setText(_translate("MainWindow", "Run Once"))
        self.runBtn.setText(_translate("MainWindow", "►"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = simulatorGui(3,16)
    ui.setupGui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

