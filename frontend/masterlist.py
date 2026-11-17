
import tkinter as tk
from tkinter import ttk, messagebox

from frontend.window import setup_window, create_search_box

from backend.students import (
    get_all_students,
    delete_student,
    get_student_by_id,
    update_student
)

from backend.courses import get_all_courses


def show_masterlist(parent=None, on_change=None):

    # =========================
    # CREATE WINDOW
    # =========================

    if parent:
        window = tk.Toplevel(parent)
    else:
        window = tk.Tk()

    setup_window(window, "Student Masterlist")

    # =========================
    # COLORS
    # =========================

    BG_COLOR = "#F3F6FC"
    PRIMARY_COLOR = "#2563EB"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#1E293B"
    MUTED_COLOR = "#64748B"
    RED_COLOR = "#DC2626"

    window.configure(bg=BG_COLOR)

    # =========================
    # COURSE FUNCTIONS
    # =========================

    def get_registered_courses():
        return get_all_courses()

    def find_registered_course(course_value):

        if not course_value:
            return None

        for course in get_registered_courses():

            course_id, course_code, course_name = course

            # Students store the course name as TEXT.
            if str(course_value).strip().casefold() in (
                str(course_name).strip().casefold(),
                str(course_code).strip().casefold()
            ):
                return course

        return None

    def get_course_display(course_value):

        course = find_registered_course(course_value)

        if course is None:
            return ""

        return course[2]

    def format_year_level(value):

        if value is None or value == "":
            return ""

        value = str(value).strip()

        if value.endswith("Year"):
            return value

        try:
            level = int(value)

            suffix = (
                "st" if level == 1 else
                "nd" if level == 2 else
                "rd" if level == 3 else
                "th"
            )

            return f"{level}{suffix} Year"

        except ValueError:
            return value

    # =========================
    # MAIN CONTENT
    # =========================

    content = tk.Frame(
        window,
        bg=BG_COLOR
    )

    content.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    # =========================
    # SEARCH SECTION
    # =========================

    search_frame = tk.Frame(
        content,
        bg=BG_COLOR
    )

    search_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        search_frame,
        text="Students Masterlist",
        font=("Arial", 13, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(side="left")

    search_box, search_entry = create_search_box(search_frame)

    search_box.pack(
        side="right",
        padx=8
    )

    # =========================
    # TABLE CARD
    # =========================

    table_card = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    table_card.pack(
        fill="both",
        expand=True
    )

    columns = (
        "student_id",
        "first_name",
        "last_name",
        "course",
        "year_level",
        "email"
    )

    tree = ttk.Treeview(
        table_card,
        columns=columns,
        show="headings",
        height=10
    )

    tree.heading("student_id", text="Student ID")
    tree.heading("first_name", text="First Name")
    tree.heading("last_name", text="Last Name")
    tree.heading("course", text="Course")
    tree.heading("year_level", text="Year Level")
    tree.heading("email", text="Email")

    tree.column("student_id", width=100, anchor="center")
    tree.column("first_name", width=120)
    tree.column("last_name", width=120)
    tree.column("course", width=180)
    tree.column("year_level", width=90, anchor="center")
    tree.column("email", width=180)

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10,
        padx=(0, 10)
    )

    # =========================
    # EMPTY STATE
    # =========================

    empty_label = tk.Label(
        table_card,
        text="No students found.",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=MUTED_COLOR
    )

    empty_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # =========================
    # SEARCH STUDENTS
    # =========================

    def search_students():

        query = search_entry.get().strip()

        students = get_all_students()

        filtered_students = [
            student for student in students
            if query.casefold() in " ".join(
                str(value or "") for value in student
            ).casefold()
        ]

        for item in tree.get_children():
            tree.delete(item)

        if filtered_students:

            empty_label.place_forget()

            for student in filtered_students:

                display_values = list(student)

                # Hide deleted or unregistered courses.
                display_values[3] = get_course_display(
                    display_values[3]
                )

                tree.insert(
                    "",
                    "end",
                    values=display_values
                )

        else:

            empty_label.config(
                text="No students found."
            )

            empty_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

    # =========================
    # CLEAR SEARCH
    # =========================

    def clear_search():

        search_entry.delete(0, tk.END)
        search_students()

    search_entry.bind(
        "<KeyRelease>",
        lambda event: search_students()
    )

    clear_button = search_box.winfo_children()[1]

    clear_button.configure(
        command=clear_search
    )

    # =========================
    # DELETE STUDENT
    # =========================

    def handle_delete():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a student to delete.",
                parent=window
            )

            return

        values = tree.item(
            selected[0],
            "values"
        )

        student_id = values[0]

        student_name = f"{values[1]} {values[2]}"

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {student_name}?\n\n"
            f"Student ID: {student_id}",
            parent=window
        )

        if not confirm:
            return

        if delete_student(student_id):

            search_students()

            if on_change:
                on_change()

            messagebox.showinfo(
                "Success",
                "Student successfully deleted.",
                parent=window
            )

        else:

            messagebox.showerror(
                "Error",
                "Could not delete the student. Check the terminal for details.",
                parent=window
            )

    # =========================
    # VIEW STUDENT DETAILS
    # =========================

    def view_student_details():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a student first.",
                parent=window
            )

            return

        values = tree.item(
            selected[0],
            "values"
        )

        student_id = values[0]

        student = get_student_by_id(student_id)

        if student is None:

            messagebox.showerror(
                "Error",
                "Could not retrieve student details.",
                parent=window
            )

            return

        details_window = tk.Toplevel(window)

        setup_window(
            details_window,
            "Student Details"
        )

        details_window.configure(
            bg=BG_COLOR
        )

        details_frame = tk.Frame(
            details_window,
            bg=WHITE,
            padx=25,
            pady=20
        )

        details_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        tk.Label(
            details_frame,
            text="Student Details",
            font=("Arial", 18, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        tk.Label(
            details_frame,
            text=f"Student ID: {student['student_id']}",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=PRIMARY_COLOR
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        fields = [
            ("First Name", "first_name"),
            ("Middle Name / Initial", "middle_name"),
            ("Last Name", "last_name"),
            ("Prefix", "prefix"),
            ("Birthday", "birthday"),
            ("Birth Place", "birth_place"),
            ("Address", "address"),
            ("Email", "email"),
            ("Contact Number", "contact_number"),
            ("Emergency Contact", "emergency_contact_number"),
            ("Admission Type", "admission_type"),
            ("Year Level", "year_level"),
        ]

        # Check if the student's course still exists.
        registered_course = find_registered_course(
            student.get("course")
        )

        # Only display Course if it exists.
        if registered_course is not None:
            fields.append(
                ("Course", "course")
            )

        for label_text, field_name in fields:

            value = student.get(field_name)

            if field_name == "year_level":
                value = format_year_level(value)

            elif field_name == "course":
                value = registered_course[2]

            if value is None or value == "":
                value = "Not provided"

            row = tk.Frame(
                details_frame,
                bg=WHITE
            )

            row.pack(
                fill="x",
                pady=3
            )

            tk.Label(
                row,
                text=f"{label_text}:",
                font=("Arial", 10, "bold"),
                bg=WHITE,
                fg=TEXT_COLOR,
                width=22,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 10),
                bg=WHITE,
                fg=MUTED_COLOR,
                anchor="w",
                justify="left",
                wraplength=350
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        # =========================
        # BOTTOM BUTTONS
        # =========================

        button_frame = tk.Frame(
            details_frame,
            bg=WHITE
        )

        button_frame.pack(
            fill="x",
            pady=(20, 0)
        )

        tk.Button(
            button_frame,
            text="Edit Student",
            width=14,
            font=("Arial", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            command=lambda: edit_student(
                student_id,
                details_window
            )
        ).pack(
            side="left",
            ipady=5
        )

        tk.Button(
            button_frame,
            text="Close",
            width=10,
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=details_window.destroy
        ).pack(
            side="right",
            ipady=5
        )

    # =========================
    # EDIT STUDENT
    # =========================

    def edit_student(student_id, details_window=None):

        student = get_student_by_id(student_id)

        if student is None:

            messagebox.showerror(
                "Error",
                "Could not retrieve student details.",
                parent=window
            )

            return

        edit_window = tk.Toplevel(window)

        setup_window(
            edit_window,
            "Edit Student"
        )

        edit_window.configure(
            bg=BG_COLOR
        )

        form = tk.Frame(
            edit_window,
            bg=WHITE,
            padx=20,
            pady=20
        )

        form.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            form,
            text=f"Edit Student — {student_id}",
            font=("Arial", 16, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 15)
        )

        # =========================
        # TEXT FIELDS
        # =========================

        field_names = [
            ("First Name", "first_name"),
            ("Middle Name / Initial", "middle_name"),
            ("Last Name", "last_name"),
            ("Prefix", "prefix"),
            ("Address", "address"),
            ("Birthday (YYYY-MM-DD)", "birthday"),
            ("Birth Place", "birth_place"),
            ("Contact Number", "contact_number"),
            ("Emergency Contact", "emergency_contact_number"),
            ("Email", "email"),
        ]

        entries = {}

        for row, (label_text, key) in enumerate(
            field_names,
            start=1
        ):

            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10),
                bg=WHITE,
                fg=TEXT_COLOR
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 12),
                pady=5
            )

            entry = tk.Entry(
                form,
                font=("Arial", 10),
                width=35
            )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                pady=5
            )

            entry.insert(
                0,
                student.get(key) or ""
            )

            entries[key] = entry

        # =========================
        # DROPDOWN FIELDS
        # =========================

        next_row = len(field_names) + 1

        dropdown_options = {
            "admission_type": (
                "Admission Type",
                ("New Student", "Returning Student")
            ),

            "year_level": (
                "Year Level",
                ("1st Year", "2nd Year", "3rd Year", "4th Year")
            ),
        }

        # Retrieve courses from the database.
        registered_courses = get_registered_courses()

        course_names = tuple(
            course[2] for course in registered_courses
        )

        # Add Course dropdown only when courses exist.
        if registered_courses:

            dropdown_options["course"] = (
                "Course",
                course_names
            )

        dropdowns = {}

        for offset, (key, (label_text, options)) in enumerate(
            dropdown_options.items()
        ):

            row = next_row + offset

            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10),
                bg=WHITE,
                fg=TEXT_COLOR
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 12),
                pady=5
            )

            combo = ttk.Combobox(
                form,
                values=options,
                state="readonly",
                width=32
            )

            combo.grid(
                row=row,
                column=1,
                sticky="ew",
                pady=5
            )

            if key == "year_level":

                combo.set(
                    format_year_level(
                        student.get(key)
                    )
                )

            elif key == "course":

                current_course = find_registered_course(
                    student.get("course")
                )

                if current_course:
                    combo.set(current_course[2])

            else:

                combo.set(
                    student.get(key) or ""
                )

            dropdowns[key] = combo

        form.columnconfigure(
            1,
            weight=1
        )

        # =========================
        # SAVE CHANGES
        # =========================

        def save_changes():

            data = {
                key: entry.get().strip()
                for key, entry in entries.items()
            }

            admission_type = dropdowns["admission_type"].get()
            year_level = dropdowns["year_level"].get()

            # Preserve old course value if no courses exist.
            if registered_courses:

                course = dropdowns["course"].get()

            else:

                course = student.get("course") or ""

            # Required field validation.
            required_fields = [
                "first_name",
                "last_name",
                "address",
                "birthday",
                "contact_number",
                "email",
            ]

            for key in required_fields:

                if not data[key]:

                    messagebox.showwarning(
                        "Missing Information",
                        f"Please enter {key.replace('_', ' ')}.",
                        parent=edit_window
                    )

                    return

            if not admission_type or not year_level:

                messagebox.showwarning(
                    "Missing Information",
                    "Please select the admission type and year level.",
                    parent=edit_window
                )

                return

            # Require course selection when courses exist.
            if registered_courses and not course:

                messagebox.showwarning(
                    "Missing Information",
                    "Please select a course.",
                    parent=edit_window
                )

                return

            # Update student database.
            success = update_student(
                student_id=student_id,
                first_name=data["first_name"],
                middle_name=data["middle_name"],
                last_name=data["last_name"],
                prefix=data["prefix"],
                address=data["address"],
                birthday=data["birthday"],
                birth_place=data["birth_place"],
                contact_number=data["contact_number"],
                emergency_contact_number=data["emergency_contact_number"],
                email=data["email"],
                admission_type=admission_type,
                year_level=year_level,
                course=course
            )

            if not success:

                messagebox.showerror(
                    "Update Failed",
                    "The student could not be updated. Check the terminal for details.",
                    parent=edit_window
                )

                return

            messagebox.showinfo(
                "Success",
                "Student information updated successfully.",
                parent=edit_window
            )

            edit_window.destroy()

            if details_window and details_window.winfo_exists():
                details_window.destroy()

            # Refresh masterlist.
            search_students()

            # Refresh dashboard.
            if on_change:
                on_change()

        # =========================
        # EDIT BUTTONS
        # =========================

        button_frame = tk.Frame(
            form,
            bg=WHITE
        )

        button_frame.grid(
            row=next_row + len(dropdown_options),
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 0)
        )

        tk.Button(
            button_frame,
            text="Save Changes",
            bg=PRIMARY_COLOR,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            command=save_changes
        ).pack(
            side="left",
            padx=(0, 8),
            ipady=5
        )

        tk.Button(
            button_frame,
            text="Cancel",
            relief="flat",
            cursor="hand2",
            command=edit_window.destroy
        ).pack(
            side="left",
            ipady=5
        )

    # =========================
    # ACTION BUTTONS
    # =========================

    actions = tk.Frame(
        content,
        bg=BG_COLOR
    )

    actions.pack(
        fill="x",
        pady=(15, 0)
    )

    tk.Button(
        actions,
        text="View Details",
        width=14,
        font=("Arial", 10, "bold"),
        bg="#0F766E",
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=view_student_details
    ).pack(
        side="left",
        padx=(0, 8),
        ipady=5
    )

    tk.Button(
        actions,
        text="Delete Record",
        width=14,
        font=("Arial", 10, "bold"),
        bg=RED_COLOR,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        command=handle_delete
    ).pack(
        side="left",
        padx=8,
        ipady=5
    )

    tk.Button(
        actions,
        text="Back",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg=TEXT_COLOR,
        relief="flat",
        cursor="hand2",
        command=window.destroy
    ).pack(
        side="right",
        ipady=5
    )

    # =========================
    # INITIAL LOAD
    # =========================

    search_students()


if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    show_masterlist(root)

    root.mainloop()
