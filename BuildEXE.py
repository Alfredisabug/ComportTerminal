#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ===Import===
import PyInstaller as PYINT
from PyInstaller.__main__ import run
UIFILENAME = 'ComportTerminal Ver 9.0 by JiRong'
PY_File_Name = "main.py"
opts = [PY_File_Name,
        '-w',
        '-F',
        '--icon=./JiRongLogo.ico',
        '-p=./ComportControl',
        '-p=./UI',
    ]
opts.append("--name="+UIFILENAME)
run(opts)
