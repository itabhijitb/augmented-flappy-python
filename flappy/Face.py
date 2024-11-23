import cv2
import multiprocessing
import time

def position(face_center_queue):
    """Detect faces, calculate their centers, and display the webcam output."""
    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the webcam (0 for default camera)
    video_capture = cv2.VideoCapture(0)
    previous_center_y = None
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

        # Find the largest face
        if len(faces) > 0:
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face

            # Calculate the center of the face
            center_x = x + w // 2
            center_y = y + h // 2

            # Push the center coordinates to the queue
            # print(previous_center_y)
            if not face_center_queue.full():
                face_center_queue.put(center_y)

            # Draw a rectangle and center point for visualization
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow('Face Detection', frame)

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Define a queue with a limited size
    face_center_queue = multiprocessing.Queue(maxsize=10)

    # Create the position process
    position_process = multiprocessing.Process(target=position, args=(face_center_queue,))

    # Start the position process
    position_process.start()

    try:
        while True:
            # Read from the queue in the main process
            if not face_center_queue.empty():
                center = face_center_queue.get()
                print(f"Detected Face Center: {center}")
            time.sleep(0.1)  # Avoid busy-waiting
    except KeyboardInterrupt:
        print("Exiting...")

    # Terminate the position process
    position_process.terminate()
    position_process.join()
