# Clinic Management System

## Installation Guide

## 1. Introduction

This document provides step by step instructions for installing and running the Clinic Management System. The application is built using Python, Tkinter, and SQLite. The database is stored locally, so no internet connection or external database server is required.

---

# 2. System Requirements

Before installing the application, ensure that your computer meets the following minimum requirements.

### Hardware Requirements

* Processor: Intel Core i3 or AMD equivalent (Intel Core i5 or higher recommended)
* RAM: Minimum 4 GB (8 GB recommended)
* Storage: At least 500 MB of free disk space
* Display Resolution: 1366 × 768 or higher

### Software Requirements

* Windows 10 or Windows 11
* Python 3.11 or later
* Visual Studio Code
* Git (Optional)
* SQLite (included with Python)
* Internet connection (only required for downloading software)

---

# 3. Required Software

Install the following software before running the project.

## Python

Download and install Python from:

https://www.python.org/downloads/

During installation:

* Check **Add Python to PATH**
* Select **Install Now**
* Complete the installation

Verify the installation:

```bash
python --version
```

or

```bash
python3 --version
```

---

## Visual Studio Code

Download Visual Studio Code from:

https://code.visualstudio.com/

Install using the default settings.

---

## Install Required VS Code Extensions

Open VS Code.

Install the following extensions:

* Python
* Pylance
* SQLite Viewer
* Black Formatter (Optional)
* Python Debugger

---

# 4. Download the Project

If using Git:

```bash
git clone https://github.com/yourusername/clinic-management-system.git
```

or download the ZIP file and extract it.

---

# 5. Open the Project

Open Visual Studio Code.

Select:

File

Open Folder

Choose:

ClinicManagementSystem

---

# 6. Create a Virtual Environment

Open Terminal.

Run:

```bash
python -m venv venv
```

Activate it.

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

---

# 7. Install Required Libraries

Install all required packages.

```bash
pip install pillow
pip install tkcalendar
pip install matplotlib
pip install reportlab
pip install pandas
pip install openpyxl
```

Or install from requirements.txt

```bash
pip install -r requirements.txt
```

---

# 8. Project Folder Structure

The project should have the following structure.

```text
ClinicManagementSystem/
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── logo/
│
├── database/
│   └── clinic.db
│
├── models/
├── controllers/
├── views/
├── reports/
├── backup/
├── utils/
├── main.py
├── requirements.txt
└── README.md
```

---

# 9. Running the Application

Open Terminal inside VS Code.

Run:

```bash
python main.py
```

The application should start automatically.

---

# 10. First Time Launch

During the first launch the application will automatically:

* Create the SQLite database
* Create all database tables
* Insert the default administrator account
* Generate required folders
* Load the dashboard

No manual database setup is required.

---

# 11. Default Login

Username

```text
admin
```

Password

```text
admin123
```

Change the password after the first login.

---

# 12. Database

Database Type

SQLite

Database Name

```text
clinic.db
```

Database Location

```text
database/clinic.db
```

The database stores:

* Users
* Patients
* Doctors
* Departments
* Appointments
* Medical Records
* Prescriptions
* Medicines
* Billing
* Payments

---

# 13. Features Verification

After logging in, verify the following modules are working correctly.

* Login
* Dashboard
* Patient Management
* Doctor Management
* Appointment Management
* Medical Records
* Prescription Management
* Medicine Inventory
* Billing
* Payments
* Reports
* User Management
* Settings
* Backup

Ensure that each module supports creating, viewing, updating, deleting, and searching records.

---

# 14. Backup Procedure

Open the application.

Navigate to:

Settings → Backup Database

Click:

Backup

A backup copy of the database will be stored in the **backup** folder.

---

# 15. Restoring a Backup

Open:

Settings

Select:

Restore Database

Browse to the backup file.

Click:

Restore

Restart the application.

---

# 16. Updating the Application

If using Git:

```bash
git pull
```

Restart the application after updating.

---

# 17. Common Troubleshooting

## Python is not recognized

Solution

Reinstall Python and enable **Add Python to PATH**.

---

## Module Not Found Error

Run:

```bash
pip install -r requirements.txt
```

---

## Database Not Found

Delete any corrupted database file.

Run the application again.

A new database will be created automatically.

---

## Login Failed

Use the default administrator credentials.

Username

```text
admin
```

Password

```text
admin123
```

If credentials were changed, reset them directly in the SQLite database.

---

## Tkinter Not Working

Verify the installation:

```bash
python -m tkinter
```

A small Tkinter test window should appear.

---

## Application Does Not Start

Check for syntax errors in the terminal.

Ensure all required Python packages are installed.

Verify that the virtual environment is activated.

---

# 18. Security Recommendations

* Change the default administrator password immediately after installation.
* Perform regular database backups.
* Restrict administrator access to authorized users.
* Keep Python and installed packages updated.
* Do not share the database file with unauthorized users.

---

# 19. Uninstallation

To remove the application:

1. Close the application.
2. Back up the **clinic.db** database if needed.
3. Delete the project folder.
4. Remove the virtual environment.
5. Uninstall Python only if it is no longer required for other projects.

---

# 20. Conclusion

Following this guide will install and configure the Clinic Management System successfully. Once installed, the system is ready to manage patients, appointments, medical records, medicines, billing, payments, reports, and user accounts using a secure local SQLite database with a modern Tkinter interface.
