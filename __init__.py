
from threading import Event

from aqt import mw
from aqt.qt import QAction, QMessageBox
from aqt.utils import tooltip

from .wheel_importer import import_module, check_imports, get_is_download_wheel

first_run = True

face_control_event = Event()

def toggle_face_control():
    global first_run
    if first_run:
        yes = import_module()
        if yes:
            first_run = False

    if get_is_download_wheel():
        tooltip("Now loading, please wait...")
        return

    if not check_imports():
        tooltip("Error: Module import failed.")
        return


    from .facecontrol import start_face_control, stop_face_control
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

# Add the menu option to toggle face control
action = QAction("Toggle Face Control", mw)
action.triggered.connect(toggle_face_control)
mw.form.menuTools.addAction(action)
