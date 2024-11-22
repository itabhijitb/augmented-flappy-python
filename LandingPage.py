import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from screeninfo import get_monitors
from UserForm import UserForm
from tkinter import messagebox
import pyglet
from Flappy import run_game


class LandingPage:
    def __init__(self, root, excel_file, logo_path, font_file):
        self.root = root
        self.root.configure(background='black')
        self.excel_file = excel_file  # Excel file with leaderboard data
        self.logo_path = logo_path  # Path to logo image
        pyglet.font.add_file(font_file)
        self.font_file = font_file  # Custom font file
        self.flappy_font = "JurassicPark"

        # Configure window dimensions based on display resolution
        monitor = get_monitors()[0]
        self.window_width = monitor.width
        self.window_height = monitor.height
        print(f"{self.window_width}x{self.window_height}")
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.title("Landing Page")
        self.root.resizable(True, True)

        self.leaderboard_data = self.load_leaderboard()

        # Create UI elements
        self.create_widgets()

    def load_leaderboard(self):
        """
        Load leaderboard data from an Excel file.
        Columns: Type, Name, Class, Score
        """
        try:
            df = pd.read_excel(self.excel_file, engine="openpyxl")
            df = df.sort_values("Score", ascending=False)  # Sort by score descending
            leaderboard_data = [
                f"{row['Type']} - {row['Name']} - {row['Class']} - {row['Score']}"
                for _, row in df.iterrows()
            ]
            return leaderboard_data
        except Exception as e:
            print(f"Error reading leaderboard file: {e}")
            return ["Error loading leaderboard data."]

    def create_widgets(self):
        # Logo
        logo_image = Image.open(self.logo_path)
        logo_aspect_ratio = logo_image.width / logo_image.height
        new_width = self.window_width // 3
        new_height = int(new_width / logo_aspect_ratio)
        logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.logo_canvas = tk.Canvas(self.root, width=self.window_width, height=new_height, bg="black", highlightthickness=0)
        self.logo_canvas.pack(pady=20)

        # Load and display the logo image while preserving its aspect ratio
        try:

            self.logo_image_tk = ImageTk.PhotoImage(logo_image)
            self.logo_canvas.create_image(self.window_width // 2, new_height // 2, image=self.logo_image_tk)
        except Exception as e:
            print(f"Error loading logo image: {e}")
            self.logo_canvas.create_text(self.window_width // 2, 100, text="Game Logo", font=(self.flappy_font, 20, "bold"))

        # Start Button
        self.start_button = tk.Button(
            self.root, text="START", command=self.start_game, font=(self.flappy_font, 30), fg='black', bg="#63F5FF", width=5
        )
        self.start_button.pack(pady=20)

        # Leaderboard Title
        leaderboard_label = tk.Label(self.root, text="Leaderboard", fg = 'white', bg="black", font=(self.flappy_font, 40, "bold"))
        leaderboard_label.pack(pady=10)

        # Scrollable Leaderboard
        self.leaderboard_frame = tk.Frame(self.root)
        self.leaderboard_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.leaderboard_frame, height=self.window_height // 3, width=self.window_width // 2)
        self.scrollbar = ttk.Scrollbar(
            self.leaderboard_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Populate leaderboard
        self.update_leaderboard()

    def update_leaderboard(self):
        """
        Populate the leaderboard with entries.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()  # Clear existing leaderboard entries

        for idx, entry in enumerate(self.leaderboard_data):
            score_label = tk.Label(
                self.scrollable_frame,
                text=f"{idx + 1}. {entry}",
                font=('Helvetica', 16),
                anchor="w",
            )
            score_label.pack(fill="x", pady=2)

    def update_leaderboard_file(self, user_data):
        """
        Append the user data to the leaderboard Excel file and ensure only the highest score
        for each user is retained.
        """
        try:
            # Read the existing file or create a new DataFrame if the file doesn't exist
            try:
                df = pd.read_excel(self.excel_file, engine="openpyxl")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["Type", "Name", "Class", "Score"])

            # Append the new user's data
            new_entry = {
                "Type": user_data["Role"],
                "Name": user_data["Name"],
                "Class": user_data.get("Class", ""),
                "Score": user_data["Score"],
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

            # Remove duplicates by keeping the highest score for each user
            df = df.sort_values("Score", ascending=False).drop_duplicates(subset=["Name"], keep="first")

            # Save back to the Excel file
            df.to_excel(self.excel_file, index=False, engine="openpyxl")
            print("Leaderboard updated successfully, duplicates removed.")
        except Exception as e:
            print(f"Error updating leaderboard file: {e}")


        except Exception as e:
            print(f"Error updating leaderboard file: {e}")

    def process_user_input(self, user_data):
        """
        Handle user input from the UserForm, run the game, and update the leaderboard.
        """

        # Hide the main window before starting the game
        self.root.withdraw()

        # Run the game
        try:
            score = run_game()  # Assume this returns the user's score
            user_data["Score"] = score
            self.update_leaderboard_file(user_data)
        finally:
            # Show the main window again after the game ends
            self.root.deiconify()

            # Refresh the leaderboard
            self.load_leaderboard()
            self.update_leaderboard()

    def start_game(self):
        """
        Placeholder for starting the game.
        """
        user_form_root = tk.Toplevel(self.root)
        UserForm(user_form_root, self.process_user_input)



if __name__ == "__main__":
    # Path to the Excel file
    excel_file_path = "res/leaderboard.xlsx"  # Replace with the path to your Excel file
    logo_image_path = "images/logo.png"  # Replace with the path to your logo file
    font_path = "res/JurassicPark.otf"
    root = tk.Tk()
    app = LandingPage(root, excel_file_path, logo_image_path, font_path)
    root.mainloop()
