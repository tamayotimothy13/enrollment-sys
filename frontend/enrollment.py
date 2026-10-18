import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window
from backend.enrollments import (
    get_available_subjects,
    save_enrollment,
    get_unenrolled_students
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

    # Search students
    tk.Label(main, text="Search Student (Name or ID)").pack(anchor="w")

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        main,
        textvariable=search_var,
        width=55
    )
    search_entry.pack(anchor="w", pady=(5, 8))

    # Student selection table
    tk.Label(main, text="Select Student").pack(anchor="w")

    student_options = {}
    all_student_options = {}

    student_table_frame = tk.Frame(main)
    student_table_frame.pack(fill="x", pady=(5, 12))

    student_columns = (
        "student_id",
        "first_name",
        "last_name",
        "course",
        "year_level",
        "admission_type"
    )

    student_table = ttk.Treeview(
        student_table_frame,
        columns=student_columns,
        show="headings",
        height=5,
        selectmode="browse"
    )

    student_table.heading("student_id", text="Student ID")
    student_table.heading("first_name", text="First Name")
    student_table.heading("last_name", text="Last Name")
    student_table.heading("course", text="Course")
    student_table.heading("year_level", text="Year Level")
    student_table.heading("admission_type", text="Admission Type")

    student_table.column("student_id", width=100)
    student_table.column("first_name", width=100)
    student_table.column("last_name", width=100)
    student_table.column("course", width=150)
    student_table.column("year_level", width=90)
    student_table.column("admission_type", width=110)

    student_table.pack(side="left", fill="x", expand=True)

    student_scrollbar = ttk.Scrollbar(
        student_table_frame,
        orient="vertical",
        command=student_table.yview
    )
    student_table.configure(yscrollcommand=student_scrollbar.set)
    student_scrollbar.pack(side="right", fill="y")

    student_var = tk.StringVar(value="Select a student...")

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

    
    def select_all_subjects():
        for var, subject_id, units in subject_vars:
            var.set(True)

        update_total_units()


    def deselect_all_subjects():
        for var, subject_id, units in subject_vars:
            var.set(False)

        update_total_units()

    subject_button_frame = tk.Frame(main)
    subject_button_frame.pack(anchor="w", pady=(5, 0))

    tk.Button(
        subject_button_frame,
        text="Select All",
        command=select_all_subjects
    ).pack(side="left", padx=(0, 5))

    tk.Button(
        subject_button_frame,
        text="Deselect All",
        command=deselect_all_subjects
    ).pack(side="left")

    
    def load_available_subjects(event=None):
        nonlocal selected_student_id

        selected = student_table.selection()

        selected_student_id = None

        for widget in subject_frame.winfo_children():
            widget.destroy()

        subject_vars.clear()
        total_units_var.set("Total Units: 0")

        if not selected:
            return

        student_values = student_table.item(
            selected[0], "values"
        )
        selected_student_id = student_values[0]

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


    
    def filter_students(event=None):
        query = search_var.get().strip().lower()

        # Clear the current selection and subject list.
        student_table.selection_remove(
            student_table.selection()
        )
        load_available_subjects()

        # Remove the currently displayed rows.
        for item in student_table.get_children():
            student_table.delete(item)

        # Display matching students.
        for student in all_student_options.values():
            (
                student_id,
                first_name,
                last_name,
                course,
                year_level,
                admission_type
            ) = student

            searchable_text = (
                f"{student_id} {first_name} {last_name} "
                f"{course} {year_level} {admission_type}"
            ).lower()

            if query in searchable_text:
                student_table.insert(
                    "",
                    "end",
                    values=(
                        student_id,
                        first_name,
                        last_name,
                        course,
                        year_level,
                        admission_type
                    )
                )


    
    def refresh_student_options(event=None):
        academic_year = academic_year_var.get().strip()
        semester = semester_var.get()

        all_student_options.clear()
        search_var.set("")

        # Clear the student table.
        for item in student_table.get_children():
            student_table.delete(item)

        # Clear the subject list.
        load_available_subjects()

        if not academic_year or not semester:
            return

        students = get_unenrolled_students(
            academic_year,
            semester
        )

        if students is None:
            messagebox.showerror(
                "Database Error",
                "Could not load available students. "
                "Check the terminal for details.",
                parent=window
            )
            return

        for student in students:
            (
                student_id,
                first_name,
                last_name,
                course,
                year_level,
                admission_type
            ) = student

            all_student_options[student_id] = student

        filter_students()
    
    student_table.bind(
        "<<TreeviewSelect>>",
        load_available_subjects
    )

    search_entry.bind(
        "<KeyRelease>",
        filter_students
    )

    semester_combo.bind(
        "<<ComboboxSelected>>",
        refresh_student_options
    )

    academic_year_entry.bind(
        "<Return>",
        refresh_student_options
    )

    academic_year_entry.bind(
        "<FocusOut>",
        refresh_student_options
    )


    def enroll_student():
        selected = student_table.selection()

        if not selected:
            messagebox.showwarning(
                "Missing Student",
                "Please select a student.",
                parent=window
            )
            return

        student_id = student_table.item(
            selected[0], "values"
        )[0]
        
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
            refresh_student_options()
            
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

    refresh_student_options()