from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt


class VideoControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        # layout.setContentsMargins(10, 10, 10, 10)
        # layout.setSpacing(15)
        
        # Oynat / Durdur
        self.play_button = QPushButton("▶️")
        layout.addWidget(self.play_button)
        
        # Geçen süre etiketi
        self.current_time_label = QLabel("00:00")
        layout.addWidget(self.current_time_label)

        # Slider (ilerleme çubuğu gibi ama fonksiyonsuz)
        self.progress_slider = QSlider(Qt.Horizontal)
        layout.addWidget(self.progress_slider)
        
        # Toplam süre etiketi
        self.total_time_label = QLabel("00:00")
        layout.addWidget(self.total_time_label)

        # Frame bilgisi
        self.frame_info_label = QLabel("0 / 0")
        layout.addWidget(self.frame_info_label)

        # Başta gizli
        self.hide()



