import tempfile

import PyPDF2
import reportlab
from PySide2.QtCore import QObject, Signal
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A3, A4, landscape, A2
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class PDFRunner(QObject):
    finished_signal = Signal()

    processing_completed_signal = Signal()

    wrong_page_format_signal = Signal(str, arguments=['file_path'])

    file_not_found_signal = Signal(str, arguments=['file_path'])

    file_corrupted_signal = Signal(str, arguments=['file_path'])

    total_quantity_of_pages_signal = Signal(int, arguments=['total_quantity'])

    rest_of_pages_signal = Signal(int, arguments=['rest_quantity'])

    modified_file_name = ""

    total_page_quantity = 0

    opacity = 0.5

    font_size = 16

    list_of_files = []

    watermark_text = [" ", " ", " "]

    def __init__(self, list_of_file, current_configuration):

        super().__init__()

        self.list_of_files = list_of_file

        self.watermark_text[0] = current_configuration['str0']

        self.watermark_text[1] = current_configuration["str1"]

        self.watermark_text[2] = current_configuration["str2"]

        self.opacity = current_configuration["opacity"] / 100.0

        self.font_size = current_configuration["font_size"]

        self.k = current_configuration['font_coefficient']

        self.A4_V_X_1 = current_configuration["A4_V_X_1"]
        self.A4_V_Y_1 = current_configuration["A4_V_Y_1"]
        self.A4_V_X_2 = current_configuration["A4_V_X_2"]
        self.A4_V_Y_2 = current_configuration["A4_V_Y_2"]

        self.A4_H_X_1 = current_configuration["A4_H_X_1"]
        self.A4_H_Y_1 = current_configuration["A4_H_Y_1"]
        self.A4_H_X_2 = current_configuration["A4_H_X_2"]
        self.A4_H_Y_2 = current_configuration["A4_H_Y_2"]

        self.A3_V_X_1 = current_configuration["A3_V_X_1"]
        self.A3_V_Y_1 = current_configuration["A3_V_Y_1"]
        self.A3_V_X_2 = current_configuration["A3_V_X_2"]
        self.A3_V_Y_2 = current_configuration["A3_V_Y_2"]
        self.A3_V_X_3 = current_configuration["A3_V_X_3"]
        self.A3_V_Y_3 = current_configuration["A3_V_Y_3"]

        self.A3_H_X_1 = current_configuration["A3_H_X_1"]
        self.A3_H_Y_1 = current_configuration["A3_H_Y_1"]
        self.A3_H_X_2 = current_configuration["A3_H_X_2"]
        self.A3_H_Y_2 = current_configuration["A3_H_Y_2"]
        self.A3_H_X_3 = current_configuration["A3_H_X_3"]
        self.A3_H_Y_3 = current_configuration["A3_H_Y_3"]

        self.A2_H_X_1 = current_configuration["A2_H_X_1"]
        self.A2_H_Y_1 = current_configuration["A2_H_Y_1"]
        self.A2_H_X_2 = current_configuration["A2_H_X_2"]
        self.A2_H_Y_2 = current_configuration["A2_H_Y_2"]
        self.A2_H_X_3 = current_configuration["A2_H_X_3"]
        self.A2_H_Y_3 = current_configuration["A2_H_Y_3"]
        self.A2_H_X_4 = current_configuration["A2_H_X_4"]
        self.A2_H_Y_4 = current_configuration["A2_H_Y_4"]
        self.A2_H_X_5 = current_configuration["A2_H_X_5"]
        self.A2_H_Y_5 = current_configuration["A2_H_Y_5"]
        self.A2_H_X_6 = current_configuration["A2_H_X_6"]
        self.A2_H_Y_6 = current_configuration["A2_H_Y_6"]

        self.A1_H_X_1 = current_configuration["A1_H_X_1"]
        self.A1_H_Y_1 = current_configuration["A1_H_Y_1"]
        self.A1_H_X_2 = current_configuration["A1_H_X_2"]
        self.A1_H_Y_2 = current_configuration["A1_H_Y_2"]
        self.A1_H_X_3 = current_configuration["A1_H_X_3"]
        self.A1_H_Y_3 = current_configuration["A1_H_Y_3"]
        self.A1_H_X_4 = current_configuration["A1_H_X_4"]
        self.A1_H_Y_4 = current_configuration["A1_H_Y_4"]
        self.A1_H_X_5 = current_configuration["A1_H_X_5"]
        self.A1_H_Y_5 = current_configuration["A1_H_Y_5"]
        self.A1_H_X_6 = current_configuration["A1_H_X_6"]
        self.A1_H_Y_6 = current_configuration["A1_H_Y_6"]

    def __del__(self):
        pass

    def run(self):

        self.total_page_quantity = 0

        if not self.list_of_files:

            self.file_not_found_signal.emit("The file list is empty.")

        else:

            new_list = []

            for path_to_file in self.list_of_files:

                try:

                    pages_in_current_file = PyPDF2.PdfFileReader(path_to_file, 'rb').getNumPages()

                    if pages_in_current_file != 0:

                        self.total_page_quantity += pages_in_current_file

                        new_list.append(path_to_file)

                    else:
                        self.file_corrupted_signal.emit(path_to_file)

                except Exception as e:

                    self.file_corrupted_signal.emit(path_to_file)

            if self.total_page_quantity:
                self.total_quantity_of_pages_signal.emit(self.total_page_quantity)

            with    tempfile.NamedTemporaryFile() as A4_V, \
                    tempfile.NamedTemporaryFile() as A4_H, \
                    tempfile.NamedTemporaryFile() as A3_V, \
                    tempfile.NamedTemporaryFile() as A3_H, \
                    tempfile.NamedTemporaryFile() as A2_H, \
                    tempfile.NamedTemporaryFile() as A1_H:

                self.create_horizontal_a3(A3_H)
                self.create_horizontal_a4(A4_H)
                self.create_vertical_a4(A4_V)
                self.create_vertical_a3(A3_V)
                self.create_horizontal_a2(A2_H)
                self.create_horizontal_a1(A1_H)

                A3_H_Reader = PyPDF2.PdfFileReader(A3_H, 'rb')
                A4_v_Reader = PyPDF2.PdfFileReader(A4_V, 'rb')
                A4_H_Reader = PyPDF2.PdfFileReader(A4_H, 'rb')
                A3_V_Reader = PyPDF2.PdfFileReader(A3_V, 'rb')
                A2_H_Reader = PyPDF2.PdfFileReader(A2_H, 'rb')
                A1_H_Reader = PyPDF2.PdfFileReader(A1_H, 'rb')

                A3_H_Watermark = A3_H_Reader.getPage(0)
                A4_v_Watermark = A4_v_Reader.getPage(0)
                A4_H_Watermark = A4_H_Reader.getPage(0)
                A3_v_Watermark = A3_V_Reader.getPage(0)
                A2_H_Watermark = A2_H_Reader.getPage(0)
                A1_H_Watermark = A1_H_Reader.getPage(0)

                for path_to_file in new_list:

                    try:
                        pdfReader = PyPDF2.PdfFileReader(path_to_file, 'rb')

                        output = PyPDF2.PdfFileWriter()

                        for i in range(pdfReader.getNumPages()):

                            self.total_page_quantity -= 1

                            self.rest_of_pages_signal.emit(self.total_page_quantity)

                            x = pdfReader.getPage(i).mediaBox.upperRight[0]

                            y = pdfReader.getPage(i).mediaBox.upperRight[1]

                            page_to_merge = pdfReader.getPage(i)

                            if ((int(x) >= 1190) and (int(x) <= 1200)) and ((int(y) >= 840) and (int(y) <= 850)):

                                page_to_merge.mergePage(A3_H_Watermark)

                            elif ((int(x) >= 590) and (int(x) <= 600)) and ((int(y) >= 840) and (int(y) <= 850)):

                                page_to_merge.mergePage(A4_v_Watermark)

                            elif ((int(x) >= 840) and (int(x) <= 850)) and ((int(y) >= 590) and (int(y) <= 600)):

                                page_to_merge.mergePage(A4_H_Watermark)

                            elif ((int(x) >= 840) and (int(x) <= 850)) and ((int(y) >= 1190) and (int(y) <= 1200)):

                                page_to_merge.mergePage(A3_v_Watermark)

                            elif ((int(x) >= 1680) and (int(x) <= 1690)) and ((int(y) >= 1190) and (int(y) <= 1200)):

                                page_to_merge.mergePage(A2_H_Watermark)

                            elif ((int(x) >= 2380) and (int(x) <= 2390)) and ((int(y) >= 1680) and (int(y) <= 1690)):

                                page_to_merge.mergePage(A1_H_Watermark)

                            else:

                                self.wrong_page_format_signal.emit(
                                    path_to_file + ' at page number = ' + str(i) + ' x=' + str(x) + ' y=' + str(y))

                                with tempfile.NamedTemporaryFile() as weird_format:

                                    self.create_centered_format(weird_format, x, y)

                                    weird_reader = PyPDF2.PdfFileReader(weird_format, 'rb')

                                    weird_format_watermark = weird_reader.getPage(0)

                                    page_to_merge.mergePage(weird_format_watermark)

                            output.addPage(page_to_merge)

                        if ".PDF" in path_to_file:

                            self.modified_file_name = path_to_file.replace(".PDF", "_marked.pdf")

                        else:

                            self.modified_file_name = path_to_file.replace(".pdf", "_marked.pdf")

                        with open(self.modified_file_name, "wb") as merged_file:

                            output.write(merged_file)

                    except Exception as e:

                        print(e)

                        self.file_not_found_signal.emit(path_to_file)

                self.processing_completed_signal.emit()

        self.finished_signal.emit()

    def create_vertical_a4(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=A4)
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=self.A4_V_X_1, y=self.A4_V_Y_1, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A4_V_X_1, y=(self.A4_V_Y_1 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A4_V_X_1, y=(self.A4_V_Y_1 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A4_V_X_2, y=self.A4_V_Y_2, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A4_V_X_2, y=(self.A4_V_Y_2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A4_V_X_2, y=(self.A4_V_Y_2 - (self.k * 2)), text=self.watermark_text[2])
        canvas.showPage()
        canvas.save()

    def create_horizontal_a4(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A4))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=self.A4_H_X_1, y=self.A4_H_Y_1, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A4_H_X_1, y=(self.A4_H_Y_1 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A4_H_X_1, y=(self.A4_H_Y_1 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A4_H_X_2, y=self.A4_H_Y_2, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A4_H_X_2, y=(self.A4_H_Y_2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A4_H_X_2, y=(self.A4_H_Y_2 - (self.k * 2)), text=self.watermark_text[2])
        canvas.showPage()
        canvas.save()

    def create_vertical_a3(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=reportlab.lib.pagesizes.A3)
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=self.A3_V_X_1, y=self.A3_V_Y_1, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A3_V_X_1, y=(self.A3_V_Y_1 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A3_V_X_1, y=(self.A3_V_Y_1 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A3_V_X_2, y=self.A3_V_Y_2, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A3_V_X_2, y=(self.A3_V_Y_2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A3_V_X_2, y=(self.A3_V_Y_2 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A3_V_X_3, y=self.A3_V_Y_3, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A3_V_X_3, y=(self.A3_V_Y_3 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A3_V_X_3, y=(self.A3_V_Y_3 - (self.k * 2)), text=self.watermark_text[2])
        canvas.showPage()
        canvas.save()

    def create_horizontal_a3(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A3))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=self.A3_H_X_1, y=self.A3_H_Y_1, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A3_H_X_1, y=(self.A3_H_Y_1 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A3_H_X_1, y=(self.A3_H_Y_1 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A3_H_X_2, y=self.A3_H_Y_2, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A3_H_X_2, y=(self.A3_H_Y_2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A3_H_X_2, y=(self.A3_H_Y_2 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A3_H_X_3, y=self.A3_H_Y_3, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A3_H_X_3, y=(self.A3_H_Y_3 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A3_H_X_3, y=(self.A3_H_Y_3 - (self.k * 2)), text=self.watermark_text[2])

        canvas.showPage()
        canvas.save()

    def create_horizontal_a2(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A2))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=self.A2_H_X_1, y=self.A2_H_Y_1, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A2_H_X_1, y=(self.A2_H_Y_1 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A2_H_X_1, y=(self.A2_H_Y_1 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A2_H_X_2, y=self.A2_H_Y_2, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A2_H_X_2, y=(self.A2_H_Y_2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A2_H_X_2, y=(self.A2_H_Y_2 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A2_H_X_3, y=self.A2_H_Y_3, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A2_H_X_3, y=(self.A2_H_Y_3 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A2_H_X_3, y=(self.A2_H_Y_3 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A2_H_X_4, y=self.A2_H_Y_4, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A2_H_X_4, y=(self.A2_H_Y_4 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A2_H_X_4, y=(self.A2_H_Y_4 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A2_H_X_5, y=self.A2_H_Y_5, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A2_H_X_5, y=(self.A2_H_Y_5 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A2_H_X_5, y=(self.A2_H_Y_5 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A2_H_X_6, y=self.A2_H_Y_6, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A2_H_X_6, y=(self.A2_H_Y_6 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A2_H_X_6, y=(self.A2_H_Y_6 - (self.k * 2)), text=self.watermark_text[2])

        canvas.showPage()
        canvas.save()

    def create_horizontal_a1(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A2))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=self.A1_H_X_1, y=self.A1_H_Y_1, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A1_H_X_1, y=(self.A1_H_Y_1 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A1_H_X_1, y=(self.A1_H_Y_1 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A1_H_X_2, y=self.A1_H_Y_2, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A1_H_X_2, y=(self.A1_H_Y_2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A1_H_X_2, y=(self.A1_H_Y_2 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A1_H_X_3, y=self.A1_H_Y_3, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A1_H_X_3, y=(self.A1_H_Y_3 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A1_H_X_1, y=(self.A1_H_Y_3 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A1_H_X_4, y=self.A1_H_Y_4, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A1_H_X_4, y=(self.A1_H_Y_4 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A1_H_X_4, y=(self.A1_H_Y_4 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A1_H_X_5, y=self.A1_H_Y_5, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A1_H_X_5, y=(self.A1_H_Y_5 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A1_H_X_5, y=(self.A1_H_Y_5 - (self.k * 2)), text=self.watermark_text[2])

        canvas.drawCentredString(x=self.A1_H_X_6, y=self.A1_H_Y_6, text=self.watermark_text[0])
        canvas.drawCentredString(x=self.A1_H_X_6, y=(self.A1_H_Y_6 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=self.A1_H_X_6, y=(self.A1_H_Y_6 - (self.k * 2)), text=self.watermark_text[2])

        canvas.showPage()
        canvas.save()

    def create_centered_format(self, temp_file_name, x, y):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=(x, y))

        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', self.font_size)
        font_color = Color(0, 0, 0, alpha=self.opacity)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=int(x/2), y=int(y/2), text=self.watermark_text[0])
        canvas.drawCentredString(x=int(x/2), y=int(y/2 - self.k), text=self.watermark_text[1])
        canvas.drawCentredString(x=int(x/2), y=int(y/2 - (self.k * 2)), text=self.watermark_text[2])

        canvas.showPage()
        canvas.save()