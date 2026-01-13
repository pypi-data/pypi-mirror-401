from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QEasingCurve
from PySide6.QtGui import QPainter, QColor
import sys
import time

from qtmui.material.styles import useTheme

COLORS = ['default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']

def alpha(color: QColor, alpha: float) -> QColor:
    """Trả về QColor với alpha (0..1)."""
    c = QColor(color)
    c.setAlphaF(alpha)  # hoặc setAlpha(int(alpha*255))
    return c


class LinearQuery(QWidget):
    def __init__(
        self,
        key: str = None,
        color: str = "default",
    ):
        super().__init__()
        self.setMinimumHeight(5)
        self.setMaximumHeight(5)
        self.setMinimumWidth(300)
        
        self.theme = useTheme()

        if color == "default":
            self.value_color = self.theme.palette.text.secondary
        elif color in COLORS:
            self.value_color = getattr(self.theme.palette, color).main
        
        self.bg_color = alpha(self.value_color, 0.16)

        self.start_time = time.time()
        self.duration = 3.0  # thời gian 1 giai đoạn
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

        self.curve1 = QEasingCurve(QEasingCurve.InOutCubic)
        self.curve2 = QEasingCurve(QEasingCurve.InOutCubic)

    def paintEvent(self, event):
        w = self.width()
        h = self.height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(0, 0, w, h, self.bg_color)

        elapsed = (time.time() - self.start_time)
        t = elapsed % (self.duration * 2)

        if t < self.duration:
            # Giai đoạn 1: width tăng từ 50% -> 66%, tốc độ InOut
            p = self.curve1.valueForProgress(t / self.duration)
            width_ratio = 0.5 + 0.16 * p
            value_width = width_ratio * w
            # chạy từ phải sang trái: bắt đầu ngoài màn hình bên phải
            x = w - (w + value_width) * p
        else:
            # Giai đoạn 2: width giảm từ 66% -> 33%
            p = self.curve2.valueForProgress((t - self.duration) / self.duration)
            width_ratio = 0.66 - 0.33 * p
            value_width = width_ratio * w
            x = w - (w + value_width) * p

        painter.fillRect(x, 0, value_width, h, self.value_color)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = LinearIndeterminateReverse()
#     w.setWindowTitle("Linear Indeterminate Reverse")
#     w.show()
#     sys.exit(app.exec())
