import mediapipe as mp
import flappy.face_mesh as face_mesh
import cv2 as cv
from flappy.util import resource_path
from constants import FRONT_CPU_BINARYPB
from util import find_highest_resolution_camera

class FaceTracker:
    def __init__(self, window_size):
        mediapipe_resource_path = resource_path(FRONT_CPU_BINARYPB)
        self.face_mesh = face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            binary_graph_path=mediapipe_resource_path
        )
        self.video_capture = cv.VideoCapture(find_highest_resolution_camera(window_size))

    def get_face_position(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return None, None

        frame = cv.flip(frame, 1)
        results = self.face_mesh.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            landmark = results.multi_face_landmarks[0].landmark[94]
            return landmark.y, frame
        return None, frame

    def release(self):
        self.video_capture.release()
        cv.destroyAllWindows()