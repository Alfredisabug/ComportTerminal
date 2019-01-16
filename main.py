# -*- coding: utf-8 -*-

__version__ = '1.0'
__auther__ = 'JiRongWu'
__update_date__ = '20190115'

# ====import sys module====
import sys
import os
from PySide import QtGui, QtCore
import serial
import serial.tools.list_ports
import WorkThread
import ComportControl
# ====import sys module end====

PRJ_DIR = os.getcwd()      # Project Directory

# ====import .py====
import MainUI
import AboutUIMain
import SettingUIMain
import ASCIITABLEMain
# ====import .py end===

# var


class MainWindow(QtGui.QMainWindow, MainUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("JiRongLogo.ico"))
        self.comport = None
        self.baudrate = 115200
        self.reply_data = None

        self.work_thread = WorkThread.WorkThread()
        self.work_thread.reply_signal.connect(self.show_return_data)
        self.work_thread.cmd_signal.connect(self.show_write_cmd_data)

        self.about_ui = AboutUIMain.AboutUIClass()
        self.setting_ui = SettingUIMain.SettingUIClass()
        self.ascii_ui = ASCIITABLEMain.ASCIIUIClass()

        regx = QtCore.QRegExp('[a-fA-F0-9+$]+$')
        validator = QtGui.QRegExpValidator(regx)
        self.send_string_lineedit.setValidator(validator)

        self.rescan_comport()

        # signal
        self.rate115200_rbtn.clicked.connect(self.change_baudrate)
        self.rate9600_rbtn.clicked.connect(self.change_baudrate)
        self.rate19200_rbtn.clicked.connect(self.change_baudrate)

        self.rescan_btn.clicked.connect(self.rescan_comport)
        self.connect_btn.clicked.connect(self.open_com)
        self.send_btn.clicked.connect(self.write_cmd)
        self.show_ascii_btn.clicked.connect(lambda: self.ascii_ui.show())

        self.display_chg_btn.clicked.connect(self.change_display_format)
        self.exit_btn.clicked.connect(self.close)
        self.show_about_btn.clicked.connect(lambda: self.about_ui.show())
        self.set_marco_btn.clicked.connect(lambda: self.setting_ui.show())
        self.save_marco_file_btn.clicked.connect(self.save_marco_to_txt)
        self.open_marco_file_btn.clicked.connect(self.open_marco_txt)

        [self.setting_ui.__dict__["pushButton_{}".format(i)].clicked.connect(self.send_marco)
         for i in xrange(1, 41)]
        [self.__dict__["marco_btn_{}".format(i)].clicked.connect(self.send_marco)
         for i in xrange(1, 41)]
        [self.setting_ui.__dict__["cmd_name_lineedit_{}".format(i)].textChanged.connect(self.change_marco)
         for i in xrange(1, 41)]

    def save_marco_to_txt(self):
        save_name = QtGui.QFileDialog.getSaveFileName(self, "Save file", "Command.txt", "*.txt")
        if save_name[0] == "" or save_name[1] == "":
            return
        file = open(save_name[0], 'w')
        for i in xrange(1, 41):
            file.writelines(self.__dict__["marco_btn_{}".format(i)].text() + '\n')
            file.writelines(self.setting_ui.__dict__["str_lineedit_{}".format(i)].text() + '\n')
        file.close()

    def open_marco_txt(self):
        file_address = QtGui.QFileDialog.getOpenFileName(self, "Open File", "./", "(*.txt)")
        if file_address[0] == "" or file_address[1] == "":
            return

        for i in xrange(1, 41):
            self.__dict__["marco_btn_{}".format(i)].setText("")
            self.setting_ui.__dict__["cmd_name_lineedit_{}".format(i)].setText("")
            self.setting_ui.__dict__["str_lineedit_{}".format(i)].setText("")

        count = 0
        target_number = 1
        with open(file_address[0], 'r') as f:
            for i in f:
                i = i.strip('\n')
                if not count % 2:
                    self.__dict__["marco_btn_{}".format(target_number)].setText(i)
                    self.setting_ui.__dict__["cmd_name_lineedit_{}".format(target_number)].setText(i)
                else:
                    self.setting_ui.__dict__["str_lineedit_{}".format(target_number)].setText(i)
                    target_number += 1
                count += 1

    def change_marco(self):
        sender = QtCore.QObject.sender(self)
        target_number = sender.objectName().split("_")[-1]
        self.__dict__["marco_btn_{}".format(target_number)].setText(sender.text())

    def send_marco(self):
        self.reply_lineedit.setText("")
        sender = QtCore.QObject.sender(self)
        src_name = sender.objectName()

        src_number = src_name.split("_")[-1]
        write_string = self.setting_ui.__dict__["str_lineedit_{}".format(src_number)].text()
        if not self.comport or (len(write_string) % 2) or write_string == "":
            return
        self.work_thread.com = self.comport
        self.work_thread.pec = self.pec_choosed_combobox.currentText()
        self.work_thread.write_string = write_string
        self.work_thread.start()
        self.send_btn.setEnabled(False)

    def change_display_format(self):
        if self.display_chg_btn.text() == "ASCII":
            if self.reply_data:
                display_str = ""
                for i in self.reply_data:
                    display_str += (hex(ord(i))) + " "
                self.reply_lineedit.setText(display_str)
            self.display_chg_btn.setText("HEX")
        elif self.display_chg_btn.text() == "HEX":
            if self.reply_data:
                self.reply_lineedit.setText(self.reply_data)
            self.display_chg_btn.setText("ASCII")

    def show_return_data(self, reply_str):
        if not reply_str:
            self.reply_lineedit.setText("Timeout!")
            self.reply_data = None
        elif self.display_chg_btn.text() == "ASCII":
            self.reply_data = reply_str
            self.reply_lineedit.setText(reply_str)
        elif self.display_chg_btn.text() == "HEX":
            self.reply_data = reply_str
            display_str = ''
            for i in reply_str:
                display_str += (hex(ord(i))) + " "
            self.reply_lineedit.setText(display_str)
        self.send_btn.setEnabled(True)

    def write_cmd(self):
        self.reply_lineedit.setText("")
        if not self.comport or (len(self.send_string_lineedit.text()) % 2) or self.send_string_lineedit.text() == "":
            return
        self.work_thread.com = self.comport
        self.work_thread.pec = self.pec_choosed_combobox.currentText()
        self.work_thread.write_string = self.send_string_lineedit.text()
        self.work_thread.start()
        self.send_btn.setEnabled(False)

    def show_write_cmd_data(self, write_string):
        show_str = ''
        for i in xrange(0, len(write_string), 2):
            show_str += write_string[i].upper() + write_string[i+1].upper() + " "
        self.marco_string_lineedit.setText(show_str)

    def open_com(self):
        if self.comport_combobox.currentText() == "":
            return
        if self.connect_btn.isChecked():
            try:
                self.comport = ComportControl.SerialControl(port=self.comport_combobox.currentText(),
                                                            baudrate=self.baudrate, timeout=1)
                self.connect_btn.setChecked(True)
                self.connect_btn.setText("Disconnect")
                self.comport_combobox.setEnabled(False)
            except serial.SerialException:
                self.connect_btn.setChecked(False)
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setWindowTitle('Error!')
                msg.setMinimumSize(600, 300)
                msg.setText('Open comport error.')
                msg.show()
                msg.exec_()
        else:
            if self.comport:
                self.comport.close()
                self.connect_btn.setChecked(False)
                self.comport = None
                self.connect_btn.setText("Connect")
                self.comport_combobox.setEnabled(True)

    def change_baudrate(self):
        sender = QtCore.QObject.sender(self)
        if sender == self.rate115200_rbtn:
            self.baudrate = 115200
        elif sender == self.rate19200_rbtn:
            self.baudrate = 19200
        elif sender == self.rate9600_rbtn:
            self.baudrate = 9600
        if self.comport:
            self.comport.baudrate=self.baudrate

    def rescan_comport(self):
        self.comport_combobox.clear()
        ports = serial.tools.list_ports.comports()
        port_list = []
        for element in ports:
            port_list.append(element[0])
        self.comport_combobox.addItems(port_list)

    def close(self):
        sys.exit()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle('ComportTesting_Ver. 9.0 by JiRong')
    main.show()
    sys.exit(app.exec_())
