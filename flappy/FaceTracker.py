import mediapipe as mp
import cv2 as cv

class FaceTracker:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.video_capture = cv.VideoCapture(0)

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