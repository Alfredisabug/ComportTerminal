# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ASCIICODEUI.ui'
#
# Created: Tue Jan 15 16:46:56 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(996, 687)
        Form.setMinimumSize(QtCore.QSize(996, 687))
        Form.setStyleSheet("QWidget{\n"
"    background-color: #EEEEEE;\n"
"}\n"
"QPushButton{\n"
"    background-color:     #CCCCCC;\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 14pt \"Times New Roman\";\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #0078D4;\n"
"    color: rgb(255, 255, 255);\n"
"    font: 14pt \"Calibri\";\n"
"}")
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ASCIICODELable = QtGui.QLabel(Form)
        self.ASCIICODELable.setStyleSheet("border-image: url(:/pic/Ascii_Table.png);")
        self.ASCIICODELable.setText("")
        self.ASCIICODELable.setObjectName("ASCIICODELable")
        self.verticalLayout.addWidget(self.ASCIICODELable)
        self.OKBtn = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setWeight(9)
        font.setItalic(False)
        font.setBold(False)
        self.OKBtn.setFont(font)
        self.OKBtn.setObjectName("OKBtn")
        self.verticalLayout.addWidget(self.OKBtn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "ASCIITABLE", None, QtGui.QApplication.UnicodeUTF8))
        self.OKBtn.setText(QtGui.QApplication.translate("Form", "OK", None, QtGui.QApplication.UnicodeUTF8))

import ascii_rc
