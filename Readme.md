# Blood Donor Management System

A desktop application for managing blood donor records, built with Python and PyQt6. This app allows you to add, search, edit, and delete donor information, as well as import/export the donor database. It is designed to be user-friendly and efficient for blood banks, hospitals, NGOs, and individuals.

---

## Features

- **Login System:** Secure access with username and password (default: `admin` / `bbn1971`).
- **Add Donor:** Easily add new donor records.
- **Search Donor:** Search for donors by blood group.
- **Edit Donor:** Update existing donor information.
- **Delete Donor:** Remove donor records and automatically renumber IDs.
- **Import/Export Database:** Import from or export to SQLite database files.
- **Refresh Data:** Reload the latest data from the database.
- **Instructions & About:** Built-in guide and about dialogs.
- **Custom UI:** Modern look with custom title bar and toolbar.

---

## Getting Started

### Prerequisites

- Python 3.8+
- [PyQt6](https://pypi.org/project/PyQt6/)
- [platformdirs](https://pypi.org/project/platformdirs/)

Install dependencies:
```bash
pip install PyQt6 platformdirs
```

### Running the Application

1. Clone or download this repository.
2. Run the main script:
    ```bash
    python main.py
    ```
3. Login with:
    - **Username:** `admin`
    - **Password:** `bbn1971`

---

## Database

- The app uses an SQLite database (`donors_records.db`) stored in your Documents folder under `donor_data`.
- On first run, the database and required tables are created automatically if they do not exist.

---

## Usage

- **Add Donor:** Use the "Add Donor" button or menu to add a new donor.
- **Search:** Use the "Search" button or menu to find donors by blood group.
- **Edit/Delete:** Select a donor in the table, then use the status bar buttons to edit or delete.
- **Import/Export:** Use the File menu to import a `.db` file or export the database as `.sql`.
- **Guide/About:** See the Help menu for instructions and app info.

---

## Screenshots

<img src="Screenshot\Screenshot_1.png" alt="ScreenShot_1">
<img src="Screenshot\Screenshot_2.png" alt="Screenshot_2">

---

## Credits

- Developed by **Navid Ul Islam**
- [Facebook](https://www.facebook.com/profile.php?id=100010379958908)
- [LinkedIn](https://www.linkedin.com/in/navid-ul-islam)

---

## License

This project is for educational and non-commercial use.

---