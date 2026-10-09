import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.students import add_student
from frontend.window import setup_window
from datetime import datetime


def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def create_field(parent, label_text, row, column, width=30):
    label = tk.Label(parent, text=label_text).grid(
        row=row, column=column, sticky="w", padx=10, pady=(5,0)
    )
    
    entry = tk.Entry(parent, width=width)
    entry.grid(
        row=row+1, column=column, sticky="ew", padx=10, pady=(5,0)
    )

    return entry

def create_personal_section(parent):
    frame = tk.LabelFrame(
        parent,
        text="Personal Information",
        padx=10,
        pady=5
    )
    frame.pack(fill="x", padx=20, pady=5)

    first_name = create_field(frame, "First Name", 0, 0)
    middle_name = create_field(frame, "Middle Name", 0, 1)
    last_name = create_field(frame, "Last Name", 0, 2)
    prefix = create_field(frame, "Prefix", 0, 3, width=15)
    
    birthday = create_field(frame, "Birthday", 2, 0)
    add_placeholder(birthday, "YYYY-MM-DD")

    birth_place = create_field(frame, "Place of Birth", 2, 1)

    return {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "prefix": prefix,
        "birthday": birthday,
        "birth_place":birth_place
    }

def create_contact_section(parent):
    frame = tk.LabelFrame(
            parent,
            text="Contact Information",
            padx=10,
            pady=5
        )
    frame.pack(fill="x", padx=20, pady=5)

    address = create_field(frame, "Address", 0, 0, width=70)
    email = create_field(frame, "Email", 0, 1, width=40)
    contact_number = create_field(frame, "Personal Contact #", 2,0)
    emergency_contact_number = create_field(frame, "Other Contact # (in case of emergency)", 2, 1)

    return {
        "address":address,
        "email":email,
        "contact_number" :contact_number,
        "emergency_contact_number":emergency_contact_number
    }

def create_academic_section(parent):
    frame = tk.LabelFrame(
                parent,
                text="Academic Information",
                padx=10,
                pady=5
            )
    frame.pack(fill="x", padx=20, pady=5)

    # admission_type dropdown
    tk.Label(frame, text="Admission Type").grid(
        row=0, column=0, sticky="w", padx=10, pady=(5, 0)
    )
    admission_type = ttk.Combobox(
        frame,
        values=("New Student", "Transferee", "Returning Student"),
        state="readonly",
        width=27
    )
    admission_type.grid(
        row=1, column=0, sticky="ew", padx=10, pady=(5, 0)
    )

    # year level dropdown
    tk.Label(frame, text="Year Level").grid(
        row=0, column=1, sticky="w", padx=10, pady=(5, 0)
    )
    year_level = ttk.Combobox(
        frame,
        values=("1st Year", "2nd Year", "3rd Year", "4th Year"),
        state="readonly",
        width=27
    )
    year_level.grid(
        row=1, column=1, sticky="ew", padx=10, pady=(5, 0)
    )

    # Course dropdown
    tk.Label(frame, text="Course").grid(
        row=0, column=2, sticky="w", padx=10, pady=(5, 0)
    )
    course = ttk.Combobox(
        frame,
        values=(
            "BS Computer Science",
            "BS Information Technology",
            "BS Information Systems"
        ),
        state="readonly",
        width=27
    )
    course.grid(
        row=1, column=2, sticky="ew", padx=10, pady=(5, 0)
    )

    return {
        "admission_type":admission_type,
        "year_level":year_level,
        "course":course
    }

def show_students():

    window = tk.Toplevel()
    setup_window(window, "Students")

    personal_fields = create_personal_section(window)
    contact_fields = create_contact_section(window)
    academic_fields = create_academic_section(window)

    def save_student():
        first_name = personal_fields["first_name"].get().strip()
        last_name = personal_fields["last_name"].get().strip()
        birthday = personal_fields["birthday"].get().strip()

        if not first_name:
            messagebox.showerror(
                "Error",
                "First name is required.",
                parent=window
            )
            return

        if not last_name:
            messagebox.showerror(
                "Error",
                "Last name is required.",
                parent=window
            )
            return
        
        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
            "Error",
            "Enter a valid birthday in YYYY-MM-DD format.",
            parent=window
            )
            return