import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoPlayer(QThread):
    frame_signal = pyqtSignal(QPixmap)

    def __init__(self, video_path, label_size):
        super().__init__()
        self.video_path = video_path
        self.running = True
        self.label_size = label_size  # QLabel'in boyutunu al

    def run(self):
        cap = cv2.VideoCapture(self.video_path)

        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            # QLabel boyutuna ORANTI KORUYARAK ölçekle
            scaled_pixmap = pixmap.scaled(self.label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.frame_signal.emit(scaled_pixmap)
            
            self.msleep(30)

        cap.release()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
