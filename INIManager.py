import configparser

from PySide2.QtCore import QObject


class INIManager(QObject):
    configuration = {}

    def read_config_file(self):

        self.reset_configuration()

        config = configparser.ConfigParser()

        if config.read('watermark.ini'):

            self.configuration["str0"] = config["watermark"]["str0"]
            self.configuration["str1"] = config["watermark"]["str1"]
            self.configuration["str2"] = config["watermark"]["str2"]

            self.configuration["opacity"] = int(config['text_property']['opacity'])

            if (self.configuration["opacity"] > 100) or (self.configuration["opacity"] < 5):
                self.configuration["opacity"] = 50

            self.configuration["font_size"] = int(config['text_property']['font_size'])

            if (self.configuration["font_size"] > 22) or (self.configuration["font_size"] < 10):
                self.configuration["font_size"] = 16

            self.configuration["font_coefficient"] = int(config['text_property']['font_coefficient'])

            if (self.configuration["font_coefficient"] > 150) or (self.configuration["font_coefficient"] < 0):
                raise ValueError("font coefficient value error")

            self.configuration["A4_V_X_1"] = int(config['a4_vertical']['X_1'])
            self.configuration["A4_V_Y_1"] = int(config['a4_vertical']['Y_1'])
            self.configuration["A4_V_X_2"] = int(config['a4_vertical']['X_2'])
            self.configuration["A4_V_Y_2"] = int(config['a4_vertical']['Y_2'])

            self.configuration["A4_H_X_1"] = int(config['a4_horizontal']['X_1'])
            self.configuration["A4_H_Y_1"] = int(config['a4_horizontal']['Y_1'])
            self.configuration["A4_H_X_2"] = int(config['a4_horizontal']['X_2'])
            self.configuration["A4_H_Y_2"] = int(config['a4_horizontal']['Y_2'])

            self.configuration["A3_V_X_1"] = int(config['a3_vertical']['X_1'])
            self.configuration["A3_V_Y_1"] = int(config['a3_vertical']['Y_1'])
            self.configuration["A3_V_X_2"] = int(config['a3_vertical']['X_2'])
            self.configuration["A3_V_Y_2"] = int(config['a3_vertical']['Y_2'])
            self.configuration["A3_V_X_3"] = int(config['a3_vertical']['X_3'])
            self.configuration["A3_V_Y_3"] = int(config['a3_vertical']['Y_3'])

            self.configuration["A3_H_X_1"] = int(config['a3_horizontal']['X_1'])
            self.configuration["A3_H_Y_1"] = int(config['a3_horizontal']['Y_1'])
            self.configuration["A3_H_X_2"] = int(config['a3_horizontal']['X_2'])
            self.configuration["A3_H_Y_2"] = int(config['a3_horizontal']['Y_2'])
            self.configuration["A3_H_X_3"] = int(config['a3_horizontal']['X_3'])
            self.configuration["A3_H_Y_3"] = int(config['a3_horizontal']['Y_3'])

            self.configuration["A2_H_X_1"] = int(config['a2_horizontal']['X_1'])
            self.configuration["A2_H_Y_1"] = int(config['a2_horizontal']['Y_1'])
            self.configuration["A2_H_X_2"] = int(config['a2_horizontal']['X_2'])
            self.configuration["A2_H_Y_2"] = int(config['a2_horizontal']['Y_2'])
            self.configuration["A2_H_X_3"] = int(config['a2_horizontal']['X_3'])
            self.configuration["A2_H_Y_3"] = int(config['a2_horizontal']['Y_3'])
            self.configuration["A2_H_X_4"] = int(config['a2_horizontal']['X_4'])
            self.configuration["A2_H_Y_4"] = int(config['a2_horizontal']['Y_4'])
            self.configuration["A2_H_X_5"] = int(config['a2_horizontal']['X_5'])
            self.configuration["A2_H_Y_5"] = int(config['a2_horizontal']['Y_5'])
            self.configuration["A2_H_X_6"] = int(config['a2_horizontal']['X_6'])
            self.configuration["A2_H_Y_6"] = int(config['a2_horizontal']['Y_6'])

            self.configuration["A1_H_X_1"] = int(config['a1_horizontal']['X_1'])
            self.configuration["A1_H_Y_1"] = int(config['a1_horizontal']['Y_1'])
            self.configuration["A1_H_X_2"] = int(config['a1_horizontal']['X_2'])
            self.configuration["A1_H_Y_2"] = int(config['a1_horizontal']['Y_2'])
            self.configuration["A1_H_X_3"] = int(config['a1_horizontal']['X_3'])
            self.configuration["A1_H_Y_3"] = int(config['a1_horizontal']['Y_3'])
            self.configuration["A1_H_X_4"] = int(config['a1_horizontal']['X_4'])
            self.configuration["A1_H_Y_4"] = int(config['a1_horizontal']['Y_4'])
            self.configuration["A1_H_X_5"] = int(config['a1_horizontal']['X_5'])
            self.configuration["A1_H_Y_5"] = int(config['a1_horizontal']['Y_5'])
            self.configuration["A1_H_X_6"] = int(config['a1_horizontal']['X_6'])
            self.configuration["A1_H_Y_6"] = int(config['a1_horizontal']['Y_6'])
        else:
            self.write_config_file()

    def write_config_file(self):

        config = configparser.ConfigParser()

        config['watermark'] = {}
        config['watermark']["str0"] = self.configuration["str0"]
        config['watermark']["str1"] = self.configuration["str1"]
        config['watermark']["str2"] = self.configuration["str2"]

        config['text_property'] = {}
        config['text_property']['opacity'] = str(self.configuration["opacity"])
        config['text_property']['font_size'] = str(self.configuration["font_size"])
        config['text_property']['font_coefficient'] = str(self.configuration["font_coefficient"])

        config['a4_vertical'] = {}
        config['a4_vertical']['X_1'] = str(self.configuration["A4_V_X_1"])
        config['a4_vertical']['Y_1'] = str(self.configuration["A4_V_Y_1"])
        config['a4_vertical']['X_2'] = str(self.configuration["A4_V_X_2"])
        config['a4_vertical']['Y_2'] = str(self.configuration["A4_V_Y_2"])

        config['a4_horizontal'] = {}
        config['a4_horizontal']['X_1'] = str(self.configuration["A4_H_X_1"])
        config['a4_horizontal']['Y_1'] = str(self.configuration["A4_H_Y_1"])
        config['a4_horizontal']['X_2'] = str(self.configuration["A4_H_X_2"])
        config['a4_horizontal']['Y_2'] = str(self.configuration["A4_H_Y_2"])

        config['a3_vertical'] = {}
        config['a3_vertical']['X_1'] = str(self.configuration["A3_V_X_1"])
        config['a3_vertical']['Y_1'] = str(self.configuration["A3_V_Y_1"])
        config['a3_vertical']['X_2'] = str(self.configuration["A3_V_X_2"])
        config['a3_vertical']['Y_2'] = str(self.configuration["A3_V_Y_2"])
        config['a3_vertical']['X_3'] = str(self.configuration["A3_V_X_3"])
        config['a3_vertical']['Y_3'] = str(self.configuration["A3_V_Y_3"])

        config['a3_horizontal'] = {}
        config['a3_horizontal']['X_1'] = str(self.configuration["A3_H_X_1"])
        config['a3_horizontal']['Y_1'] = str(self.configuration["A3_H_Y_1"])
        config['a3_horizontal']['X_2'] = str(self.configuration["A3_H_X_2"])
        config['a3_horizontal']['Y_2'] = str(self.configuration["A3_H_Y_2"])
        config['a3_horizontal']['X_3'] = str(self.configuration["A3_H_X_3"])
        config['a3_horizontal']['Y_3'] = str(self.configuration["A3_H_Y_3"])

        config['a2_horizontal'] = {}
        config['a2_horizontal']['X_1'] = str(self.configuration["A2_H_X_1"])
        config['a2_horizontal']['Y_1'] = str(self.configuration["A2_H_Y_1"])
        config['a2_horizontal']['X_2'] = str(self.configuration["A2_H_X_2"])
        config['a2_horizontal']['Y_2'] = str(self.configuration["A2_H_Y_2"])
        config['a2_horizontal']['X_3'] = str(self.configuration["A2_H_X_3"])
        config['a2_horizontal']['Y_3'] = str(self.configuration["A2_H_Y_3"])
        config['a2_horizontal']['X_4'] = str(self.configuration["A2_H_X_4"])
        config['a2_horizontal']['Y_4'] = str(self.configuration["A2_H_Y_4"])
        config['a2_horizontal']['X_5'] = str(self.configuration["A2_H_X_5"])
        config['a2_horizontal']['Y_5'] = str(self.configuration["A2_H_Y_5"])
        config['a2_horizontal']['X_6'] = str(self.configuration["A2_H_X_6"])
        config['a2_horizontal']['Y_6'] = str(self.configuration["A2_H_Y_6"])

        config['a1_horizontal'] = {}
        config['a1_horizontal']['X_1'] = str(self.configuration["A1_H_X_1"])
        config['a1_horizontal']['Y_1'] = str(self.configuration["A1_H_Y_1"])
        config['a1_horizontal']['X_2'] = str(self.configuration["A1_H_X_2"])
        config['a1_horizontal']['Y_2'] = str(self.configuration["A1_H_Y_2"])
        config['a1_horizontal']['X_3'] = str(self.configuration["A1_H_X_3"])
        config['a1_horizontal']['Y_3'] = str(self.configuration["A1_H_Y_3"])
        config['a1_horizontal']['X_4'] = str(self.configuration["A1_H_X_4"])
        config['a1_horizontal']['Y_4'] = str(self.configuration["A1_H_Y_4"])
        config['a1_horizontal']['X_5'] = str(self.configuration["A1_H_X_5"])
        config['a1_horizontal']['Y_5'] = str(self.configuration["A1_H_Y_5"])
        config['a1_horizontal']['X_6'] = str(self.configuration["A1_H_X_6"])
        config['a1_horizontal']['Y_6'] = str(self.configuration["A1_H_Y_6"])

        with open('watermark.ini', 'w') as configfile:
            config.write(configfile)

    def reset_configuration(self):

        self.configuration = {
            "str0": "Trade secret",
            "str1": "Horns and Hooves LLC.",
            "str2": "Neverland, Chernomorsk city",
            "opacity": 50,
            "font_size": 16,
            "font_coefficient": 20,
            "A4_V_X_1": 600,
            "A4_V_Y_1": 300,
            "A4_V_X_2": 420,
            "A4_V_Y_2": -120,

            "A4_H_X_1": 420,
            "A4_H_Y_1": 140,
            "A4_H_X_2": 580,
            "A4_H_Y_2": -260,

            "A3_V_X_1": 840,
            "A3_V_Y_1": 540,
            "A3_V_X_2": 700,
            "A3_V_Y_2": 160,
            "A3_V_X_3": 600,
            "A3_V_Y_3": -260,

            "A3_H_X_1": 600,
            "A3_H_Y_1": 300,
            "A3_H_X_2": 840,
            "A3_H_Y_2": -520,
            "A3_H_X_3": 740,
            "A3_H_Y_3": -120,

            "A2_H_X_1": 600,
            "A2_H_Y_1": 300,
            "A2_H_X_2": 840,
            "A2_H_Y_2": -520,
            "A2_H_X_3": 740,
            "A2_H_Y_3": -120,
            "A2_H_X_4": 1250,
            "A2_H_Y_4": 100,
            "A2_H_X_5": 1250,
            "A2_H_Y_5": -320,
            "A2_H_X_6": 1250,
            "A2_H_Y_6": -720,

            "A1_H_X_1": 1200,
            "A1_H_Y_1": 800,
            "A1_H_X_2": 1200,
            "A1_H_Y_2": 40,
            "A1_H_X_3": 1200,
            "A1_H_Y_3": -820,
            "A1_H_X_4": 450,
            "A1_H_Y_4": -60,
            "A1_H_X_5": 1900,
            "A1_H_Y_5": 20,
            "A1_H_X_6": 1900,
            "A1_H_Y_6": -860
        }

    def get_configuration(self):
        return self.configuration

    def set_configuration(self, configuration):
        self.configuration = configuration
