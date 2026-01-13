from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QSize

def widget_to_pixmap(widget):
    """Chuyển đổi một QWidget thành QPixmap."""
    # Tạo một đối tượng QPixmap với kích thước của widget
    pixmap = QPixmap(widget.size())
    
    # Bắt đầu vẽ nội dung của widget lên pixmap
    widget.render(pixmap)
    
    return pixmap

class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Tạo layout và label đơn giản
        layout = QVBoxLayout(self)
        label = QPushButton("Hello, QLabel in QWidget!")
        label.setStyleSheet('background: red;')
        layout.addWidget(label)
        
        self.setLayout(layout)
        self.setFixedSize(QSize(200, 40))

class PixmapWidget(QWidget):
    def __init__(self):
        super().__init__()

        
        self.setFixedSize(QSize(200, 40))
        

    def paintEvent(self, event):
        # Chuyển đổi widget thành QPixmap
        pixmap = widget_to_pixmap(ExampleWidget())
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

        painter.drawRoundedRect(self.rect(), 200, 40)

        super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication([])

    # Tạo một widget ví dụ
    widget = PixmapWidget()
    widget.show()



    app.exec()
