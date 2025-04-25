from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class CollapsibleHeaderWidget(QWidget):
    def __init__(self, title: str, content_widget: QWidget, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: lightgray;")

        # Başlık barı
        self.header = QWidget()
        self.header_layout = QHBoxLayout(self.header)
        self.header.setStyleSheet("background-color: #2E2E2E; color: white;")

        # Başlık metni (sola dayalı)
        self.header_label = QLabel(title)
        self.header_label.setStyleSheet("font-size: 14px; color: white;")
        
        # Başlık metnini sola dayalı ekle
        self.header_layout.addWidget(self.header_label, alignment=Qt.AlignLeft)

        # İkonlar için yeni bir layout oluşturuyoruz
        icon_layout = QHBoxLayout()
        
        # Açma/Kapama ikonu (sağa dayalı)
        self.toggle_button = QPushButton("▲")
        self.toggle_button.setStyleSheet("background-color: transparent; color: white; border: none; font-size: 18px;")  # İkon boyutunu arttırdık
        self.toggle_button.clicked.connect(self.toggle_content)

        # # Kapatma butonu (sağa dayalı)
        # self.close_button = QPushButton("×")
        # self.close_button.setStyleSheet("background-color: transparent; color: white; border: none; font-size: 18px;")  # İkon boyutunu arttırdık
        # self.close_button.clicked.connect(self.close_widget)

        # İkonları içeren layout'u sağa dayalı ekle
        icon_layout.addWidget(self.toggle_button)
        # icon_layout.addWidget(self.close_button)
        icon_layout.setAlignment(Qt.AlignRight)

        # İkonları başlık barına ekle
        self.header_layout.addLayout(icon_layout)

        # İçerik widget'ı
        self.content_widget = content_widget
        self.content_widget.setVisible(True) 

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.content_widget)

        self.is_visible = True

    def toggle_content(self):
        """
        Widget'ı açıp kapama işlevi.
        """
        if self.is_visible:
            self.content_widget.setVisible(False)
            self.toggle_button.setText("▼")
        else:
            self.content_widget.setVisible(True)
            self.toggle_button.setText("▲")
        self.is_visible = not self.is_visible

