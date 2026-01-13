import sys
import random
from PySide6.QtWidgets import (QFrame, QWidget, QVBoxLayout)
from PySide6.QtCore import (Qt, QVariantAnimation, QSize)
from PySide6.QtGui import (QPen, QPainter, QColor)
from PySide6.QtCore import Qt, QVariantAnimation, QEasingCurve

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from ..widget_base import PyWidgetBase

from qtmui.material.styles import useTheme

class Arc:
    def __init__(self, 
                 color=None,
                 diameter=None
                 ):
        self.diameter = diameter
        self.color = QColor(color)
        self.span = random.randint(40, 150)
        self.direction = 1 if random.randint(10, 15) % 2 == 0 else -1
        self.startAngle = random.randint(40, 200)


class ArcWidget(QWidget):
    def __init__(self, 
                 parent=None, 
                 color="#888888",
                 size="medium"
                 ):
        super().__init__(parent)
        self.initUI()

        if size == "small":
            self._diameter = 24
            self._width = 26
        elif size == "medium":
            self._diameter = 32
            self._width = 34
        else:
            self._diameter = 40
            self._width = 42

        self.arc = Arc(color=color, diameter=self._diameter)
        self.setFixedSize(QSize(self._width, self._width))
        self.startAnime()

    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)

    def set_color(self, color):
        self.arc.color = color

    def startAnime(self):
        # Animation chính để quay vòng cung, sử dụng Linear để quay đều
        self.anim = QVariantAnimation(self, duration=1000)
        self.anim.setStartValue(0)
        self.anim.setEndValue(360)
        self.anim.setEasingCurve(QEasingCurve.Linear)
        self.anim.valueChanged.connect(self.update)

        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(self.arc.color), 2, Qt.SolidLine))

        # Tính toán độ dài của cung tăng dần từ 0-180 độ và giảm dần từ 180-360 độ
        current_angle = self.anim.currentValue()
        if current_angle <= 180:
            # Tăng dần từ 40 đến 240 (ví dụ)
            span_length = 40 + (current_angle / 180) * 200
        else:
            # Giảm dần từ 240 về 40
            span_length = 240 - ((current_angle - 180) / 180) * 200

        self.arc.span = span_length

        # Vẽ cung với độ dài thay đổi theo vị trí trong vòng quay
        painter.drawArc(
            1, 1, self.arc.diameter, self.arc.diameter,
            self.anim.currentValue() * 16 * self.arc.direction + self.arc.startAngle * 16,
            int(self.arc.span) * 16
        )

        # Khi kết thúc một vòng, bắt đầu lại mà không cần dừng
        if self.anim.currentValue() == 360:
            self.anim.setCurrentTime(0)
            self.anim.start()


class CircularProgress(QFrame, PyWidgetBase):
    def __init__(self, 
                 key=None, 
                 color: str = "primary",
                 size: str = "medium",
                 variant: str = "determinate", # "determinate" | 
                 value: int = 0, # "determinate" | 
                 thickness: int = 0, # "determinate" | 
                 sx: object = None, # "determinate" | 
                 ):
        super().__init__()

        self._key = key
        self._color = color
        self._size = size

        self._init_ui()

        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)
        self.slot_set_stylesheet()

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.arcwidget = ArcWidget(size=self._size)
        self.layout().addWidget(self.arcwidget)
        self.setStyleSheet("background-color: transparent;border: none;")


    def _set_stylesheet(self):
        theme = useTheme()
        is_light_mode = theme.palette.mode == 'light'
        if self._color in ['primary', 'secondary', 'info', 'success', 'warning', 'error']:
            palette_color: PaletteColor = getattr(theme.palette, self._color)
            self._circle_color = palette_color.main
        else: # inherit
            self._circle_color = theme.palette.grey._800 if is_light_mode else theme.palette.common.white

        self.arcwidget.set_color(self._circle_color)


        """
        https://anjalp.github.io/PySide2extn/
        """