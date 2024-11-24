import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from screeninfo import get_monitors

JURASSIC_PARK_FONT = "JurassicPark"
class UserForm:
    def __init__(self, root, call_back):
        self.root = root
        self.call_back = call_back
        self.root.title("User Form")
        # Configure window dimensions based on display resolution
        monitor = get_monitors()[0]
        self.window_width = monitor.width // 4
        self.window_height = monitor.height // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        # Input Variables
        self.name_var = tk.StringVar()
        self.role_var = tk.StringVar(value="Teacher")
        self.class_var = tk.StringVar()
        self.section_var = tk.StringVar()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Name Input

        name_label = tk.Label(self.root, text="Name", font=(JURASSIC_PARK_FONT, 30))
        name_label.pack(pady=10)
        name_entry = tk.Entry(self.root, textvariable=self.name_var, font=(JURASSIC_PARK_FONT, 30), width=10)
        name_entry.pack()

        # Role Dropdown
        role_label = tk.Label(self.root, text="Role", font=(JURASSIC_PARK_FONT, 30))
        role_label.pack(pady=10)
        role_dropdown = ttk.Combobox(
            self.root, textvariable=self.role_var, values=["Teacher", "Parent", "Student"], state="readonly", font=(JURASSIC_PARK_FONT, 30), width=2
        )
        role_dropdown.bind("<<ComboboxSelected>>", self.on_role_change)
        role_dropdown.pack()

        # Student-specific fields (hidden by default)
        self.student_frame = tk.Frame(self.root)

        class_label = tk.Label(self.student_frame, text="Class", font=(JURASSIC_PARK_FONT, 30))
        class_label.grid(row=0, column=0, padx=5, pady=5)
        class_entry = tk.Entry(self.student_frame, textvariable=self.class_var, font=(JURASSIC_PARK_FONT, 30), width=10)
        class_entry.grid(row=0, column=1, padx=5, pady=5)

        section_label = tk.Label(self.student_frame, text="Section", font=(JURASSIC_PARK_FONT, 30))
        section_label.grid(row=1, column=0, padx=5, pady=5)
        section_entry = tk.Entry(self.student_frame, textvariable=self.section_var, font=(JURASSIC_PARK_FONT, 30), width=10)
        section_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit, font=(JURASSIC_PARK_FONT, 30), bg="#63F5FF")
        self.submit_button.pack(pady=20)

    def on_role_change(self, event):
        # Show or hide student-specific fields based on role
        if self.role_var.get() == "Student":
            self.student_frame.pack(pady=10)
            self.submit_button.pack_forget()
            self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit, font=(JURASSIC_PARK_FONT, 30),
                                           bg="#63F5FF")
            self.submit_button.pack(pady=20)

        else:
            self.student_frame.pack_forget()

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
        self.call_back(user_data)
        self.root.destroy()