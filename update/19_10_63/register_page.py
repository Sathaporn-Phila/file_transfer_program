from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import file_database

class RegisterPage(QDialog):

    def __init__(self,parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register")
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
        self.name_label = {"Username : ":'',"Password : ":''}
        self.name_button = {"OK":'',"Cancel":''}
        for item in self.name_label.keys():
            label = QLabel(self)
            label.setText(item)
            text_edit = QLineEdit(self)
            self.name_label[item] = text_edit
            self.form_layout.addRow(label,text_edit)

        self.horizon_layout = QHBoxLayout(self)
        self.horizon_layout.addStretch(1)
        for item in self.name_button.keys():
            if item == "OK":
                button = QDialogButtonBox(QDialogButtonBox.Ok)
                button.clicked.connect(self.ok_command)
            else :
                button = QDialogButtonBox(QDialogButtonBox.Cancel)
                button.clicked.connect(self.cancel_command)
            self.name_button[item] = button
            self.horizon_layout.addWidget(button)
        self.form_layout.addRow(self.horizon_layout)
        self.setLayout(self.form_layout)

    def ok_command(self):
        self.database = file_database.File_database()
        username_textedit = self.name_label["Username : "].text()
        password_textedit = self.name_label["Password : "].text()
        self.database.register_account(username_textedit,password_textedit)
        self.database.check_all_id()
        self.close()

    def cancel_command(self):
        self.close()