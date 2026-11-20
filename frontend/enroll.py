
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window

from backend.enrollments import (
    get_unenrolled_students,
    get_available_subjects,
    save_enrollment,
    get_year_number
)


# ==========================================
# COLORS
# ==========================================

BG_COLOR = "#F3F6FC"
PRIMARY_COLOR = "#2563EB"
WHITE = "#FFFFFF"
TEXT_COLOR = "#1E293B"
MUTED_COLOR = "#64748B"
RED_COLOR = "#DC2626"


# ==========================================
# STUDENT ENROLLMENT
# ==========================================

def student_list(parent=None):

    window = tk.Toplevel(parent) if parent else tk.Tk()

    setup_window(window, "Student Enrollment")
    window.configure(bg=BG_COLOR)

    main = tk.Frame(
        window,
        bg=BG_COLOR,
        padx=15,
        pady=15
    )

    main.pack(fill="both", expand=True)

    selected_student = None
    available_subject_map = {}

    # ======================================
    # TITLE
    # ======================================

    tk.Label(
        main,
        text="Student Enrollment",
        font=("Arial", 16, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", pady=(0, 12))

    # ======================================
    # ACADEMIC YEAR AND SEMESTER
    # ======================================

    settings_frame = tk.Frame(
        main,
        bg=WHITE,
        padx=12,
        pady=12
    )

    settings_frame.pack(fill="x", pady=(0, 12))

    tk.Label(
        settings_frame,
        text="Academic Year:",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).grid(row=0, column=0, sticky="w", padx=5)

    academic_year_entry = tk.Entry(
        settings_frame,
        font=("Arial", 10),
        width=18,
        relief="solid",
        bd=1
    )

    academic_year_entry.grid(
        row=0,
        column=1,
        padx=8
    )

    tk.Label(
        settings_frame,
        text="Semester:",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).grid(row=0, column=2, sticky="w", padx=5)

    semester_combo = ttk.Combobox(
        settings_frame,
        values=[
            "1st Semester",
            "2nd Semester"
        ],
        state="readonly",
        width=18,
        font=("Arial", 10)
    )

    semester_combo.grid(
        row=0,
        column=3,
        padx=8
    )

    semester_combo.set("1st Semester")

    # ======================================
    # STUDENT LIST
    # ======================================

    tk.Label(
        main,
        text="Students Available for Enrollment",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", pady=(5, 5))

    student_frame = tk.Frame(main)

    student_frame.pack(
        fill="both",
        expand=True
    )

    student_columns = (
        "student_id",
        "student_name",
        "course",
        "year_level",
        "admission_type"
    )

    student_tree = ttk.Treeview(
        student_frame,
        columns=student_columns,
        show="headings",
        height=6,
        selectmode="browse"
    )

    student_headings = {
        "student_id": "Student ID",
        "student_name": "Student Name",
        "course": "Course",
        "year_level": "Year Level",
        "admission_type": "Admission Type"
    }

    for column, heading in student_headings.items():
        student_tree.heading(column, text=heading)
        student_tree.column(
            column,
            width=140,
            anchor="center"
        )

    student_tree.column("student_name", width=190)
    student_tree.column("course", width=180)

    student_scrollbar = ttk.Scrollbar(
        student_frame,
        orient="vertical",
        command=student_tree.yview
    )

    student_tree.configure(
        yscrollcommand=student_scrollbar.set
    )

    student_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    student_scrollbar.pack(
        side="right",
        fill="y"
    )

    # ======================================
    # SELECTED STUDENT INFORMATION
    # ======================================

    student_info_frame = tk.Frame(
        main,
        bg="#E2E8F0",
        padx=12,
        pady=10
    )

    student_info_frame.pack(
        fill="x",
        pady=12
    )

    student_info_label = tk.Label(
        student_info_frame,
        text="Select a student to view available subjects.",
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg=TEXT_COLOR
    )

    student_info_label.pack(anchor="w")

    # ======================================
    # SUBJECTS
    # ======================================

    tk.Label(
        main,
        text="Available Subjects",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        main,
        text=(
            "Select the subjects for enrollment. "
            "Current-year subjects are automatically selected. "
            "Transferees may also select previous-year subjects."
        ),
        font=("Arial", 9),
        bg=BG_COLOR,
        fg=MUTED_COLOR
    ).pack(anchor="w", pady=(0, 8))

    subject_frame = tk.Frame(main)

    subject_frame.pack(
        fill="both",
        expand=True
    )

    subject_columns = (
        "code",
        "name",
        "units",
        "year_level"
    )

    subject_tree = ttk.Treeview(
        subject_frame,
        columns=subject_columns,
        show="headings",
        height=8,
        selectmode="extended"
    )

    subject_tree.heading("code", text="Subject Code")
    subject_tree.heading("name", text="Subject Name")
    subject_tree.heading("units", text="Units")
    subject_tree.heading("year_level", text="Year Level")

    subject_tree.column(
        "code",
        width=130,
        anchor="center"
    )

    subject_tree.column(
        "name",
        width=300
    )

    subject_tree.column(
        "units",
        width=80,
        anchor="center"
    )

    subject_tree.column(
        "year_level",
        width=130,
        anchor="center"
    )

    subject_scrollbar = ttk.Scrollbar(
        subject_frame,
        orient="vertical",
        command=subject_tree.yview
    )

    subject_tree.configure(
        yscrollcommand=subject_scrollbar.set
    )

    subject_tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    subject_scrollbar.pack(
        side="right",
        fill="y"
    )

    # ======================================
    # TOTAL UNITS
    # ======================================

    total_units_label = tk.Label(
        main,
        text="Selected Subjects: 0 | Total Units: 0",
        font=("Arial", 10, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    )

    total_units_label.pack(
        anchor="e",
        pady=8
    )

    # ======================================
    # UPDATE TOTAL UNITS
    # ======================================

    def update_total_units(event=None):

        total_units = 0
        selected_count = 0

        for item in subject_tree.selection():

            selected_count += 1

            subject_id = int(
                subject_tree.item(item, "tags")[0]
            )

            subject = available_subject_map.get(subject_id)

            if subject:
                total_units += subject[4] or 0

        total_units_label.config(
            text=(
                f"Selected Subjects: {selected_count} "
                f"| Total Units: {total_units}"
            )
        )

    subject_tree.bind(
        "<<TreeviewSelect>>",
        update_total_units
    )

    # ======================================
    # CLEAR SUBJECTS
    # ======================================

    def clear_subjects():

        for item in subject_tree.get_children():
            subject_tree.delete(item)

        available_subject_map.clear()

        update_total_units()

    # ======================================
    # LOAD STUDENTS
    # ======================================

    def load_students():

        nonlocal selected_student

        academic_year = academic_year_entry.get().strip()
        semester = semester_combo.get()

        if not academic_year:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the academic year.",
                parent=window
            )
            return

        if not semester:
            messagebox.showwarning(
                "Missing Information",
                "Please select a semester.",
                parent=window
            )
            return

        selected_student = None

        for item in student_tree.get_children():
            student_tree.delete(item)

        clear_subjects()

        student_info_label.config(
            text="Select a student to view available subjects."
        )

        students = get_unenrolled_students(
            academic_year,
            semester
        )

        if students is None:
            messagebox.showerror(
                "Error",
                "Could not load student records.",
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

            student_tree.insert(
                "",
                "end",
                values=(
                    student_id,
                    f"{first_name} {last_name}",
                    course,
                    year_level,
                    admission_type
                )
            )

    # ======================================
    # LOAD SUBJECTS FOR SELECTED STUDENT
    # ======================================

    def load_student_subjects(event=None):

        nonlocal selected_student

        selected = student_tree.selection()

        if not selected:
            return

        values = student_tree.item(
            selected[0],
            "values"
        )

        student_id = values[0]
        student_name = values[1]
        course = values[2]
        year_level = values[3]
        admission_type = values[4]

        selected_student = {
            "student_id": student_id,
            "name": student_name,
            "course": course,
            "year_level": year_level,
            "admission_type": admission_type
        }

        clear_subjects()

        year_number = get_year_number(year_level)

        if year_number is None:
            messagebox.showerror(
                "Invalid Year Level",
                "The student's year level could not be determined.",
                parent=window
            )
            return

        year_names = {
            1: "1st Year",
            2: "2nd Year",
            3: "3rd Year",
            4: "4th Year"
        }

        current_year_name = year_names.get(year_number)

        if current_year_name is None:
            messagebox.showerror(
                "Invalid Year Level",
                "The student's year level must be between 1st and 4th Year.",
                parent=window
            )
            return

        semester = semester_combo.get()

        if not semester:
            return

        subjects = get_available_subjects(
            student_id,
            semester
        )

        student_info_label.config(
            text=(
                f"Student: {student_name}    "
                f"Course: {course}    "
                f"Year Level: {current_year_name}    "
                f"Admission: {admission_type}"
            )
        )

        if not subjects:
            messagebox.showinfo(
                "No Available Subjects",
                "No subjects were found for this student, "
                "semester, and year level.",
                parent=window
            )
            return

        # Display all permitted subjects.
        # The backend already filters by admission type.

        for subject in subjects:

            (
                subject_id,
                subject_code,
                subject_name,
                subject_year,
                units
            ) = subject

            subject_id = int(subject_id)

            available_subject_map[subject_id] = subject

            item = subject_tree.insert(
                "",
                "end",
                values=(
                    subject_code,
                    subject_name,
                    units,
                    subject_year
                ),
                tags=(str(subject_id),)
            )

            # Automatically select current-year subjects only.
            subject_year_number = get_year_number(subject_year)

            if subject_year_number == year_number:
                subject_tree.selection_add(item)

        update_total_units()

    student_tree.bind(
        "<<TreeviewSelect>>",
        load_student_subjects
    )

    # ======================================
    # SAVE ENROLLMENT
    # ======================================

    def enroll_student():

        if selected_student is None:
            messagebox.showwarning(
                "No Student Selected",
                "Please select a student first.",
                parent=window
            )
            return

        academic_year = academic_year_entry.get().strip()
        semester = semester_combo.get()

        if not academic_year:
            messagebox.showwarning(
                "Missing Academic Year",
                "Please enter the academic year.",
                parent=window
            )
            return

        if not semester:
            messagebox.showwarning(
                "Missing Semester",
                "Please select a semester.",
                parent=window
            )
            return

        selected_items = subject_tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "No Subjects Selected",
                "Please select at least one subject.",
                parent=window
            )
            return

        subject_ids = []

        for item in selected_items:

            subject_id = int(
                subject_tree.item(item, "tags")[0]
            )

            subject_ids.append(subject_id)

        confirm = messagebox.askyesno(
            "Confirm Enrollment",
            (
                f"Enroll {selected_student['name']}?\n\n"
                f"Academic Year: {academic_year}\n"
                f"Semester: {semester}\n"
                f"Year Level: {selected_student['year_level']}\n"
                f"Selected Subjects: {len(subject_ids)}"
            ),
            parent=window
        )

        if not confirm:
            return

        enrollment_id = save_enrollment(
            selected_student["student_id"],
            academic_year,
            semester,
            subject_ids
        )

        if enrollment_id:

            messagebox.showinfo(
                "Enrollment Successful",
                (
                    f"Student enrolled successfully!\n\n"
                    f"Enrollment ID: {enrollment_id}"
                ),
                parent=window
            )

            load_students()

        else:

            messagebox.showerror(
                "Enrollment Failed",
                (
                    "Could not save the enrollment.\n\n"
                    "Check that the selected subjects match "
                    "the student's year level and semester, "
                    "and that the student is not already enrolled."
                ),
                parent=window
            )

    # ======================================
    # BUTTONS
    # ======================================

    button_frame = tk.Frame(
        main,
        bg=BG_COLOR
    )

    button_frame.pack(
        fill="x",
        pady=(10, 0)
    )

    tk.Button(
        button_frame,
        text="Load Students",
        width=15,
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg=TEXT_COLOR,
        relief="flat",
        cursor="hand2",
        command=load_students
    ).pack(side="left", padx=(0, 8))

    tk.Button(
        button_frame,
        text="Enroll Student",
        width=16,
        font=("Arial", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=enroll_student
    ).pack(side="left")

    tk.Button(
        button_frame,
        text="Close",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg=TEXT_COLOR,
        relief="flat",
        cursor="hand2",
        command=window.destroy
    ).pack(side="right")

    # ======================================
    # INITIAL SETTINGS
    # ======================================

    window.geometry("1050x800")

    if parent is None:
        window.mainloop()
