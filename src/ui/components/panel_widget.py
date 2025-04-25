from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from .object_detection import ObjectDetectionWidget
from .segmentation import SegmentationWidget  # Yeni bileşeni içe aktar

class PanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Yatay layout (QHBoxLayout) oluştur
        horizontal_layout = QHBoxLayout()

        # ObjectDetectionWidget ve SegmentationWidget oluştur
        self.detection_widget = ObjectDetectionWidget()
        self.segmentation_widget = SegmentationWidget()

        # Bileşenleri yatay layout'a ekle
        horizontal_layout.addWidget(self.detection_widget, alignment=Qt.AlignTop)
        horizontal_layout.addWidget(self.segmentation_widget, alignment=Qt.AlignTop)

        # Yatay layout'u ana layout'a ekle
        layout.addLayout(horizontal_layout)
    
        self.setLayout(layout)

    def get_detector_widget(self):
        return self.detection_widget

    def resizeEvent(self, event):
        # Bileşenlerin genişliğini ayarla
        self.detection_widget.setFixedWidth(self.parent().width() // 5)
        self.segmentation_widget.setFixedWidth(self.parent().width() // 5)
        super().resizeEvent(event)
