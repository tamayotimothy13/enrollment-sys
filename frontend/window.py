import tkinter as tk

def setup_window(window, title):
    window.title(title)

    width = 800
    height = 450

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate center position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set size and position
    window.geometry(f"{width}x{height}+{x}+{y}")

    # Prevent resizing
    window.resizable(False, False)