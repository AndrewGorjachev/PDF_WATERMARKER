import configparser

from PySide2.QtCore import QObject, Signal


class INIManager(QObject):
    configuration = {
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

        "
    }



    def __init__(self):
        pass

    def __del__(self):
        pass

    def read_config_file(self):

        config = configparser.ConfigParser()

        if config.read('watermark.ini'):
            self.configuration["str0"] = config["watermark"]["str0"]
            self.configuration["str1"] = config["watermark"]["str1"]
            self.configuration["str2"] = config["watermark"]["str2"]

            self.configuration["opacity"] = int(config['text_property']['opacity'])

            self.configuration["font_size"] = int(config['text_property']['font_size'])

            if (self.configuration["font_size"] > 22) and (self.configuration["font_size"] < 10):
                self.configuration["font_size"] = 16
            else:
                raise Exception('Wrong ini format.')

    def write_config_file(self):
        config = configparser.ConfigParser()
        config['watermark'] = {}
        config['watermark']["str0"] = self.configuration["str0"]
        config['watermark']["str1"] = self.configuration["str1"]
        config['watermark']["str2"] = self.configuration["str2"]

        config['text_property'] = {}
        config['text_property']['opacity'] = self.configuration["opacity"]
        config['text_property']['font_size'] = self.configuration["font_size"]
        config['text_property']['font_coefficient'] = self.configuration["font_coefficient"]

        config['a4_vertical'] = {}
        config['a4_vertical']['X_1'] = self.configuration["A4_V_X_1"]
        config['a4_vertical']['Y_1'] = self.configuration["A4_V_Y_1"]
        config['a4_vertical']['X_2'] = self.configuration["A4_V_X_2"]
        config['a4_vertical']['Y_2'] = self.configuration["A4_V_Y_2"]

        config['a4_horizontal'] = {}
        config['a4_horizontal']['X_1'] = self.configuration["A4_H_X_1"]
        config['a4_horizontal']['Y_1'] = self.configuration["A4_H_Y_1"]
        config['a4_horizontal']['X_2'] = self.configuration["A4_H_X_2"]
        config['a4_horizontal']['Y_2'] = self.configuration["A4_H_Y_2"]

        config['a3_vertical'] = {}
        config['a3_vertical']['X_1'] = self.configuration["A3_V_X_1"]
        config['a3_vertical']['Y_1'] = self.configuration["A3_V_Y_1"]
        config['a3_vertical']['X_2'] = self.configuration["A3_V_X_2"]
        config['a3_vertical']['Y_2'] = self.configuration["A3_V_Y_2"]
        config['a3_vertical']['X_3'] = self.configuration["A3_V_X_3"]
        config['a3_vertical']['Y_3'] = self.configuration["A3_V_Y_3"]

        config['a3_horizontal'] = {}
        config['a3_horizontal']['X_1'] = self.configuration["A3_H_X_1"]
        config['a3_horizontal']['Y_1'] = self.configuration["A3_H_Y_1"]
        config['a3_horizontal']['X_2'] = self.configuration["A3_H_X_2"]
        config['a3_horizontal']['Y_2'] = self.configuration["A3_H_Y_2"]
        config['a3_horizontal']['X_3'] = self.configuration["A3_H_X_3"]
        config['a3_horizontal']['Y_3'] = self.configuration["A3_H_Y_3"]


        self.A2_H_X_1 = 600
        self.A2_H_Y_1 = 300
        self.A2_H_X_2 = 840
        self.A2_H_Y_2 = -520
        self.A2_H_X_3 = 740
        self.A2_H_Y_3 = -120
        self.A2_H_X_4 = 1250
        self.A2_H_Y_4 = 100
        self.A2_H_X_5 = 1250
        self.A2_H_Y_5 = -320
        self.A2_H_X_6 = 1250
        self.A2_H_Y_6 = -720

        self.A1_H_X_1 = 1200
        self.A1_H_Y_1 = 800
        self.A1_H_X_2 = 1200
        self.A1_H_Y_2 = 40
        self.A1_H_X_3 = 1200
        self.A1_H_Y_3 = -820
        self.A1_H_X_4 = 450
        self.A1_H_Y_4 = -60
        self.A1_H_X_5 = 1900
        self.A1_H_Y_5 = 20
        self.A1_H_X_6 = 1900
        self.A1_H_Y_6 = -860

        with open('watermark.ini', 'w') as configfile:
            config.write(configfile)

    def get_configuration(self):
        return self.configuration
