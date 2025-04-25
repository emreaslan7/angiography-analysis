from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QMessageBox
import sys


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # "Dosya" menüsünü oluştur
        file_menu = self.addMenu("Main")

        # "Dosya Aç" seçeneği
        open_action = QAction("Dosya Aç", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # "Çıkış" seçeneği
        exit_action = QAction("Çıkış", self)
        exit_action.triggered.connect(self.exit_app)
        file_menu.addAction(exit_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Resim Dosyaları (*.png *.jpg *.bmp *.mp4)")
        if file_path:
            QMessageBox.information(self, "Seçilen Dosya", f"Seçilen dosya:\n{file_path}")

    def exit_app(self):
        sys.exit()
