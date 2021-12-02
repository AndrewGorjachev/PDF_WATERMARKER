import PyPDF2
import reportlab
from PySide2.QtCore import QObject, Signal
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A3, A4, landscape, A2
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class PDFRunner(QObject):

    finished = Signal()

    files_didnt_found = Signal()

    processing_has_been_completed = Signal()

    page_has_been_completed = Signal()

    total_quantity_of_pages = Signal(int, arguments=['total_quantity'])

    modified_file_name = ""

    total_page_quantity = 0;

    list_of_files = []

    watermark_text = []

    def __init__(self, list_of_file, watermark_text):

        super().__init__()

        self.total_page_quantity = 0;

        self.list_of_files = list_of_file

        self.watermark_text = watermark_text

    def __del__(self):
        print("runner deleted")

    def run(self):

        if not self.list_of_files:

            self.files_didnt_found.emit()

        else:

            for path_to_files in self.list_of_files:
                self.total_page_quantity += PyPDF2.PdfFileReader(path_to_files, 'rb').getNumPages()

            print(self.total_page_quantity);

            """
            with    tempfile.NamedTemporaryFile() as A4_V, \
                    tempfile.NamedTemporaryFile() as A4_H, \
                    tempfile.NamedTemporaryFile() as A3_V, \
                    tempfile.NamedTemporaryFile() as A3_H, \
                    tempfile.NamedTemporaryFile() as A2_H:

                self.create_horizontal_a3(A3_H)
                self.create_horizontal_a4(A4_H)
                self.create_vertical_a4(A4_V)
                self.create_vertical_a3(A3_V)
                self.create_horizontal_a2(A2_H)

                A3_H_Reader = PyPDF2.PdfFileReader(A3_H, 'rb')
                A4_v_Reader = PyPDF2.PdfFileReader(A4_V, 'rb')
                A4_H_Reader = PyPDF2.PdfFileReader(A4_H, 'rb')
                A3_V_Reader = PyPDF2.PdfFileReader(A3_V, 'rb')
                A2_H_Reader = PyPDF2.PdfFileReader(A2_H, 'rb')

                A3_H_Watermark = A3_H_Reader.getPage(0)
                A4_v_Watermark = A4_v_Reader.getPage(0)
                A4_H_Watermark = A4_H_Reader.getPage(0)
                A3_v_Watermark = A3_V_Reader.getPage(0)
                A2_H_Watermark = A2_H_Reader.getPage(0)

                for path_to_files in self.list_of_files:

                    print(path_to_files)

                    try:
                        pdfReader = PyPDF2.PdfFileReader(path_to_files, 'rb')

                        output = PyPDF2.PdfFileWriter()

                        for i in range(pdfReader.getNumPages()):

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

                            else:
                                print("unknown page format")

                                print('x=' + str(x) + '  y=' + str(y))

                                continue

                            output.addPage(page_to_merge)

                            if ".PDF" in path_to_files:
                                self.modified_file_name = path_to_files.replace(".PDF", "_marked.pdf")
                            else:
                                self.modified_file_name = path_to_files.replace(".pdf", "_marked.pdf")

                            with open(self.modified_file_name, "wb") as merged_file:

                                output.write(merged_file)

                                self.processing_has_been_completed.emit()

                    except Exception as e:
                        print(e)
                        self.files_didnt_found.emit()
            """
        self.finished.emit()

    def create_vertical_a4(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=A4)
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.25)
        canvas.setFillColor(font_color)
        canvas.drawCentredString(x=600, y=300, text=self.watermark_text[0])
        canvas.drawCentredString(x=600, y=280, text=self.watermark_text[1])
        canvas.drawCentredString(x=600, y=260, text=self.watermark_text[2])
        canvas.drawCentredString(x=420, y=-100, text=self.watermark_text[0])
        canvas.drawCentredString(x=420, y=-120, text=self.watermark_text[1])
        canvas.drawCentredString(x=420, y=-140, text=self.watermark_text[2])
        canvas.showPage()
        canvas.save()

    def create_horizontal_a4(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A4))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)
        canvas.drawCentredString(x=420, y=140, text=self.watermark_text[0])
        canvas.drawCentredString(x=420, y=120, text=self.watermark_text[1])
        canvas.drawCentredString(x=420, y=100, text=self.watermark_text[2])
        canvas.drawCentredString(x=580, y=-260, text=self.watermark_text[0])
        canvas.drawCentredString(x=580, y=-280, text=self.watermark_text[1])
        canvas.drawCentredString(x=580, y=-300, text=self.watermark_text[2])
        canvas.showPage()
        canvas.save()

    def create_vertical_a3(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=reportlab.lib.pagesizes.A3)
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)
        canvas.drawCentredString(x=840, y=540, text=self.watermark_text[0])
        canvas.drawCentredString(x=840, y=520, text=self.watermark_text[1])
        canvas.drawCentredString(x=840, y=500, text=self.watermark_text[2])

        canvas.drawCentredString(x=700, y=160, text=self.watermark_text[0])
        canvas.drawCentredString(x=700, y=140, text=self.watermark_text[1])
        canvas.drawCentredString(x=700, y=120, text=self.watermark_text[2])

        canvas.drawCentredString(x=600, y=-260, text=self.watermark_text[0])
        canvas.drawCentredString(x=600, y=-280, text=self.watermark_text[1])
        canvas.drawCentredString(x=600, y=-300, text=self.watermark_text[2])
        canvas.showPage()
        canvas.save()

    def create_horizontal_a3(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A3))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=600, y=300, text=self.watermark_text[0])
        canvas.drawCentredString(x=600, y=280, text=self.watermark_text[1])
        canvas.drawCentredString(x=600, y=260, text=self.watermark_text[2])

        canvas.drawCentredString(x=840, y=-520, text=self.watermark_text[0])
        canvas.drawCentredString(x=840, y=-540, text=self.watermark_text[1])
        canvas.drawCentredString(x=840, y=-560, text=self.watermark_text[2])

        canvas.drawCentredString(x=740, y=-120, text=self.watermark_text[0])
        canvas.drawCentredString(x=740, y=-140, text=self.watermark_text[1])
        canvas.drawCentredString(x=740, y=-160, text=self.watermark_text[2])

        canvas.showPage()
        canvas.save()

    def create_horizontal_a2(self, temp_file_name):
        canvas = reportlab.pdfgen.canvas.Canvas(temp_file_name, pagesize=landscape(A2))
        canvas.rotate(45)
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        canvas.setFont('Arial', 16)
        font_color = Color(0, 0, 0, alpha=0.5)
        canvas.setFillColor(font_color)

        canvas.drawCentredString(x=600, y=300, text=self.watermark_text[0])
        canvas.drawCentredString(x=600, y=280, text=self.watermark_text[1])
        canvas.drawCentredString(x=600, y=260, text=self.watermark_text[2])

        canvas.drawCentredString(x=840, y=-520, text=self.watermark_text[0])
        canvas.drawCentredString(x=840, y=-540, text=self.watermark_text[1])
        canvas.drawCentredString(x=840, y=-560, text=self.watermark_text[2])

        canvas.drawCentredString(x=740, y=-120, text=self.watermark_text[0])
        canvas.drawCentredString(x=740, y=-140, text=self.watermark_text[1])
        canvas.drawCentredString(x=740, y=-160, text=self.watermark_text[2])

        canvas.drawCentredString(x=1200, y=300, text=self.watermark_text[0])
        canvas.drawCentredString(x=1200, y=280, text=self.watermark_text[1])
        canvas.drawCentredString(x=1200, y=260, text=self.watermark_text[2])

        canvas.drawCentredString(x=1680, y=-520, text=self.watermark_text[0])
        canvas.drawCentredString(x=1680, y=-540, text=self.watermark_text[1])
        canvas.drawCentredString(x=1680, y=-560, text=self.watermark_text[2])

        canvas.drawCentredString(x=1480, y=-120, text=self.watermark_text[0])
        canvas.drawCentredString(x=1480, y=-140, text=self.watermark_text[1])
        canvas.drawCentredString(x=1480, y=-160, text=self.watermark_text[2])

        canvas.showPage()
        canvas.save()
