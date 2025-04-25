from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt
from .collapsible_header import CollapsibleHeaderWidget
from functions.detection_utils import handle_detection  

class ObjectDetectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Confidence threshold slider
        self.conf_label = QLabel("Confidence Threshold: 0.5")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.update_confidence_label)

        # Detect button
        self.detect_button = QPushButton("Detect Stenosis")
        self.detect_button.setStyleSheet("background-color: lightblue; color: black;")
        self.detect_button.clicked.connect(self.handle_detection_and_update)

        # İçeriği oluştur
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.addWidget(self.conf_label)
        content_layout.addWidget(self.slider)
        content_layout.addWidget(self.detect_button)

        # CollapsibleHeaderWidget kullan
        self.collapsible_header = CollapsibleHeaderWidget("Object Detection", content_widget)

        # Layout'u ayarla
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.collapsible_header)


    def update_confidence_label(self, value):
        conf = value / 100
        self.conf_label.setText(f"Confidence Threshold: {conf:.2f}")

    def get_confidence_threshold(self):
        return self.slider.value() / 100
    
    def handle_detection_and_update(self):
        main_window = self.parent().parent().parent()
        print(f"main_window: {main_window}")
        handle_detection(self.get_confidence_threshold(), main_window)


    
    
    
    

