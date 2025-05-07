from PyQt6.QtWidgets import QApplication, QLabel, QComboBox, QWidget, QGridLayout, QLineEdit, QPushButton,\
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Donar Management System")
        self.setMinimumSize(800,600)

        file_menu_item = self.menuBar().addMenu("File")
        edit_menu_item = self.menuBar().addMenu("Edit")
        help_menu_item = self.menuBar().addMenu("Help")
        

        #Add insert action
        add_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_action)

        # Add Refresh action
        refresh_action = QAction(QIcon("icons/refresh.png"),"Refresh", self)
        refresh_action.triggered.connect(self.load_data)
        file_menu_item.addAction(refresh_action)

        #Add about action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        #Add Search action
        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Blood Group", "Phone Number", "Address"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Add Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.addAction(add_action)
        toolbar.addAction(search_action)
        toolbar.addAction(refresh_action)

        #Add Statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        #Detect a click 
        self.table.cellClicked.connect(self.cell_clicked)
        self.table.clearSelection()  # Clear selection initially
        self.table.itemSelectionChanged.connect(self.clear_statusbar)  # Connect to clear status bar

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Remove existing buttons from the status bar
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add new buttons to the status bar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def clear_statusbar(self):
        # Clear the status bar if no cell is selected
        if not self.table.selectedItems():
            children = self.findChildren(QPushButton)
            if children:
                for child in children:
                    self.statusbar.removeWidget(child)

    def load_data(self):
        # Clear the table before loading new data
        self.table.setRowCount(0)
        
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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Donar's Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = mainwindows.table.currentRow()

        #Get the donar id
        self.donar_id = mainwindows.table.item(index, 0).text()

        #Edit donar name
        donar_name = mainwindows.table.item(index, 1).text()
        self.donar_name = QLineEdit(donar_name)
        self.donar_name.setPlaceholderText("Name")
        layout.addWidget(self.donar_name)

        #Edit Blood Group
        blood_group = mainwindows.table.item(index, 2).text()
        self.blood_group = QComboBox()
        blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
        self.blood_group.addItems(blood_groups)
        self.blood_group.setCurrentText(blood_group)
        layout.addWidget(self.blood_group)

        #Edit Phone number
        phone = mainwindows.table.item(index, 3).text()
        self.phone = QLineEdit(phone)
        self.phone.setPlaceholderText("Phone number")
        layout.addWidget(self.phone)

        #Edit Address
        address = mainwindows.table.item(index, 4).text()
        self.address = QLineEdit(address)
        self.address.setPlaceholderText("Address")
        layout.addWidget(self.address)

        #Add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_record)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def update_record(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?,blood_group = ?,mobile = ?,address = ? WHERE id = ?",
                       (self.donar_name.text(),
                        self.blood_group.itemText(self.blood_group.currentIndex()),
                        self.phone.text(),
                        self.address.text(),
                        self.donar_id))
        
        connection.commit()
        cursor.close()
        connection.close()

        #Refresh the main window
        mainwindows.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Donar's Record")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.delete_donar)
        no_button.clicked.connect(self.close)

    def delete_donar(self):
        # Get the donar id
        index = mainwindows.table.currentRow()
        donar_id = mainwindows.table.item(index, 0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Delete the selected row
        cursor.execute("DELETE FROM students WHERE id = ?", (donar_id,))
        connection.commit()

        # Renumber the id column
        cursor.execute("CREATE TEMPORARY TABLE students_backup AS SELECT * FROM students")
        cursor.execute("DELETE FROM students")
        cursor.execute("""
            INSERT INTO students (id, name, blood_group, mobile, address)
            SELECT ROW_NUMBER() OVER (ORDER BY id) AS id, name, blood_group, mobile, address
            FROM students_backup
        """)
        cursor.execute("DROP TABLE students_backup")
        connection.commit()

        cursor.close()
        connection.close()

        # Refresh the main window
        mainwindows.load_data()

        self.close()

        # Show confirmation message
        confirmation_message = QMessageBox()
        confirmation_message.setWindowTitle("Successful")
        confirmation_message.setText("The record was deleted successfully.")
        confirmation_message.exec()
        

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


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Donar")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        #Search by blood group

        self.targername = QLineEdit()
        self.targername.setPlaceholderText("Blood Group")
        layout.addWidget(self.targername)

        #Search button
        button = QPushButton("Search")
        button.clicked.connect(self.search_donar)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_donar(self):
        blood_group = self.targername.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE blood_group = ?",(blood_group,))
        items = mainwindows.table.findItems(blood_group, Qt.MatchFlag.MatchFixedString)

        for item in items:
            mainwindows.table.item(item.row(),1).setSelected(True)
        
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
mainwindows = MainWindow()
mainwindows.show()
mainwindows.load_data()
sys.exit(app.exec())

