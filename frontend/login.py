import tkinter as tk
from backend.auth import login
from frontend.dashboard import show_dashboard
from frontend.window import setup_window


def show_login():

    window = tk.Tk()
    setup_window(window, "Login")

    username_textbox = tk.Entry(window)
    username_textbox.pack()

    password_textbox = tk.Entry(window, show="*")
    password_textbox.pack()

    def attempt_login():

        username = username_textbox.get()
        password = password_textbox.get()

        if login(username, password):
            window.destroy()
            show_dashboard()
        else:
            print("Invalid username or password.")

    login_button = tk.Button(
        window,
        text="Login",
        command=attempt_login
    )
    login_button.pack()

    window.mainloop()