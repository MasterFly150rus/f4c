# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TourI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TourI(object):
    def setupUi(self, TourI):
        TourI.setObjectName("TourI")
        TourI.setWindowModality(QtCore.Qt.ApplicationModal)
        TourI.resize(879, 617)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TourI.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(TourI)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(TourI)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.frame = QtWidgets.QFrame(TourI)
        self.frame.setMinimumSize(QtCore.QSize(0, 40))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMinimumSize(QtCore.QSize(70, 26))
        self.pushButton.setMaximumSize(QtCore.QSize(70, 26))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(TourI)
        QtCore.QMetaObject.connectSlotsByName(TourI)

    def retranslateUi(self, TourI):
        _translate = QtCore.QCoreApplication.translate
        TourI.setWindowTitle(_translate("TourI", "F-4C ФАС России I тур"))
        self.pushButton.setText(_translate("TourI", "Печать"))
import Resourses_rc
