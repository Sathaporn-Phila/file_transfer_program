from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from file_database import File_database

class TreeView(QTreeView): #update

    def __init__(self,parent):
        super().__init__(parent)
        super().setHeaderHidden(True)
        self.set_structure()

    def set_structure(self):

        self.data_all = []
        self.tree_view = super()

        self.tree_model = QStandardItemModel()
        self.root_node = self.tree_model.invisibleRootItem()

        self.tree_view.setModel(self.tree_model)
        self.tree_view.expandAll()

    def add_item(self,item):
        title = Item(item[0])
        author = Item("Author : "+item[1])
        file_name = Item("File : "+item[2])
        title.appendRow(author)
        title.appendRow(file_name)
        self.root_node.appendRow(title)
        self.data_all.append(item)

    def clear(self):
        self.tree_model.clear()
        self.data_all = []
        self.set_structure()


class Item(QStandardItem):

    def __init__(self,text = "",color = QColor(Qt.black),fontSize = 20):
        super().__init__()
        font = QFont("Times New Roman",fontSize)
        self.setEditable(False)
        self.setFont(font)
        self.setText(text)

class ComboBox(QComboBox):

    type_item = pyqtSignal(str)

    def __init__(self,list_item):

        super().__init__()
        self.type_choose = None
        self.addItems(list_item)
        self.activated.connect(self.get_type_choose)

    def get_type_choose(self):

        self.type_choose = self.currentText()
        if self.type_choose != None :
            self.type_item.emit(self.type_choose)

class ImportTreeView(TreeView):

    signal = pyqtSignal(str)

    def __init__(self,parent):
        super().__init__(parent)
        self.tree_view.doubleClicked.connect(self.getValue)
        self.fileName = None
    def add_item(self,item):
        title = Item(item[0])
        author = Item("Author : "+item[1])
        file_name = Item("File : "+item[2])
        file_name.setData(item)
        title.appendRow(author)
        title.appendRow(file_name)
        self.root_node.appendRow(title)
        self.data_all.append(item)
    def getValue(self,val):
        item = val.data()
        if item.startswith('File') :
            self.fileName = item[7:]
            self.signal.emit(self.fileName)


class ImportFileDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.database = File_database()
        self.show_type_database = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Import File to Computer")
        self.center()
        self.set_gui()
        self.show()

    def center(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def set_gui(self):
        self.main_layout = QVBoxLayout(self)
        self.top_form_layout = QFormLayout(self)
        self.bottom_horizontal_layout = QHBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText("Selected from : ")

        self.file_label = QLabel(self)
        self.file_label.setText("File : ")

        self.file_lineEdit = QLineEdit(self)
        self.file_lineEdit.setReadOnly(True)

        self.notice_label = QLabel(self)
        self.notice_label.setText("Note : doubleclicked at file item before you imported file to computer ")

        self.combo = ComboBox(["Public","Inbox","All"])
        self.treeView = ImportTreeView(self)
        self.treeView.signal.connect(lambda: self.insert_file_to_lineEdit(self.treeView.fileName))
        self.combo.type_item.connect(lambda : self.get_type_database(self.combo.type_choose))

        self.top_form_layout.addRow(self.label,self.combo)
        self.top_form_layout.addRow(self.file_label,self.file_lineEdit)
        self.top_form_layout.addWidget(self.notice_label)

        self.ok_button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.ok_button.clicked.connect(self.ok_command)
        self.cancel_button = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.cancel_button.clicked.connect(self.cancel_command)

        self.bottom_horizontal_layout.addStretch(1)
        self.bottom_horizontal_layout.addWidget(self.ok_button)
        self.bottom_horizontal_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(self.top_form_layout)
        self.main_layout.addWidget(self.treeView)
        self.main_layout.addLayout(self.bottom_horizontal_layout)

        self.setLayout(self.main_layout)

    def get_type_database(self,data):
        if data != self.show_type_database :
            self.treeView.clear()
            if data == "Public":
                for item in self.database.get_public() :
                    self.treeView.add_item(item)
            elif data == "Inbox" :
                for item in self.database.get_inbox() :
                    self.treeView.add_item(item)
            elif data == "All" :
                for item in self.database.get_public() :
                    self.treeView.add_item(item)
                for item in self.database.get_inbox() :
                    self.treeView.add_item(item)
            self.show_type_database = data

    def insert_file_to_lineEdit(self,data):
        self.file_lineEdit.setText(data)

    def ok_command(self):
        if len(self.file_lineEdit.text()) > 0 :
            print(self.file_lineEdit.text())
            #ส่งไปยัง websocket เพื่อสร้างไฟล์
        self.close()
    def cancel_command(self):
        self.close()
    

    