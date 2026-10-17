import tkinter as tk
from tkinter import ttk, messagebox
from frontend.window import setup_window

from backend.subjects import (
    create_subjects_table,
    add_subject,
    get_all_subjects,
    update_subject,
    delete_subject
)

def show_subjects(parent=None):
    selected_subject_id = tk.StringVar(value="")

    if not create_subjects_table():
        messagebox.showerror(
            "Database Error",
            "Could not prepare the subjects table."
        )
        return

    if parent:
        window = tk.Toplevel(parent)
    else:
        window = tk.Tk()

    setup_window(window, "Subject Management")

    # Subject details
    form = ttk.LabelFrame(
        window,
        text="Subject Information",
        padding=15
    )
    form.pack(fill="x", padx=15, pady=15)

    ttk.Label(form, text="Subject Code").grid(
        row=0, column=0, sticky="w", padx=5, pady=5
    )
    code_entry = ttk.Entry(form, width=25)
    code_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form, text="Subject Name").grid(
        row=0, column=2, sticky="w", padx=5, pady=5
    )
    name_entry = ttk.Entry(form, width=30)
    name_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(form, text="Units").grid(
        row=1, column=0, sticky="w", padx=5, pady=5
    )
    units_entry = ttk.Entry(form, width=25)
    units_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form, text="Year Level").grid(
        row=1, column=2, sticky="w", padx=5, pady=5
    )
    year_var = tk.StringVar(value="1st Year")
    year_combo = ttk.Combobox(
        form,
        textvariable=year_var,
        values=(
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ),
        state="readonly",
        width=27
    )
    year_combo.grid(row=1, column=3, padx=5, pady=5)

    ttk.Label(form, text="Semester").grid(
        row=2, column=0, sticky="w", padx=5, pady=5
    )
    semester_var = tk.StringVar(value="1st Semester")
    semester_combo = ttk.Combobox(
        form,
        textvariable=semester_var,
        values=("1st Semester",),
        state="readonly",
        width=22
    )
    semester_combo.grid(row=2, column=1, padx=5, pady=5)

    # Table of saved subjects
    table_frame = ttk.LabelFrame(
        window,
        text="Subject List",
        padding=10
    )
    table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    columns = (
        "id",
        "code",
        "name",
        "units",
        "year",
        "semester"
    )

    subject_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "id": "ID",
        "code": "Subject Code",
        "name": "Subject Name",
        "units": "Units",
        "year": "Year Level",
        "semester": "Semester"
    }

    for column, heading in headings.items():
        subject_table.heading(column, text=heading)

    subject_table.column("id", width=45, anchor="center")
    subject_table.column("code", width=110)
    subject_table.column("name", width=250)
    subject_table.column("units", width=60, anchor="center")
    subject_table.column("year", width=100)
    subject_table.column("semester", width=120)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=subject_table.yview
    )
    subject_table.configure(yscrollcommand=scrollbar.set)

    subject_table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def load_subjects():
        for item in subject_table.get_children():
            subject_table.delete(item)

        for subject in get_all_subjects():
            subject_table.insert("", "end", values=subject)

    
    def edit_subject():
        selected = subject_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a subject to edit.",
                parent=window
            )
            return

        values = subject_table.item(selected[0], "values")

        code_entry.delete(0, tk.END)
        code_entry.insert(0, values[1])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[2])

        units_entry.delete(0, tk.END)
        units_entry.insert(0, values[3])

        year_var.set(values[4])
        semester_var.set(values[5])

        selected_subject_id.set(values[0])
        save_button.config(text="Save Changes")


    def clear_form():
        code_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        units_entry.delete(0, tk.END)

        year_var.set("1st Year")
        semester_var.set("1st Semester")

        selected_subject_id.set("")
        save_button.config(text="Add Subject")

        code_entry.focus_set()
    
    def remove_subject():
        selected = subject_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a subject to delete.",
                parent=window
            )
            return

        values = subject_table.item(selected[0], "values")
        subject_id = values[0]
        subject_code = values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete subject {subject_code}?",
            parent=window
        )

        if not confirm:
            return

        if delete_subject(subject_id):
            messagebox.showinfo(
                "Success",
                "Subject deleted successfully.",
                parent=window
            )
            load_subjects()
            selected_subject_id.set("")
            save_button.config(text="Add Subject")

            code_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            units_entry.delete(0, tk.END)
            year_var.set("1st Year")
            semester_var.set("1st Semester")
        else:
            messagebox.showerror(
                "Error",
                "Could not delete the subject.",
                parent=window
            )

    def save_subject():
        code = code_entry.get().strip()
        name = name_entry.get().strip()
        units_text = units_entry.get().strip()

        if not code or not name or not units_text:
            messagebox.showwarning(
                "Missing Information",
                "Please complete all subject fields.",
                parent=window
            )
            return

        try:
            units = int(units_text)
            if units <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Units",
                "Units must be a positive whole number.",
                parent=window
            )
            return

        if selected_subject_id.get():
            success = update_subject(
                int(selected_subject_id.get()),
                code,
                name,
                units,
                year_var.get(),
                semester_var.get()
            )
        else:
            success = add_subject(
                code,
                name,
                units,
                year_var.get(),
                semester_var.get()
            )

        
        if success:
            action = (
                "updated"
                if selected_subject_id.get()
                else "added"
            )

            messagebox.showinfo(
                "Success",
                f"Subject {action} successfully.",
                parent=window
            )

            # Clear the form
            code_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            units_entry.delete(0, tk.END)

            # Exit edit mode
            selected_subject_id.set("")
            save_button.config(text="Add Subject")

            # Refresh the table
            load_subjects()
            code_entry.focus_set()

        else:
            messagebox.showerror(
                "Unable to Add Subject",
                "The subject could not be saved. Check the console "
                "for database errors or verify that the subject "
                "code is not already in use.",
                parent=window
            )

    button_frame = ttk.Frame(form)
    button_frame.grid(
        row=2, column=2, columnspan=2,
        sticky="e", padx=5, pady=5
    )

    save_button = ttk.Button(
        button_frame,
        text="Add Subject",
        command=save_subject
    )
    save_button.pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Edit Selected",
        command=edit_subject
    ).pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Delete Selected",
        command=remove_subject
    ).pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Refresh",
        command=load_subjects
    ).pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Close",
        command=window.destroy
    ).pack(side="left", padx=5)

    ttk.Button(
        button_frame,
        text="Cancel Edit / Clear",
        command=clear_form
    ).pack(side="left", padx=5)

    load_subjects()
    code_entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_subjects(root)
    root.mainloop()