# This Python file uses the following encoding: utf-8
import re

import tempfile

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.colors import HexColor, PCMYKColor, PCMYKColorSep, Color, black, blue, red
from reportlab.lib.styles import getSampleStyleSheet
import PyPDF2
from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer


# from EnableRTLRunner import EnableRTLRunner


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
        self.create_horizontal_a3()
        print("main window controller has started")

    def __del__(self):
        pass

    def create_vertical_a4(self):
        canvas = reportlab.pdfgen.canvas.Canvas("a4_v.pdf", pagesize=A4)
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

    def create_horizontal_a4(self):
        canvas = reportlab.pdfgen.canvas.Canvas("a4_h.pdf", pagesize=landscape(A4))
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

    def create_vertical_a3(self):
        canvas = reportlab.pdfgen.canvas.Canvas("a3_v.pdf", pagesize=reportlab.lib.pagesizes.A3)
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

    def create_horizontal_a3(self):
        canvas = reportlab.pdfgen.canvas.Canvas("a3_h.pdf", pagesize=landscape(A3))
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

            watermark_pdf = PyPDF2.PdfFileReader('a3_h.pdf', 'rb')

            for i in range(pdfReader.getNumPages()):

                x = pdfReader.getPage(i).mediaBox.upperRight[0]

                y = pdfReader.getPage(i).mediaBox.upperRight[1]

                if (int(x) == 1190) and (int(y) == 841):

                    print(i)

                    watermark_page = watermark_pdf.getPage(0)

                    page_to_merge = pdfReader.getPage(i)

                    page_to_merge.mergePage(watermark_page)

                    output.addPage(page_to_merge)
                else:
                    print("unknown page format")

                    print('x=' + str(x) + '  y=' + str(y))

            if ".PDF" in self.path_to_files:
                self.modified_file_name = self.path_to_files.replace(".PDF", "_marked.pdf")

            else:
                self.modified_file_name = self.path_to_files.replace(".pdf", "_marked.pdf")

            with open(self.modified_file_name, "wb") as merged_file:

                output.write(merged_file)

        except Exception as e:
            print(e)
            self.files_didnt_found.emit()



        # print(pdfReader.getPage(0).mediaBox.upperRight[0])
        #
        # pdfReader1 = PyPDF2.PdfFileReader('a3_h.pdf', 'rb')
        #
        # print(pdfReader1.getNumPages())
        #
        # print(pdfReader1.getPage(0).mediaBox)
        #
        # pdfReader2 = PyPDF2.PdfFileReader('a3_v.pdf', 'rb')
        #
        # print(pdfReader2.getNumPages())
        #
        # print(pdfReader2.getPage(0).mediaBox)
        #
        #
        #
        # print(pdfReader3.getNumPages())
        #
        # print(pdfReader3.getPage(0).mediaBox)


        # with tempfile.NamedTemporaryFile() as tmp:
        #
        #     pdfWriter = PyPDF2.PdfFileWriter()
        #
        #     pdfWriter.addBlankPage(219, 297)
        #
        #     print(tmp.name)

        # self.directory_didnt_exist.emit()
        #
        # self.files_didnt_found.emit()
        #
        # self.processing_has_been_completed.emit()
        #
        # self.error_while_processing.emit(path_to_directory)
