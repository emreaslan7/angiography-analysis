from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QMessageBox

class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__("Araçlar", parent)
        self.parent = parent  # MainWindow erişimi için
        
        # self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # "Dosya Aç" butonu
        open_action = QAction("Open File", self)
        open_icon = QIcon("public/icons/file_toolbar_icon.png")
        open_action.setIcon(open_icon)  
        open_action.triggered.connect(self.open_file)
        self.addAction(open_action)

        # Object Detection için aksiyon
        self.object_detection_action = QAction("Object Detection", self)
        object_detection_icon = QIcon("public/icons/object_detection_toolbar_icon.svg")
        self.object_detection_action.setText("Object Detection")
        self.object_detection_action.setIcon(object_detection_icon)  
        self.object_detection_action.triggered.connect(self.toggle_object_detection)
        self.addAction(self.object_detection_action)

        # Segmentation için aksiyon
        self.segmentation_action = QAction("Segmentation", self)
        segmentation_icon = QIcon("public/icons/segmentation_toolbar_icon.png")
        self.segmentation_action.setText("Segmentation") 
        self.segmentation_action.setIcon(segmentation_icon) 
        self.segmentation_action.triggered.connect(self.toggle_segmentation)
        self.addAction(self.segmentation_action)

        # QToolButton üzerinden düzenleme
        self.update_button_styles()

    def update_button_styles(self):
        # Her bir butonun ikon boyutunu ve metin padding'ini ayarlıyoruz
        for action in self.actions():
            button = self.widgetForAction(action)
            if button:
                button.setIconSize(QSize(24, 24))  # İkon boyutunu ayarlıyoruz (Örneğin 24x24 px)
                
                # İkon ile metin arasındaki boşluk ve metin padding'ini ayarlıyoruz
                button.setStyleSheet("""
                    padding: 4px 8px;
                    margin: 5px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    color: #333;
                    background-color: #f0f0f0;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    text-decoration: none;
                    text-transform: uppercase;
                    padding-left: 8px;
                """)
                
                # ToolButtonStyle ayarlarını yapıyoruz
                button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Medya Dosyaları (*.png *.jpg *.bmp *.mp4 *.avi)")
        
        print(f"seçilen dosya yolu tool_bar içinde: {file_path}")
        if file_path:
            if file_path.endswith((".png", ".jpg", ".bmp")):
                self.show_image(file_path)
            elif file_path.endswith((".mp4", ".avi")):
                self.parent.select_content_widget.set_video(file_path)

    def show_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            media_label = self.parent.select_content_widget.media_label

            scaled_pixmap = pixmap.scaled(
                media_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            media_label.setPixmap(scaled_pixmap)
            self.parent.select_content_widget.set_image(scaled_pixmap, file_path=file_path)

    def toggle_object_detection(self):
        """
        Object Detection bileşenini görünür yapmak veya gizlemek için.
        """
        if self.parent.panel_widget.detection_widget.isVisible():
            self.parent.panel_widget.detection_widget.setVisible(False)
        else:
            self.parent.panel_widget.detection_widget.setVisible(True)

    def toggle_segmentation(self):
        """
        Segmentation bileşenini görünür yapmak veya gizlemek için.
        """
        if self.parent.panel_widget.segmentation_widget.isVisible():
            self.parent.panel_widget.segmentation_widget.setVisible(False)
        else:
            self.parent.panel_widget.segmentation_widget.setVisible(True)
