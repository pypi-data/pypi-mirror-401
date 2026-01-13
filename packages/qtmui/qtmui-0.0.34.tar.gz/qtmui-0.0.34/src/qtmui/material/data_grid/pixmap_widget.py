from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter, QBrush
from PySide6.QtCore import Qt

def widget_to_pixmap(widget):
    """Chuyển đổi một QWidget thành QPixmap."""
    # Tạo một đối tượng QPixmap với kích thước của widget
    pixmap = QPixmap(widget.size())
    
    # Bắt đầu vẽ nội dung của widget lên pixmap
    widget.render(pixmap)
    
    return pixmap


class PixmapWidget(QWidget):
    def __init__(self, widget):
        super().__init__()

        self._widget = widget
        self._width = widget.width()
        self._height = widget.height()


        self.setFixedSize(widget.size())

        

    def paintEvent(self, event):
        # Chuyển đổi widget thành QPixmap
        pixmap = widget_to_pixmap(self._widget)
        # Lưu QPixmap ra file ảnh PNG để kiểm tra
        # pixmap.save("widget_capture.png", "PNG")
        scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  

        brush = QBrush()
        brush.setStyle(Qt.Dense2Pattern)
        brush.setTexture(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)

        painter.drawRoundedRect(self.rect(), self._width, self._height)

        super().paintEvent(event)


# if __name__ == "__main__":
#     app = QApplication([])

#     # Tạo một widget ví dụ
#     widget = PixmapWidget()
#     widget.show()
#     app.exec()
