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
    "packages": ["PIL", "pygame", "mediapipe", "pyglet", "pandas", "screeninfo", "openpyxl", "cv2", "playsound"],
    "include_files": include_files,
}

# Define the MSI-specific options
bdist_msi_options = {
    "add_to_path": True,  # Optionally, add the executable to PATH
    "initial_target_dir": r"[LocalAppDataFolder]\Flappy",  # Default installation directory
    "upgrade_code": "{e66802b1-e824-4998-9bb8-a08b5c7c049b}",  # Replace with a GUID for upgrade support
    "data": {
        "Shortcut": [
            (
                "DesktopShortcut",  # Shortcut identifier
                "DesktopFolder",  # Directory for the shortcut (e.g., DesktopFolder, StartMenuFolder)
                "Flappy Bird",  # Shortcut name
                "TARGETDIR",  # The base directory for the target executable
                "[TARGETDIR]Flappy.exe",  # Target executable path
                None,  # Arguments (if any)
                None,  # Description
                None,  # Icon (optional)
                None,  # Icon index
                None,  # Working directory
            ),
            (
                "StartMenuShortcut",  # Shortcut identifier
                "StartMenuFolder",  # Directory for the shortcut (Start Menu folder)
                "Flappy Bird",  # Shortcut name
                "TARGETDIR",  # The base directory for the target executable
                "[TARGETDIR]Flappy.exe",  # Target executable path
                None,  # Arguments (if any)
                None,  # Description
                None,  # Icon (optional)
                None,  # Icon index
                None,  # Working directory
            ),
        ]
    },
    "install_icon": "flappy/images/pterodactyl.ico",
    "summary_data": {
        "author": "Aditya Bhattacharjee",
        "comments": "Augmented Reality Flappy Pterodactyl",
        "keywords": "Application, Pterodactyl, Flappy, Augmented Reality"
    },
    "target_name": "FlappyPterodactyl.msi",
    "compressed": True,
    "optimize": 2
}
# Main script and metadata
setup(
    name="Flappy Pterodactyl",
    version="1.0",
    description="Flappy Pterodactyl Game",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=[Executable("flappy/Flappy.py", base=None)],
)
