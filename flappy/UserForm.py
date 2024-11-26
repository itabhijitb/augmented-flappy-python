import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from screeninfo import get_monitors
from flappy.util import center_window

class UserForm:
    def __init__(self, root, call_back):
        self.root = root
        self.call_back = call_back
        self.root.overrideredirect(True)  # Remove window title bar

        # Configure window dimensions based on display resolution
        monitor = get_monitors()[0]
        self.window_width = monitor.width // 3
        self.window_height = monitor.height // 2
        center_window(self.root, self.window_width, self.window_height)
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        # Calculate dynamic font size based on screen resolution
        self.base_font_size = self.window_width // 50
        self.font = ("Courier", self.base_font_size, "bold")  # Retro console style with monospaced font

        # Input Variables
        self.name_var = tk.StringVar()
        self.role_var = tk.StringVar(value="Teacher")
        self.class_var = tk.StringVar()
        self.section_var = tk.StringVar()

        # Create UI elements
        self.create_widgets()

        # Add drag functionality for the custom window
        self.add_drag_functionality()


    def create_widgets(self):
        # Create a canvas to draw the rectangle
        canvas = tk.Canvas(self.root, bg="#0015ac", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

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

        # "Player Details" label positioned on the rectangle
        player_label = tk.Label(
            canvas,
            text=" Player Details ",
            font=self.font,
            bg="#0015ac",
            fg="white",
        )
        player_label.place(relx=0.5, y=0, anchor="n")

        # Main Frame for content
        main_frame = tk.Frame(canvas, bg="#0015ac")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Name Input
        name_label = tk.Label(main_frame, text="Name:", font=self.font, fg="white", bg="#0015ac")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(
            main_frame,
            textvariable=self.name_var,
            font=self.font,
            width=25,
            bg="#47a3b0",
            fg="black",
            insertbackground="black",
            relief="flat",  # Remove border
            highlightthickness=0,  # Remove inner white border
        )
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Role Dropdown
        role_label = tk.Label(main_frame, text="Role:", font=self.font, fg="white", bg="#0015ac")
        role_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        role_dropdown = ttk.Combobox(
            main_frame,
            textvariable=self.role_var,
            values=["Teacher", "Parent", "Student"],
            state="readonly",
            font=self.font,
        )
        role_dropdown.bind("<<ComboboxSelected>>", self.on_role_change)
        role_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Student-specific fields (hidden by default)
        self.student_frame = tk.Frame(main_frame, bg="#0015ac")

        class_label = tk.Label(self.student_frame, text="Class:", font=self.font, fg="white", bg="#0015ac")
        class_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        class_dropdown = ttk.Combobox(
            self.student_frame,
            textvariable=self.class_var,
            values=["Nursery", "LKG", "UKG", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            state="readonly",
            font=self.font,
        )
        class_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        section_label = tk.Label(self.student_frame, text="Section:", font=self.font, fg="white", bg="#0015ac")
        section_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        section_dropdown = ttk.Combobox(
            self.student_frame,
            textvariable=self.section_var,
            values=["A", "B", "C", "D", "E"],
            state="readonly",
            font=self.font,
        )
        section_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Submit and Cancel Buttons
        button_frame = tk.Frame(main_frame, bg="#0015ac")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        submit_button = tk.Button(
            button_frame,
            text="Submit",
            command=self.on_submit,
            font=self.font,
            bg="black",
            fg="lightgreen",
            activebackground="lightgreen",
            activeforeground="black",
        )
        submit_button.pack(side=tk.LEFT, padx=10)

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel,
            font=self.font,
            bg="black",
            fg="red",
            activebackground="red",
            activeforeground="black",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)

    def on_role_change(self, event):
        # Show or hide student-specific fields based on role
        if self.role_var.get() == "Student":
            self.student_frame.grid(row=3, column=0, columnspan=2, pady=10)
        else:
            self.student_frame.grid_forget()

    def on_submit(self):
        # Validate inputs
        name = self.name_var.get().strip()
        role = self.role_var.get()
        class_name = self.class_var.get().strip()
        section = self.section_var.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Please enter your name.")
            return

        if role == "Student" and (not class_name or not section):
            messagebox.showerror("Input Error", "Please enter both Class and Section.")
            return

        # Display user data
        user_data = {"Name": name, "Role": role}
        if role == "Student":
            user_data["Class"] = class_name
            user_data["Section"] = section
        self.root.destroy()
        self.call_back(user_data)


    def on_cancel(self):
        # Close the application without submitting data
        self.root.destroy()

    def add_drag_functionality(self):
        # Enable dragging the custom window
        def start_drag(event):
            self.x_offset = event.x
            self.y_offset = event.y

        def do_drag(event):
            x = self.root.winfo_pointerx() - self.x_offset
            y = self.root.winfo_pointery() - self.y_offset
            self.root.geometry(f"+{x}+{y}")

        self.root.bind("<Button-1>", start_drag)
        self.root.bind("<B1-Motion>", do_drag)


def run_user_form():
    def display_user_data(user_data):
        messagebox.showinfo("User Data", f"Collected Data:\n{user_data}")

    root = tk.Tk()
    app = UserForm(root, display_user_data)
    root.mainloop()


if __name__ == "__main__":
    run_user_form()
