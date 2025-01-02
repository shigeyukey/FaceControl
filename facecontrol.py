import cv2
import dlib
import time
import os
import traceback

from aqt import mw

# Initialize face detector and predictor
detector = dlib.get_frontal_face_detector()
current_dir = os.path.dirname(os.path.abspath(__file__))
shape_predictor_path = os.path.join(current_dir, "resources", "shape_predictor.dat")
predictor = dlib.shape_predictor(shape_predictor_path)

# Global flag to control the face control loop
face_control_running = False

videoWindow = None

def calculate_movement(landmarks, reference_point):
    """Calculate horizontal and vertical nose tip movement."""
    nose_x = landmarks.part(30).x
    nose_y = landmarks.part(30).y

    horizontal_diff = nose_x - reference_point[0]  # Left/Right movement
    vertical_diff = nose_y - reference_point[1]    # Up/Down movement

    return horizontal_diff, vertical_diff

def get_face_control_running():
    return face_control_running

def face_control_loop():
    """Direct face control loop."""
    global face_control_running
    global videoWindow

    from .q_camera import VideoWindow
    if not isinstance(videoWindow, VideoWindow):
        videoWindow = VideoWindow(mw)

    if not videoWindow.camera.isActive():
        print("Error: Unable to access the camera.")
        face_control_running = False


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
