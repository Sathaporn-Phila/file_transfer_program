from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class App(QWidget):
    border = 20
    normal_font_size = 20
    # initialized value before runs application
    def __init__(self):
        super().__init__()
        self.screen_width = 1366
        self.screen_height = 768
        self.title = "File transfer program"
        self.app_width = 800
        self.app_height = 600
        self.initial_x = (self.screen_width - self.app_width)//2
        self.initial_y = (self.screen_height - self.app_height)//2
        self.init_gui()
    
    def init_gui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.initial_x, self.initial_y, self.app_width, self.app_height)
        self.search_box()
        self.show()

    def paintEvent(self,event):
        self.qpaint = QPainter()
        self.qpaint.begin(self)
        top = self.header()
        file_transfer_button = self.prepare_file_transfer_button()
        slide_tab = self.slide_bar()
        show_event = self.main_show_event()
        self.qpaint.end()

    def header(self):
        self.header_font = self.app_height//16
        self.header_width = self.app_width-2*self.border
        self.header_height = self.app_height//4

        self.qpaint.setPen(QColor(Qt.blue))
        
        self.qpaint.drawRect(self.border,self.border,self.header_width,self.header_height)
        self.qpaint.fillRect(self.border,self.border,self.header_width,self.header_height,QBrush(Qt.blue))

        self.qpaint.setPen(QColor(Qt.white))
        self.qpaint.setFont(QFont('Times New Roman',self.header_font))
        self.qpaint.drawText(self.border*2,self.border+self.header_height//2,"Username:..........")

    def prepare_file_transfer_button(self):
        self.transfer_button_width = self.header_height//2 - self.border
        self.transfer_button_height = self.header_height - 2*self.border
        x = self.app_width - 2*self.border -  self.transfer_button_width
        y = 2*self.border
        self.qpaint.setPen(QColor(Qt.white))
        self.qpaint.drawRect(x,y,self.transfer_button_width,self.transfer_button_height)
        self.qpaint.fillRect(x,y,self.transfer_button_width,self.transfer_button_height,QBrush(Qt.white))

        self.qpaint.setPen(QColor(Qt.black))
        self.qpaint.setFont(QFont('Times New Roman',self.header_font))
        self.qpaint.drawText(x+self.transfer_button_width//4,y+self.transfer_button_height//2,"+")

    def slide_bar(self):
        x = self.border
        y = self.header_height+ 2*self.border
        self.button_width = self.header_width//4
        self.button_height = (self.app_height - y - self.border)//3
        num_button = 3
        self.qpaint.setPen(QColor(Qt.black))
        for num_item in range(num_button):
            self.qpaint.drawRect(x,y,self.button_width,self.button_height)
            self.qpaint.fillRect(x,y,self.button_width,self.button_height,QBrush(Qt.white))
            y += self.button_height + 5

        y_mid = self.header_height+ 2*self.border + self.button_height//2
        x_mid = self.border + self.button_width//2
        self.qpaint.setPen(QColor(Qt.black))
        self.qpaint.setFont(QFont('Times New Roman',20))
        name_button = ["public","inbox","send"]
        for num_item in range(len(name_button)):
            self.qpaint.drawText(x_mid,y_mid,name_button[num_item])
            y_mid += self.button_height

    def main_show_event(self):
        x = self.button_width + 2*self.border
        y = self.header_height+ 2*self.border
        main_show_width = self.app_width - self.border - x
        main_show_height = self.app_height - y - 2*self.border - self.button_height//2
        self.qpaint.setPen(QColor(Qt.red))
        self.qpaint.drawRect(x,y,main_show_width,main_show_height)

    def search_box(self):
        button_height = (self.app_height - self.app_height//4 - 3*self.border)//3
        x = self.app_width//4 + 2*self.border
        y = self.app_height - self.border - button_height//2
        self.textbox = QLineEdit(self)
        self.textbox.move(x,y)
        self.textbox_width = self.app_width - 4*self.border - x 
        self.textbox_height = button_height//2
        self.textbox.resize(self.textbox_width,self.textbox_height)

def run_app():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

run_app()