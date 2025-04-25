

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from ui.components.video_control_panel import VideoControlPanel
from ui.video_player import VideoPlayer  # <-- EKLENDİ
from state_manager import StateManager
import os

class SelectContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.state_manager = StateManager()

        # Ana yatay layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.media_label = QLabel()
        self.media_label.setFixedSize(900, 900)
        self.media_label.setAlignment(Qt.AlignTop)
        self.media_label.setStyleSheet("border: 2px dashed gray;")
        self.set_placeholder_text()
        layout.addWidget(self.media_label)

        # Video kontrol paneli
        self.video_control_panel = VideoControlPanel()
        layout.addWidget(self.video_control_panel)

        self.video_player = None  # <-- EKLENDİ

    def set_placeholder_text(self):
        pixmap = QPixmap(self.media_label.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QColor("gray"))
        painter.setFont(QFont("Arial", 20))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Resim veya Video Buraya Gelecek")
        painter.end()
        self.media_label.setPixmap(pixmap)

    def set_image(self, pixmap: QPixmap, file_path=None):
        scaled_pixmap = pixmap.scaled(
            self.media_label.width(),
            self.media_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.media_label.setPixmap(scaled_pixmap)
        self.hide_video_controls()
        self.stop_video()

        if file_path and "output" not in file_path:
            self.state_manager.set("image_path", file_path)
            print(f"Selected Image Path: {self.state_manager.get('image_path')}")


    def show_video_controls(self):
        self.video_control_panel.show()

    def hide_video_controls(self):
        self.video_control_panel.hide()

    # -----------------------------
    # 🎬 VideoPlayer Fonksiyonları
    # -----------------------------
    
    def set_video(self, video_path):
        """Video yükle ve başlat."""
        self.state_manager.set("image_path", video_path)
        self.show_video_controls()
        self.start_video(video_path)

    # def start_video(self, path):
    #     if self.video_player:
    #         self.video_player.stop()

    #     self.video_player = VideoPlayer(path, self.media_label.size())
    #     self.video_player.frame_signal.connect(self.media_label.setPixmap)
    #     self.video_player.start()

    #     # Düğme bağlantıları
    #     self.video_control_panel.play_button.clicked.connect(self.toggle_play_pause)        
    #     self.video_player.progress_signal.connect(self.update_slider)
    #     self.video_control_panel.progress_slider.sliderMoved.connect(self.slider_moved)
    
    def start_video(self, path):
        if self.video_player:
            self.video_player.stop()
            self.video_player.deleteLater()  # bellek sızıntısını önle
            self.video_player = None

        # Yeni video player başlat
        self.video_player = VideoPlayer(path, self.media_label.size())
        self.video_player.frame_signal.connect(self.media_label.setPixmap)
        self.video_player.start()

        # Önce eski bağlantıları temizle (kısa ve güvenli yöntem)
        try:
            self.video_control_panel.play_button.clicked.disconnect()
        except TypeError:
            pass
        try:
            self.video_control_panel.progress_slider.sliderMoved.disconnect()
        except TypeError:
            pass
        try:
            self.video_player.progress_signal.disconnect()
        except TypeError:
            pass

        # Bağlantıları yeniden yap
        self.video_control_panel.play_button.clicked.connect(self.toggle_play_pause)
        self.video_control_panel.progress_slider.sliderMoved.connect(self.slider_moved)
        self.video_player.progress_signal.connect(self.update_slider)


    def stop_video(self):
        if self.video_player:
            self.video_player.stop()
            self.video_player = None

    def toggle_play_pause(self):
        if self.video_player:
            if self.video_player.paused:
                self.video_player.resume()
            else:
                self.video_player.pause()
            
    def update_slider(self, current, total):
        self.video_control_panel.progress_slider.blockSignals(True)
        self.video_control_panel.progress_slider.setMaximum(total)
        self.video_control_panel.progress_slider.setValue(current)
        self.video_control_panel.progress_slider.blockSignals(False)

        # ⏱ Zaman bilgisi (saniyeye çevriliyor)
        current_sec = int(current / 30)  # 30 fps varsaydık
        total_sec = int(total / 30)

        def format_time(seconds):
            return f"{seconds // 60:02}:{seconds % 60:02}"

        self.video_control_panel.current_time_label.setText(format_time(current_sec))
        self.video_control_panel.total_time_label.setText(format_time(total_sec))

        # 🖼 Frame bilgisi
        self.video_control_panel.frame_info_label.setText(f"{current} / {total}")

    def slider_moved(self, value):
        if self.video_player:
            self.video_player.pause()
            self.video_player.seek(value)

            # Frame bilgisini güncelle
            total = self.video_player.total_frames  # Bu property varsa, yoksa başka yerden alabiliriz

            current_sec = int(value / 30)
            total_sec = int(total / 30)

            def format_time(seconds):
                return f"{seconds // 60:02}:{seconds % 60:02}"

            self.video_control_panel.current_time_label.setText(format_time(current_sec))
            self.video_control_panel.total_time_label.setText(format_time(total_sec))
            self.video_control_panel.frame_info_label.setText(f"{value} / {total}")



