import sys
import tkinter as tk
from views.clinic_ui import LoginWindow


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        from database.database import ClinicDatabase
        db = ClinicDatabase()
        db.initialize()
        print("Database initialized successfully.")
    else:
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()
