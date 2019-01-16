# !/usr/bin/env python
# -*- coding:utf-8 -*-
# python 2.7
# @Author    : alfredwu


import serial
import time


class SerialControl(serial.Serial):
    def __int__(self, comport, baudrate, timeout):
        serial.Serial.__init__(comport, baudrate=self.baudrate, timeout=self.timeout)

    def read_data(self, stop_time):
        star_time = time.time()
        while not self.inWaiting():
            time.sleep(0.01)
            if time.time()-star_time > stop_time:
                break
        length = self.inWaiting()
        if not length == 0:
            return self.read(length).decode("latin-1")
        else:
            return False

    def write_with_2scomplement(self, data):
        sum = 0
        data = data.decode('hex')
        for i in data:
            sum += int(i.encode('hex'), 16)
        pec = ('%02x' % (0xFFFF - sum + 1)).decode('hex')
        self.write(data + pec)
        return data+pec

