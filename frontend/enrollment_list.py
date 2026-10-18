import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window, create_search_box
from backend.enrollments import (
    get_all_enrollments,
    get_enrollment_details,
    delete_enrollment
)


def show_enrollment_list(parent=None):
    window = tk.Toplevel(parent) if parent else tk.Tk()
    setup_window(window, "Enrollment List")

    window.configure(bg="#F3F6FC")

    main = tk.Frame(window, padx=15, pady=15, bg="#F3F6FC")
    main.pack(fill="both", expand=True)
    
    # Enrollment Records title and search
    title_frame = tk.Frame(main, bg="#F3F6FC")
    title_frame.pack(fill="x", pady=(0, 10))

    tk.Label(
        title_frame,
        text="Enrollment Records",
        font=("Arial", 13, "bold"),
        bg="#F3F6FC"
    ).pack(side="left")

    search_box, search_entry = create_search_box(title_frame)
    search_box.pack(side="right", padx=8)

    # Enrollment table
    table_frame = tk.Frame(main)
    table_frame.pack(fill="both", expand=True)

    columns = (
        "enrollment_id",
        "student_id",
        "student_name",
        "course",
        "year_level",
        "academic_year",
        "semester"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    headings = {
        "enrollment_id": "Enrollment ID",
        "student_id": "Student ID",
        "student_name": "Student Name",
        "course": "Course",
        "year_level": "Year",
        "academic_year": "Academic Year",
        "semester": "Semester"
    }

    for column, heading in headings.items():
        tree.heading(column, text=heading)
        tree.column(column, width=120, anchor="center")

    tree.column("student_name", width=170)
    tree.column("course", width=200)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Selected enrollment's subjects
    tk.Label(
        main,
        text="Enrolled Subjects",
        font=("Arial", 13, "bold"), 
        bg="#F3F6FC"
    ).pack(anchor="w", pady=(15, 5))

    subject_tree = ttk.Treeview(
        main,
        columns=("code", "name", "units"),
        show="headings",
        height=6
    )

    subject_tree.heading("code", text="Subject Code")
    subject_tree.heading("name", text="Subject Name")
    subject_tree.heading("units", text="Units")

    subject_tree.column("code", width=120, anchor="center")
    subject_tree.column("name", width=350)
    subject_tree.column("units", width=80, anchor="center")

    subject_tree.pack(fill="both", expand=True)

    total_label = tk.Label(
        main,
        text="Total Units: 0",
        font=("Arial", 10, "bold"), 
        bg="#F3F6FC"
    )
    total_label.pack(anchor="e", pady=5)

    def load_enrollments():
        for item in tree.get_children():
            tree.delete(item)

        for enrollment in get_all_enrollments():
            (
                enrollment_id,
                student_id,
                first_name,
                last_name,
                course,
                year_level,
                academic_year,
                semester,
                enrollment_date
            ) = enrollment

            tree.insert(
                "",
                "end",
                values=(
                    enrollment_id,
                    student_id,
                    f"{first_name} {last_name}",
                    course,
                    f"{year_level}{'st' if year_level == 1 else 'nd' if year_level == 2 else 'rd' if year_level == 3 else 'th'} Year",
                    academic_year,
                    semester
                )
            )

    
    def search_enrollments():
        query = search_entry.get().strip().casefold()

        for item in tree.get_children():
            tree.delete(item)

        for enrollment in get_all_enrollments():
            (
                enrollment_id,
                student_id,
                first_name,
                last_name,
                course,
                year_level,
                academic_year,
                semester,
                enrollment_date
            ) = enrollment

            values = (
                enrollment_id,
                student_id,
                f"{first_name} {last_name}",
                course,
                f"{year_level}{'st' if year_level == 1 else 'nd' if year_level == 2 else 'rd' if year_level == 3 else 'th'} Year",
                academic_year,
                semester
            )

            if query in " ".join(
                str(value or "") for value in values
            ).casefold():
                tree.insert("", "end", values=values)
                
        tree.selection_remove(tree.selection())

        for item in subject_tree.get_children():
            subject_tree.delete(item)

        total_label.config(text="Total Units: 0")


    def clear_search():
        search_entry.delete(0, tk.END)
        load_enrollments()

    clear_button = search_box.winfo_children()[1]
    clear_button.configure(command=clear_search)

    search_entry.bind(
        "<KeyRelease>",
        lambda event: search_enrollments()
    )

    def show_selected_subjects(event=None):
        selected = tree.selection()

        for item in subject_tree.get_children():
            subject_tree.delete(item)

        total_units = 0

        if not selected:
            total_label.config(text="Total Units: 0")
            return

        enrollment_id = tree.item(
            selected[0], "values"
        )[0]

        details = get_enrollment_details(enrollment_id)

        for row in details:
            subject_id = row[5]
            subject_code = row[6]
            subject_name = row[7]
            units = row[8]

            if subject_id is None:
                continue

            subject_tree.insert(
                "",
                "end",
                values=(subject_code, subject_name, units)
            )

            total_units += units

        total_label.config(
            text=f"Total Units: {total_units}"
        )
    tree.bind("<<TreeviewSelect>>", show_selected_subjects)

    def delete_selected_enrollment():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an enrollment to delete.",
                parent=window
            )
            return

        values = tree.item(selected[0], "values")
        enrollment_id = values[0]
        student_name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete the enrollment for {student_name}?\n\n"
            "This action cannot be undone.",
            parent=window
        )

        if not confirm:
            return

        try:
            success = delete_enrollment(enrollment_id)

            if success:
                load_enrollments()

                for item in subject_tree.get_children():
                    subject_tree.delete(item)

                total_label.config(text="Total Units: 0")

                messagebox.showinfo(
                    "Success",
                    "Enrollment deleted successfully.",
                    parent=window
                )
            else:
                messagebox.showerror(
                    "Deletion Failed",
                    "The enrollment could not be deleted. "
                    "It may no longer exist, or a database error occurred.",
                    parent=window
                )

        except Exception as error:
            messagebox.showerror(
                "Deletion Failed",
                f"An unexpected error occurred:\n{error}",
                parent=window
            )

    button_frame = tk.Frame(main, bg="#F3F6FC")
    button_frame.pack(fill="x", pady=(10, 0))

    tk.Button(
        button_frame,
        text="Delete Enrollment",
        width=16,
        font=("Arial", 10, "bold"),
        bg="#DC2626",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=delete_selected_enrollment
    ).pack(side="left")

    tk.Button(
        button_frame,
        text="Close",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg="#1E293B",
        relief="flat",
        cursor="hand2",
        command=window.destroy
    ).pack(side="right")

    load_enrollments()

    if parent is None:
        window.mainloop()