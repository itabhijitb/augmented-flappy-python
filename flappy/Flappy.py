import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from typing import List, Optional, Dict, Any
from screeninfo import get_monitors
from UserForm import UserForm
from constants import (
    FONT_FAMILY,
    BACKGROUND_COLOR,
    BUTTON_COLOR,
    TEXT_COLOR,
    EXCEL_FILE_PATH,
    LOGO_IMAGE_PATH,
    SCHOOL_IMAGE_PATH,
    FONT_FILE_PATH,
)
import pyglet
from GameEngine import run_game

class Flappy:
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.excel_file: str = EXCEL_FILE_PATH
        self.logo_path: str = LOGO_IMAGE_PATH
        self.font_file: str = FONT_FILE_PATH
        self.leaderboard_data: List[str] = []

        # Configure main window
        self.root.configure(background=BACKGROUND_COLOR)
        pyglet.font.add_file(self.font_file)

        # Configure window dimensions based on primary monitor resolution
        monitor = get_monitors()[0]
        self.window_width: int = monitor.width
        self.window_height: int = monitor.height
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.title("Flappy")
        self.root.resizable(True, True)

        # Load leaderboard data
        self.leaderboard_data = self.manage_leaderboard()

        # Create UI elements
        self.create_widgets()

    def manage_leaderboard(self, user_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Manage the leaderboard by reading, updating, and returning leaderboard data.
        """
        try:
            # Load existing leaderboard data or initialize an empty DataFrame
            try:
                df: pd.DataFrame = pd.read_excel(
                    self.excel_file, engine="openpyxl", converters={"Class": str, "Section": str}
                )
                df = df.fillna("Not Applicable")
            except FileNotFoundError:
                print("Leaderboard file not found. Creating a new one.")
                df = pd.DataFrame(columns=["Type", "Name", "Class", "Section", "Score"])

            if user_data:
                # Add new entry and remove duplicates
                new_entry: Dict[str, Any] = {
                    "Type": user_data["Role"],
                    "Name": user_data["Name"],
                    "Class": user_data.get("Class", "N/A"),
                    "Section": user_data.get("Section", "N/A"),
                    "Score": user_data["Score"],
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                df = df.sort_values("Score", ascending=False).drop_duplicates(
                    subset=["Name", "Class", "Section"], keep="first"
                )
                df.to_excel(self.excel_file, index=False, engine="openpyxl")
                print("Leaderboard updated successfully.")

            # Return leaderboard data as a list of dictionaries for display
            leaderboard_data: List[Dict[str, str]] = df.sort_values("Score", ascending=False).to_dict(orient="records")
            return leaderboard_data

        except Exception as e:
            print(f"Error managing leaderboard: {e}")
            return []

    def create_widgets(self) -> None:
        self.add_logo()

        # Add START button
        self.start_button: tk.Button = tk.Button(
            self.root,
            text="START",
            command=self.start_game,
            font=(FONT_FAMILY, 30),
            fg="black",
            bg=BUTTON_COLOR,
            width=5,
        )
        self.start_button.pack(pady=20)
        # Add leaderboard title
        leaderboard_label: tk.Label = tk.Label(
            self.root,
            text="Leaderboard",
            fg="white",
            bg=BACKGROUND_COLOR,
            font=(FONT_FAMILY, 40, "bold"),
        )
        leaderboard_label.pack(pady=10)

        self.add_leaderboard()

    def add_logo(self) -> None:
        """Add and display the logo image."""
        try:
            logo_image: Image.Image = Image.open(self.logo_path)
            logo_aspect_ratio: float = logo_image.width / logo_image.height
            new_width: int = self.window_width
            new_height: int = int(new_width / logo_aspect_ratio)
            logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            self.logo_canvas: tk.Canvas = tk.Canvas(
                self.root,
                width=self.window_width,
                height=new_height,
                bg=BACKGROUND_COLOR,
                highlightthickness=0,
            )
            self.logo_canvas.pack(pady=20)

            self.logo_image_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(logo_image)
            self.logo_canvas.create_image(
                self.window_width // 2,
                new_height // 2,
                image=self.logo_image_tk,
            )

        except Exception as e:
            print(f"Error loading logo image: {e}")
            self.logo_canvas = tk.Canvas(self.root, width=self.window_width, height=100, bg=BACKGROUND_COLOR, highlightthickness=0)
            self.logo_canvas.pack(pady=20)
            self.logo_canvas.create_text(
                self.window_width // 2,
                50,
                text="Game Logo",
                font=(FONT_FAMILY, 20, "bold"),
                fill=TEXT_COLOR,
            )

    def add_leaderboard(self) -> None:
        """
        Add a scrollable leaderboard to the UI.
        """
        self.leaderboard_frame = tk.Frame(self.root)
        self.leaderboard_frame.pack(pady=10)

        self.canvas = tk.Canvas(
            self.leaderboard_frame,
            height=self.window_height // 3,
            width=self.window_width // 2,
        )
        self.scrollbar = ttk.Scrollbar(
            self.leaderboard_frame,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Load and update leaderboard data
        self.leaderboard_data = self.manage_leaderboard()
        self.update_leaderboard()

    def update_leaderboard(self) -> None:
        """
        Update the leaderboard display in a grid format.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Define column headers
        headers = ["Rank", "Type", "Name".center(120), "Class", "Section", "Score".center(10)]
        for col, header in enumerate(headers):
            header_label = tk.Label(
                self.scrollable_frame,
                text=header,
                font=("Helvetica", 14, "bold"),
                bg="#f0f0f0",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            header_label.grid(row=0, column=col, sticky="nsew")

        # Populate leaderboard rows
        for idx, entry in enumerate(self.leaderboard_data):
            rank_label = tk.Label(
                self.scrollable_frame,
                text=f"{idx + 1}",
                font=("Helvetica", 12),
                bg="#ffffff",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            rank_label.grid(row=idx + 1, column=0, sticky="nsew")

            type_label = tk.Label(
                self.scrollable_frame,
                text=entry.get("Type", ""),
                font=("Helvetica", 12),
                bg="#ffffff",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            type_label.grid(row=idx + 1, column=1, sticky="nsew")

            name_label = tk.Label(
                self.scrollable_frame,
                text=entry.get("Name", ""),
                font=("Helvetica", 12),
                bg="#ffffff",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            name_label.grid(row=idx + 1, column=2, sticky="nsew")

            class_label = tk.Label(
                self.scrollable_frame,
                text=entry.get("Class", ""),
                font=("Helvetica", 12),
                bg="#ffffff",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            class_label.grid(row=idx + 1, column=3, sticky="nsew")

            section_label = tk.Label(
                self.scrollable_frame,
                text=entry.get("Section", ""),
                font=("Helvetica", 12),
                bg="#ffffff",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            section_label.grid(row=idx + 1, column=4, sticky="nsew")

            score_label = tk.Label(
                self.scrollable_frame,
                text=entry.get("Score", ""),
                font=("Helvetica", 12),
                bg="#ffffff",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=5,
            )
            score_label.grid(row=idx + 1, column=5, sticky="nsew")

    def start_game(self) -> None:
        user_form_root: tk.Toplevel = tk.Toplevel(self.root)
        UserForm(user_form_root, self.process_user_input)

    def process_user_input(self, user_data: Dict[str, Any]) -> None:
        self.root.withdraw()
        try:
            score: int = run_game()
            user_data["Score"] = score
            self.leaderboard_data = self.manage_leaderboard(user_data)
        finally:
            self.root.deiconify()
            self.update_leaderboard()
def main() -> None:

    root: tk.Tk = tk.Tk()
    icon = tk.PhotoImage(file='images/pterodactyl.png')
    root.iconphoto(False, icon)
    Flappy(root)
    root.mainloop()


if __name__ == "__main__":
    main()