import cv2
import dlib
import time
import os
import traceback

from .ui_control import facecontrol_queue

# Initialize face detector and predictor
detector = dlib.get_frontal_face_detector()
current_dir = os.path.dirname(os.path.abspath(__file__))
shape_predictor_path = os.path.join(current_dir, "resources", "shape_predictor.dat")
predictor = dlib.shape_predictor(shape_predictor_path)

# Global flag to control the face control loop
face_control_running = False

def calculate_movement(landmarks, reference_point):
    """Calculate horizontal and vertical nose tip movement."""
    nose_x = landmarks.part(30).x
    nose_y = landmarks.part(30).y

    horizontal_diff = nose_x - reference_point[0]  # Left/Right movement
    vertical_diff = nose_y - reference_point[1]    # Up/Down movement

    return horizontal_diff, vertical_diff

def face_control_loop():
    """Direct face control loop."""
    global face_control_running
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        face_control_running = False
        return

    reference_point = None
    last_action_time = time.time()  # To throttle input commands

    try:
        while face_control_running:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame from camera.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            for face in faces:
                try:
                    landmarks = predictor(gray, face)
                    if reference_point is None:
                        reference_point = (landmarks.part(30).x, landmarks.part(30).y)

                    horizontal_diff, vertical_diff = calculate_movement(landmarks, reference_point)

                    # Throttle input commands
                    current_time = time.time()

                    if current_time - last_action_time > 2:  # 500ms cooldown
                        if horizontal_diff > 50:
                            facecontrol_queue.put(('undo',))
                        elif horizontal_diff > 20:
                            facecontrol_queue.put(('Again'))
                        elif horizontal_diff < -20:
                            facecontrol_queue.put(('space',))

                        last_action_time = current_time

                    if vertical_diff > 10:
                        facecontrol_queue.put(('scrollUp'))
                    elif vertical_diff < -10:
                        facecontrol_queue.put(('scrollDown'))


                except Exception as e:
                    print(f"Error processing face landmarks: {e}")
                    traceback.print_exc()

            time.sleep(0.1)

    except Exception as e:
        print(f"Unhandled exception in face control loop: {e}")
        traceback.print_exc()

    finally:
        # Release resources when exiting
        cap.release()
        cv2.destroyAllWindows()

def start_face_control():
    """Start the face control (blocking loop)."""
    global face_control_running
    if not face_control_running:
        face_control_running = True
        face_control_loop()

def stop_face_control():
    """Stop the face control."""
    global face_control_running
    face_control_running = False
