import tkinter as tk
from tkinter import messagebox
from backend.auth import login
from frontend.dashboard import show_dashboard
from frontend.window import setup_window


def show_login():

    window = tk.Tk()
    setup_window(window, "Enrollment System")

    login_frame = tk.Frame(window)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(
        login_frame,
        text="Student Enrollment System",
        font=("Arial", 18)
    )
    title_label.pack(pady=(0, 20))

    username_textbox = tk.Entry(login_frame)
    username_textbox.pack()

    password_textbox = tk.Entry(login_frame, show="*")
    password_textbox.pack()

    def attempt_login():

        username = username_textbox.get()
        password = password_textbox.get()

        if login(username, password):
            window.destroy()
            show_dashboard()
        else:
            messagebox.showerror(
            "Login Failed",
            "Invalid username or password.",
            parent=window
        )

    login_button = tk.Button(
        login_frame,
        text="Login",
        command=attempt_login
    )
    login_button.pack(pady=5)
    window.bind("<Return>", lambda event: attempt_login())

    window.mainloop()