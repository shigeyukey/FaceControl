import time
import traceback
from queue import Queue

from aqt.qt import QDialog, QVBoxLayout,  pyqtSignal, QThread, QImage, Qt, QTimer, pyqtSlot
from PyQt6.QtMultimedia import QMediaDevices, QMediaCaptureSession, QCamera, QImageCapture
from PyQt6.QtMultimediaWidgets import QVideoWidget

from .ui_control import facecontrol_queue
import numpy as np

class ImageProcessingWorker(QThread):
    processed = pyqtSignal(np.ndarray)

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

        from .facecontrol import detector, predictor, calculate_movement, get_face_control_running
        self.detector = detector
        self.predictor = predictor
        self.calculate_movement = calculate_movement
        self.get_face_control_running = get_face_control_running

        self.reference_point = None
        self.last_action_time = time.time()

    def run(self):
        while True:
            try:
                image = self.queue.get() # type:QImage
                if image is None:
                    continue
                ptr = image.bits()
                ptr.setsize(image.sizeInBytes())
                arr = np.array(ptr).reshape(image.height(), image.width(), 4)
                gray = np.dot(arr[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)
                self.processed_face_control(gray)

            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
                break

    def processed_face_control(self, gray:QImage):
        try:
            if not self.get_face_control_running():
                return

            faces = self.detector(gray)

            for face in faces:
                landmarks = self.predictor(gray, face)
                if self.reference_point is None:
                    self.reference_point = (landmarks.part(30).x, landmarks.part(30).y)

                horizontal_diff, vertical_diff = self.calculate_movement(landmarks, self.reference_point)

                current_time = time.time()

                print(f"X:{horizontal_diff} Y:{vertical_diff}")

                if current_time - self.last_action_time > 0.5:  # 500ms cooldown
                    if horizontal_diff > 50:
                        facecontrol_queue.put(('undo'))
                    elif horizontal_diff > 20:
                        facecontrol_queue.put(('Again')) # Again
                    elif horizontal_diff < -20:
                        facecontrol_queue.put(('space')) # Good

                    self.last_action_time = current_time

                if vertical_diff > 10:
                    facecontrol_queue.put(('scrollDown', 4))
                elif vertical_diff < -10:
                    facecontrol_queue.put(('scrollUp', 4))

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()


class VideoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint| Qt.WindowType.Dialog)

        self.available_cameras = QMediaDevices.videoInputs()
        if not self.available_cameras:
            return

        self.viewfinder = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.viewfinder)
        self.setLayout(layout)

        self.select_camera(0)

        self.image_queue = Queue(maxsize=100)
        self.worker = ImageProcessingWorker(self.image_queue)
        self.worker.start()

        self.capture_loop_timer = QTimer()
        self.capture_loop_timer.timeout.connect(self.capture_loop)
        self.capture_loop_timer.start(100) # Instead of "time.sleep(0.1)"


    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.capture_session = QMediaCaptureSession()
        self.capture_session.setCamera(self.camera)
        self.capture_session.setVideoOutput(self.viewfinder)
        self.image_capture = QImageCapture(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.image_capture.imageCaptured.connect(self.on_image_captured)

        self.camera.start()
        self.current_camera_name = self.available_cameras[i].description()

    def capture_loop(self):
        self.image_capture.capture()

    @pyqtSlot(int, QImage)
    def on_image_captured(self, id, image: QImage):
        if not self.image_queue.empty():
            self.image_queue.get()
        self.image_queue.put(image)



