import tkinter as tk
from tkinter import messagebox
from backend.students import add_student


def show_students():

    window = tk.Toplevel()
    window.title("Students")
    window.geometry("500x700")

    title = tk.Label(
        window,
        text="Add Student",
        font=("Arial", 20)
    )
    title.pack(pady=20)

    # Student ID
    tk.Label(window, text="Student ID").pack()
    student_id = tk.Entry(window)
    student_id.pack()

    # First Name
    tk.Label(window, text="First Name").pack()
    first_name = tk.Entry(window)
    first_name.pack()

    # Middle Name
    tk.Label(window, text="Middle Name").pack()
    middle_name = tk.Entry(window)
    middle_name.pack()

    # Last Name
    tk.Label(window, text="Last Name").pack()
    last_name = tk.Entry(window)
    last_name.pack()

    # Prefix
    tk.Label(window, text="Prefix").pack()
    prefix = tk.Entry(window)
    prefix.pack()

    # Address
    tk.Label(window, text="Address").pack()
    address = tk.Entry(window, width=40)
    address.pack()

    # Birthday
    tk.Label(window, text="Birthday").pack()
    birthday = tk.Entry(window)
    birthday.pack()

    # Contact Number
    tk.Label(window, text="Contact Number").pack()
    contact_number = tk.Entry(window)
    contact_number.pack()

    # Email
    tk.Label(window, text="Email").pack()
    email = tk.Entry(window)
    email.pack()

    # Admission Type
    tk.Label(window, text="Admission Type").pack()
    admission_type = tk.Entry(window)
    admission_type.pack()

    # Year Level
    tk.Label(window, text="Year Level").pack()
    year_level = tk.Entry(window)
    year_level.pack()

    # Course
    tk.Label(window, text="Course").pack()
    course = tk.Entry(window)
    course.pack()

    def save_student():

        if student_id.get() == "":
            messagebox.showerror(
                "Error",
                "Student ID is required."
            )
            return

        if first_name.get() == "":
            messagebox.showerror(
                "Error",
                "First name is required."
            )
            return

        if last_name.get() == "":
            messagebox.showerror(
                "Error",
                "Last name is required."
            )
            return

        success = add_student(
            student_id.get(),
            first_name.get(),
            middle_name.get(),
            last_name.get(),
            prefix.get(),
            address.get(),
            birthday.get(),
            contact_number.get(),
            email.get(),
            admission_type.get(),
            year_level.get(),
            course.get()
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )

            # Clear the form
            student_id.delete(0, tk.END)
            first_name.delete(0, tk.END)
            middle_name.delete(0, tk.END)
            last_name.delete(0, tk.END)
            prefix.delete(0, tk.END)
            address.delete(0, tk.END)
            birthday.delete(0, tk.END)
            contact_number.delete(0, tk.END)
            email.delete(0, tk.END)
            admission_type.delete(0, tk.END)
            year_level.delete(0, tk.END)
            course.delete(0, tk.END)

        else:
            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )
        print("Student added successfully.")

    add_button = tk.Button(
        window,
        text="Add Student",
        command=save_student
    )
    add_button.pack(pady=20)