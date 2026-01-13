from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Property

class Paper(QFrame):
    def __init__(self, parent=None, elevation=1, color="#FFFFFF", radius=8):
        super().__init__(parent)

        self._elevation = elevation
        self._color = QColor(color)
        self._radius = radius

        self._shadow_effect = QGraphicsDropShadowEffect(self)
        self._shadow_effect.setOffset(0, self._elevation)  # bóng đổ hướng xuống
        self._shadow_effect.setBlurRadius(self._blur_for_elevation(self._elevation))
        self._shadow_effect.setColor(QColor(0, 0, 0, 30 + self._elevation * 5))
        self.setGraphicsEffect(self._shadow_effect)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self._color.name()};
                border-radius: {self._radius}px;
            }}
        """)

    # --- Tính độ mờ của bóng dựa vào elevation ---
    def _blur_for_elevation(self, elevation: int) -> int:
        return max(4, min(64, elevation * 3))

    # --- Getter / Setter ---
    def getElevation(self) -> int:
        return self._elevation

    def setElevation(self, value: int):
        self._elevation = max(0, min(24, value))
        self._shadow_effect.setBlurRadius(self._blur_for_elevation(value))
        self._shadow_effect.setOffset(0, value)
        self._shadow_effect.setColor(QColor(0, 0, 0, 30 + value * 5))

    elevation = Property(int, getElevation, setElevation)

    def getColor(self) -> QColor:
        return self._color

    def setColor(self, color):
        self._color = QColor(color)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self._color.name()};
                border-radius: {self._radius}px;
            }}
        """)

    color = Property(QColor, getColor, setColor)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
    import sys

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    # Paper độ cao thấp
    paper1 = Paper(elevation=1)
    paper1.setFixedSize(200, 100)
    layout.addWidget(paper1)

    # Paper độ cao cao hơn
    paper2 = Paper(elevation=12, color="#FAFAFA")
    paper2.setFixedSize(200, 100)
    layout.addWidget(paper2)

    window.show()
    sys.exit(app.exec())
