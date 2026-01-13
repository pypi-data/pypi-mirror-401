from weakref import ref
import random
from PySide6.QtGui import QPen, QPainter, QColor, QPixmap, QIcon
from PySide6.QtCore import Qt, QVariantAnimation, QRectF, QEasingCurve, QSize
from PySide6.QtWidgets import QApplication, QPushButton

from qtmui.material.styles import useTheme


class Arc:
    def __init__(self):
        theme = useTheme()
        self.diameter = 40  # Đường kính vòng cung
        self.color = QColor(theme.palette.grey._500)
        self.span = random.randint(40, 150)  # Độ dài cung ban đầu
        self.direction = 1 if random.randint(10, 15) % 2 == 0 else -1
        self.startAngle = random.randint(0, 360)


class LoadingIcon(QIcon):
    def __init__(self, button: QPushButton, diameter=40, parent=None):
        """
        Biểu tượng loading dưới dạng QIcon.

        Parameters:
        - button: QPushButton, nút sẽ hiển thị biểu tượng.
        - diameter: int, đường kính của vòng cung.
        """
        super().__init__(parent)
        self.button_ref = ref(button)  # Nút để cập nhật biểu tượng
        self.arc = Arc()
        self.arc.diameter = diameter
        self.pixmap_size = diameter + 10  # Kích thước QPixmap (để chứa vòng cung)
        self.startAnime()

    def startAnime(self):
        """Khởi động animation quay vòng."""
        self.anim = QVariantAnimation(duration=1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.setEasingCurve(QEasingCurve.Linear)
        self.anim.setLoopCount(-1)  # Lặp lại vô hạn
        self.anim.valueChanged.connect(self.updatePixmap)
        self.anim.start()

    def updatePixmap(self, value):
        """
        Cập nhật QPixmap theo góc quay của animation.
        """
        # Tạo QPixmap trống
        pixmap = QPixmap(self.pixmap_size, self.pixmap_size)
        pixmap.fill(Qt.transparent)  # Nền trong suốt

        # Vẽ vòng cung lên QPixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.arc.color, 3, Qt.SolidLine))

        # Tính toán tọa độ và độ dài cung
        current_angle = value
        start_angle = current_angle * self.arc.direction + self.arc.startAngle
        rect = QRectF(
            5, 5, self.arc.diameter, self.arc.diameter
        )  # Vùng chứa vòng cung

        # Điều chỉnh độ dài cung thay đổi từ 40 -> 240
        if current_angle <= 180:
            span_length = 40 + (current_angle / 180) * 200
        else:
            span_length = 240 - ((current_angle - 180) / 180) * 200

        # Vẽ vòng cung
        painter.drawArc(rect, int(start_angle) * 16, int(span_length) * 16)
        painter.end()

        # Cập nhật QIcon bằng QPixmap
        self.addPixmap(pixmap)

        # Kiểm tra xem nút còn tồn tại trước khi cập nhật
        try:
            button = self.button_ref()
            if button:
                button.setIcon(self)
        except Exception as e:
            self.anim.valueChanged.disconnect(self.updatePixmap)

    def stopAnimation(self):
        """Dừng animation."""
        if self.anim:
            self.anim.stop()


# if __name__ == "__main__":

#     app = QApplication(sys.argv)

#     # Tạo một QPushButton và sử dụng LoadingIcon làm biểu tượng
#     button = QPushButton("Loading Button")
#     loading_icon = LoadingIcon(button, diameter=40)  # Truyền tham chiếu tới nút
#     button.setIconSize(QSize(loading_icon.pixmap_size, loading_icon.pixmap_size))
#     button.resize(200, 100)
#     button.show()

#     sys.exit(app.exec())
