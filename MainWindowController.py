# This Python file uses the following encoding: utf-8
import re

from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer
#from EnableRTLRunner import EnableRTLRunner


class MainWindowController(QObject):

    def __init__(self):
        print("main window controller has started")

        super().__init__()

    def __del__(self):
        pass

