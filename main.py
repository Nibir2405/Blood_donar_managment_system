from PyQt6.QtWidgets import QApplication, QLabel, QComboBox, QWidget, QGridLayout, QLineEdit, QPushButton,\
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Donar Management System")

        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

        add_action = QAction("Add Student", self)
        add_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Blood Group", "Phone Number", "Address"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        self.table.insertRow(0)
        
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number,column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Donar")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        #Add donar name
        self.donar_name = QLineEdit()
        self.donar_name.setPlaceholderText("Name")
        layout.addWidget(self.donar_name)

        #Add Blood Groups
        self.blood_group = QComboBox()
        blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
        self.blood_group.addItems(blood_groups)
        layout.addWidget(self.blood_group)

        #Add Phone number
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone number")
        layout.addWidget(self.phone)

        #Add Address
        self.address = QLineEdit()
        self.address.setPlaceholderText("Address")
        layout.addWidget(self.address)

        #Add a submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_donar)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_donar(self):
        name = self.donar_name.text() 
        blood_group = self.blood_group.itemText(self.blood_group.currentIndex())
        mobile = self.phone.text()
        address = self.address.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,blood_group,mobile,address) VALUES (?,?,?,?)",(name,blood_group,mobile,address))
        connection.commit()
        cursor.close()
        connection.close()
        mainwindows.load_data()




app = QApplication(sys.argv)
mainwindows = MainWindow()
mainwindows.show()
mainwindows.load_data()
sys.exit(app.exec())

    