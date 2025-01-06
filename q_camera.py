import time
import traceback
from queue import Queue

from aqt import mw
from aqt.qt import QDialog, QVBoxLayout,  pyqtSignal, QThread, QImage, Qt, QTimer, pyqtSlot
from PyQt6.QtMultimedia import QMediaDevices, QMediaCaptureSession, QCamera, QImageCapture
from PyQt6.QtMultimediaWidgets import QVideoWidget

from .ui_control import facecontrol_queue, scroll_queue, reset_queue, reset_scroll_queue
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
        self.need_cooldown = False

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
                time.sleep(0.1)

            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
                break

    def processed_face_control(self, gray:QImage):
        try:
            if not self.get_face_control_running():
                self.reference_point = None
                self.last_action_time = time.time()
                self.need_cooldown = False
                return

            config = mw.addonManager.getConfig(__name__)
            threshold_h = config.get("threshold_h", 20)
            threshold_v = config.get("threshold_v", 10)
            threshold_undo = config.get("threshold_undo", 50)
            cooldown = config.get("cooldown", 0.5)

            faces = self.detector(gray)

            for face in faces:
                landmarks = self.predictor(gray, face)
                if self.reference_point is None:
                    self.reference_point = (landmarks.part(30).x, landmarks.part(30).y)

                horizontal_diff, vertical_diff = self.calculate_movement(landmarks, self.reference_point)


                if (horizontal_diff < threshold_h and vertical_diff < threshold_v
                    and horizontal_diff > -threshold_h and vertical_diff > -threshold_v):
                    # Disable cooldown if user looks at the front.
                    self.need_cooldown = False
                current_time = time.time()

                print(f" X:{horizontal_diff} Y:{vertical_diff} C:{self.need_cooldown}")

                if current_time - self.last_action_time > cooldown and not self.need_cooldown:  # 500ms cooldown
                    self.need_cooldown = True # If answered, enable cooldown and disables control.
                    if horizontal_diff > threshold_undo:
                        reset_queue()
                        facecontrol_queue.put("undo")
                    elif horizontal_diff > threshold_h:
                        reset_queue()
                        facecontrol_queue.put("Again")
                    elif horizontal_diff < -threshold_h:
                        reset_queue()
                        facecontrol_queue.put("space") # Good
                    else:
                        self.need_cooldown = False # If no answer, the enable cooldown is canceled.

                    self.last_action_time = current_time

                if vertical_diff > threshold_v:
                    reset_scroll_queue()
                    scroll_queue.put("scrollDown")
                elif vertical_diff < -threshold_v:
                    reset_scroll_queue()
                    scroll_queue.put("scrollUp")

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



