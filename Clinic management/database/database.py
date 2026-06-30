import os
import sqlite3
import hashlib
from datetime import datetime


class ClinicDatabase:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), "clinic.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.initialize()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT,
                status TEXT DEFAULT 'Active',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                gender TEXT,
                dob TEXT,
                age INTEGER,
                phone TEXT,
                email TEXT,
                address TEXT,
                blood_group TEXT,
                emergency_contact TEXT,
                guardian_name TEXT,
                national_id TEXT,
                registration_date TEXT,
                status TEXT DEFAULT 'Active'
            );

            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                gender TEXT,
                department TEXT,
                qualification TEXT,
                specialization TEXT,
                experience TEXT,
                phone TEXT,
                email TEXT,
                room_number TEXT,
                working_days TEXT,
                consultation_fee REAL,
                status TEXT DEFAULT 'Active'
            );

            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_number TEXT UNIQUE NOT NULL,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                department TEXT,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                purpose TEXT,
                status TEXT DEFAULT 'Scheduled',
                notes TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
            );

            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department_name TEXT UNIQUE NOT NULL,
                description TEXT,
                head_doctor TEXT,
                staff_count TEXT
            );

            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT UNIQUE NOT NULL,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                diagnosis TEXT,
                symptoms TEXT,
                treatment TEXT,
                doctor_notes TEXT,
                visit_date TEXT,
                vital_signs TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
            );

            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id TEXT UNIQUE NOT NULL,
                medicine_name TEXT NOT NULL,
                category TEXT,
                supplier TEXT,
                batch_number TEXT,
                manufacture_date TEXT,
                expiry_date TEXT,
                purchase_price REAL,
                selling_price REAL,
                quantity INTEGER,
                minimum_stock INTEGER,
                location TEXT
            );

            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prescription_id TEXT UNIQUE NOT NULL,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                medicine_name TEXT,
                dosage TEXT,
                frequency TEXT,
                duration TEXT,
                instructions TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
            );

            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_number TEXT UNIQUE NOT NULL,
                patient_id TEXT NOT NULL,
                consultation_fee REAL,
                medicine_charges REAL,
                lab_charges REAL,
                other_charges REAL,
                discount REAL,
                tax REAL,
                total REAL,
                amount_paid REAL,
                balance REAL,
                payment_status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            );

            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id TEXT UNIQUE NOT NULL,
                bill_number TEXT,
                payment_method TEXT,
                amount REAL,
                payment_date TEXT,
                status TEXT DEFAULT 'Completed'
            );

            CREATE TABLE IF NOT EXISTS lab_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT UNIQUE NOT NULL,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                sample TEXT,
                result TEXT,
                status TEXT,
                test_date TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
            );
            """
        )
        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            password_hash = self.hash_password("admin123")
            cursor.execute(
                "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                ("admin", password_hash, "Admin", "System Administrator"),
            )
            cursor.execute(
                "INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                ("reception", password_hash, "Receptionist", "Reception Desk"),
            )

        if not self.has_seed_data("patients"):
            self._seed_sample_data(conn)

        conn.commit()
        conn.close()

    def has_seed_data(self, table: str) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def _seed_sample_data(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO patients (patient_id, full_name, gender, dob, age, phone, email, address, blood_group, emergency_contact, guardian_name, national_id, registration_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("P001", "Alice Turay", "Female", "2008-04-20", 18, "079323135", "aliceturay@.gmail.com", "Sierra Leone", "O+", "078075757", "Saffie Kallokoh", "12345678", datetime.now().strftime("%Y-%m-%d"), "Active"),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO doctors (doctor_id, full_name, gender, department, qualification, specialization, experience, phone, email, room_number, working_days, consultation_fee, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("D001", "Dr. Mercy Otieno", "Female", "General", "MBBS", "Family Medicine", "10 years", "0721122334", "mercy@example.com", "Room 12", "Mon-Fri", 1500.0, "Active"),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO medicines (medicine_id, medicine_name, category, supplier, batch_number, manufacture_date, expiry_date, purchase_price, selling_price, quantity, minimum_stock, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("M001", "Paracetamol", "Pain Relief", "MedSup", "B001", "2024-01-01", "2026-12-30", 50.0, 80.0, 120, 20, "Shelf A1"),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO appointments (appointment_number, patient_id, doctor_id, department, appointment_date, appointment_time, purpose, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("A001", "P001", "D001", "General", datetime.now().strftime("%Y-%m-%d"), "09:00", "Routine Checkup", "Scheduled", "Needs follow-up"),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO departments (department_name, description, head_doctor, staff_count) VALUES (?, ?, ?, ?)",
            ("General Medicine", "Primary care and consultations", "Dr. Mercy Otieno", "24"),
        )
        cursor.execute(
            "INSERT OR IGNORE INTO medical_records (record_id, patient_id, doctor_id, diagnosis, symptoms, treatment, doctor_notes, visit_date, vital_signs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("R001", "P001", "D001", "Mild fever", "Headache, fatigue", "Rest and fluids", "Monitor symptoms", datetime.now().strftime("%Y-%m-%d"), "BP 120/80 • Temp 37.2°C"),
        )

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(input_password: str, stored_hash: str) -> bool:
        return hashlib.sha256(input_password.encode()).hexdigest() == stored_hash

    def backup_database(self, destination: str) -> str:
        import shutil

        shutil.copy2(self.db_path, destination)
        return destination

    def restore_database(self, source: str) -> None:
        import shutil

        shutil.copy2(source, self.db_path)
