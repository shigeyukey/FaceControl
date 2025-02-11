import cv2
import dlib
import pyautogui
import time
import os
import traceback

# Initialize face detector and predictor
detector = dlib.get_frontal_face_detector()
addon_path = os.path.dirname(__file__)
shape_predictor_path = os.path.join(addon_path,  "user_files", "resources", "shape_predictor.dat")
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
                    if current_time - last_action_time > 0.5:  # 500ms cooldown
                        if horizontal_diff > 50:
                            pyautogui.hotkey('ctrl', 'z')  # Undo
                        elif horizontal_diff > 20:
                            pyautogui.press('1')         # Again
                        elif horizontal_diff < -20:
                            pyautogui.press('space')       # Show card, Good
                                            
                        last_action_time = current_time
                    
                    if vertical_diff > 10:
                            pyautogui.scroll(-100)         # Scroll down
                    elif vertical_diff < -10:
                            pyautogui.scroll(100)          # Scroll up
                    
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