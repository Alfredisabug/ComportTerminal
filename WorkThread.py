# !/usr/bin/env python
# -*- coding:utf-8 -*-
# python 2.7
# @Author    : alfredwu


import ComportControl
import serial
from PySide import QtCore


class WorkThread(QtCore.QThread):
    reply_signal = QtCore.Signal(str)
    cmd_signal = QtCore.Signal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.com = None
        self.write_string = None
        self.pec = None

    def run(self, *args, **kwargs):
        if self.pec == "NONE":
            send_str = self.write_string.decode("hex")
            self.com.write(send_str)
        elif self.pec == "1Byte PEC 2's complement":
            print "No support yet."
        elif self.pec == "2Byte PEC 2's complement":
            send_str = self.com.write_with_2scomplement(self.write_string)

        self.cmd_signal.emit(send_str.encode('hex'))
        data = self.com.read_data(1)
        self.reply_signal.emit(data)
