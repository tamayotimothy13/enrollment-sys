import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window
from backend.subjects import get_all_subjects

from backend.courses import (
    create_courses_table,
    add_course,
    get_all_courses,
    create_course_subjects_table,
    assign_subject_to_course,
    get_course_subjects,
    remove_subject_from_course
)

def show_courses(parent=None):
    if not create_courses_table():
        messagebox.showerror(
            "Database Error",
            "Could not prepare the courses table."
        )
        return

    window = tk.Toplevel(parent)
    setup_window(window, "Courses")

    main = tk.Frame(window, padx=20, pady=20)
    main.pack(fill="both", expand=True)

    tk.Label(
        main,
        text="Course Management",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", pady=(0, 15))

    # Course form
    form = tk.LabelFrame(
        main,
        text="Add New Course",
        padx=10,
        pady=10
    )
    form.pack(fill="x", pady=(0, 15))

    tk.Label(form, text="Course Code").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )

    code_entry = tk.Entry(form, width=25)
    code_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Course Name").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )

    name_entry = tk.Entry(form, width=35)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    # Course list
    tree = ttk.Treeview(
        main,
        columns=("course_id", "course_code", "course_name"),
        show="headings"
    )

    tree.heading("course_id", text="ID")
    tree.heading("course_code", text="Course Code")
    tree.heading("course_name", text="Course Name")

    tree.column("course_id", width=50, anchor="center")
    tree.column("course_code", width=130)
    tree.column("course_name", width=350)

    tree.pack(fill="both", expand=True)

    def load_courses():
        for item in tree.get_children():
            tree.delete(item)

        for course in get_all_courses():
            tree.insert("", "end", values=course)

    def save_course():
        code = code_entry.get().strip()
        name = name_entry.get().strip()

        if not code or not name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both the course code and course name.",
                parent=window
            )
            return

        if add_course(code, name):
            messagebox.showinfo(
                "Success",
                "Course added successfully.",
                parent=window
            )

            code_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            load_courses()

        else:
            messagebox.showerror(
                "Unable to Add Course",
                "The course code may already exist, or a database error occurred.",
                parent=window
            )
      
    def manage_subjects():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Course Selected",
                "Please select a course first.",
                parent=window
            )
            return

        values = tree.item(selected[0], "values")
        course_id = int(values[0])
        course_code = values[1]
        course_name = values[2]

        open_course_subjects(
            window, course_id, course_code, course_name
        )

    tk.Button(
        form,
        text="Add Course",
        command=save_course
    ).grid(row=2, column=1, sticky="e", padx=5, pady=8)
        
    tk.Button(
        main,
        text="Manage Subjects",
        command=manage_subjects
    ).pack(anchor="w", pady=(10, 0))

    ttk.Button(
        main,
        text="Close",
        command=window.destroy
    ).pack(anchor="e", pady=(10, 0))

    load_courses()

def open_course_subjects(
    parent, course_id, course_code, course_name
):
    if not create_course_subjects_table():
        messagebox.showerror(
            "Database Error",
            "Could not prepare course subjects.",
            parent=parent
        )
        return

    window = tk.Toplevel(parent)
    setup_window(
        window,
        f"Subjects - {course_code}"
    )

    main = ttk.Frame(window, padding=15)
    main.pack(fill="both", expand=True)

    ttk.Label(
        main,
        text=f"{course_code} - {course_name}",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", pady=(0, 10))

    form = ttk.LabelFrame(
        main, text="Assign Existing Subject", padding=10
    )
    form.pack(fill="x", pady=(0, 10))

    subjects = get_all_subjects()

    subject_lookup = {
        f"{subject[1]} - {subject[2]}": subject[0]
        for subject in subjects
    }

    subject_var = tk.StringVar()

    subject_combo = ttk.Combobox(
        form,
        textvariable=subject_var,
        values=list(subject_lookup.keys()),
        state="readonly",
        width=45
    )
    subject_combo.pack(
        side="left", padx=5, pady=5
    )

    year_var = tk.StringVar(value="1st Year")
    year_combo = ttk.Combobox(
        form,
        textvariable=year_var,
        values=(
            "1st Year", "2nd Year",
            "3rd Year", "4th Year"
        ),
        state="readonly",
        width=12
    )
    year_combo.pack(side="left", padx=5)

    semester_var = tk.StringVar(value="1st Semester")
    semester_combo = ttk.Combobox(
        form,
        textvariable=semester_var,
        values=("1st Semester", "2nd Semester"),
        state="readonly",
        width=15
    )
    semester_combo.pack(side="left", padx=5)

    columns = (
        "subject_id", "code", "name",
        "units", "year", "semester"
    )

    table = ttk.Treeview(
        main, columns=columns, show="headings"
    )

    headings = {
        "subject_id": "ID",
        "code": "Subject Code",
        "name": "Subject Name",
        "units": "Units",
        "year": "Year Level",
        "semester": "Semester"
    }

    for column, heading in headings.items():
        table.heading(column, text=heading)

    for column, width in (
        ("subject_id", 45),
        ("code", 100),
        ("name", 240),
        ("units", 60),
        ("year", 100),
        ("semester", 120)
    ):
        table.column(column, width=width)

    table.pack(fill="both", expand=True, pady=10)

    def load_assignments():
        for item in table.get_children():
            table.delete(item)

        for subject in get_course_subjects(course_id):
            table.insert("", "end", values=subject)

    def assign_subject():
        selected_subject = subject_var.get()

        if not selected_subject:
            messagebox.showwarning(
                "Missing Subject",
                "Please select a subject.",
                parent=window
            )
            return

        subject_id = subject_lookup[selected_subject]

        success = assign_subject_to_course(
            course_id,
            subject_id,
            year_var.get(),
            semester_var.get()
        )

        if success:
            messagebox.showinfo(
                "Success",
                "Subject assigned to course.",
                parent=window
            )
            load_assignments()
        else:
            messagebox.showerror(
                "Assignment Failed",
                "The subject may already be assigned "
                "to this course, or a database error occurred.",
                parent=window
            )

    def remove_assignment():
        selected = table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Select an assigned subject to remove.",
                parent=window
            )
            return

        values = table.item(selected[0], "values")
        subject_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirm Removal",
            "Remove this subject from the course? "
            "The subject will remain in the catalog.",
            parent=window
        )

        if confirm:
            if remove_subject_from_course(
                course_id, subject_id
            ):
                load_assignments()
            else:
                messagebox.showerror(
                    "Error",
                    "Could not remove the assignment.",
                    parent=window
                )

    ttk.Button(
        form,
        text="Assign Subject",
        command=assign_subject
    ).pack(side="left", padx=5)

    ttk.Button(
        main,
        text="Remove Selected Assignment",
        command=remove_assignment
    ).pack(anchor="w")

    ttk.Button(
        main,
        text="Close",
        command=window.destroy
    ).pack(anchor="e", pady=(10, 0))
    
    load_assignments()