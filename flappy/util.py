import sys
import os
import cv2 as cv
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


def find_highest_resolution_camera(window_size):
    # Try opening cameras 0 to 9 (you can increase the range if you have more cameras)
    for camera_index in range(10):  # Adjust the range based on your system
        cap = cv.VideoCapture(camera_index)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, window_size[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, window_size[1])
        width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera Index {camera_index} has resolution {width} x {height}")
        if width == window_size[0] and height == window_size[1]:
            print("Selected")
            return camera_index
        else:
            print("Skipped")
    else:
        return -1