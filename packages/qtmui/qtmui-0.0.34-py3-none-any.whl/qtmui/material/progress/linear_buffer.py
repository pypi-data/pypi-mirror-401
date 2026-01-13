from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QTimer, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QBrush
import sys
import time
import random


from qtmui.material.styles import useTheme

COLORS = ['default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']

def alpha(color: QColor, alpha: float) -> QColor:
    """Trả về QColor với alpha (0..1)."""
    c = QColor(color)
    c.setAlphaF(alpha)  # hoặc setAlpha(int(alpha*255))
    return c


class LinearBuffer(QWidget):
    def __init__(
        self,
        key: str = None,
        color: str = "default",
        value: float = 0.0,
        buffer: float = 0.0,
    ):
        super().__init__()
        self.setMinimumHeight(5)
        self.setMinimumWidth(400)

        # Progress & buffer giống MUI
        self.progress = value
        self.buffer = buffer

        # Màu sắc
        self.theme = useTheme()
        
        if color == "default":
            self.value_color = self.theme.palette.text.secondary
        elif color in COLORS:
            self.value_color = getattr(self.theme.palette, color).main
        
        self.bg_color = alpha(self.value_color, 0.16)
        self.buffer_color = alpha(self.value_color, 0.3)
        self.dotted_color = alpha(self.value_color, 0.5)

        # Dotted effect
        self.start_time = time.time()
        self.curve = QEasingCurve(QEasingCurve.InOutCubic)

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
            self.buffer = 10
        else:
            diff2 = random.uniform(0, 10)
            self.progress += diff
            self.buffer = min(self.progress + diff2, 100)

    def paintEvent(self, event):
        w = self.width()
        h = self.height()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Nền
        painter.fillRect(0, 0, w, h, self.bg_color)

        # Buffer
        buffer_width = w * (self.buffer / 100)
        painter.fillRect(0, 0, buffer_width, h, self.buffer_color)

        # Value
        value_width = w * (self.progress / 100)
        painter.fillRect(0, 0, value_width, h, self.value_color)

        # Dotted effect (chạy từ phải sang trái)
        elapsed = (time.time() - self.start_time) % 2  # 2 giây 1 chu kỳ
        if elapsed < 1:
            # Fade in + move từ ngoài phải vào
            t = self.curve.valueForProgress(elapsed / 1.0)
            opacity = int(50 * t)
            x = w + 50 - (w + 100) * t  # chạy từ ngoài phải vào ngoài trái
        else:
            # Fade out
            t = self.curve.valueForProgress((elapsed-1)/1.0)
            opacity = int(50 * (1-t))
            x = -50  # giữ ngoài trái

        painter.setBrush(QBrush(QColor(self.dotted_color.red(),
                                       self.dotted_color.green(),
                                       self.dotted_color.blue(),
                                       opacity)))
        dot_width = 6
        spacing = 10
        # vẽ dotted
        for i in range(-3, int(w/dot_width)+3):
            xpos = x + i * (dot_width + spacing)
            if 0 <= xpos <= w:
                painter.fillRect(xpos, 0, dot_width, h, painter.brush())

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = LinearBufferProgress()
#     w.setWindowTitle("Linear Buffer with Dotted Stream (Right to Left)")
#     w.show()
#     sys.exit(app.exec())
