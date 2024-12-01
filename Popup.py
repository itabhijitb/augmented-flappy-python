import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
from flappy.util import center_window
from flappy.constants import CONSOLE_BLUE

class Popup:
    def __init__(self, root, title, rules):
        self.root = root
        self.rules = rules
        self.title = title
        self.root.overrideredirect(True)  # Remove window title bar

        # Configure window dimensions based on display resolution
        monitor = get_monitors()[0]
        self.window_width = int(monitor.width // 1.5)
        self.window_height = int(monitor.height // 1.5)
        center_window(self.root, self.window_width, self.window_height)
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        # Calculate dynamic font size based on screen resolution
        self.base_font_size = self.window_width // 65
        self.font = ("Courier", self.base_font_size, "bold")  # Retro console style with monospaced font

        # Create UI elements
        self.create_widgets()


    def create_widgets(self):
        # Create ttk styles

        # Create a canvas to draw the rectangle
        canvas = tk.Canvas(self.root, bg=CONSOLE_BLUE, highlightthickness=0)
        canvas.place(x=0, y=0, width=self.window_width, height=self.window_height)

        # Draw a rectangle border
        rect_margin = 10  # Margin for the rectangle
        canvas.create_rectangle(
            rect_margin,
            rect_margin,
            self.window_width - rect_margin,
            self.window_height - rect_margin,
            outline="white",
            width=1,  # Thickness of the rectangle border
        )

        # "Game Rules" label positioned on the rectangle
        rules_label = tk.Label(
            self.root,
            text=f" {self.title} ",
            font=self.font,
            bg=CONSOLE_BLUE,  # Explicit background color for tk.Label
            fg="white",  # Explicit foreground color
        )
        rules_label.place(x=50, y=0)

        # Main Frame for content
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.place(x=20, y=30, width=self.window_width - 40, height=self.window_height - 100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Rules Content (Text Widget with Scrollbar)
        rules_text = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=self.font,
            bg=CONSOLE_BLUE,
            fg="white",
            relief="flat",
            highlightthickness=0,
            yscrollcommand=scrollbar.set,  # Link scrollbar to Text widget
        )
        rules_text.insert("1.0", self.rules)
        rules_text.configure(state="disabled")  # Make text read-only
        rules_text.grid(row=0, column=0, sticky="nsew")

        # Configure scrollbar to interact with the Text widget
        scrollbar.config(command=rules_text.yview)

        # Adjust grid weights to allow stretching
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # OK Button to close the popup
        ok_button = ttk.Button(
            self.root,
            text="OK",
            command=self.on_ok,
            style="TButton",
        )
        ok_button.place(x=self.window_width // 2 - 50, y=self.window_height - 75, width=100, height=50)

    def on_ok(self):
        # Close the popup
        self.root.destroy()