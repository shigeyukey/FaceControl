
from aqt import mw
from aqt.qt import QAction, QMessageBox
from threading import Thread, Event

from .wheel_importer import run_wheel_importer

face_control_event = Event()

def toggle_face_control():
    """Toggle face control (start or stop)."""

    # Download and import the modules
    if not run_wheel_importer():
        # Return until modules import successfully.
        return

    # This must be done after downloading the module, so put it in the function.
    from .facecontrol import start_face_control, stop_face_control

    if face_control_event.is_set():  # Stop it if it's running
        face_control_event.clear() # Signal the thread to stop
        stop_face_control()
        QMessageBox.information(mw, "Face Control", "Face control has been disabled.")
    else:  # Start it if it's not running
        try:
            face_control_event.set() # Signal the thread to run
            Thread(target=start_face_control, daemon=True).start()  # Run in a separate thread
            QMessageBox.information(mw, "Face Control", "Face control has been enabled.")
        except Exception as e:
            QMessageBox.critical(
                mw,
                "Face Control Error",
                f"An error occurred: {e}"
            )

def run_face_control():
    """Run the face control loop, respecting the event."""
    from .facecontrol import start_face_control, stop_face_control
    while face_control_event.is_set():
        start_face_control()
    stop_face_control() #Ensure cleanup when stopping
    
# Add the menu option to toggle face control
action = QAction("Toggle Face Control", mw)
action.triggered.connect(toggle_face_control)
mw.form.menuTools.addAction(action)
