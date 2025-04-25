import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

# UI
from ui.components.panel_widget import PanelWidget

# Components
from .menu_bar import MenuBar
from .tool_bar import ToolBar
from ui.components.select_content import SelectContentWidget

# Functions
from functions.image_utils import load_image
from functions.video_utils import play_video
from functions.detection_utils import handle_detection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anjiyografi Analiz Aracı")
        self.showFullScreen()  # Tam ekran başlat

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Sol: İçerik bileşeni
        self.select_content_widget = SelectContentWidget()
        main_layout.addWidget(self.select_content_widget, stretch=1, alignment=Qt.AlignTop)

        # Sağ: Panel bileşeni (burada ObjectDetectionWidget zaten var)
        self.panel_widget = PanelWidget()
        main_layout.addWidget(self.panel_widget, stretch=1)

        # Menü ve araç çubuğu
        self.setMenuBar(MenuBar(self))
        self.addToolBar(ToolBar(self))

        # Video player (isteğe bağlı)
        # self.video_player = None


    def load_image(self, file_path):
        load_image(file_path, self.select_content_widget)

    def play_video(self, file_path):
        self.video_player = play_video(file_path, self)

    def update_media_label(self, pixmap, file_path=None):
        """Gelen videodan alınan kareyi component'e gönder."""
        self.select_content_widget.set_image(pixmap, file_path=file_path)
        
    def get_select_content_widget(self):
        """SelectContentWidget'i döndür."""
        return self.select_content_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
