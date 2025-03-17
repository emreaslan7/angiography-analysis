from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QMessageBox

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Araçlar", parent)
        self.parent = parent  # MainWindow erişimi için

        # "Dosya Aç" butonu
        open_action = QAction("📂 Dosya Aç", self)
        open_action.triggered.connect(self.open_file)
        self.addAction(open_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Medya Dosyaları (*.png *.jpg *.bmp *.mp4 *.avi)")
        if file_path:
            if file_path.endswith((".png", ".jpg", ".bmp")):
                self.show_image(file_path)
            elif file_path.endswith((".mp4", ".avi")):
                self.parent.play_video(file_path)

    def show_image(self, file_path):
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Hata", "Görüntü dosyası yüklenemedi.")
            return
        
        # QLabel boyutuna göre ORANTI KORUYARAK ölçekle
        scaled_pixmap = pixmap.scaled(self.parent.media_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.parent.media_label.setPixmap(scaled_pixmap)
