# This Python file uses the following encoding: utf-8

import configparser
import glob as glob
import os

from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer

import PDFRunner as PDFRunner


class MainWindowController(QObject):

    directory_didnt_exist = Signal()

    files_didnt_found = Signal()

    processing_has_been_completed = Signal()

    error_while_processing = Signal(str, arguments=['file_path'])

    set_watermark_text_to_view = Signal(str, arguments=['watrmark_text'])

    useful_text = ['Trade secret', 'Horns and Hooves LLC.', 'Neverland, Chernomorsk city']

    path_to_files = ""

    modified_file_name = ""

    def __init__(self):

        super().__init__()

        self.read_config_file()

        self.thread = QThread(parent=self)

        QTimer.singleShot(1000, self.set_config_into_view)

    def __del__(self):
        pass

    @Slot(str, str)
    def process_pdfs(self, path_to_directory, watermark_text):

        if str(path_to_directory).startswith("file:///"):

            pdffiles = []

            for file in glob.glob(path_to_directory.replace("file:///", "") + '/**/*.pdf', recursive=True):

                buff = file.replace("\\", '/')

                if os.path.exists(buff):

                    pdffiles.append(buff)

                else:
                    self.files_didnt_found.emit()

            if pdffiles:

                if self.thread.isRunning():

                    self.pleaseWait.emit()

                else:

                    self.runner = PDFRunner.PDFRunner(pdffiles, self.useful_text)

                    self.runner.moveToThread(self.thread)

                    self.runner.files_didnt_found.connect(self.files_didnt_found)

                    self.runner.finished.connect(self.stop_thread)

                    #self.runner.finished.connect(self.runner.deleteLater())

                    self.thread.started.connect(self.runner.run)

                    self.thread.start()

            else:
                self.files_didnt_found.emit()

        else:
            self.directory_didnt_exist.emit()

        # self.directory_didnt_exist.emit()
        #
        # self.processing_has_been_completed.emit()
        #
        # self.error_while_processing.emit(path_to_directory)

    def read_config_file(self):
        config = configparser.ConfigParser()

        try:
            if config.read('watermark.ini'):
                self.useful_text[0] = config["watermark"]["str0"]
                self.useful_text[1] = config["watermark"]["str1"]
                self.useful_text[2] = config["watermark"]["str2"]
            else:
                raise Exception('Wrong ini format.')

        except Exception as e:
            config['watermark'] = {}
            config['watermark']["str0"] = self.useful_text[0]
            config['watermark']["str1"] = self.useful_text[1]
            config['watermark']["str2"] = self.useful_text[2]

            with open('watermark.ini', 'w') as configfile:
                config.write(configfile)

    @Slot(str)
    def write__config_file(self):
        pass

    def set_config_into_view(self):
        self.set_watermark_text_to_view.emit(
            self.useful_text[0] + " \n" +
            self.useful_text[1] + " \n" +
            self.useful_text[2])

    @Slot()
    def stop_thread(self):

        if self.thread:

            self.thread.quit()

            self.thread.wait()