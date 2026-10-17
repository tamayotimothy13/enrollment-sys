import tkinter as tk
import re
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


def get_field_value(entry, placeholder):
    value = entry.get().strip()

    if value == placeholder:
        return ""

    return value

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
    add_placeholder(first_name, "e.g  Juan")

    last_name = create_field(frame, "Last Name", 0, 1)
    add_placeholder(last_name, "e.g  Dela Cruz")

    middle_initial = create_field(frame, "M.I", 0, 2, width=15)
    add_placeholder(middle_initial, "e.g  J.")

    prefix = create_field(frame, "Prefix", 0, 3, width=15)
    add_placeholder(prefix, "e.g  Jr, II")
    
    birthday = create_field(frame, "Birthday", 2, 0)
    add_placeholder(birthday, "YYYY-MM-DD")

    birth_place = create_field(frame, "Place of Birth", 2, 1)
    add_placeholder(birth_place, "e.g  Marikina City")

    return {
        "first_name": first_name,
        "middle_initial": middle_initial,
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
    add_placeholder(address, "House/Unit/Lot No., Street Name, Subdivision/Village, Barangay, City")
    
    email = create_field(frame, "Email", 0, 1, width=40)
    add_placeholder(email, "example@email.com")

    contact_number = create_field(frame, "Personal Contact #", 2,0)
    add_placeholder(contact_number, "09XXXXXXXXX")

    emergency_contact_number = create_field(frame, "Other Contact # (in case of emergency)", 2, 1)
    add_placeholder(emergency_contact_number, "09XXXXXXXXX")

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
        values=("New Student", "Returning Student"),
        state="readonly",
        width=27
    )
    admission_type.grid(
        row=1, column=0, sticky="ew", padx=10, pady=(5, 0)
    )

    # year level dropdown
    tk.Label(frame, text="Year Level (this s.y.)").grid(
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

    def update_year_levels(event=None):
                selected_type = admission_type.get()
    
                if selected_type == "New Student":
                    year_level["values"] = ("1st Year",)
                    year_level.set("1st Year")
                else:
                    year_level["values"] = (
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "4th Year"
                )
                year_level.set("")

    admission_type.bind("<<ComboboxSelected>>", update_year_levels)

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

def is_valid_contact_number(number):
    return bool(re.fullmatch(r"09\d{9}", number))

def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))

def show_students():

    window = tk.Toplevel()
    setup_window(window, "Students")

    personal_fields = create_personal_section(window)
    contact_fields = create_contact_section(window)
    academic_fields = create_academic_section(window)

    def save_student():
        first_name = get_field_value(personal_fields["first_name"], "e.g  Juan")
        middle_initial = get_field_value(personal_fields["middle_initial"], "e.g  J.")
        last_name = get_field_value(personal_fields["last_name"], "e.g  Dela Cruz")
        prefix = get_field_value(personal_fields["prefix"], "e.g  Jr, II")
        birthday = get_field_value(personal_fields["birthday"], "YYYY-MM-DD")
        birth_place = get_field_value(personal_fields["birth_place"], "e.g  Marikina City")
        address = get_field_value(contact_fields["address"], "House/Unit/Lot No., Street Name, Subdivision/Village, Barangay, City")
        email = get_field_value(contact_fields["email"], "example@email.com")
        contact_number = get_field_value(contact_fields["contact_number"], "09XXXXXXXXX")
        emergency_contact_number = get_field_value(contact_fields["emergency_contact_number"], "09XXXXXXXXX")
        admission_type = academic_fields["admission_type"].get()
        year_level = academic_fields["year_level"].get()
        course = academic_fields["course"].get()

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
            birth_date = datetime.strptime(
            birthday, "%Y-%m-%d"
            ).date()

            if birth_date > datetime.today().date():
                raise ValueError

        except ValueError:
            messagebox.showerror(
            "Invalid Birthday",
            "Enter a valid birthday in YYYY-MM-DD format. "
            "Birthday cannot be in the future.",
            parent=window
            )
            return

        if not birth_place:
            messagebox.showerror(
                "Error",
                "Birth place is required.",
                parent=window
            )
            return

        if not address or not email or not contact_number:
                    messagebox.showerror(
                        "Error",
                        "Please complete Contact Information fields.",
                        parent=window
                    )
                    return

        if not is_valid_email(email):
            messagebox.showerror(
            "Invalid Email",
            "Please enter a valid email address, such as name@example.com.",
            parent=window
            )
            return

        if not is_valid_contact_number(contact_number):
            messagebox.showerror(
            "Invalid Contact Number",
            "Please input valid format",
            parent=window
            )
            return

        if emergency_contact_number and not is_valid_contact_number(emergency_contact_number):
            messagebox.showerror(
            "Invalid Emergency Contact",
            "Please input valid format",
            parent=window
            )
            return
        
        if not admission_type or not year_level or not course:
            messagebox.showerror(
                "Error",
                "Please complete all Academic Information fields.",
                parent=window
            )
            return

        
        success = add_student(
            first_name=first_name,
            middle_name=middle_initial,
            last_name=last_name,
            prefix=prefix,
            address=address,
            birthday=birthday,
            birth_place=birth_place,
            contact_number=contact_number,
            emergency_contact_number=emergency_contact_number,
            email=email,
            admission_type=admission_type,
            year_level=year_level,
            course=course
        )

        if not success:
            messagebox.showerror(
                "Database Error",
                "Could not save the student. Check the terminal for details.",
                parent=window
            )
            return

        messagebox.showinfo(
            "Success",
            "Student successfully added!",
            parent=window
        )

        # Clear text fields and restore placeholders.
        personal_placeholders = {
            "first_name": "e.g  Juan",
            "middle_initial": "e.g  J.",
            "last_name": "e.g  Dela Cruz",
            "prefix": "e.g  Jr, II",
            "birthday": "YYYY-MM-DD",
            "birth_place": "e.g  Marikina City"
        }

        contact_placeholders = {
            "address": "House/Unit/Lot No., Street Name, Subdivision/Village, Barangay, City",
            "email": "example@email.com",
            "contact_number": "09XXXXXXXXX",
            "emergency_contact_number": "09XXXXXXXXX"
        }

        for name, entry in personal_fields.items():
            entry.delete(0, tk.END)
            add_placeholder(entry, personal_placeholders[name])

        for name, entry in contact_fields.items():
            entry.delete(0, tk.END)
            add_placeholder(entry, contact_placeholders[name])

        # Reset academic dropdowns.
        academic_fields["admission_type"].set("")
        academic_fields["year_level"]["values"] = (
            "1st Year", "2nd Year", "3rd Year", "4th Year"
        )
        academic_fields["year_level"].set("")
        academic_fields["course"].set("")

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    close_button = tk.Button(
        button_frame,
        text="Close",
        command=window.destroy
    )
    close_button.pack(side="left", padx=5)

    save_button = tk.Button(
        button_frame,
        text="Save Student",
        command=save_student
    )
    save_button.pack(side="left", padx=5)