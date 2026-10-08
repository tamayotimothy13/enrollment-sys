import tkinter as tk
from backend.auth import login
from frontend.dashboard import show_dashboard


def show_login():

    window = tk.Tk()
    window.title("Enrollment System")
    window.geometry("400x300")

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