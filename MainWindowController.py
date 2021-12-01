# This Python file uses the following encoding: utf-8

import tempfile

import PyPDF2
import reportlab
from PySide2.QtCore import QObject, Signal, Slot
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from PDFRunner import PDFRunner


class MainWindowController(QObject):
    directory_didnt_exist = Signal()

    files_didnt_found = Signal()

    processing_has_been_completed = Signal()

    error_while_processing = Signal(str, arguments=['file_path'])

    useful_text = ['«Trade secret»', 'Horns and Hooves LLC.', 'Neverland, Chernomorsk city']

    path_to_files = ""

    modified_file_name = ""

    def __init__(self):
        super().__init__()

    def __del__(self):
        pass

    def create_vertical_a4(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=A4)
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.25)
        canvas.setFillColor(font_color)
        canvas.drawCentredString(x=600, y=300, text=self.useful_text[0])
        canvas.drawCentredString(x=600, y=280, text=self.useful_text[1])
        canvas.drawCentredString(x=600, y=260, text=self.useful_text[2])
        canvas.drawCentredString(x=420, y=-100, text=self.useful_text[0])
        canvas.drawCentredString(x=420, y=-120, text=self.useful_text[1])
        canvas.drawCentredString(x=420, y=-140, text=self.useful_text[2])
        canvas.showPage()
        canvas.save()

    def create_horizontal_a4(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A4))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)
        canvas.drawCentredString(x=420, y=140, text=self.useful_text[0])
        canvas.drawCentredString(x=420, y=120, text=self.useful_text[1])
        canvas.drawCentredString(x=420, y=100, text=self.useful_text[2])
        canvas.drawCentredString(x=580, y=-260, text=self.useful_text[0])
        canvas.drawCentredString(x=580, y=-280, text=self.useful_text[1])
        canvas.drawCentredString(x=580, y=-300, text=self.useful_text[2])
        canvas.showPage()
        canvas.save()

    def create_vertical_a3(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=reportlab.lib.pagesizes.A3)
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)
        canvas.drawCentredString(x=840, y=540, text=self.useful_text[0])
        canvas.drawCentredString(x=840, y=520, text=self.useful_text[1])
        canvas.drawCentredString(x=840, y=500, text=self.useful_text[2])

        canvas.drawCentredString(x=700, y=160, text=self.useful_text[0])
        canvas.drawCentredString(x=700, y=140, text=self.useful_text[1])
        canvas.drawCentredString(x=700, y=120, text=self.useful_text[2])

        canvas.drawCentredString(x=600, y=-260, text=self.useful_text[0])
        canvas.drawCentredString(x=600, y=-280, text=self.useful_text[1])
        canvas.drawCentredString(x=600, y=-300, text=self.useful_text[2])
        canvas.showPage()
        canvas.save()

    def create_horizontal_a3(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A3))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=600, y=300, text=self.useful_text[0])
        canvas.drawCentredString(x=600, y=280, text=self.useful_text[1])
        canvas.drawCentredString(x=600, y=260, text=self.useful_text[2])

        canvas.drawCentredString(x=840, y=-520, text=self.useful_text[0])
        canvas.drawCentredString(x=840, y=-540, text=self.useful_text[1])
        canvas.drawCentredString(x=840, y=-560, text=self.useful_text[2])

        canvas.drawCentredString(x=740, y=-120, text=self.useful_text[0])
        canvas.drawCentredString(x=740, y=-140, text=self.useful_text[1])
        canvas.drawCentredString(x=740, y=-160, text=self.useful_text[2])

        canvas.showPage()
        canvas.save()

    @Slot(str, str)
    def process_pdfs(self, path_to_directory, watermark_text):

        print(path_to_directory)

        if "file:///" in path_to_directory:

            self.path_to_files = path_to_directory.replace("file:///", "")

        else:

            self.path_to_files = path_to_directory

        try:
            pdfReader = PyPDF2.PdfFileReader(self.path_to_files, 'rb')

            output = PyPDF2.PdfFileWriter()

            with tempfile.NamedTemporaryFile() as A3_H, \
                 tempfile.NamedTemporaryFile() as A4_V, \
                 tempfile.NamedTemporaryFile() as A4_H, \
                 tempfile.NamedTemporaryFile() as A3_V:

                self.create_horizontal_a3(A3_H)
                self.create_horizontal_a4(A4_H)
                self.create_vertical_a4(A4_V)
                self.create_vertical_a3(A3_V)

                A3_H_Reader = PyPDF2.PdfFileReader(A3_H, 'rb')
                A4_v_Reader = PyPDF2.PdfFileReader(A4_V, 'rb')
                A4_H_Reader = PyPDF2.PdfFileReader(A4_H, 'rb')
                A3_V_Reader = PyPDF2.PdfFileReader(A3_V, 'rb')

                A3_H_Watermark = A3_H_Reader.getPage(0)
                A4_v_Watermark = A4_v_Reader.getPage(0)
                A4_H_Watermark = A4_H_Reader.getPage(0)
                A3_v_Watermark = A3_V_Reader.getPage(0)

                for i in range(pdfReader.getNumPages()):

                    x = pdfReader.getPage(i).mediaBox.upperRight[0]

                    y = pdfReader.getPage(i).mediaBox.upperRight[1]

                    page_to_merge = pdfReader.getPage(i)

                    if (int(x) == 1190) and (int(y) == 841):

                        page_to_merge.mergePage(A3_H_Watermark)

                    elif (int(x) == 595) and (int(y) == 841):

                        page_to_merge.mergePage(A4_v_Watermark)

                    elif (int(x) == 841) and (int(y) == 595):

                        page_to_merge.mergePage(A4_H_Watermark)

                    elif (int(x) == 841) and (int(y) == 1190):

                        page_to_merge.mergePage(A3_v_Watermark)

                    else:
                        print("unknown page format")

                        print('x=' + str(x) + '  y=' + str(y))

                    output.addPage(page_to_merge)

                if ".PDF" in self.path_to_files:
                    self.modified_file_name = self.path_to_files.replace(".PDF", "_marked.pdf")
                else:
                    self.modified_file_name = self.path_to_files.replace(".pdf", "_marked.pdf")

                with open(self.modified_file_name, "wb") as merged_file:

                    output.write(merged_file)

                    self.processing_has_been_completed.emit()

        except Exception as e:
            print(e)
            self.files_didnt_found.emit()


        # self.directory_didnt_exist.emit()
        #
        # self.files_didnt_found.emit()
        #
        # self.processing_has_been_completed.emit()
        #
        # self.error_while_processing.emit(path_to_directory)