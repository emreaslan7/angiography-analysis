import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

class VideoPlayer(QThread):
    frame_signal = pyqtSignal(QPixmap)
    progress_signal = pyqtSignal(int, int)  # <--- Eklendi: (current_frame, total_frames)
    seek_request = None
    
    def __init__(self, video_path, size):
        super().__init__()
        self.video_path = video_path
        self.size = size
        self.running = True
        self.paused = False
        self.cap = None
        self.seek_frame = None 
    
    def run(self):
        self.cap = cv2.VideoCapture(self.video_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while self.cap.isOpened():
            if not self.running:
                break
            
            if self.seek_frame is not None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.seek_frame)
                # Doğru frame'e ulaşana kadar okumaya devam et
                while True:
                    current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    if current_frame >= self.seek_frame:
                        break
                    self.cap.read()
                self.seek_frame = None 

            if self.paused:
                self.msleep(100)
                continue

            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img).scaled(
                self.size.width(), self.size.height(), Qt.KeepAspectRatio
            )
            self.frame_signal.emit(pixmap)
            self.progress_signal.emit(current_frame, self.total_frames)  

            self.msleep(30)

        self.cap.release()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False
        self.wait()

    def seek(self, frame_index):
        """Belirli frame'e git"""
        self.seek_frame = frame_index

