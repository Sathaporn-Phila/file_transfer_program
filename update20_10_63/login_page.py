from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import file_database
import index_page,register_page

class Login_page(QWidget):

    switch_window = pyqtSignal(str)

    def __init__(self):
        self.app_index_page = None
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.set_gui()
        self.setWindowTitle("Login Page")
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def set_gui(self):
        self.name_label = ["Login to File transfer system","Name : ","Password : "]
        self.name_button = ["Register","Login"]
        self.button = []
        self.entry_item = []
        self.grid_layout = QGridLayout()

        for item in range(1,len(self.name_label)):
            text_name = self.name_label[item]
            label = QLabel()
            label.setText(text_name)
            self.grid_layout.addWidget(label,item-1,0,1,1)
            if text_name == "Password : " :
                text_edit = QLineEdit(self)
                text_edit.setEchoMode(QLineEdit.Password)
            else:
                text_edit = QLineEdit(self)
            self.entry_item.append(text_edit)
            self.grid_layout.addWidget(text_edit,item-1,1,1,3)

        self.header = QLabel()
        self.header.setText((self.name_label[0]))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.adjustSize()

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addStretch(1)
        for item in self.name_button :
            button = QPushButton(self)
            button.setText(item)
            if item == "Register" :
                button.clicked.connect(self.register)
            else :
                button.clicked.connect(self.login)
            self.horizontal_layout.addWidget(button)
            self.button.append(button)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.header)
        self.vertical_layout.addLayout(self.grid_layout)
        self.vertical_layout.addLayout(self.horizontal_layout)
        
        self.setLayout(self.vertical_layout)

    def login(self):
        self.username,self.password = self.entry_item[0].text(),self.entry_item[1].text()
        self.database = file_database.File_database()
        self.username = self.database.login(self.username,self.password)
        if (self.username != None) :
            self.switch_window.emit(self.username)
            
    def register(self):
        self.dialog = register_page.RegisterPage(self)
        
class Controller :

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.show_login()
    def show_login(self):
        self.loginPage = Login_page()
        self.loginPage.switch_window.connect(lambda:self.show_index_page(self.loginPage.username))
        self.loginPage.show()
    def show_index_page(self,username):
        self.main_page = index_page.PublicPage(username)
        self.main_page.my_database = self.loginPage.database
        print(self.main_page.my_database.get_send_history(),self.main_page.my_database.get_inbox())
        self.main_page.switch_window.connect(lambda:self.show_login_again())
        self.loginPage.close()
        self.main_page.show()
    def show_login_again(self):
        print(1)
        self.main_page.close()
        self.main_page.background_thread.terminate()
        self.show_login()

def test():
    program_test = Controller()
    sys.exit(program_test.app.exec_())
test()