# This Python file uses the following encoding: utf-8
import sys
import os
from MainWindowController import MainWindowController

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

import qml_rc

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    mainWindowController = MainWindowController()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('controller', mainWindowController)
    engine.load(":/MainWindow.qml")

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
