from PyQt6.QtWidgets import QApplication, QLabel, QComboBox, QWidget, QGridLayout, QLineEdit, QPushButton,\
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class DatabaseConnection:
    def __init__(self,database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blood Donor Management System")
        self.setMinimumSize(800,600)

        #Add Menu Item
        file_menu_item = self.menuBar().addMenu("File")
        edit_menu_item = self.menuBar().addMenu("Edit")
        help_menu_item = self.menuBar().addMenu("Help")
        

        #Add insert action
        add_action = QAction(QIcon("icons/add.png"),"Add Donor", self)
        add_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_action)

        # Add Refresh action
        refresh_action = QAction(QIcon("icons/refresh.png"),"Refresh", self)
        refresh_action.triggered.connect(self.load_data)
        file_menu_item.addAction(refresh_action)

        #Add instruction action
        instruction_action = QAction(QIcon("icons/instruction.png"),"Guide", self)
        help_menu_item.addAction(instruction_action)
        instruction_action.triggered.connect(self.instruction)

        #Add about action
        about_action = QAction(QIcon("icons/about.png"),"About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        #Add Search action
        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        #Add Table to Main Window
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

        #Add version number to the statusbar
        version_no = QLabel(f"v{QApplication.applicationVersion()}")
        self.statusbar.addPermanentWidget(version_no)

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
        
        connection = DatabaseConnection().connect()
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

    def instruction(self):
        dialog = GuideDialog()
        dialog.exec()

    
    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class GuideDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guide")
        self.setMinimumWidth(1000)
        
        #Add main content for the Guide dialog box
        main_content = (
            "Blood Donor Management System - Instructions\n"
            "============================================\n\n"

            "1. **Add a Donor**:\n"
            "- Click on the 'Add Student' button in the toolbar or select it from the 'File' menu.\n"
            "- Fill in the donor's details (Name, Blood Group, Phone Number, Address) in the form.\n"
            "- Click 'Submit' to save the donor's information.\n\n"

            "2. **Search for a Donor**:\n"
            "- Click on the 'Search' button in the toolbar or select it from the 'Edit' menu.\n"
            "- Enter the desired blood group in the search field.\n"
            "- Click 'Search' to highlight matching donors in the table.\n\n"

            "3. **Edit a Donor's Information**:\n"
            "- Select a donor from the table by clicking on their row.\n"
            "- Click the 'Edit Record' button in the status bar.\n"
            "- Update the donor's details in the form and click 'Update' to save changes.\n\n"

            "4. **Delete a Donor**:\n"
            "- Select a donor from the table by clicking on their row.\n"
            "- Click the 'Delete Record' button in the status bar.\n"
            "- Confirm the deletion in the dialog box.\n\n"

            "5. **Refresh Data**:\n"
            "- Click on the 'Refresh' button in the toolbar or select it from the "
            "'File' menu to reload the latest data from the database.\n\n"

            "6. **View About Information**:\n"
            "- Click on the 'About' button in the 'Help' menu to learn more about the application and its purpose.\n\n"

            "7. **Exit the Application**:\n"
            "- Close the window or use the system's close button to exit the application.\n\n"

            "Thank you for using the Blood Donor Management System!"
        )
        content_label = QLabel(main_content)
        #To wrap words inside the qlabel
        content_label.setWordWrap(True)

        layout = QGridLayout()
        layout.addWidget(content_label)
        self.setLayout(layout)

        #Adding the background picture to the dialogbox and color to the qlabel text
        self.setStyleSheet(
            """
            QDialog {
               background-image: url("background/background2.png");
               background-repeat: no-repeat;
               background-position: center;
               
            }
            QLabel {
               color: black;
               font-size: 14px;
            }
            """
        )


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About The App")
        self.setMinimumWidth(1000)
          

        # Main content for the dialog box
        main_content = (
            "<h2>Blood Donor Management System</h2>"
            "<hr>"
            "<p><strong>About the Application:</strong></p>"
            "<p>The Blood Donor Management System is a desktop application designed to efficiently manage blood donor records. "
            "It provides a user-friendly interface for managing donor information such as name, blood group, phone number, and address.</p>"
            f"<p><strong>Version:</strong>{QApplication.applicationVersion()}</p>"
            "<p><strong>Key Features:</strong></p>"
            "<ul>"
            "<li>Add Donor: Easily add new donor records to the database.</li>"
            "<li>Search Donor: Search for donors by blood group to quickly find matching records.</li>"
            "<li>Edit Donor: Update existing donor information with ease.</li>"
            "<li>Delete Donor: Remove donor records and automatically renumber the IDs for consistency.</li>"
            "<li>Refresh Data: Reload the donor data to ensure the latest information is displayed.</li>"
            "<li>Instruction: Learn how to use the app.</li>"
            "<li>About Section: Learn more about the application and its owner.</li>"
            "</ul>"
            "<p><strong>How This App is Useful:</strong></p>"
            "<ul>"
            "<li>For Blood Banks: Helps blood banks maintain an organized database of donors, making it easier to find donors during emergencies.</li>"
            "<li>For Hospitals: Enables hospitals to quickly search for donors with specific blood groups.</li>"
            "<li>For NGOs: Assists NGOs in managing donor information for blood donation drives.</li>"
            "<li>For Individuals: Allows individuals to maintain a personal database of blood donors for emergencies.</li>"
            "</ul>"
            "<p><strong>Developed By:</strong> NAVID UL ISLAM</p>"
            "<p>This application simplifies the process of managing donor records, ensuring that critical information is always accessible when needed.</p>"
            "<p><strong>Thank you for using the Blood Donor Management System!</strong></p>"
        )

        # Add Facebook and LinkedIn links
        profile_content = (
            '<p><strong>Feel free to contact me:</strong></p>'
            '<p>'
            '<img src="icons/facebook.png" width="40" height="40" style="vertical-align:middle;"> '
            '<a href="https://www.facebook.com/profile.php?id=100010379958908"><b>Facebook Profile</b></a>'
            '</p>'
            '<p>'
            '<img src="icons/linkedin.png" width="40" height="40" style="vertical-align:middle;"> '
            '<a href="https://www.linkedin.com/in/navid-ul-islam" target="_blank"><b>LinkedIn Profile</b></a>'
            '</p>'
        )

        # Combine main content and profile content
        full_content = f"{main_content}{profile_content}"

        # Create a QLabel to display the content
        content_label = QLabel(full_content)
        content_label.setTextFormat(Qt.TextFormat.RichText)  # Enable rich text formatting
        content_label.setWordWrap(True)  # Allow text to wrap within the dialog
        content_label.setOpenExternalLinks(True)  # Enable hyperlink interaction
        content_label.setGeometry(20, 20, 760, 560)  # Position the content inside the dialog
        

        # Create a layout and add the QLabel
        layout = QVBoxLayout()
        layout.addWidget(content_label)

        # Set the layout for the dialog
        self.setLayout(layout)

        # Set the stylesheet for the dialog
        self.setStyleSheet(
            """
            QDialog {
               background-image: url("background/background3.jpeg");
               background-repeat: no-repeat;
               background-position: center;
               
            }
            QLabel {
               color: black;
               font-size: 14px;
            }
            QLabel a{
                color: black;
                text-decoration:none;
            }
            QLabel a:hover {
                color:black;
                text-decoration:underline;
            }
            """
        )


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Donar's Record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()

        #Get the donar id
        self.donar_id = main_window.table.item(index, 0).text()

        #Edit donar name
        donor_name = main_window.table.item(index, 1).text()
        self.donor_name = QLineEdit(donor_name)
        self.donor_name.setPlaceholderText("Name")
        layout.addWidget(self.donor_name)

        #Edit Blood Group
        blood_group = main_window.table.item(index, 2).text()
        self.blood_group = QComboBox()
        blood_groups = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
        self.blood_group.addItems(blood_groups)
        self.blood_group.setCurrentText(blood_group)
        layout.addWidget(self.blood_group)

        #Edit Phone number
        phone = main_window.table.item(index, 3).text()
        self.phone = QLineEdit(phone)
        self.phone.setPlaceholderText("Phone number")
        layout.addWidget(self.phone)

        #Edit Address
        address = main_window.table.item(index, 4).text()
        self.address = QLineEdit(address)
        self.address.setPlaceholderText("Address")
        layout.addWidget(self.address)

        #Add a update button
        button = QPushButton("Update")
        button.clicked.connect(self.update_record)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def update_record(self):
        connection = DatabaseConnection().connect()        
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?,blood_group = ?,mobile = ?,address = ? WHERE id = ?",
                       (self.donor_name.text(),
                        self.blood_group.itemText(self.blood_group.currentIndex()),
                        self.phone.text(),
                        self.address.text(),
                        self.donar_id))
        
        connection.commit()
        cursor.close()
        connection.close()

        #Refresh the main window
        main_window.load_data()

        self.close()


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

        yes_button.clicked.connect(self.delete_donor)
        no_button.clicked.connect(self.close)

    def delete_donor(self):
        # Get the donor id
        index = main_window.table.currentRow()
        donor_id = main_window.table.item(index, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Delete the selected row
        cursor.execute("DELETE FROM students WHERE id = ?", (donor_id,))
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
        main_window.load_data()

        self.close()

        # Show confirmation message
        confirmation_message = QMessageBox()
        confirmation_message.setWindowTitle("Successful")
        confirmation_message.setText("The record was deleted successfully.")
        confirmation_message.exec()
        

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Donor")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        #Add donar name
        self.donor_name = QLineEdit()
        self.donor_name.setPlaceholderText("Name")
        layout.addWidget(self.donor_name)

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
        button.clicked.connect(self.add_donor)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_donor(self):
        name = self.donor_name.text() 
        blood_group = self.blood_group.itemText(self.blood_group.currentIndex())
        mobile = self.phone.text()
        address = self.address.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,blood_group,mobile,address) VALUES (?,?,?,?)",(name,blood_group,mobile,address))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


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
        button.clicked.connect(self.search_donor)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_donor(self):
        blood_group = self.targername.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE blood_group = ?",(blood_group,))
        items = main_window.table.findItems(blood_group, Qt.MatchFlag.MatchFixedString)

        for item in items:
            main_window.table.item(item.row(),1).setSelected(True)
        
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
app.setApplicationVersion("1.0.1")
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

