# This Python file uses the following encoding: utf-8
import sys
import os
import qml_rc

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from MainWindowController import MainWindowController

VERSION = "1.1"

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    mainWindowController = MainWindowController()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('controller', mainWindowController)
    #engine.load(os.path.join(os.path.dirname(__file__), "MainWindow.qml"))

    engine.load(":/MainWindow.qml")
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("A_Goryachev")
    app.setOrganizationDomain("HOME")

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
