from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QColor
import sys
import random


from qtmui.material.styles import useTheme

COLORS = ['default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']

def alpha(color: QColor, alpha: float) -> QColor:
    """Trả về QColor với alpha (0..1)."""
    c = QColor(color)
    c.setAlphaF(alpha)  # hoặc setAlpha(int(alpha*255))
    return c

class LinearDeterminate(QWidget):
    def __init__(
        self,
        key: str = None,
        color: str = "default",
        value: float = 0.0,
    ):
        super().__init__()
        self.setMinimumHeight(5)
        self.setMinimumWidth(300)

        # Progress giống MUI
        self.progress = value

        # Màu sắc
        self.theme = useTheme()
        
        if color == "default":
            self.value_color = self.theme.palette.text.secondary
        elif color in COLORS:
            self.value_color = getattr(self.theme.palette, color).main
        
        self.bg_color = alpha(self.value_color, 0.16)


        # Timer mô phỏng MUI progress
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(500)

        # Timer refresh vẽ
        self.render_timer = QTimer()
        self.render_timer.timeout.connect(self.update)
        self.render_timer.start(16)  # ~60 FPS

    def update_progress(self):
        # Random increment giống MUI
        diff = random.uniform(0, 10)
        if self.progress + diff > 100:
            self.progress = 0
        else:
            self.progress += diff

    def paintEvent(self, event):
        w = self.width()
        h = self.height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Nền
        painter.fillRect(0, 0, w, h, self.bg_color)

        # Value
        value_width = w * (self.progress / 100)
        painter.fillRect(0, 0, value_width, h, self.value_color)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = LinearDeterminate()
#     w.setWindowTitle("Linear Determinate Progress")
#     w.show()
#     sys.exit(app.exec())
