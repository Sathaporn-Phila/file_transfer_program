from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL.ImageQt import ImageQt
import sys,image_create

class Button(QPushButton):

    def __init__(self,parent,text):
        super().__init__(parent)
        self.text = text
class TreeView(QTreeView):

    def __init__(self,parent):
        super().__init__(parent)
        super().setHeaderHidden(True)

class Item(QStandardItem):

    def __init__(self,text = "",color = QColor(Qt.black),fontSize = 20):
        super().__init__()
        font = QFont("Times New Roman",fontSize)
        self.setEditable(False)
        self.setFont(font)
        self.setText(text)

class TreeModel(QStandardItemModel):

    def __init__(self,parent):
        super().__init__(parent)
        self.root_node = super().invisibleRootItem

class Header :

    def __init__(self,user_name):
        self.user_image = ImageQt(image_create.user_image(user_name,"darkblue"))
    
class PublicPage(QWidget):

    def __init__(self,user_name):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.user_name = user_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File transfer system")
        self.center()
        self.set_gui()
        self.show()
        sys.exit(self.app.exec_())

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def set_gui(self):

        self.line = 0

        content_button = ["Public", "Inbox", "Send", "Export", "Import","Log out"]
        self.header_image = self.image(Header(self.user_name).user_image)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.header_image)

        self.main_zone = QGridLayout()
        for num in range(len(content_button)):
            item = Button(self,content_button[num])
            item.setStyleSheet("background-color : rgb(0,255,0);")
            item.setText(item.text)
            self.main_zone.addWidget(item,num*2,0,2,2)
            self.line += num

        self.main_zone.addWidget(TreeView(self),0,3,2*len(content_button),2*len(content_button))
        
        find_label = QLabel()
        find_label.setText("find : ")
        find_label.setAlignment(Qt.AlignCenter)
        self.main_zone.addWidget(find_label,self.line+1,0,2,2)
        self.main_zone.addWidget(QLineEdit(self),self.line+1,3,2,2*(len(content_button)-1))

        self.search_button_function_name = ["----->","Reset"]
        
        for num in range(len(self.search_button_function_name)):
            item = Button(self,self.search_button_function_name[num])
            item.setStyleSheet("background-color : rgb(0,255,100);")
            item.setText(item.text)
            self.main_zone.addWidget(item,self.line+1,3+2*(len(content_button)-1)+num,1,1)
        
        
        self.vertical_layout.addLayout(self.main_zone)
        self.setLayout(self.vertical_layout)

    def image(self,picture):
        self.new_image = QLabel("",self)
        new_image = QPixmap.fromImage(picture)
        self.new_image.setPixmap(new_image.scaled(new_image.width()//2,new_image.height()//2))
        self.new_image.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        self.new_image.setAlignment(Qt.AlignCenter)
        return self.new_image

ex = PublicPage("Nuieasy")
   
        
    
