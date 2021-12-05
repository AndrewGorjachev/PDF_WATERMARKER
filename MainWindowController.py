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

    set_watermark_text_to_view = Signal(int, str, arguments=['line_number', 'watermark_text'])

    processing_progress = Signal(int,  arguments=['count'])

    useful_text = ['Trade secret', 'Horns and Hooves LLC.', 'Neverland, Chernomorsk city']

    path_to_files = ""

    modified_file_name = ""

    total_quantity_pages = 0

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

                    self.runner.total_quantity_of_pages.connect(self.total_pages_slot)

                    self.runner.total_quantity_of_pages.connect(self.total_pages_slot)

                    self.runner.rest_of_pages.connect(self.pages_done_slot)

                    self.runner.processing_has_been_completed.connect(self.processing_complete)

                    self.thread.started.connect(self.runner.run)

                    self.thread.start()

            else:
                self.files_didnt_found.emit()

        else:
            self.directory_didnt_exist.emit()

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

    @Slot(int)
    def total_pages_slot(self, total_quantity_pages):

        self.total_quantity_pages = total_quantity_pages

    @Slot(int)
    def pages_done_slot(self, rest_quantity):

        buff = ((self.total_quantity_pages - rest_quantity)/self.total_quantity_pages )*100

        self.processing_progress.emit(int(buff))

    @Slot(str)
    def write_config_file(self, watermark_text):

        if watermark_text:

            buff = watermark_text.split('\n')

            if buff[0]:

                self.useful_text[0] = buff[0]

            if buff[1]:

                self.useful_text[1] = buff[1]

            if buff[2]:

                self.useful_text[2] = buff[2]

            config = configparser.ConfigParser()
            config['watermark'] = {}
            config['watermark']["str0"] = self.useful_text[0]
            config['watermark']["str1"] = self.useful_text[1]
            config['watermark']["str2"] = self.useful_text[2]

            with open('watermark.ini', 'w') as configfile:
                config.write(configfile)

    @Slot()
    def processing_complete(self):
        self.processing_has_been_completed.emit()

    def set_config_into_view(self):
        self.set_watermark_text_to_view.emit(0, self.useful_text[0])
        self.set_watermark_text_to_view.emit(1, self.useful_text[1])
        self.set_watermark_text_to_view.emit(2, self.useful_text[2])

    @Slot()
    def stop_thread(self):

        if self.thread:

            self.thread.quit()

            self.thread.wait()
