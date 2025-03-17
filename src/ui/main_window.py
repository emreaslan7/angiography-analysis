import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt
from .menu_bar import MenuBar
from .tool_bar import ToolBar
from .video_player import VideoPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anjiyografi Analiz Aracı")

        # **Pencereyi tam ekran yap**
        self.showFullScreen()

        # **Merkez widget**
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # **Ana dikey düzen**
        main_layout = QVBoxLayout(central_widget)

        # **Ortak Medya Alanı (Video + Resim)**
        self.media_label = QLabel(self)
        self.media_label.setFixedSize(1000, 1000)  # **Sabit kare alan**
        self.media_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # **Sol üst köşeye hizala**
        self.media_label.setStyleSheet("border: 2px dashed gray;")  # **Çizgili border**
        self.set_placeholder_text()  # **Başlangıçta yazı ekle**

        # **Layout'a ekleme**
        main_layout.addWidget(self.media_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # **Menü ve araç çubuğu ekleme**
        self.setMenuBar(MenuBar(self))
        self.addToolBar(ToolBar(self))

        # **Video oynatıcıyı başlatmak için değişken**
        self.video_player = None

    def set_placeholder_text(self):
        """Resim alanına varsayılan yazıyı ekler."""
        pixmap = QPixmap(self.media_label.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QColor("gray"))
        painter.setFont(QFont("Arial", 20))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Resim veya Video Buraya Gelecek")
        painter.end()

        self.media_label.setPixmap(pixmap)

    def play_video(self, file_path):
        """Bir video seçildiğinde oynatıcıyı başlatır ve QLabel'e gönderir."""
        if self.video_player:
            self.video_player.stop()
        self.video_player = VideoPlayer(file_path, label_size=self.media_label.size())
        self.video_player.frame_signal.connect(self.update_media_label)
        self.video_player.start()

    def load_image(self, file_path):
        """Seçilen resmi çerçeveye tam oturtarak göster."""
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.set_placeholder_text()
        else:
            scaled_pixmap = pixmap.scaled(
                self.media_label.width(),
                self.media_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.media_label.setPixmap(scaled_pixmap)

    def update_media_label(self, pixmap):
        """Gelen kareyi QLabel içine uygun şekilde yerleştirir."""
        scaled_pixmap = pixmap.scaled(
            self.media_label.width(),
            self.media_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.media_label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
