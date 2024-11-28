import tkinter as tk
from tkinter import ttk

from flappy.util import center_window


class LoadingBar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading Game......")

        self.root.geometry("400x150")
        center_window(self.root, 400, 150)
        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
        # Add a label
        self.message_label = tk.Label(self.root, text="Initializing.....")
        self.message_label.pack(pady=10)
        self.progress_bar["maximum"] = 100

    def __call__(self, value, message):
        self.progress_bar["value"] = value
        self.progress_bar.update()
        self.message_label.config(text=message)
        if value >= 100:
            self.message_label.config(text="Task Completed! Starting in 3 seconds...")
            self.root.after(3000, self.root.destroy)
