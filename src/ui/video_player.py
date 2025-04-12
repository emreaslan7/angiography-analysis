import time
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
        self.paused = False
        self.cap = None 
        self.label_size = label_size  # QLabel'in boyutunu al
    
    def get_position(self):
        """Videonun şu anki pozisyonunu milisaniye cinsinden döndür"""
        if self.cap and self.cap.isOpened():
            return int(self.cap.get(cv2.CAP_PROP_POS_MSEC))
        return 0

    def get_duration(self):
        """Video süresini milisaniye cinsinden döndür"""
        if self.cap and self.cap.isOpened():
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            return int((frame_count / fps) * 1000)
        return 0

    def set_position(self, position_ms):
        """Videoyu belirtilen pozisyona ayarla"""
        if self.cap and self.cap.isOpened():
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_number = int((position_ms / 1000) * fps)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def is_playing(self):
        """Video oynatılıyor mu kontrolü"""
        return self.running and not self.paused

    def run(self):
        self.running = True
        self.cap = cv2.VideoCapture(self.video_path)
        
        while self.running:
            if not self.paused:
                ret, frame = self.cap.read()
                if ret:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_frame.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    # Görüntüyü label boyutuna ölçekle
                    pixmap = QPixmap.fromImage(qt_image).scaled(
                        self.label_size.width(),
                        self.label_size.height(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.frame_signal.emit(pixmap)
                    time.sleep(1/30)  # FPS kontrolü
                else:
                    self.running = False
            else:
                time.sleep(0.1)
                
        self.cap.release()
        

    def pause(self):
        """Videoyu duraklatır"""
        self.paused = True

    def resume(self):
        """Videoyu devam ettirir"""
        self.paused = False

   
