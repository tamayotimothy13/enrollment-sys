import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from frontend.window import setup_window
from backend.students import (get_all_students, 
                              delete_student, 
                              get_student_by_id,
                              update_student)


def show_masterlist():

    window = tk.Tk()
    setup_window(window, "Student Masterlist")

    # Colors
    BG_COLOR = "#F3F6FC"
    PRIMARY_COLOR = "#2563EB"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#1E293B"
    MUTED_COLOR = "#64748B"
    RED_COLOR = "#DC2626"

    window.configure(bg=BG_COLOR)

    # =========================
    # HEADER
    # =========================321321
 
    # =========================
    # MAIN CONTENT
    # =========================
    content = tk.Frame(window, bg=BG_COLOR)
    content.pack(fill="both", expand=True, padx=25, pady=20)

    # Search section
    search_frame = tk.Frame(content, bg=BG_COLOR)
    search_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        search_frame,
        text="Students Masterlist",
        font=("Arial", 13, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(side="left")

    # Container for the search entry and clear button
    search_box = tk.Frame(
        search_frame,
        relief="solid",
        bd=1
    )
    search_box.pack(side="right", padx=8)

    # Search entry
    search_entry = tk.Entry(
        search_box,
        font=("Arial", 10),
        width=25,
        relief="flat",
        bd=0
    )
    search_entry.pack(side="left", ipady=6)
    search_entry.bind("<KeyRelease>", lambda event: search_students())

    # Small X button
    clear_button = tk.Button(
        search_box,
        text="×",
        font=("Arial", 12),
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: clear_search()
    )
    clear_button.pack(side="right", padx=(0, 4))
    # =========================
    # TABLE CARD
    # =========================
    table_card = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    table_card.pack(fill="both", expand=True)

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
    tree.column("course", width=130)
    tree.column("year_level", width=90, anchor="center")
    tree.column("email", width=180)

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )
    scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

    def load_students():
        for item in tree.get_children():
            tree.delete(item)

        students = get_all_students()

        if students:
            empty_label.place_forget()

            for student in students:
                tree.insert("", "end", values=student)
        else:
            empty_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )
    # =========================
    # EMPTY STATE
    # =========================
    # No student records are loaded yet.
    # The message is shown while the table is empty.
    empty_label = tk.Label(
        table_card,
        text="No students found.",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=MUTED_COLOR
    )
    empty_label.place(relx=0.5, rely=0.5, anchor="center")

    load_students()


    def handle_delete():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a student to delete.",
                parent=window
            )
            return

        # Get the selected row's values
        values = tree.item(selected[0], "values")
        student_id = values[0]
        student_name = f"{values[1]} {values[2]}"

        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {student_name}?\n\n"
            f"Student ID: {student_id}",
            parent=window
        )

        if not confirm:
            return

        if delete_student(student_id):
            load_students()

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


    def view_student_details():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a student first.",
                parent=window
            )
            return

        # Get the Student ID from the selected row
        values = tree.item(selected[0], "values")
        student_id = values[0]

        # Retrieve the complete student record
        student = get_student_by_id(student_id)

        if student is None:
            messagebox.showerror(
                "Error",
                "Could not retrieve student details.",
                parent=window
            )
            return

        # Create a separate details window
        details_window = tk.Toplevel(window)
        setup_window(details_window, "Student Details")
        details_window.configure(bg=BG_COLOR)

        # Main container
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

        # Window heading
        tk.Label(
            details_frame,
            text="Student Details",
            font=("Arial", 18, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            details_frame,
            text=f"Student ID: {student['student_id']}",
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=PRIMARY_COLOR
        ).pack(anchor="w", pady=(0, 15))

        # Fields to display
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
            ("Course", "course"),
        ]

        # Display each field
        for label_text, field_name in fields:
            value = student[field_name]

            if field_name == "year_level" and value:
                value = f"{value}{'st' if value == 1 else 'nd' if value == 2 else 'rd' if value == 3 else 'th'} Year"

            if value is None or value == "":
                value = "Not provided"

            row = tk.Frame(details_frame, bg=WHITE)
            row.pack(fill="x", pady=3)

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
            ).pack(side="left", fill="x", expand=True)

        # Bottom buttons
        button_frame = tk.Frame(details_frame, bg=WHITE)
        button_frame.pack(fill="x", pady=(20, 0))

        tk.Button(
            button_frame,
            text="Edit Student",
            width=14,
            font=("Arial", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            command=lambda: edit_student(student_id)
        ).pack(side="left", ipady=5)

        tk.Button(
            button_frame,
            text="Close",
            width=10,
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=details_window.destroy
        ).pack(side="right", ipady=5)

    def search_students():
        query = search_entry.get().strip()

        # Ignore the placeholder text
        if query.lower() == "search students...":
            query = ""

        students = get_all_students()

        # Filter records using the search query
        filtered_students = [
            student for student in students
            if query.casefold() in " ".join(
                str(value or "") for value in student
            ).casefold()
        ]

        # Clear the current table
        for item in tree.get_children():
            tree.delete(item)

        # Display matching records
        if filtered_students:
            empty_label.place_forget()

            for student in filtered_students:
                tree.insert("", "end", values=student)
        else:
            empty_label.config(text="No students found.")
            empty_label.place(
                relx=0.5,
                rely=0.5,
                anchor="center"
            )

    def clear_search():
        search_entry.delete(0, tk.END)
        load_students()

    def edit_student(student_id):
        student = get_student_by_id(student_id)

        if student is None:
            messagebox.showerror(
                "Error",
                "Could not retrieve student details.",
                parent=window
            )
            return

        edit_window = tk.Toplevel(window)
        setup_window(edit_window, "Edit Student")
        edit_window.configure(bg=BG_COLOR)

        form = tk.Frame(edit_window, bg=WHITE, padx=20, pady=20)
        form.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            form,
            text=f"Edit Student — {student_id}",
            font=("Arial", 16, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Text fields: label, database key
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

        for row, (label_text, key) in enumerate(field_names, start=1):
            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10),
                bg=WHITE,
                fg=TEXT_COLOR
            ).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=5)

            entry = tk.Entry(form, font=("Arial", 10), width=35)
            entry.grid(row=row, column=1, sticky="ew", pady=5)
            entry.insert(0, student[key] or "")
            entries[key] = entry

        # Dropdown fields
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
            "course": (
                "Course",
                (
                    "BS Computer Science",
                    "BS Information Technology",
                    "BS Information Systems"
                )
            ),
        }

        dropdowns = {}

        for offset, (key, (label_text, options)) in enumerate(
            dropdown_options.items()
        ):
            row = next_row + offset

            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            ).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=5)

            combo = ttk.Combobox(
                form,
                values=options,
                state="readonly",
                width=32
            )
            combo.grid(row=row, column=1, sticky="ew", pady=5)

            if key == "year_level":
                level = int(student[key])
                combo.set(f"{level}{'st' if level == 1 else 'nd' if level == 2 else 'rd' if level == 3 else 'th'} Year")
            else:
                combo.set(student[key] or "")

            dropdowns[key] = combo

        form.columnconfigure(1, weight=1)

        def save_changes():
            data = {
                key: entry.get().strip()
                for key, entry in entries.items()
            }

            admission_type = dropdowns["admission_type"].get()
            year_level = dropdowns["year_level"].get()
            course = dropdowns["course"].get()

            # Basic required-field validation
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

            if not admission_type or not year_level or not course:
                messagebox.showwarning(
                    "Missing Information",
                    "Please select the admission type, year level, and course.",
                    parent=edit_window
                )
                return

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

            # Close the old details window if it still exists.
            for child in window.winfo_children():
                if isinstance(child, tk.Toplevel) and child.title() == "Student Details":
                    child.destroy()

            load_students()

        button_frame = tk.Frame(form, bg=WHITE)
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
        ).pack(side="left", padx=(0, 8), ipady=5)

        tk.Button(
            button_frame,
            text="Cancel",
            relief="flat",
            cursor="hand2",
            command=edit_window.destroy
        ).pack(side="left", ipady=5)

    # =========================
    # ACTION BUTTONS
    # =========================
    actions = tk.Frame(content, bg=BG_COLOR)
    actions.pack(fill="x", pady=(15, 0))

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
    ).pack(side="left", padx=(0, 8), ipady=5)

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
    ).pack(side="left", padx=8, ipady=5)

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
    ).pack(side="right", ipady=5)

    window.mainloop()


if __name__ == "__main__":
    show_masterlist()