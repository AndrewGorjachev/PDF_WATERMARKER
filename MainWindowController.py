# This Python file uses the following encoding: utf-8

import configparser
import glob
import os

from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer


class MainWindowController(QObject):

    directory_didnt_exist = Signal()

    files_didnt_found = Signal()

    processing_has_been_completed = Signal()

    error_while_processing = Signal(str, arguments=['file_path'])

    set_watermark_text_to_view = Signal(str, arguments=['watrmark_text'])

    useful_text = ['«Trade secret»', 'Horns and Hooves LLC.', 'Neverland, Chernomorsk city']

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

        print(path_to_directory)

        txtfiles = []
        for file in glob.glob(path_to_directory, "*.txt"):
            print(file)
            txtfiles.append(file)

        #for path, subdirs, files in os.walk(path_to_directory):


            # for name in files:
            #     if fnmatch(name, pattern):
            #         print
            #         os.path.join(path, name)


        # self.directory_didnt_exist.emit()
        #
        # self.files_didnt_found.emit()
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
