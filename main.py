from PyQt6.QtWidgets import QApplication, QLabel, QComboBox, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Donar Management System")

        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

        add_action = QAction("Add Student", self)
        file_menu_item.addAction(add_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Blood Group", "Address", "Phone Number"))
        self.setCentralWidget(self.table)



app = QApplication(sys.argv)
mainwindows = MainWindow()
mainwindows.show()
sys.exit(app.exec())

    