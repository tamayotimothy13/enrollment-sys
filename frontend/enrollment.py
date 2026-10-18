import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window
from backend.students import get_all_students
from backend.enrollments import (
    get_available_subjects,
    save_enrollment
)


def show_enrollment(parent=None):
    window = tk.Toplevel(parent) if parent else tk.Tk()
    setup_window(window, "Enroll Student")

    main = tk.Frame(window, padx=20, pady=20)
    main.pack(fill="both", expand=True)

    tk.Label(
        main,
        text="Student Enrollment",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", pady=(0, 15))

    # Student selection
    tk.Label(main, text="Select Student").pack(anchor="w")

    students = get_all_students()
    student_options = {}

    for student in students:
        student_id, first_name, last_name, course, year_level, email = student
        display = (
            f"{student_id} - {first_name} {last_name} "
            f"({course}, Year {year_level})"
        )
        student_options[display] = student_id

    student_var = tk.StringVar()
    student_combo = ttk.Combobox(
        main,
        textvariable=student_var,
        values=list(student_options.keys()),
        state="readonly",
        width=55
    )
    student_combo.pack(anchor="w", pady=(5, 12))

    # Academic year
    tk.Label(main, text="Academic Year").pack(anchor="w")

    academic_year_var = tk.StringVar(value="2026-2027")
    academic_year_entry = tk.Entry(
        main,
        textvariable=academic_year_var,
        width=20
    )
    academic_year_entry.pack(anchor="w", pady=(5, 12))

    # Semester
    tk.Label(main, text="Semester").pack(anchor="w")

    semester_var = tk.StringVar(value="1st Semester")
    semester_combo = ttk.Combobox(
        main,
        textvariable=semester_var,
        values=("1st Semester", "2nd Semester"),
        state="readonly",
        width=20
    )
    semester_combo.pack(anchor="w", pady=(5, 12))

    # Available subjects
    tk.Label(
        main,
        text="Available Subjects",
        font=("Arial", 11, "bold")
    ).pack(anchor="w", pady=(5, 5))

    subject_frame = tk.Frame(main)
    subject_frame.pack(fill="both", expand=True)

    subject_vars = []
    selected_student_id = None

    total_units_var = tk.StringVar(value="Total Units: 0")

    tk.Label(
        main,
        textvariable=total_units_var,
        font=("Arial", 10, "bold")
    ).pack(anchor="w", pady=10)

    def update_total_units():
        total = sum(
            units
            for var, subject_id, units in subject_vars
            if var.get()
        )
        total_units_var.set(f"Total Units: {total}")

    def load_available_subjects(event=None):
        nonlocal selected_student_id

        selected_display = student_var.get()
        selected_student_id = student_options.get(selected_display)

        for widget in subject_frame.winfo_children():
            widget.destroy()

        subject_vars.clear()
        total_units_var.set("Total Units: 0")

        if not selected_student_id:
            return

        subjects = get_available_subjects(
            selected_student_id,
            semester_var.get()
        )

        if not subjects:
            tk.Label(
                subject_frame,
                text="No subjects found for this student and semester."
            ).pack(anchor="w", pady=5)
            return

        for subject_id, code, name, units in subjects:
            var = tk.BooleanVar(value=False)

            tk.Checkbutton(
                subject_frame,
                text=f"{code} - {name} ({units} units)",
                variable=var,
                command=update_total_units
            ).pack(anchor="w")

            subject_vars.append((var, subject_id, units))

    def on_semester_change(event=None):
        load_available_subjects()

    student_combo.bind(
        "<<ComboboxSelected>>",
        load_available_subjects
    )
    semester_combo.bind(
        "<<ComboboxSelected>>",
        on_semester_change
    )

    def enroll_student():
        student_id = student_options.get(student_var.get())
        academic_year = academic_year_var.get().strip()
        semester = semester_var.get()

        if not student_id:
            messagebox.showwarning(
                "Missing Student",
                "Please select a student.",
                parent=window
            )
            return

        if not academic_year:
            messagebox.showwarning(
                "Missing Academic Year",
                "Please enter the academic year.",
                parent=window
            )
            return

        subject_ids = [
            subject_id
            for var, subject_id, units in subject_vars
            if var.get()
        ]

        if not subject_ids:
            messagebox.showwarning(
                "No Subjects Selected",
                "Please select at least one subject.",
                parent=window
            )
            return

        enrollment_id = save_enrollment(
            student_id,
            academic_year,
            semester,
            subject_ids
        )

        if enrollment_id is not None:
            messagebox.showinfo(
                "Success",
                f"Enrollment saved successfully!\n"
                f"Enrollment ID: {enrollment_id}",
                parent=window
            )

            load_available_subjects()
        else:
            messagebox.showerror(
                "Enrollment Failed",
                "Could not save enrollment. The student may "
                "already be enrolled for this academic year "
                "and semester. Check the terminal for details.",
                parent=window
            )

    tk.Button(
        main,
        text="Save Enrollment",
        command=enroll_student
    ).pack(anchor="w", pady=(5, 10))

    ttk.Button(
        main,
        text="Close",
        command=window.destroy
    ).pack(anchor="e")

    if students:
        student_combo.current(0)
        load_available_subjects()
    else:
        messagebox.showinfo(
            "No Students",
            "Add a student before creating an enrollment.",
            parent=window
        )