from flappy.util import resource_path
# Font settings
FONT_FAMILY = "JurassicPark"
FONT_SIZE_LARGE = 30
FONT_SIZE_MEDIUM = 20

# Color scheme
BACKGROUND_COLOR = "black"
BUTTON_COLOR = "#63F5FF"
TEXT_COLOR = "white"

# File paths
EXCEL_FILE_PATH = resource_path("res/leaderboard.xlsx")
LOGO_IMAGE_PATH = resource_path("images/logo.png")
SCHOOL_IMAGE_PATH = resource_path("images/NHPS.png")
FONT_FILE_PATH = resource_path("res/JurassicPark.otf")
SPRITE_PIPES = resource_path("images/pipe.png")
SPRITE_BIRD = resource_path("images/pterodactyl.gif")
SPRITE_LOGO = resource_path("images/logo.png")
ICON = resource_path("images/pterodactyl.png")


# Default messages
LEADERBOARD_LOAD_ERROR = ["Error loading leaderboard data."]
LEADERBOARD_FILE_NOT_FOUND = ["Leaderboard file not found."]
ERROR_NAME_REQUIRED = "Please enter your name."
ERROR_CLASS_SECTION_REQUIRED = "Please enter both Class and Section."

# Dropdown Options
ROLE_OPTIONS = ["Teacher", "Student"]


# Game Configuration
PIPE_DISTANCE_BETWEEN = 500
PIPE_SPACE_BETWEEN = 500
PIPE_SPAWN_INTERVAL = 40
STAGE_INTERVAL = 10  # Time in seconds before stage increases


# Bird Configuration
BIRD_WIDTH = 50
BIRD_HEIGHT = 37


# Face Tracking Configuration
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Colors
 # Black


