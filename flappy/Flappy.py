import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import pandas as pd
from typing import List, Optional, Dict, Any
from screeninfo import get_monitors
import pyglet

from flappy.MusicPlayer import MusicPlayer
from flappy.Rules import show_rules_popup
# Constants
from flappy.constants import (
    FONT_FAMILY,
    BACKGROUND_COLOR,
    TEXT_COLOR,
    EXCEL_FILE_PATH,
    LOGO_IMAGE_PATH,
    FONT_FILE_PATH,
    ICON,
    CONSOLE_BLUE, JURASSIC_PARK_THEME
)

# Game components
from flappy.GameEngine import run_game
from flappy.UserForm import UserForm
from flappy.credits import show_credits_popup


def _manage_leaderboard(user_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Manage leaderboard data by reading, updating, and returning leaderboard records."""
    try:
        # Read existing leaderboard data
        try:
            df: pd.DataFrame = pd.read_excel(
                Flappy.excel_file, engine="openpyxl", converters={"Class": str, "Section": str}
            )
            df.fillna("Not Applicable", inplace=True)
        except FileNotFoundError:
            print("Leaderboard file not found. Initializing a new leaderboard.")
            df = pd.DataFrame(columns=["Type", "Name", "Class", "Section", "Score"])

        # Update leaderboard with new user data
        if user_data:
            new_entry: Dict[str, Any] = {
                "Type": user_data["Role"],
                "Name": user_data["Name"],
                "Class": user_data.get("Class", "N/A"),
                "Section": user_data.get("Section", "N/A"),
                "Score": user_data["Score"],
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.sort_values("Score", ascending=False, inplace=True)
            df.drop_duplicates(subset=["Name", "Class", "Section"], keep="first", inplace=True)
            df.to_excel(Flappy.excel_file, index=False, engine="openpyxl")
            print("Leaderboard updated successfully.")

        # Convert leaderboard to a list of dictionaries
        return df.sort_values("Score", ascending=False).to_dict(orient="records")
    except Exception as e:
        print(f"Error managing leaderboard: {e}")
        return []


class Flappy:
    """Main class for the Flappy game."""
    excel_file: str = EXCEL_FILE_PATH
    logo_path: str = LOGO_IMAGE_PATH
    font_file: str = FONT_FILE_PATH
    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.music_player = MusicPlayer(JURASSIC_PARK_THEME)
        self.music_player.play()
        self.leaderboard_data: List[Dict[str, Any]] = []

        # Configure the root window
        self._configure_window()

        # Load leaderboard data
        self.leaderboard_data = _manage_leaderboard()

        # Create UI components
        self._create_widgets()

    def _configure_window(self) -> None:
        """Configure the root window's settings."""
        self.root.configure(background=BACKGROUND_COLOR)
        pyglet.font.add_file(Flappy.font_file)

        # Get monitor dimensions
        monitor = get_monitors()[0]
        self.window_width: int = monitor.width
        self.window_height: int = monitor.height

        # Set window geometry and attributes
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.title("Flappy")
        self.root.resizable(True, True)
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.theme_create("retro", parent="clam", settings={
            "TFrame": {
                "configure": {
                    "background": "black",
                }
            },
            "TLabel": {
                "configure": {
                    "background": "black",
                    "foreground": "green",
                    "font": ("Courier", 12),
                }
            },
            "TButton": {
                "configure": {
                    "background": "green",
                    "foreground": "white",
                    "font": ("Courier", 24),
                    "borderwidth": 1,
                    "anchor": "center",
                },
                "map": {
                    "background": [("active", "green")],
                    "foreground": [("active", "black")],
                }
            },
            "Treeview": {
                "configure": {
                    "background": "black",
                    "foreground": "green",
                    "fieldbackground": "black",
                    "font": ("Courier", 16),
                    "borderwidth": 0,
                },
                "map": {
                    "background": [("selected", "green")],
                    "foreground": [("selected", "black")],
                }
            },
            "Treeview.Heading": {
                "configure": {
                    "background": "green",
                    "foreground": "blue",
                    "font": ("Courier", 16, "bold"),
                    "borderwidth": 1,
                }
            },
            "TScrollbar": {
                "configure": {
                    "background": "black",
                    "troughcolor": "green",
                    "arrowcolor": "white",
                    "borderwidth": 1,
                },
                "map": {
                    "background": [("active", "green")],
                    "arrowcolor": [("active", "black")],
                }
            },
        })
        self.style.theme_use('retro')


    def _create_widgets(self) -> None:
        """Create and arrange UI components."""
        self.root.grid_columnconfigure(0, weight=1)

        self._add_logo()
        self._add_button()
        self._add_leaderboard_title()
        self._add_leaderboard()

    def _add_logo(self) -> None:
        """Add the game's logo to the UI with dynamic resizing."""

        def resize_logo(event: tk.Event) -> None:
            """Resize the logo based on the current window size."""
            # Avoid resizing if the window dimensions are too small
            if event.width < 200 or event.height < 200:
                return

            try:
                # Calculate new dimensions while maintaining aspect ratio
                logo_aspect_ratio: float = self.original_logo_image.width / self.original_logo_image.height
                new_width: int = event.width
                new_height: int = int(new_width / logo_aspect_ratio)

                # Resize the logo image
                resized_logo_image: Image.Image = self.original_logo_image.resize(
                    (new_width, new_height), Image.Resampling.LANCZOS
                )

                # Update the Canvas with the resized image
                self.logo_image_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(resized_logo_image)
                self.logo_canvas.configure(width=new_width, height=new_height)
                self.logo_canvas.create_image(
                    new_width // 2, new_height // 2, image=self.logo_image_tk
                )
            except Exception as e:
                print(f"Error resizing logo image: {e}")
        try:
            # Load the logo image
            self.original_logo_image: Image.Image = Image.open(Flappy.logo_path)

            # Create a Canvas to hold the image
            self.logo_canvas: tk.Canvas = tk.Canvas(
                self.root,
                bg=BACKGROUND_COLOR,
                highlightthickness=0
            )
            self.logo_canvas.grid(row=0, column=0, pady=20, sticky="nsew")

            # Bind resize event to dynamically resize the logo
            self.root.bind("<Configure>", resize_logo)
        except Exception as e:
            print(f"Error loading logo image: {e}")
            self._display_logo_placeholder()


    def _display_logo_placeholder(self) -> None:
        """Display a placeholder for the logo if loading fails."""
        self.logo_canvas: tk.Canvas = tk.Canvas(
            self.root, width=self.window_width, height=100, bg=BACKGROUND_COLOR, highlightthickness=0
        )
        self.logo_canvas.grid(row=0, column=0, pady=20)
        self.logo_canvas.create_text(
            self.window_width // 2,
            50,
            text="Game Logo",
            font=(FONT_FAMILY, 20, "bold"),
            fill=TEXT_COLOR,
        )

    def _add_button(self) -> None:
        """Add the START, RULES, and CREDITS buttons to the UI."""
        # Create a frame to hold the buttons
        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.grid(row=1, column=0, pady=20, padx=10)

        # Center the button frame within the root
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # START button
        self.start_button: ttk.Button = ttk.Button(
            button_frame,
            text="START",
            command=self._start_game,  # Replace with the correct callback
            width=10,
        )
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        # RULES button
        self.rules_button: ttk.Button = ttk.Button(
            button_frame,
            text="RULES",
            command=self._show_rules,  # Replace with the correct callback
            width=10,
        )
        self.rules_button.grid(row=0, column=1, padx=10, pady=10)

        # CREDITS button
        self.credits_button: ttk.Button = ttk.Button(
            button_frame,
            text="CREDITS",
            command=self._show_credits,  # Replace with the correct callback
            width=10,
        )
        self.credits_button.grid(row=0, column=2, padx=10, pady=10)

        # Configure columns in the button frame for even spacing
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

    def _add_leaderboard_title(self) -> None:
        """Add the leaderboard title to the UI."""
        leaderboard_label: tk.Label = tk.Label(
            self.root,
            text="Leaderboard",
            fg=CONSOLE_BLUE,
            bg="black",
            font=(FONT_FAMILY, 40, "bold"),
        )
        leaderboard_label.grid(row=2, column=0, pady=10)

    def _add_leaderboard(self) -> None:
        """Add a scrollable leaderboard to the UI."""
        columns = ("Type", "Name", "Class", "Section", "Score")

        # Frame for the leaderboard
        leaderboard_frame = ttk.Frame(self.root)
        leaderboard_frame.grid(row=3, column=0, padx=20, pady=20)

        self.leaderboard = ttk.Treeview(leaderboard_frame, columns=columns, show="headings")
        for column in columns:
            self.leaderboard.heading(column, text=column)
            self.leaderboard.column(column)

        # Scrollbar for the leaderboard
        v_scrollbar = ttk.Scrollbar(leaderboard_frame, orient="vertical", command=self.leaderboard.yview)
        self.leaderboard.configure(yscrollcommand=v_scrollbar.set)

        # Place Treeview and scrollbar
        self.leaderboard.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        leaderboard_frame.grid_rowconfigure(0, weight=1)
        leaderboard_frame.grid_columnconfigure(0, weight=1)

        # Load and display leaderboard data
        self._update_leaderboard()

    def _update_leaderboard(self) -> None:
        """Update the leaderboard with current data."""
        self.leaderboard.delete(*self.leaderboard.get_children())
        for entry in self.leaderboard_data:
            values = (
                entry["Type"],
                entry["Name"],
                entry.get("Class", ""),
                entry.get("Section", ""),
                entry["Score"],
            )
            self.leaderboard.insert("", tk.END, values=values)

    def _start_game(self) -> None:
        """Start the game by opening the user form."""
        root: tk.Toplevel = tk.Toplevel(self.root)
        UserForm(root, self._process_user_input)

    def _show_rules(self) -> None:
        """Start the game by opening the user form."""
        root: tk.Toplevel = tk.Toplevel(self.root)
        show_rules_popup(root)

    def _show_credits(self) -> None:
        """Start the game by opening the user form."""
        root: tk.Toplevel = tk.Toplevel(self.root)
        show_credits_popup(root)

    def _process_user_input(self, user_data: Dict[str, Any]) -> None:
        """Process user input and update the leaderboard."""
        self.root.withdraw()
        try:
            self.music_player.stop()
            score: int = run_game()
            self.music_player.play()
            user_data["Score"] = score
            self.leaderboard_data = _manage_leaderboard(user_data)
        finally:
            self.root.deiconify()
            self._update_leaderboard()


def main() -> None:
    """Main function to launch the Flappy game."""
    root: tk.Tk = tk.Tk()
    icon = tk.PhotoImage(file=ICON)
    root.iconphoto(False, icon)
    Flappy(root)
    root.mainloop()


if __name__ == "__main__":
    main()
