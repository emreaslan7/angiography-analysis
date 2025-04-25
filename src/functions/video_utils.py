import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

def play_video(file_path, main_window):
    
    print(f"Video dosyası yüklendi video utils: : {file_path}")
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Video dosyası açılamadı.")
        return None

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            print("Video bitti.")
            cap.release()
            timer.stop()
            return

        # OpenCV -> QPixmap dönüşümü
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # Ana pencereye frame gönder
        main_window.update_media_label(pixmap, file_path=file_path)

    timer = QTimer()
    timer.timeout.connect(update_frame)
    timer.start(30)  # yaklaşık 30 FPS

    return timer  # Dilersen bu timer'ı main_window'da saklayabilirsin
