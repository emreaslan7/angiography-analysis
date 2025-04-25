from PyQt5.QtGui import QPixmap

def load_image(file_path, select_content_widget):
    
    print(f"IMAGE UTİLS : Loading image from: {file_path}")
    
    pixmap = QPixmap(file_path)
    if pixmap.isNull():
        select_content_widget.set_placeholder_text()
    else:
        select_content_widget.set_image(pixmap)
