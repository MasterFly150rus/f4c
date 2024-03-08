# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Info.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Info(object):
    def setupUi(self, Info):
        Info.setObjectName("Info")
        Info.setWindowModality(QtCore.Qt.ApplicationModal)
        Info.resize(371, 287)
        Info.setMinimumSize(QtCore.QSize(371, 287))
        Info.setMaximumSize(QtCore.QSize(371, 287))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Ico/logo_301.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Info.setWindowIcon(icon)
        Info.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Info)
        self.buttonBox.setGeometry(QtCore.QRect(80, 240, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Info)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 311, 210))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_prototype = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_prototype.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_prototype.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_prototype.setObjectName("lineEdit_prototype")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_prototype)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_scale = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_scale.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_scale.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_scale.setObjectName("lineEdit_scale")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_scale)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(0, 20))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_speed = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_speed.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_speed.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_speed.setObjectName("lineEdit_speed")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_speed)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setMinimumSize(QtCore.QSize(0, 20))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_number = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_number.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_number.setText("")
        self.label_number.setObjectName("label_number")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_number)
        self.lineEdit_surname = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_surname.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_surname.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_surname.setObjectName("lineEdit_surname")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_surname)
        self.lineEdit_region = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_region.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_region.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_region.setObjectName("lineEdit_region")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_region)
        self.lineEdit_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_name.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_name.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(0, 20))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_cls = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_cls.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_cls.setText("")
        self.label_cls.setObjectName("label_cls")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_cls)

        self.retranslateUi(Info)
        self.buttonBox.accepted.connect(Info.accept) # type: ignore
        self.buttonBox.rejected.connect(Info.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Info)

    def retranslateUi(self, Info):
        _translate = QtCore.QCoreApplication.translate
        Info.setWindowTitle(_translate("Info", "Информация"))
        self.label_2.setText(_translate("Info", "Имя"))
        self.label_3.setText(_translate("Info", "№"))
        self.label_4.setText(_translate("Info", "Прототип"))
        self.label_5.setText(_translate("Info", "Масштаб"))
        self.label_6.setText(_translate("Info", "Скорость прототипа"))
        self.label_7.setText(_translate("Info", "Регион"))
        self.label.setText(_translate("Info", "Фамилия"))
        self.label_8.setText(_translate("Info", "Класс"))
import Resourses_rc
