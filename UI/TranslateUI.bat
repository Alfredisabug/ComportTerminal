@echo off
pyside-uic -o MainUI.py MainUI_Ver_2.ui
pyside-uic -o ASCIICODEUI.py ASCIICODEUI.ui
pyside-uic -o AboutUI.py About.ui
pyside-uic -o SettingUI.py Setting.ui
pyside-rcc -o ascii_rc.py ascii.qrc