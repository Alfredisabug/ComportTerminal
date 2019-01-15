# !/usr/bin/env python
# -*- coding:utf-8 -*-
# python 2.7
# @Author    : alfredwu


from PySide import QtGui, QtCore
import SettingUI


class SettingUIClass(QtGui.QWidget, SettingUI.Ui_ScriptSetting):
    def __init__(self, parent=None):
        super(SettingUIClass, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("JiRongLogo.ico"))

        self.ok_btn.clicked.connect(lambda: self.close())
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)

        [self.__dict__["cmd_name_lineedit_{}".format(i)].textChanged.connect(self.change_btn)
         for i in xrange(1, 41)]

    def change_btn(self):
        sender = QtCore.QObject.sender(self)
        target_number = sender.objectName().split("_")[-1]
        self.__dict__["pushButton_{}".format(target_number)].setText(sender.text())
