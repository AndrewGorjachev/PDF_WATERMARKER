# This Python file uses the following encoding: utf-8

import configparser
import glob as glob
import os

from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer

import PDFRunner as PDFRunner


class MainWindowController(QObject):
    wrong_ini_signal = Signal()

    files_not_found_signal = Signal()

    processing_started_signal = Signal()

    directory_not_exist_signal = Signal()

    processing_completed_signal = Signal()

    file_corrupted_signal = Signal(str, arguments=['file_path'])

    error_while_processing_signal = Signal(str, arguments=['file_path'])

    set_watermark_text_to_view_signal = Signal(int, str, arguments=['line_number',
                                                                    'watermark_text'])
    set_watermark_opacity_signal = Signal(int, arguments=['opacity'])

    set_font_size_signal = Signal(int, arguments=['font_size'])

    processing_progress_signal = Signal(int, arguments=['count'])

    useful_text = ['Trade secret',
                   'Horns and Hooves LLC.',
                   'Neverland, Chernomorsk city']

    path_to_files = ""

    total_quantity_pages = 0

    opacity = 50

    font_size = 16

    is_ini_corrupted = False;

    def __init__(self):

        super().__init__()

        self.read_config_file()

        self.thread = QThread(parent=self)

        QTimer.singleShot(500, self.set_config_into_view)

    def __del__(self):
        pass

    @Slot(str)
    def process_pdfs(self, path_to_directory):

        if str(path_to_directory).startswith("file:///"):

            pdffiles = []

            self.path_to_files = path_to_directory.replace("file:///", "")

            for file in glob.glob(self.path_to_files + '/**/*.pdf', recursive=True):

                buff = file.replace("\\", '/')

                if os.path.exists(buff):

                    pdffiles.append(buff)

                else:
                    self.files_not_found_signal.emit()

            if pdffiles:

                if self.thread.isRunning():

                    self.pleaseWait.emit()

                else:

                    self.runner = PDFRunner.PDFRunner(pdffiles, self.useful_text, self.opacity, self.font_size)

                    self.runner.moveToThread(self.thread)

                    self.runner.finished_signal.connect(self.stop_thread_slot)

                    self.runner.processing_completed_signal.connect(self.processing_completed_slot)

                    self.runner.total_quantity_of_pages_signal.connect(self.total_quantity_of_pages_slot)

                    self.runner.rest_of_pages_signal.connect(self.rest_of_pages_slot)

                    self.runner.file_not_found_signal.connect(self.error_while_file_processing)

                    self.runner.wrong_page_format_signal.connect(self.wrong_page_format_slot)

                    self.runner.file_corrupted_signal.connect(self.file_corrupted_slot)

                    self.thread.started.connect(self.runner.run)

                    self.processing_started_signal.emit()

                    self.thread.start()

            else:
                self.files_not_found_signal.emit()

        else:
            self.directory_not_exist_signal.emit()

    def read_config_file(self):
        config = configparser.ConfigParser()

        try:
            if config.read('watermark.ini'):
                self.useful_text[0] = config["watermark"]["str0"]
                self.useful_text[1] = config["watermark"]["str1"]
                self.useful_text[2] = config["watermark"]["str2"]

                self.opacity = int(config['text_property']['opacity'])

                self.font_size = int(config['text_property']['font_size'])

                if (self.font_size > 22) and (self.font_size < 10):
                    self.font_size = 16
            else:
                raise Exception('Wrong ini format.')

        except Exception as e:

            self.is_ini_corrupted = True

            self.write_config_file()

    @Slot(str)
    def watermark_slot(self, watermark_text):
        if watermark_text:
            buff = watermark_text.split('\n')
            if buff[0]:
                self.useful_text[0] = buff[0]
            if buff[1]:
                self.useful_text[1] = buff[1]
            if buff[2]:
                self.useful_text[2] = buff[2]

    @Slot()
    def write_config_file(self):
        config = configparser.ConfigParser()
        config['watermark'] = {}
        config['watermark']["str0"] = self.useful_text[0]
        config['watermark']["str1"] = self.useful_text[1]
        config['watermark']["str2"] = self.useful_text[2]
        config['text_property'] = {}
        config['text_property']['opacity'] = str(self.opacity)
        config['text_property']['font_size'] = str(self.font_size)

        with open('watermark.ini', 'w') as configfile:
            config.write(configfile)

    def set_config_into_view(self):
        self.set_watermark_text_to_view_signal.emit(0, self.useful_text[0])
        self.set_watermark_text_to_view_signal.emit(1, self.useful_text[1])
        self.set_watermark_text_to_view_signal.emit(2, self.useful_text[2])
        self.set_watermark_opacity_signal.emit(int(self.opacity))
        if self.is_ini_corrupted:
            self.wrong_ini_signal.emit()

    @Slot(int)
    def total_quantity_of_pages_slot(self, total_quantity_pages):
        self.total_quantity_pages = total_quantity_pages

    @Slot(int)
    def rest_of_pages_slot(self, rest_quantity):
        buff = ((self.total_quantity_pages - rest_quantity) / self.total_quantity_pages) * 100
        self.processing_progress_signal.emit(int(buff))

    @Slot()
    def processing_completed_slot(self):
        self.processing_completed_signal.emit()

    @Slot()
    def stop_thread_slot(self):
        if self.thread:
            self.thread.quit()
            self.thread.wait()

    @Slot(str)
    def error_while_file_processing(self, file_path):
        if file_path == "The file list is empty.":
            self.files_not_found_signal.emit()
        else:
            self.error_while_processing_signal.emit(file_path.replace(self.path_to_files, " .."))

    @Slot(str)
    def wrong_page_format_slot(self, file_path):
        self.error_while_processing_signal.emit(file_path.replace(self.path_to_files, " .."))

    @Slot(str)
    def file_corrupted_slot(self, file_path):
        self.file_corrupted_signal.emit(file_path.replace(self.path_to_files, " .."))

    @Slot(int)
    def opacity_slot(self, opacity):
        buf = int(opacity)
        print(buf)
        if opacity != buf:
            self.opacity = buf

    @Slot(int)
    def font_size_slot(self, font_size):
        self.font_size = int(font_size)
        print(self.font_size)
