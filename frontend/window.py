import tkinter as tk
import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).resolve().parent / "settings.json"

def setup_window(window, title):
    window.title(title)

    # Load saved settings
    default_settings = {
        "window_width": 1000,
        "window_height": 800,
        "window_x": 100,
        "window_y": 100
    }

    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = {**default_settings, **json.load(file)}
    except (FileNotFoundError, json.JSONDecodeError):
        settings = default_settings.copy()

    width = settings["window_width"]
    height = settings["window_height"]
    x = settings["window_x"]
    y = settings["window_y"]

    # Set initial window size and position
    window.geometry(f"{width}x{height}+{x}+{y}")

    # Allow resizing
    window.resizable(True, True)

    # Save window settings when closing
    def save_window_settings():
        settings = {
            "window_width": window.winfo_width(),
            "window_height": window.winfo_height(),
            "window_x": window.winfo_x(),
            "window_y": window.winfo_y()
        }

        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)

        window.destroy()

    window.protocol("WM_DELETE_WINDOW", save_window_settings)


def create_search_box(parent, search_command=None, clear_command=None):
    search_box = tk.Frame(
        parent,
        bg="#FFFFFF",
        relief="solid",
        bd=1
    )

    search_entry = tk.Entry(
        search_box,
        font=("Arial", 10),
        width=25,
        relief="flat",
        bd=0
    )
    search_entry.pack(side="left", ipady=6, padx=(5, 0))

    clear_button = tk.Button(
        search_box,
        text="×",
        font=("Arial", 12),
        bg="#FFFFFF",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: clear_command() if clear_command else search_entry.delete(0, tk.END)
    )
    clear_button.pack(side="right", padx=(0, 4))

    if search_command:
        search_entry.bind(
            "<Return>",
            lambda event: search_command()
        )

    return search_box, search_entry