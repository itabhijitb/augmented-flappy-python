import sys
import os
# Use this to resolve the path for bundled resources
def resource_path(relative_path):
    """Get the absolute path to the resource."""
    try:
        # PyInstaller creates a temp folder and stores files in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Fallback for running without PyInstaller
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)