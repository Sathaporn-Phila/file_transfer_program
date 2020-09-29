from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Login_page(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.set_gui()
        self.setWindowTitle("Login Page")
        self.center()
        self.show()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def set_gui(self):
        self.name_label = ["Login to File transfer system","Name : ","Password : "]
        self.name_button = ["Register","Login"]
        self.button = []
        self.grid_layout = QGridLayout()

        for item in range(1,len(self.name_label)):
            text_name = self.name_label[item]
            label = QLabel()
            label.setText(text_name)
            self.grid_layout.addWidget(label,item-1,0,1,1)
            if text_name == "Password : " :
                text_edit = QLineEdit()
                text_edit.setEchoMode(QLineEdit.Password)
            else:
                text_edit = QLineEdit()
            self.grid_layout.addWidget(text_edit,item-1,1,1,3)

        self.header = QLabel()
        self.header.setText((self.name_label[0]))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.adjustSize()

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addStretch(1)
        for item in self.name_button :
            button = QPushButton()
            button.setText(item)
            self.horizontal_layout.addWidget(button)
            self.button.append(button)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.header)
        self.vertical_layout.addLayout(self.grid_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)
        
        self.setLayout(self.vertical_layout)