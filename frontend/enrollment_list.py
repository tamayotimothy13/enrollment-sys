
import tkinter as tk
from tkinter import ttk, messagebox
import re

from frontend.window import setup_window, create_search_box
from backend.enrollments import (
    get_all_enrollments,
    get_enrollment_details,
    get_available_subjects,
    update_enrollment_subjects,
    delete_enrollment
)


def show_enrollment_list(parent=None):
    window = tk.Toplevel(parent) if parent else tk.Tk()
    setup_window(window, "Enrollment List")

    window.configure(bg="#F3F6FC")

    main = tk.Frame(window, padx=15, pady=15, bg="#F3F6FC")
    main.pack(fill="both", expand=True)

    # =========================
    # TITLE AND SEARCH
    # =========================

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

    # =========================
    # ENROLLMENT TABLE
    # =========================

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

    # =========================
    # ENROLLED SUBJECTS TABLE
    # =========================

    tk.Label(
        main,
        text="Enrolled Subjects",
        font=("Arial", 13, "bold"),
        bg="#F3F6FC"
    ).pack(anchor="w", pady=(15, 5))

    subject_tree = ttk.Treeview(
        main,
        columns=("code", "name", "units", "year_level"),
        show="headings",
        height=6
    )

    subject_tree.heading("code", text="Subject Code")
    subject_tree.heading("name", text="Subject Name")
    subject_tree.heading("units", text="Units")
    subject_tree.heading("year_level", text="Year Level")

    subject_tree.column("code", width=120, anchor="center")
    subject_tree.column("name", width=300)
    subject_tree.column("units", width=80, anchor="center")
    subject_tree.column("year_level", width=120, anchor="center")

    subject_tree.pack(fill="both", expand=True)

    total_label = tk.Label(
        main,
        text="Total Units: 0",
        font=("Arial", 10, "bold"),
        bg="#F3F6FC"
    )

    total_label.pack(anchor="e", pady=5)

    # =========================
    # YEAR LEVEL FUNCTIONS
    # =========================

    def format_year_level(year_level):
        if year_level is None:
            return "N/A"

        year_level = str(year_level).strip()

        if year_level.endswith("Year"):
            return year_level

        try:
            number = int(year_level)

            suffix = (
                "st" if number == 1 else
                "nd" if number == 2 else
                "rd" if number == 3 else
                "th"
            )

            return f"{number}{suffix} Year"

        except ValueError:
            return year_level

    def get_year_number(year_level):
        """
        Converts different year level formats into integers.

        Examples:
        2          -> 2
        '2'        -> 2
        '2nd Year' -> 2
        'Second Year' -> 2
        """

        if year_level is None:
            return None

        value = str(year_level).strip().lower()

        word_numbers = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4
        }

        for word, number in word_numbers.items():
            if word in value:
                return number

        match = re.search(r"\d+", value)

        if match:
            return int(match.group())

        return None

    def clear_subject_display():
        for item in subject_tree.get_children():
            subject_tree.delete(item)

        total_label.config(text="Total Units: 0")

    # =========================
    # LOAD ENROLLMENTS
    # =========================

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
                    format_year_level(year_level),
                    academic_year,
                    semester
                )
            )

    # =========================
    # SEARCH ENROLLMENTS
    # =========================

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
                format_year_level(year_level),
                academic_year,
                semester
            )

            if query in " ".join(
                str(value or "") for value in values
            ).casefold():

                tree.insert("", "end", values=values)

        tree.selection_remove(tree.selection())
        clear_subject_display()

    def clear_search():
        search_entry.delete(0, tk.END)
        load_enrollments()
        clear_subject_display()

    clear_button = search_box.winfo_children()[1]
    clear_button.configure(command=clear_search)

    search_entry.bind(
        "<KeyRelease>",
        lambda event: search_enrollments()
    )

    # =========================
    # DISPLAY SELECTED SUBJECTS
    # =========================

    def show_selected_subjects(event=None):

        selected = tree.selection()
        clear_subject_display()

        if not selected:
            return

        enrollment_id = tree.item(
            selected[0], "values"
        )[0]

        details = get_enrollment_details(enrollment_id)

        total_units = 0

        for row in details:

            subject_id = row[5]
            subject_code = row[6]
            subject_name = row[7]
            units = row[8]
            subject_year_level = row[9]

            if subject_id is None:
                continue

            subject_tree.insert(
                "",
                "end",
                values=(
                    subject_code,
                    subject_name,
                    units,
                    format_year_level(subject_year_level)
                )
            )

            total_units += units or 0

        total_label.config(
            text=f"Total Units: {total_units}"
        )

    tree.bind(
        "<<TreeviewSelect>>",
        show_selected_subjects
    )

    # =========================
    # EDIT ENROLLED SUBJECTS
    # =========================

    def edit_selected_subjects():

        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an enrollment first.",
                parent=window
            )
            return

        values = tree.item(selected[0], "values")

        enrollment_id = values[0]

        details = get_enrollment_details(enrollment_id)

        if not details:
            messagebox.showerror(
                "Error",
                "Enrollment details could not be found.",
                parent=window
            )
            return

        student_id = details[0][1]
        semester = details[0][3]

        # Get student's current year level.
        selected_year_level = values[4]

        selected_year_number = get_year_number(
            selected_year_level
        )

        if selected_year_number is None:
            messagebox.showerror(
                "Error",
                "Could not determine the student's year level.",
                parent=window
            )
            return

        # =========================
        # CURRENT SUBJECTS
        # =========================

        current_subjects = {}

        for row in details:

            subject_id = row[5]

            if subject_id is None:
                continue

            current_subjects[int(subject_id)] = (
                subject_id,
                row[6],
                row[7],
                row[9],
                row[8]
            )

        try:

            # Get available subjects for the student's
            # course, current year level, and semester.
            available_subjects = get_available_subjects(
                student_id,
                semester
            )

            subject_map = {}

            for subject in available_subjects:

                subject_id = int(subject[0])

                subject_map[subject_id] = subject

            # Keep previously enrolled subjects visible,
            # even if they belong to previous year levels.
            for subject_id, subject in current_subjects.items():

                if subject_id not in subject_map:
                    subject_map[subject_id] = subject

            # =========================
            # AUTOMATIC SUBJECT SELECTION
            # =========================

            # Only automatically select subjects that
            # match the student's CURRENT year level.
            #
            # Previous year subjects remain visible
            # but will NOT be automatically selected.

            available_subject_ids = set()

            for subject in available_subjects:

                subject_id = int(subject[0])

                # Subject structure:
                # (subject_id, code, name, year_level, units)

                subject_year_level = subject[3]

                subject_year_number = get_year_number(
                    subject_year_level
                )

                if subject_year_number == selected_year_number:

                    available_subject_ids.add(subject_id)

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not load available subjects:\n{error}",
                parent=window
            )

            return

        # =========================
        # EDITOR WINDOW
        # =========================

        editor = tk.Toplevel(window)

        editor.title("Edit Enrolled Subjects")
        editor.configure(bg="#F3F6FC")
        editor.transient(window)
        editor.grab_set()

        editor.geometry("900x650")
        editor.resizable(True, True)

        editor_main = tk.Frame(
            editor,
            padx=15,
            pady=15,
            bg="#F3F6FC"
        )

        editor_main.pack(fill="both", expand=True)

        tk.Label(
            editor_main,
            text="Edit Enrolled Subjects",
            font=("Arial", 14, "bold"),
            bg="#F3F6FC"
        ).pack(anchor="w")

        # =========================
        # YEAR LEVEL INFORMATION
        # =========================

        year_frame = tk.Frame(
            editor_main,
            bg="#E2E8F0",
            padx=10,
            pady=8
        )

        year_frame.pack(fill="x", pady=(12, 8))

        tk.Label(
            year_frame,
            text="Student Year Level:",
            font=("Arial", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B"
        ).pack(side="left")

        tk.Label(
            year_frame,
            text=selected_year_level,
            font=("Arial", 10, "bold"),
            bg="#E2E8F0",
            fg="#2563EB"
        ).pack(side="left", padx=5)

        tk.Label(
            editor_main,
            text=(
                "All subjects are displayed for reference.\n"
                "Only subjects matching the student's current "
                "year level and semester are automatically selected.\n"
                "Previous-year subjects can still be selected manually.\n"
                "Use Ctrl or Shift to select multiple subjects."
            ),
            font=("Arial", 9),
            bg="#F3F6FC",
            fg="#64748B",
            wraplength=850,
            justify="left"
        ).pack(anchor="w", pady=(5, 12))

        # =========================
        # SUBJECT TABLE
        # =========================

        subject_frame = tk.Frame(editor_main)
        subject_frame.pack(fill="both", expand=True)

        edit_tree = ttk.Treeview(
            subject_frame,
            columns=("code", "name", "units", "year_level"),
            show="headings",
            selectmode="extended"
        )

        edit_tree.heading("code", text="Subject Code")
        edit_tree.heading("name", text="Subject Name")
        edit_tree.heading("units", text="Units")
        edit_tree.heading("year_level", text="Year Level")

        edit_tree.column("code", width=150, anchor="center")
        edit_tree.column("name", width=350)
        edit_tree.column("units", width=80, anchor="center")
        edit_tree.column("year_level", width=130, anchor="center")

        edit_scrollbar = ttk.Scrollbar(
            subject_frame,
            orient="vertical",
            command=edit_tree.yview
        )

        edit_tree.configure(
            yscrollcommand=edit_scrollbar.set
        )

        edit_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        edit_scrollbar.pack(
            side="right",
            fill="y"
        )

        # =========================
        # INSERT AND SELECT SUBJECTS
        # =========================

        for subject_id, subject in subject_map.items():

            subject_id = int(subject[0])

            subject_code = subject[1]
            subject_name = subject[2]
            subject_year_level = subject[3]
            units = subject[4]

            item = edit_tree.insert(
                "",
                "end",
                values=(
                    subject_code,
                    subject_name,
                    units,
                    format_year_level(subject_year_level)
                ),
                tags=(str(subject_id),)
            )

            # Automatically select only subjects
            # belonging to the student's current year.
            if subject_id in available_subject_ids:

                edit_tree.selection_add(item)

        # =========================
        # SAVE SUBJECT CHANGES
        # =========================

        def save_subject_changes():

            selected_items = edit_tree.selection()

            selected_subject_ids = []

            for item in selected_items:

                subject_id = int(
                    edit_tree.item(item, "tags")[0]
                )

                selected_subject_ids.append(subject_id)

            confirm = messagebox.askyesno(
                "Confirm Changes",
                "Save the updated list of enrolled subjects?",
                parent=editor
            )

            if not confirm:
                return

            try:

                success = update_enrollment_subjects(
                    enrollment_id,
                    selected_subject_ids
                )

                if success:

                    editor.destroy()

                    load_enrollments()

                    # Restore selected enrollment.
                    for item in tree.get_children():

                        item_values = tree.item(
                            item, "values"
                        )

                        if str(item_values[0]) == str(enrollment_id):

                            tree.selection_set(item)
                            tree.focus(item)
                            tree.see(item)

                            show_selected_subjects()

                            break

                    messagebox.showinfo(
                        "Success",
                        "Enrolled subjects updated successfully.",
                        parent=window
                    )

                else:

                    messagebox.showerror(
                        "Update Failed",
                        "The enrolled subjects could not be updated.",
                        parent=editor
                    )

            except Exception as error:

                messagebox.showerror(
                    "Update Failed",
                    f"An error occurred while updating subjects:\n{error}",
                    parent=editor
                )

        # =========================
        # EDITOR BUTTONS
        # =========================

        editor_buttons = tk.Frame(
            editor_main,
            bg="#F3F6FC"
        )

        editor_buttons.pack(
            fill="x",
            pady=(12, 0)
        )

        tk.Button(
            editor_buttons,
            text="Save Changes",
            width=15,
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=save_subject_changes
        ).pack(side="left")

        tk.Button(
            editor_buttons,
            text="Cancel",
            width=12,
            font=("Arial", 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            relief="flat",
            cursor="hand2",
            command=editor.destroy
        ).pack(side="right")

    # =========================
    # DELETE ENROLLMENT
    # =========================

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
                clear_subject_display()

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

    # =========================
    # MAIN BUTTONS
    # =========================

    button_frame = tk.Frame(
        main,
        bg="#F3F6FC"
    )

    button_frame.pack(
        fill="x",
        pady=(10, 0)
    )

    tk.Button(
        button_frame,
        text="Edit Subjects",
        width=14,
        font=("Arial", 10, "bold"),
        bg="#2563EB",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=edit_selected_subjects
    ).pack(side="left", padx=(0, 8))

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

    # =========================
    # INITIAL LOAD
    # =========================

    load_enrollments()

    if parent is None:
        window.mainloop()
