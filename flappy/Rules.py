import tkinter as tk

from Popup import Popup

RULES = """
1. Objective:
   - Control the pterodactyl to avoid as many pipes as possible and achieve 
     the highest score within 2 minutes.

2. Controls:
   - Tilt your head up to make the pterodactyl rise.
   - Tilt your head down to make the pterodactyl descend.
   - Keep neutral to maintain the current altitude.

3. Player Registration:
   - Before the game starts, each player must enter their details:
     - Player Type: Select one of the following:
       - Teacher
       - Parent
       - Student
     - Name: Enter your name.
     - For Students: Additional fields for Grade and Section are required.

4. Scoring:
   - Earn 1 point for every pipe successfully avoided.

5. Timer:
   - The game lasts exactly 2 minutes.
   - The game ends when the timer runs out or the pterodactyl collides with a 
     pipe.

6. Obstacles:
   - The only obstacles are pipes placed at varying heights.
   - Avoid crashing into the pipes to keep playing.

7. Difficulty Progression:
   - The game gets harder over time as pipes begin to emerge faster.
   - Each increase in pipe speed raises the stage level by 1.

8. Leaderboard:
   - After the game ends, the player's score is recorded in a leaderboard based 
     on their player type:
     - Teacher Leaderboard
     - Parent Leaderboard
     - Student Leaderboard
   - Players can compare their scores with others of the same type.

9. Game Over:
   - Colliding with a pipe ends the game immediately.
"""


def show_rules_popup(root):
    rules = RULES
    Popup(root, "Rules", rules)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    show_rules_popup(root)
