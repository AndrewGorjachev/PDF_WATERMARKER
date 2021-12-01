#!/bin/bash

pyside2-rcc qml.qrc -o qml_rc.py 

pyinstaller main.py MainWindowController.py qml_rc.py --windowed --onefile --name PDF_WATERMARKER --icon=app.ico 
