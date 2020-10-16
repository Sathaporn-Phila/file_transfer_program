from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import websocket
import asyncio
from pathlib import Path

class ExportForm(QDialog):

    uri = "ws://localhost:8000"

    def __init__(self,user_name):
        super().__init__()
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Export Form")
        self.center()
        self.set_gui()
        self.show()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def set_gui(self):
        self.form_layout = QFormLayout(self)
        self.entry_item = []
        self.dynamic_item = []
        self.name_label = ["Title : ","Author : ","Send to : ","User to receive : ","File : " ]
        for item in self.name_label :
            label = QLabel(self)
            label.setText(item)
            if item == "Send to : ":
                self.row_layout = QHBoxLayout(self)
                radio_button_name = ["Public","Private"]
                for item in radio_button_name :
                    radio_button = QRadioButton(item,self)
                    self.dynamic_item.append(radio_button)
                    self.row_layout.addWidget(radio_button)
                self.form_layout.addRow(label,self.row_layout)
            else:
                textbox = QLineEdit(self)
                if item == "User to receive : " :
                    textbox.setReadOnly(True)
                    textbox.setStyleSheet("background-color : rgb(216,216,216);")
                    self.dynamic_item.append(textbox)
                    self.form_layout.addRow(label,textbox)
                elif item == "Author : " :
                    textbox.setText(self.user_name)
                    textbox.setReadOnly(True)
                    self.form_layout.addRow(label,textbox)  
                else : 
                    self.entry_item.append(textbox)
                    if item == 'File : ' :
                        open_file_button = QPushButton(self)
                        open_file_button.setText("Add path")
                        open_file_button.clicked.connect(self.file_dialog)
                        
                        self.row_layout2 = QHBoxLayout(self)
                        self.row_layout2.addWidget(textbox)
                        self.row_layout2.addWidget(open_file_button)
                        self.form_layout.addRow(label,self.row_layout2)
                    else:
                        self.form_layout.addRow(label,textbox)
                    

        self.ok_button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.ok_button.clicked.connect(self.ok_command)
        self.cancel_button = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.cancel_button.clicked.connect(self.cancel_command)

        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.addStretch(1)
        self.horizontal_layout.addWidget(self.ok_button)
        self.horizontal_layout.addWidget(self.cancel_button)

        self.form_layout.addRow(self.horizontal_layout)
        self.setLayout(self.form_layout)
        self.set_button_function()

    def set_button_function(self):
        public_button = self.dynamic_item[0]
        public_button.toggled.connect(lambda:self.set_textbox_editable(True))
        private_button = self.dynamic_item[1]
        private_button.toggled.connect(lambda:self.set_textbox_editable(False))
    
    def set_textbox_editable(self,bool_type):
        textbox = self.dynamic_item[-1]
        textbox.setReadOnly(bool_type)
        if bool_type :
            textbox.setStyleSheet("background-color : rgb(216,216,216);")
            textbox.clear()
            self.sendItemType = "send_private"
        else :
            textbox.setStyleSheet("background-color : rgb(255,255,255);")
            self.sendItemType = "send_public"

    def file_dialog(self):
        home_dir = str(Path.home)
        data = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        self.fileLineEdit = self.entry_item[-1]
        if len(self.fileLineEdit.text()) != 0 :
            self.fileLineEdit.clear()
        self.fileLineEdit.setText(data[0])

    def ok_command(self):
        self.all_item = {}
        self.name_of_item = ["Title : ","Author : ","File : "]
        for item1,item2 in zip(self.name_of_item,self.entry_item) :
            self.all_item[item1] = item2.text()
        self.all_item["Send to : "] = self.sendItemType
        self.all_item["User to receive : "] = self.dynamic_item[-1].text()
        print(self.all_item)
        #asyncio.run(lambda : self.send_item(self.all_item))
        self.close()
    
    '''async def send_item(item):
        async with websocket.server(self.uri) as websocket :
            await websocket.send(item)
            websocket.close()'''

    def cancel_command(self):
        self.close()