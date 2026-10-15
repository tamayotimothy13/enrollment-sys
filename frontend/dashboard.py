import tkinter as tk
from frontend.student import show_students
from frontend.window import setup_window
from frontend.masterlist import show_masterlist

def show_dashboard():

    window = tk.Tk()
    setup_window(window, "Enrollment System")

    title = tk.Label(
        window,
        text="Enrollment System",
        font=("Arial", 20)
    )
    title.pack(pady=30)

    students_button = tk.Button(
        window,
        text="Add Student(s)",
        width=20,
        command=show_students
    )
    students_button.pack(pady=5)

    subjects_button = tk.Button(
        window,
        text="Enroll Student(s)",
        width=20
    )
    subjects_button.pack(pady=5)

    masterlist_button = tk.Button(
        window,
        text="View Masterlist",
        width=20,
        command=show_masterlist
    )
    masterlist_button.pack(pady=5)

    courses_button = tk.Button(
            window,
            text="Courses",
            width=20
    )
    courses_button.pack(pady=5)

    logout_button = tk.Button(
        window,
        text="Logout",
        width=20,
        command=window.destroy
    )
    logout_button.pack(pady=20)

    window.mainloop()