import sys
import os

# Add the lib folder to sys.path
addon_dir = os.path.dirname(__file__)
lib_dir = os.path.join(addon_dir, "lib")

if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from aqt import mw
from aqt.qt import QAction, QMessageBox
from threading import Event
from .facecontrol import start_face_control, stop_face_control

face_control_event = Event()

def toggle_face_control():
    if face_control_event.is_set():
        face_control_event.clear()
        stop_face_control()
        QMessageBox.information(mw, "Face Control", "Face control has been disabled.")
    else:
        try:
            face_control_event.set()
            start_face_control()
            QMessageBox.information(mw, "Face Control", "Face control has been enabled.")
        except Exception as e:
            QMessageBox.critical(
                mw,
                "Face Control Error",
                f"An error occurred: {e}"
            )

def run_face_control():
    """Run the face control loop, respecting the event."""
    while face_control_event.is_set():
        start_face_control()
    stop_face_control() #Ensure cleanup when stopping

# Add the menu option to toggle face control
action = QAction("Toggle Face Control", mw)
action.triggered.connect(toggle_face_control)
mw.form.menuTools.addAction(action)
