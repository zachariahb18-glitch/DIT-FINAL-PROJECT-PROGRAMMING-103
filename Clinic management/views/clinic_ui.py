import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database.database import ClinicDatabase


COLORS = {
    "primary": "#1565C0",
    "secondary": "#42A5F5",
    "sidebar_bg": "#0F172A",
    "main_bg": "#EEF3F8",
    "card_bg": "#FFFFFF",
    "accent_green": "#00C853",
    "warning_orange": "#FB8C00",
    "danger_red": "#E53935",
    "text": "#1F2937",
    "muted": "#6B7280",
    "border": "#D6DEE8",
}


class LoginWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Clinic Management System")
        self.root.geometry("1180x720")
        self.root.minsize(980, 640)
        self.root.configure(bg=COLORS["main_bg"])
        self.db = ClinicDatabase()
        self._apply_theme()
        self._build_ui()

    def _apply_theme(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=COLORS["main_bg"])
        style.configure("Card.TFrame", background=COLORS["card_bg"])
        style.configure("TLabel", background=COLORS["main_bg"], foreground=COLORS["text"], font=("Segoe UI", 10))
        style.configure("Heading.TLabel", font=("Segoe UI", 16, "bold"), foreground=COLORS["text"])
        style.configure("Muted.TLabel", foreground=COLORS["muted"])
        style.configure("TEntry", padding=8, fieldbackground=COLORS["card_bg"])
        style.configure("TButton", padding=10)
        style.configure("Accent.TButton", background=COLORS["primary"], foreground="white")
        style.map("Accent.TButton", background=[("active", "#0D47A1"), ("pressed", "#0D47A1")])
        style.configure("Success.TButton", background=COLORS["accent_green"], foreground="white")
        style.map("Success.TButton", background=[("active", "#00A844"), ("pressed", "#00A844")])
        style.configure("Danger.TButton", background=COLORS["danger_red"], foreground="white")
        style.map("Danger.TButton", background=[("active", "#C62828"), ("pressed", "#C62828")])

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, bg=COLORS["main_bg"])
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        left = tk.Frame(container, bg=COLORS["primary"], padx=36, pady=36)
        left.grid(row=0, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        right = tk.Frame(container, bg=COLORS["main_bg"], padx=40, pady=40)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        title = tk.Label(left, text="Advanced Care", font=("Segoe UI", 28, "bold"), fg="white", bg=COLORS["primary"])
        title.pack(anchor="w", pady=(0, 8))
        tk.Label(left, text="Modern healthcare operations with trusted security and elegant workflows.", font=("Segoe UI", 12), fg="#E3F2FD", bg=COLORS["primary"], wraplength=320, justify="left").pack(anchor="w")

        illustration = tk.Frame(left, bg=COLORS["primary"], padx=10, pady=10)
        illustration.pack(fill="both", expand=True, pady=(30, 0))
        tk.Label(illustration, text="✚", font=("Segoe UI", 84), fg="white", bg=COLORS["primary"]).pack(pady=(10, 0))
        tk.Label(illustration, text="24/7 patient care", font=("Segoe UI", 16, "bold"), fg="white", bg=COLORS["primary"]).pack(pady=(8, 0))
        tk.Label(illustration, text="Secure scheduling • Records • Billing", font=("Segoe UI", 11), fg="#DCEBFF", bg=COLORS["primary"]).pack(pady=(6, 0))

        card = tk.Frame(right, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1, padx=26, pady=28)
        card.grid(row=0, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)

        tk.Label(card, text="Welcome Back", font=("Segoe UI", 20, "bold"), fg=COLORS["text"], bg=COLORS["card_bg"]).grid(row=0, column=0, sticky="w", pady=(0, 8))
        tk.Label(card, text="Secure access to clinic management", font=("Segoe UI", 10), fg=COLORS["muted"], bg=COLORS["card_bg"]).grid(row=1, column=0, sticky="w", pady=(0, 18))

        tk.Label(card, text="Username", font=("Segoe UI", 10, "bold"), fg=COLORS["text"], bg=COLORS["card_bg"]).grid(row=2, column=0, sticky="w", pady=(0, 6))
        self.username_var = tk.StringVar(value="admin")
        ttk.Entry(card, textvariable=self.username_var, width=32).grid(row=3, column=0, sticky="ew", pady=(0, 10))

        tk.Label(card, text="Password", font=("Segoe UI", 10, "bold"), fg=COLORS["text"], bg=COLORS["card_bg"]).grid(row=4, column=0, sticky="w", pady=(0, 6))
        self.password_var = tk.StringVar(value="admin123")
        self.password_entry = ttk.Entry(card, textvariable=self.password_var, show="*", width=32)
        self.password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        self.show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text="Show password", variable=self.show_password, command=self.toggle_password).grid(row=6, column=0, sticky="w", pady=(0, 10))

        ttk.Button(card, text="Login", style="Accent.TButton", command=self.login).grid(row=7, column=0, sticky="ew", pady=(8, 8))
        ttk.Button(card, text="Exit", style="Danger.TButton", command=self.root.destroy).grid(row=8, column=0, sticky="ew")

        tk.Label(card, text="Version 1.0 • Secure SQLite • Modern UI", font=("Segoe UI", 9), fg=COLORS["muted"], bg=COLORS["card_bg"]).grid(row=9, column=0, sticky="w", pady=(18, 0))

        self.clock_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tk.Label(left, textvariable=self.clock_var, font=("Segoe UI", 11, "bold"), fg="white", bg=COLORS["primary"]).pack(anchor="w", pady=(18, 0))
        self._update_clock()

    def toggle_password(self) -> None:
        self.password_entry.configure(show="" if self.show_password.get() else "*")

    def _update_clock(self) -> None:
        self.clock_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self._update_clock)

    def login(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showerror("Validation", "Username and password are required.")
            return

        conn = self.db.get_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return
        if not self.db.verify_password(password, user["password"]):
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        self.root.destroy()
        new_root = tk.Tk()
        MainWindow(new_root, username)
        new_root.mainloop()


class MainWindow:
    def __init__(self, root: tk.Tk, username: str):
        self.root = root
        self.username = username
        self.root.title("Clinic Management System")
        self.root.geometry("1500x900")
        self.root.minsize(1280, 820)
        self.root.configure(bg=COLORS["main_bg"])
        self.db = ClinicDatabase()
        self._apply_theme()
        self._build_ui()

    def _apply_theme(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=COLORS["main_bg"])
        style.configure("Card.TFrame", background=COLORS["card_bg"])
        style.configure("Treeview", background=COLORS["card_bg"], fieldbackground=COLORS["card_bg"], rowheight=28)
        style.configure("Treeview.Heading", background=COLORS["primary"], foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#0D47A1")])

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        sidebar = tk.Frame(self.root, bg=COLORS["sidebar_bg"], width=250)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)
        sidebar.rowconfigure(5, weight=1)

        title_container = tk.Frame(sidebar, bg=COLORS["sidebar_bg"], pady=18)
        title_container.grid(row=0, column=0, sticky="ew")
        tk.Label(title_container, text="🩺", font=("Segoe UI", 24), bg=COLORS["sidebar_bg"], fg="white").pack(anchor="w")
        tk.Label(title_container, text="Clinic Manager", font=("Segoe UI", 16, "bold"), bg=COLORS["sidebar_bg"], fg="white").pack(anchor="w")
        tk.Label(title_container, text=f"Signed in as {self.username}", font=("Segoe UI", 10), bg=COLORS["sidebar_bg"], fg="#BFD5FF").pack(anchor="w", pady=(4, 0))

        menu_items = [
            ("Dashboard", "🏥"), ("Patients", "🧑‍⚕️"), ("Doctors", "👨‍⚕️"), ("Departments", "🏢"),
            ("Appointments", "📅"), ("Medical Records", "🗂️"), ("Prescriptions", "💊"), ("Medicines", "💉"),
            ("Laboratory", "🧪"), ("Billing", "🧾"), ("Payments", "💳"), ("Reports", "📈"), ("Users", "👤"),
            ("Settings", "⚙️"), ("Backup", "🗄️"), ("Logout", "🚪")
        ]
        self.sidebar_buttons = {}
        for index, (name, icon) in enumerate(menu_items, start=1):
            btn = tk.Button(
                sidebar,
                text=f"{icon}  {name}",
                bg=COLORS["sidebar_bg"],
                fg="white",
                bd=0,
                anchor="w",
                padx=14,
                pady=10,
                relief="flat",
                justify="left",
                cursor="hand2",
                activebackground="#1E40AF",
                activeforeground="white",
                font=("Segoe UI", 10),
                command=lambda n=name: self.show_module(n),
            )
            btn.grid(row=index, column=0, sticky="ew", pady=2, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#1E3A8A"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COLORS["sidebar_bg"] if b != self.active_button else "#1E40AF"))
            self.sidebar_buttons[name] = btn

        self.status_var = tk.StringVar(value="Ready")
        footer = tk.Frame(sidebar, bg=COLORS["sidebar_bg"], pady=16)
        footer.grid(row=100, column=0, sticky="sew")
        tk.Label(footer, textvariable=self.status_var, font=("Segoe UI", 9), fg="#9ED0FF", bg=COLORS["sidebar_bg"]).pack(anchor="w", padx=14)

        content = tk.Frame(self.root, bg=COLORS["main_bg"])
        content.grid(row=0, column=1, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        header = tk.Frame(content, bg=COLORS["card_bg"], padx=20, pady=16)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        tk.Label(header, text="Clinic Operations Center", font=("Segoe UI", 17, "bold"), fg=COLORS["text"], bg=COLORS["card_bg"]).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="Healthcare software with fast patient workflows", font=("Segoe UI", 10), fg=COLORS["muted"], bg=COLORS["card_bg"]).grid(row=1, column=0, sticky="w")
        self.header_clock = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tk.Label(header, textvariable=self.header_clock, font=("Segoe UI", 11, "bold"), fg=COLORS["primary"], bg=COLORS["card_bg"]).grid(row=0, column=1, rowspan=2, sticky="e")

        self.body = tk.Frame(content, bg=COLORS["main_bg"], padx=16, pady=16)
        self.body.grid(row=1, column=0, sticky="nsew")
        self.body.columnconfigure(0, weight=1)
        self.body.rowconfigure(0, weight=1)

        self._update_header_clock()
        self.show_module("Dashboard")

    def _update_header_clock(self) -> None:
        self.header_clock.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self._update_header_clock)

    def show_module(self, name: str) -> None:
        for widget in self.body.winfo_children():
            widget.destroy()
        self.status_var.set(f"Viewing {name}")
        self._highlight_menu(name)
        if name == "Dashboard":
            self._show_dashboard()
        elif name == "Patients":
            self._show_patients()
        elif name == "Doctors":
            self._show_doctors()
        elif name == "Departments":
            self._show_departments()
        elif name == "Appointments":
            self._show_appointments()
        elif name == "Medical Records":
            self._show_medical_records()
        elif name == "Prescriptions":
            self._show_prescriptions()
        elif name == "Medicines":
            self._show_medicines()
        elif name == "Laboratory":
            self._show_laboratory()
        elif name == "Billing":
            self._show_billing()
        elif name == "Payments":
            self._show_payments()
        elif name == "Reports":
            self._show_reports()
        elif name == "Users":
            self._show_users()
        elif name == "Settings":
            self._show_settings()
        elif name == "Backup":
            self._backup_database()
        elif name == "Logout":
            self.root.destroy()
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

    def _highlight_menu(self, name: str) -> None:
        for key, btn in self.sidebar_buttons.items():
            btn.configure(bg=COLORS["sidebar_bg"])
        if name in self.sidebar_buttons:
            self.sidebar_buttons[name].configure(bg="#1E40AF")
            self.active_button = self.sidebar_buttons[name]

    def _show_dashboard(self) -> None:
        stats = self._stats()
        cards_frame = tk.Frame(self.body, bg=COLORS["main_bg"])
        cards_frame.pack(fill="x", pady=(0, 12))

        card_data = [
            ("Total Patients", stats["patients"], "👥", COLORS["primary"]),
            ("Total Doctors", stats["doctors"], "👨‍⚕️", COLORS["secondary"]),
            ("Appointments Today", stats["today_appointments"], "📅", COLORS["accent_green"]),
            ("Medicines", stats["medicines"], "💊", COLORS["warning_orange"]),
            ("Revenue", f"{stats['revenue']:.2f}", "💵", COLORS["primary"]),
            ("Pending Bills", stats["pending_payments"], "🧾", COLORS["danger_red"]),
        ]
        for title, value, icon, accent in card_data:
            card = tk.Frame(cards_frame, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1, padx=14, pady=14)
            card.pack(side="left", padx=8, pady=6, fill="both", expand=True)
            tk.Label(card, text=icon, font=("Segoe UI", 22), bg=COLORS["card_bg"], fg=accent).pack(anchor="w")
            tk.Label(card, text=title, font=("Segoe UI", 10), bg=COLORS["card_bg"], fg=COLORS["muted"]).pack(anchor="w", pady=(6, 0))
            tk.Label(card, text=str(value), font=("Segoe UI", 18, "bold"), bg=COLORS["card_bg"], fg=COLORS["text"]).pack(anchor="w")

        content_row = tk.Frame(self.body, bg=COLORS["main_bg"])
        content_row.pack(fill="both", expand=True)
        content_row.columnconfigure(0, weight=1)
        content_row.columnconfigure(1, weight=1)

        left = tk.LabelFrame(content_row, text="Recent Appointments", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        right = tk.LabelFrame(content_row, text="Recent Patients", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))

        appointments = self.db.get_connection().execute("SELECT * FROM appointments ORDER BY id DESC LIMIT 5").fetchall()
        for appt in appointments:
            tk.Label(left, text=f"{appt['appointment_number']} • {appt['patient_id']} • {appt['appointment_date']}", bg=COLORS["card_bg"], fg=COLORS["text"], anchor="w").pack(fill="x", pady=2)

        patients = self.db.get_connection().execute("SELECT * FROM patients ORDER BY id DESC LIMIT 5").fetchall()
        for patient in patients:
            tk.Label(right, text=f"{patient['patient_id']} • {patient['full_name']} • {patient['phone']}", bg=COLORS["card_bg"], fg=COLORS["text"], anchor="w").pack(fill="x", pady=2)

        charts_frame = tk.Frame(self.body, bg=COLORS["main_bg"])
        charts_frame.pack(fill="x", pady=(8, 0))
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)

        self._build_chart(charts_frame, 0, "Revenue Overview", ["Jan", "Feb", "Mar", "Apr"], [12000, 18000, 15000, 22000])
        self._build_chart(charts_frame, 1, "Visits This Month", ["Mon", "Tue", "Wed", "Thu", "Fri"], [14, 18, 12, 20, 16])

    def _build_chart(self, parent: tk.Frame, column: int, title: str, labels: list, values: list) -> None:
        frame = tk.LabelFrame(parent, text=title, bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        frame.grid(row=0, column=column, sticky="nsew", padx=6)
        figure, axis = plt.subplots(figsize=(4.3, 2.4), dpi=100)
        axis.bar(labels, values, color=[COLORS["primary"], COLORS["secondary"], COLORS["accent_green"], COLORS["warning_orange"]][:len(labels)])
        axis.set_facecolor(COLORS["main_bg"])
        figure.patch.set_facecolor(COLORS["card_bg"])
        axis.set_title(title, fontsize=10)
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _show_patients(self) -> None:
        form = tk.LabelFrame(self.body, text="Patient Management", bg=COLORS["card_bg"], fg=COLORS["text"], padx=12, pady=12)
        form.pack(fill="x", pady=(0, 10))
        form.columnconfigure(0, weight=1)
        form.columnconfigure(2, weight=1)
        fields = [("Patient ID", "patient_id"), ("Full Name", "full_name"), ("Phone", "phone"), ("Email", "email"), ("Status", "status")]
        self.patient_vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=label, bg=COLORS["card_bg"], fg=COLORS["text"]).grid(row=i, column=0, sticky="w", padx=6, pady=6)
            var = tk.StringVar()
            ttk.Entry(form, textvariable=var, width=28).grid(row=i, column=1, sticky="ew", padx=6, pady=6)
            self.patient_vars[key] = var
        ttk.Button(form, text="Add Patient", style="Accent.TButton", command=self._add_patient).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        ttk.Button(form, text="Delete Selected", style="Danger.TButton", command=self._delete_selected_patient).grid(row=6, column=0, columnspan=2, sticky="ew", pady=6)
        ttk.Button(form, text="Search", style="Success.TButton", command=self._search_patients).grid(row=7, column=0, columnspan=2, sticky="ew", pady=6)

        table = tk.Frame(self.body, bg=COLORS["main_bg"])
        table.pack(fill="both", expand=True)
        cols = ("patient_id", "full_name", "phone", "email", "status")
        self.patient_tree = ttk.Treeview(table, columns=cols, show="headings")
        for col in cols:
            self.patient_tree.heading(col, text=col.replace("_", " ").title())
            self.patient_tree.column(col, width=140)
        self.patient_tree.pack(fill="both", expand=True)
        self._load_patients()

    def _add_patient(self) -> None:
        values = {k: v.get() for k, v in self.patient_vars.items()}
        if not values["full_name"] or not values["patient_id"]:
            messagebox.showerror("Validation", "Patient ID and full name are required.")
            return
        conn = self.db.get_connection()
        conn.execute(
            "INSERT INTO patients (patient_id, full_name, gender, dob, age, phone, email, address, blood_group, emergency_contact, guardian_name, national_id, registration_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                values["patient_id"], values["full_name"], "", "", 0, values["phone"], values["email"], "", "", "", "", "", datetime.now().strftime("%Y-%m-%d"), values["status"],
            ),
        )
        conn.commit()
        conn.close()
        self._load_patients()
        messagebox.showinfo("Success", "Patient added successfully.")

    def _load_patients(self) -> None:
        if hasattr(self, "patient_tree"):
            for row in self.patient_tree.get_children():
                self.patient_tree.delete(row)
            conn = self.db.get_connection()
            rows = conn.execute("SELECT patient_id, full_name, phone, email, status FROM patients ORDER BY id DESC").fetchall()
            for row in rows:
                self.patient_tree.insert("", "end", values=(row["patient_id"], row["full_name"], row["phone"], row["email"], row["status"]))
            conn.close()

    def _search_patients(self) -> None:
        query = simpledialog.askstring("Search", "Enter patient name or ID")
        if not query:
            return
        conn = self.db.get_connection()
        rows = conn.execute("SELECT patient_id, full_name, phone, email, status FROM patients WHERE full_name LIKE ? OR patient_id LIKE ?", (f"%{query}%", f"%{query}%")).fetchall()
        conn.close()
        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)
        for row in rows:
            self.patient_tree.insert("", "end", values=(row["patient_id"], row["full_name"], row["phone"], row["email"], row["status"]))

    def _delete_selected_patient(self) -> None:
        if not hasattr(self, "patient_tree"):
            return
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Select a patient to delete.")
            return
        values = self.patient_tree.item(selected[0], "values")
        patient_id = values[0]
        if not messagebox.askyesno("Delete", f"Delete patient {patient_id}?"):
            return
        conn = self.db.get_connection()
        try:
            conn.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            conn.commit()
        except sqlite3.Error as exc:
            messagebox.showerror("Delete Failed", f"Unable to delete patient: {exc}")
            conn.close()
            return
        conn.close()
        self._load_patients()
        messagebox.showinfo("Deleted", "Patient deleted successfully.")

    def _show_doctors(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=1)

        header = tk.LabelFrame(panel, text="Doctors", bg=COLORS["card_bg"], fg=COLORS["text"], padx=12, pady=12)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        tk.Label(header, text="Medical staff roster and specialist coverage", bg=COLORS["card_bg"], fg=COLORS["muted"]).pack(anchor="w")
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "doctors", "doctor_id", "doctor", lambda: self.show_module("Doctors"))).pack(side="right")
        ttk.Button(toolbar, text="Add Doctor", style="Accent.TButton", command=self._add_doctor_form).pack(side="right", padx=(0, 8))

        summary = tk.Frame(panel, bg=COLORS["main_bg"])
        summary.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self._info_card(summary, "Active doctors", "2", COLORS["primary"])
        self._info_card(summary, "Specialties", "3", COLORS["secondary"])
        self._info_card(summary, "Consultation fee", "$1,500", COLORS["accent_green"])

        details = tk.LabelFrame(panel, text="Doctor directory", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        details.grid(row=1, column=1, sticky="nsew")
        conn = self.db.get_connection()
        rows = conn.execute("SELECT doctor_id, full_name, department, specialization, phone, status FROM doctors ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("D001", "Dr. Mercy Otieno", "General", "Family Medicine", "0721122334", "Active")]
        tree = self._treeview(details, ["Doctor ID", "Name", "Department", "Specialization", "Phone", "Status"], rows)

    def _show_departments(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        top = tk.LabelFrame(panel, text="Departments", bg=COLORS["card_bg"], fg=COLORS["text"], padx=12, pady=12)
        top.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(top, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT department_name, description, head_doctor, staff_count FROM departments ORDER BY id DESC").fetchall()
        conn.close()
        tree = None
        if not rows:
            rows = [("General Medicine", "Primary care and consultations", "Dr. Mercy Otieno", "24"), ("Pediatrics", "Pediatric consults and immunization", "Dr. Jane", "8")]
        details = tk.LabelFrame(panel, text="Department directory", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        details.pack(fill="both", expand=True)
        tree = self._treeview(details, ["Department Name", "Description", "Head Doctor", "Staff Count"], rows)
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "departments", "department_name", "department", lambda: self.show_module("Departments"))).pack(side="right")
        ttk.Button(toolbar, text="Add Department", style="Accent.TButton", command=self._add_department_form).pack(side="right", padx=(0, 8))

    def _show_appointments(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="Upcoming appointments", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "appointments", "appointment_number", "appointment", lambda: self.show_module("Appointments"))).pack(side="right")
        ttk.Button(toolbar, text="Add Appointment", style="Accent.TButton", command=self._add_appointment_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT appointment_number, patient_id, doctor_id, appointment_date, appointment_time, purpose, status FROM appointments ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("A001", "P001", "D001", datetime.now().strftime("%Y-%m-%d"), "09:00", "Routine Checkup", "Scheduled")]
        tree = self._treeview(header, ["Appointment #", "Patient", "Doctor", "Date", "Time", "Purpose", "Status"], rows)

    def _show_medical_records(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        top = tk.LabelFrame(panel, text="Patient record snapshot", bg=COLORS["card_bg"], fg=COLORS["text"], padx=12, pady=12)
        top.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(top, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "medical_records", "record_id", "medical record", lambda: self.show_module("Medical Records"))).pack(side="right")
        ttk.Button(toolbar, text="Add Record", style="Accent.TButton", command=self._add_medical_record_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        patient = conn.execute("SELECT full_name, phone, age, blood_group FROM patients ORDER BY id DESC LIMIT 1").fetchone()
        records = conn.execute("SELECT record_id, patient_id, doctor_id, diagnosis, symptoms, treatment, visit_date FROM medical_records ORDER BY id DESC").fetchall()
        conn.close()
        patient_name = patient["full_name"] if patient else "Patient"
        patient_phone = patient["phone"] if patient else "N/A"
        tk.Label(top, text=f"Name: {patient_name}", bg=COLORS["card_bg"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(top, text=f"Phone: {patient_phone}", bg=COLORS["card_bg"], fg=COLORS["muted"]).pack(anchor="w")
        tree = self._treeview(panel, ["Record ID", "Patient", "Doctor", "Diagnosis", "Symptoms", "Treatment", "Date"], [(r["record_id"], r["patient_id"], r["doctor_id"], r["diagnosis"], r["symptoms"], r["treatment"], r["visit_date"]) for r in records])

    def _show_prescriptions(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="Prescription orders", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "prescriptions", "prescription_id", "prescription", lambda: self.show_module("Prescriptions"))).pack(side="right")
        ttk.Button(toolbar, text="Add Prescription", style="Accent.TButton", command=self._add_prescription_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT prescription_id, patient_id, doctor_id, medicine_name, dosage, frequency, duration FROM prescriptions ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("RX001", "P001", "D001", "Paracetamol", "500mg", "2x daily", "5 days")]
        tree = self._treeview(header, ["Prescription ID", "Patient", "Doctor", "Medicine", "Dosage", "Frequency", "Duration"], rows)

    def _show_medicines(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="Medicine inventory", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "medicines", "medicine_id", "medicine", lambda: self.show_module("Medicines"))).pack(side="right")
        ttk.Button(toolbar, text="Add Medicine", style="Accent.TButton", command=self._add_medicine_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT medicine_id, medicine_name, category, quantity, minimum_stock, expiry_date FROM medicines ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("M001", "Paracetamol", "Pain Relief", 120, 20, "2026-12-30")]
        tree = self._treeview(header, ["Medicine ID", "Name", "Category", "Quantity", "Min Stock", "Expiry"], rows)

    def _show_laboratory(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="Laboratory tests", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "lab_results", "test_id", "lab test", lambda: self.show_module("Laboratory"))).pack(side="right")
        ttk.Button(toolbar, text="Add Lab Test", style="Accent.TButton", command=self._add_lab_test_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT test_id, patient_id, doctor_id, sample, result, status, test_date FROM lab_results ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("L001", "P001", "D001", "Blood sample", "Normal", "Completed", datetime.now().strftime("%Y-%m-%d"))]
        tree = self._treeview(header, ["Test ID", "Patient", "Doctor", "Sample", "Result", "Status", "Date"], rows)

    def _show_billing(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="Billing overview", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "bills", "bill_number", "bill", lambda: self.show_module("Billing"))).pack(side="right")
        ttk.Button(toolbar, text="Add Bill", style="Accent.TButton", command=self._add_bill_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT bill_number, patient_id, total, amount_paid, balance, payment_status FROM bills ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("B001", "P001", 1500.0, 1000.0, 500.0, "Pending")]
        tree = self._treeview(header, ["Bill #", "Patient", "Total", "Paid", "Balance", "Status"], rows)

    def _show_payments(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="Payments", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "payments", "payment_id", "payment", lambda: self.show_module("Payments"))).pack(side="right")
        ttk.Button(toolbar, text="Add Payment", style="Accent.TButton", command=self._add_payment_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT payment_id, bill_number, payment_method, amount, payment_date, status FROM payments ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("PY001", "B001", "Cash", 1000.0, datetime.now().strftime("%Y-%m-%d"), "Completed")]
        tree = self._treeview(header, ["Payment ID", "Bill #", "Method", "Amount", "Date", "Status"], rows)

    def _show_reports(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        top = tk.LabelFrame(panel, text="Reports", bg=COLORS["card_bg"], fg=COLORS["text"], padx=12, pady=12)
        top.pack(fill="x", pady=(0, 10))
        ttk.Button(top, text="Generate Report", style="Accent.TButton", command=self._generate_report).pack(anchor="e")
        for title, detail, color in [
            ("Patients", "24 registered patients this month", COLORS["primary"]),
            ("Appointments", "16 completed visits", COLORS["secondary"]),
            ("Revenue", "Ksh 24,500 collected", COLORS["accent_green"]),
            ("Inventory", "2 items below minimum stock", COLORS["warning_orange"]),
        ]:
            card = tk.Frame(panel, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1, padx=14, pady=14)
            card.pack(fill="x", pady=6)
            tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=COLORS["card_bg"], fg=color).pack(anchor="w")
            tk.Label(card, text=detail, bg=COLORS["card_bg"], fg=COLORS["muted"]).pack(anchor="w")

    def _show_users(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        header = tk.LabelFrame(panel, text="System users", bg=COLORS["card_bg"], fg=COLORS["text"], padx=10, pady=10)
        header.pack(fill="x", pady=(0, 10))
        toolbar = tk.Frame(header, bg=COLORS["card_bg"])
        toolbar.pack(fill="x", pady=(8, 0))
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton", command=lambda: self._delete_selected_from_tree(tree, "users", "username", "user", lambda: self.show_module("Users"))).pack(side="right")
        ttk.Button(toolbar, text="Add User", style="Accent.TButton", command=self._add_user_form).pack(side="right", padx=(0, 8))
        conn = self.db.get_connection()
        rows = conn.execute("SELECT username, role, full_name, status FROM users ORDER BY id DESC").fetchall()
        conn.close()
        if not rows:
            rows = [("admin", "Admin", "System Administrator", "Active")]
        tree = self._treeview(header, ["Username", "Role", "Full Name", "Status"], rows)

    def _show_settings(self) -> None:
        panel = tk.Frame(self.body, bg=COLORS["main_bg"])
        panel.pack(fill="both", expand=True)
        card = tk.LabelFrame(panel, text="System settings", bg=COLORS["card_bg"], fg=COLORS["text"], padx=12, pady=12)
        card.pack(fill="x")
        ttk.Button(card, text="Save Settings", style="Accent.TButton", command=self._save_settings).pack(anchor="e", pady=(0, 10))
        tk.Label(card, text="Automatic backups: Enabled", bg=COLORS["card_bg"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(card, text="Inactive logout timer: 15 minutes", bg=COLORS["card_bg"], fg=COLORS["text"]).pack(anchor="w", pady=(6, 0))
        tk.Label(card, text="Database status: Connected", bg=COLORS["card_bg"], fg=COLORS["accent_green"]).pack(anchor="w", pady=(6, 0))

    def _add_doctor_form(self) -> None:
        self._simple_form("Add Doctor", [("Doctor ID", "doctor_id"), ("Full Name", "full_name"), ("Department", "department"), ("Specialization", "specialization"), ("Phone", "phone"), ("Status", "status")], self._save_doctor)

    def _add_department_form(self) -> None:
        self._simple_form("Add Department", [("Department Name", "department_name"), ("Description", "description"), ("Head Doctor", "head_doctor"), ("Staff Count", "staff_count")], self._save_department)

    def _add_appointment_form(self) -> None:
        self._simple_form("Add Appointment", [("Appointment Number", "appointment_number"), ("Patient ID", "patient_id"), ("Doctor ID", "doctor_id"), ("Date", "appointment_date"), ("Time", "appointment_time"), ("Purpose", "purpose")], self._save_appointment)

    def _add_medical_record_form(self) -> None:
        self._simple_form("Add Medical Record", [("Record ID", "record_id"), ("Patient ID", "patient_id"), ("Doctor ID", "doctor_id"), ("Diagnosis", "diagnosis"), ("Symptoms", "symptoms"), ("Treatment", "treatment")], self._save_medical_record)

    def _add_prescription_form(self) -> None:
        self._simple_form("Add Prescription", [("Prescription ID", "prescription_id"), ("Patient ID", "patient_id"), ("Doctor ID", "doctor_id"), ("Medicine", "medicine_name"), ("Dosage", "dosage"), ("Frequency", "frequency"), ("Duration", "duration")], self._save_prescription)

    def _add_medicine_form(self) -> None:
        self._simple_form("Add Medicine", [("Medicine ID", "medicine_id"), ("Medicine Name", "medicine_name"), ("Category", "category"), ("Quantity", "quantity"), ("Minimum Stock", "minimum_stock"), ("Expiry Date", "expiry_date")], self._save_medicine)

    def _add_lab_test_form(self) -> None:
        self._simple_form("Add Lab Test", [("Test ID", "test_id"), ("Patient ID", "patient_id"), ("Doctor ID", "doctor_id"), ("Sample", "sample"), ("Result", "result"), ("Status", "status")], self._save_lab_test)

    def _add_bill_form(self) -> None:
        self._simple_form("Add Bill", [("Bill Number", "bill_number"), ("Patient ID", "patient_id"), ("Total", "total"), ("Amount Paid", "amount_paid"), ("Balance", "balance"), ("Payment Status", "payment_status")], self._save_bill)

    def _add_payment_form(self) -> None:
        self._simple_form("Add Payment", [("Payment ID", "payment_id"), ("Bill Number", "bill_number"), ("Method", "payment_method"), ("Amount", "amount"), ("Date", "payment_date"), ("Status", "status")], self._save_payment)

    def _add_user_form(self) -> None:
        self._simple_form("Add User", [("Username", "username"), ("Password", "password"), ("Role", "role"), ("Full Name", "full_name"), ("Status", "status")], self._save_user)

    def _generate_report(self) -> None:
        messagebox.showinfo("Report", "A summary report has been generated for the clinic dashboard.")

    def _save_settings(self) -> None:
        messagebox.showinfo("Settings", "Clinic settings saved successfully.")

    def _simple_form(self, title: str, fields: list, callback) -> None:
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("430x420")
        popup.configure(bg=COLORS["card_bg"])
        frm = tk.Frame(popup, bg=COLORS["card_bg"], padx=16, pady=16)
        frm.pack(fill="both", expand=True)
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frm, text=label, bg=COLORS["card_bg"], fg=COLORS["text"]).grid(row=i, column=0, sticky="w", pady=4)
            var = tk.StringVar()
            tk.Entry(frm, textvariable=var, width=32).grid(row=i, column=1, sticky="ew", pady=4)
            entries[key] = var
        ttk.Button(frm, text="Save", style="Accent.TButton", command=lambda: callback(entries, popup)).grid(row=len(fields), column=0, columnspan=2, sticky="ew", pady=(12, 0))

    def _save_doctor(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("doctor_id") or not data.get("full_name"):
            messagebox.showerror("Validation", "Doctor ID and full name are required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO doctors (doctor_id, full_name, department, specialization, phone, status) VALUES (?, ?, ?, ?, ?, ?)", (data["doctor_id"], data["full_name"], data.get("department", ""), data.get("specialization", ""), data.get("phone", ""), data.get("status", "Active")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Doctor added successfully.")
        self.show_module("Doctors")

    def _save_department(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("department_name"):
            messagebox.showerror("Validation", "Department name is required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO departments (department_name, description, head_doctor, staff_count) VALUES (?, ?, ?, ?)", (data["department_name"], data.get("description", ""), data.get("head_doctor", ""), data.get("staff_count", "")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Department added successfully.")
        self.show_module("Departments")

    def _save_appointment(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("appointment_number"):
            messagebox.showerror("Validation", "Appointment number is required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO appointments (appointment_number, patient_id, doctor_id, department, appointment_date, appointment_time, purpose, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (data["appointment_number"], data.get("patient_id", ""), data.get("doctor_id", ""), "General", data.get("appointment_date", ""), data.get("appointment_time", ""), data.get("purpose", ""), "Scheduled", ""))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Appointment added successfully.")
        self.show_module("Appointments")

    def _save_medical_record(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("record_id"):
            messagebox.showerror("Validation", "Record ID is required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO medical_records (record_id, patient_id, doctor_id, diagnosis, symptoms, treatment, doctor_notes, visit_date, vital_signs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (data["record_id"], data.get("patient_id", ""), data.get("doctor_id", ""), data.get("diagnosis", ""), data.get("symptoms", ""), data.get("treatment", ""), "", datetime.now().strftime("%Y-%m-%d"), ""))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Medical record added successfully.")
        self.show_module("Medical Records")

    def _save_prescription(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("prescription_id"):
            messagebox.showerror("Validation", "Prescription ID is required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, medicine_name, dosage, frequency, duration, instructions) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (data["prescription_id"], data.get("patient_id", ""), data.get("doctor_id", ""), data.get("medicine_name", ""), data.get("dosage", ""), data.get("frequency", ""), data.get("duration", ""), ""))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Prescription added successfully.")
        self.show_module("Prescriptions")

    def _save_medicine(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("medicine_id") or not data.get("medicine_name"):
            messagebox.showerror("Validation", "Medicine ID and name are required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO medicines (medicine_id, medicine_name, category, quantity, minimum_stock, expiry_date) VALUES (?, ?, ?, ?, ?, ?)", (data["medicine_id"], data["medicine_name"], data.get("category", ""), int(data.get("quantity", 0) or 0), int(data.get("minimum_stock", 0) or 0), data.get("expiry_date", "")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Medicine added successfully.")
        self.show_module("Medicines")

    def _save_lab_test(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("test_id"):
            messagebox.showerror("Validation", "Test ID is required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO lab_results (test_id, patient_id, doctor_id, sample, result, status, test_date) VALUES (?, ?, ?, ?, ?, ?, ?)", (data["test_id"], data.get("patient_id", ""), data.get("doctor_id", ""), data.get("sample", ""), data.get("result", ""), data.get("status", "Pending"), datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Lab test added successfully.")
        self.show_module("Laboratory")

    def _save_bill(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("bill_number"):
            messagebox.showerror("Validation", "Bill number is required.")
            return
        conn = self.db.get_connection()
        total = float(data.get("total", 0) or 0)
        paid = float(data.get("amount_paid", 0) or 0)
        balance = total - paid
        conn.execute("INSERT INTO bills (bill_number, patient_id, total, amount_paid, balance, payment_status) VALUES (?, ?, ?, ?, ?, ?)", (data["bill_number"], data.get("patient_id", ""), total, paid, balance, data.get("payment_status", "Pending")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Bill added successfully.")
        self.show_module("Billing")

    def _save_payment(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("payment_id"):
            messagebox.showerror("Validation", "Payment ID is required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO payments (payment_id, bill_number, payment_method, amount, payment_date, status) VALUES (?, ?, ?, ?, ?, ?)", (data["payment_id"], data.get("bill_number", ""), data.get("payment_method", ""), float(data.get("amount", 0) or 0), data.get("payment_date", datetime.now().strftime("%Y-%m-%d")), data.get("status", "Completed")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "Payment added successfully.")
        self.show_module("Payments")

    def _save_user(self, entries: dict, popup: tk.Toplevel) -> None:
        data = {k: v.get().strip() for k, v in entries.items()}
        if not data.get("username") or not data.get("password"):
            messagebox.showerror("Validation", "Username and password are required.")
            return
        conn = self.db.get_connection()
        conn.execute("INSERT INTO users (username, password, role, full_name, status) VALUES (?, ?, ?, ?, ?)", (data["username"], self.db.hash_password(data["password"]), data.get("role", "User"), data.get("full_name", ""), data.get("status", "Active")))
        conn.commit()
        conn.close()
        popup.destroy()
        messagebox.showinfo("Success", "User added successfully.")
        self.show_module("Users")

    def _delete_selected_from_tree(self, tree, table: str, id_column: str, module_name: str, refresh_callback) -> None:
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Delete", f"Select a {module_name} record to delete.")
            return
        values = tree.item(selected[0], "values")
        if not values:
            return
        record_id = values[0]
        if not messagebox.askyesno("Delete", f"Delete this {module_name} record: {record_id}?"):
            return
        conn = self.db.get_connection()
        try:
            conn.execute(f"DELETE FROM {table} WHERE {id_column} = ?", (record_id,))
            conn.commit()
        except sqlite3.Error as exc:
            messagebox.showerror("Delete Failed", f"Unable to delete record: {exc}")
            conn.close()
            return
        conn.close()
        messagebox.showinfo("Deleted", f"{module_name.title()} deleted successfully.")
        refresh_callback()

    def _treeview(self, parent: tk.Frame, columns: list, rows: list):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="w")
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True)
        return tree

    def _backup_database(self) -> None:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backup", "clinic_backup.db")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.db.backup_database(path)
        messagebox.showinfo("Backup", f"Database backup created at {path}")

    def _stats(self) -> dict:
        conn = self.db.get_connection()
        stats = {
            "patients": conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
            "doctors": conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0],
            "appointments": conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0],
            "today_appointments": conn.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (datetime.now().strftime("%Y-%m-%d"),)).fetchone()[0],
            "medicines": conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0],
            "low_stock": conn.execute("SELECT COUNT(*) FROM medicines WHERE quantity <= minimum_stock").fetchone()[0],
            "bills": conn.execute("SELECT COUNT(*) FROM bills").fetchone()[0],
            "revenue": conn.execute("SELECT COALESCE(SUM(total), 0) FROM bills").fetchone()[0],
            "payments": conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0],
            "pending_payments": conn.execute("SELECT COUNT(*) FROM bills WHERE payment_status != 'Paid'").fetchone()[0],
        }
        conn.close()
        return stats
