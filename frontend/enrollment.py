import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window
from backend.enrollments import (
    get_available_subjects,
    save_enrollment,
    get_unenrolled_students
)


def show_enrollment(parent=None):
    BG_COLOR = "#F3F6FC"
    PRIMARY_COLOR = "#2563EB"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#1E293B"
    MUTED_COLOR = "#64748B"
    RED_COLOR = "#DC2626"

    window = tk.Toplevel(parent) if parent else tk.Tk()
    setup_window(window, "Enroll Student")

    window.configure(bg=BG_COLOR)

    main = tk.Frame(window, padx=20, pady=20, bg=BG_COLOR)
    main.pack(fill="both", expand=True)

    tk.Label(
        main,
        text="Student Enrollment",
        font=("Arial", 18, "bold"),
        bg=BG_COLOR
    ).pack(anchor="w", pady=(0, 15))

    # Search students
    tk.Label(main, text="Search Student (Name or ID)", bg=BG_COLOR).pack(anchor="w")

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        main,
        textvariable=search_var,
        width=55
    )
    search_entry.pack(anchor="w", pady=(5, 8))

    # Student selection table
    tk.Label(main, text="Select Student", bg=BG_COLOR).pack(anchor="w")

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

    # Academic Year and Semester
    academic_semester_frame = tk.Frame(main, bg=BG_COLOR)
    academic_semester_frame.pack(
        fill="x",
        pady=(5, 12)
    )

    # Academic Year - left side
    academic_frame = tk.Frame(academic_semester_frame, bg=BG_COLOR)
    academic_frame.pack(side="left", anchor="nw", padx=(0, 25))

    tk.Label(
        academic_frame,
        text="Academic Year",
        bg=BG_COLOR
    ).pack(anchor="w")

    academic_year_var = tk.StringVar(value="2026-2027")

    academic_year_entry = tk.Entry(
        academic_frame,
        textvariable=academic_year_var,
        width=20
    )
    academic_year_entry.pack(anchor="w", pady=(5, 0))

    # Semester - right side
    semester_frame = tk.Frame(academic_semester_frame, bg=BG_COLOR)
    semester_frame.pack(side="left", anchor="nw")

    tk.Label(
        semester_frame,
        text="Semester",
        bg=BG_COLOR
    ).pack(anchor="w")

    semester_var = tk.StringVar(value="1st Semester")

    semester_combo = ttk.Combobox(
        semester_frame,
        textvariable=semester_var,
        values=("1st Semester", "2nd Semester"),
        state="readonly",
        width=20
    )
    semester_combo.pack(anchor="w", pady=(5, 0))

    # Available subjects
    tk.Label(
        main,
        text="Available Subjects",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    ).pack(anchor="w", pady=(5, 5))

    subject_frame = tk.Frame(main)
    subject_frame.pack(fill="both", expand=True)

    subject_columns = ("select", "code", "name", "year_level", "units")

    subject_table = ttk.Treeview(
        subject_frame,
        columns=subject_columns,
        show="headings",
        height=6,
        selectmode="browse"
    )

    subject_table.heading("select", text="Select")
    subject_table.heading("code", text="Subject Code")
    subject_table.heading("name", text="Subject Name")
    subject_table.heading("year_level", text="Year Level")
    subject_table.heading("units", text="Units")

    subject_table.column("select", width=55, anchor="center")
    subject_table.column("code", width=110, anchor="w")
    subject_table.column("name", width=250, anchor="w")
    subject_table.column("year_level", width=100, anchor="center")
    subject_table.column("units", width=60, anchor="center")

    subject_scrollbar = ttk.Scrollbar(
        subject_frame,
        orient="vertical",
        command=subject_table.yview
    )

    subject_table.configure(
        yscrollcommand=subject_scrollbar.set
    )

    subject_table.pack(side="left", fill="both", expand=True)
    subject_scrollbar.pack(side="right", fill="y")

    subject_vars = []

    total_units_var = tk.StringVar(value="Total Units: 0")

    tk.Label(
        main,
        textvariable=total_units_var,
        font=("Arial", 10, "bold")
    ).pack(anchor="w", pady=10)


    def update_total_units():
        total = sum(
            units
            for subject_id, units, selected in subject_vars
            if selected
        )
        total_units_var.set(f"Total Units: {total}")


    def select_all_subjects():
        for index, (subject_id, units, _) in enumerate(subject_vars):
            subject_vars[index] = (subject_id, units, True)

            item_id = str(subject_id)
            if subject_table.exists(item_id):
                values = subject_table.item(item_id, "values")
                subject_table.item(
                    item_id,
                    values=("☑", values[1], values[2], values[3], values[4])
                )

        update_total_units()


    def deselect_all_subjects():
        for index, (subject_id, units, _) in enumerate(subject_vars):
            subject_vars[index] = (subject_id, units, False)

            item_id = str(subject_id)
            if subject_table.exists(item_id):
                values = subject_table.item(item_id, "values")
                subject_table.item(
                    item_id,
                    values=("☐", values[1], values[2], values[3], values[4])
                )

        update_total_units()


    def toggle_subject(event):
        item_id = subject_table.identify_row(event.y)
        column = subject_table.identify_column(event.x)

        # Toggle only when the selection column is clicked.
        if not item_id or column != "#1":
            return

        for index, (subject_id, units, selected) in enumerate(subject_vars):
            if str(subject_id) == item_id:
                selected = not selected
                subject_vars[index] = (subject_id, units, selected)

                values = subject_table.item(item_id, "values")
                subject_table.item(
                    item_id,
                    values=(
                        "☑" if selected else "☐",
                        values[1],
                        values[2],
                        values[3],
                        values[4]
                    )
                )
                break

        update_total_units()

    def load_available_subjects(event=None):
        selected = student_table.selection()

        for item in subject_table.get_children():
            subject_table.delete(item)

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
            return

        for subject_id, code, name, year_level, units in subjects:
            subject_id = str(subject_id)
            subject_vars.append((subject_id, units, False))

            subject_table.insert(
                "",
                "end",
                iid=subject_id,
                values=("☐", code, name, year_level, units)
            )

    
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

    subject_table.bind(
        "<Button-1>",
        toggle_subject
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
            for subject_id, units, selected in subject_vars
            if selected
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

    subject_button_frame = tk.Frame(main, bg=BG_COLOR)
    subject_button_frame.pack(fill="x", pady=(0, 5))

    tk.Button(
        subject_button_frame,
        text="Select All",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#0F766E",
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=select_all_subjects
    ).pack(side="left", padx=(0, 5))

    tk.Button(
        subject_button_frame,
        text="Deselect All",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#0F766E",
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=deselect_all_subjects
    ).pack(side="left")

    tk.Button(
        subject_button_frame,
        text="Close",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg=TEXT_COLOR,
        relief="flat",
        cursor="hand2",
        command=window.destroy
    ).pack(side="right")

    tk.Button(
        subject_button_frame,
        text="Enroll Student",
        width=14,
        font=("Arial", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=enroll_student
    ).pack(side="right", padx=(0, 5))

    refresh_student_options()