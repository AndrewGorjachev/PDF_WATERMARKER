from PySide2.QtCore import QObject, Signal, Slot, QThread

class PDFRunner(QObject):

    def __init__(self):

        super().__init__()

    @Slot()
    def run(self):
        pass
