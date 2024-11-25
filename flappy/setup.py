from cx_Freeze import setup, Executable
import os
# Define additional files to include
include_files = [
    ("flappy/audio/", "audio"),
    ("flappy/images/", "images"),
    ("flappy/mediapipe/modules/face_landmark/face_landmark_front_cpu.binarypb", "mediapipe/modules/face_landmark/face_landmark_front_cpu.binarypb"),
    ("flappy/res/JurassicPark.otf", "res/JurassicPark.otf"),
    ("flappy/res/leaderboard.xlsx", "res/leaderboard.xlsx")
]

# Specify the packages required
build_exe_options = {
    "packages": ["PIL", "pygame", "mediapipe", "pyglet", "pandas", "screeninfo", "openpyxl", "cv2"],
    "include_files": include_files,
}

# Main script and metadata
setup(
    name="Flappy",
    version="1.0",
    description="Flappy Bird Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("flappy/Flappy.py", base=None)],
)
