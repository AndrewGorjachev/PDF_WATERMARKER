#!/bin/bash

version=$(cat main.py | grep "VERSION = " |  grep -oP '(?<=").*(?=")' )

pyside2-rcc qml.qrc -o qml_rc.py 

pyinstaller main.py MainWindowController.py PDFRunner.py qml_rc.py --windowed --onefile --name PDF_WATERMARKER_${version} --icon=app.ico
