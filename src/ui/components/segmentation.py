from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .collapsible_header import CollapsibleHeaderWidget  # Yeni bileşeni içe aktar

class SegmentationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # İçeriği oluştur
        content_widget = QWidget()  # Şu an içi boş
        content_layout = QVBoxLayout(content_widget)  # İçerik layoutu, şu anda herhangi bir widget eklenmiyor

        # CollapsibleHeaderWidget kullan
        self.collapsible_header = CollapsibleHeaderWidget("Segmentation", content_widget)

        # Layout'u ayarla
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.collapsible_header)
        self.setLayout(self.layout)
