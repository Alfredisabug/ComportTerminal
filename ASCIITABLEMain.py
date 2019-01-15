# !/usr/bin/env python
# -*- coding:utf-8 -*-
# python 2.7
# @Author    : alfredwu


from PySide import QtGui, QtCore
import ASCIICODEUI


class ASCIIUIClass(QtGui.QWidget, ASCIICODEUI.Ui_Form):
    def __init__(self, parent=None):
        super(ASCIIUIClass, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("JiRongLogo.ico"))

        self.OKBtn.clicked.connect(lambda: self.close())
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)

