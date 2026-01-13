from typing import Callable, List, Optional, Union, Dict, Any

from qtmui.hooks import State

from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
    QPoint,
    QPointF,
    QRectF,
    QEasingCurve,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    Slot,
    Property,
)

from PySide6.QtWidgets import QCheckBox, QWidget
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter

from qtmui.material.styles import useTheme

from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

class Switch(QCheckBox):
    """
    Switch kiểu Material UI (React):
    - Handle nhỏ hơn bar
    - Handle nằm trong bar
    - Unchecked: handle đồng tâm bo tròn trái
    - Checked: handle đồng tâm bo tròn phải
    """

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    SIZE_MAP: Dict[str, Dict] = {
        "small": {
            "size": QSize(35, int(46 * 45 / 58)),
            "bar_ratio": 0.48,      # barHeight / contentHeight
            "handle_ratio": 0.18,   # handleRadius / contentHeight
            "pulse_ratio": 1.6,    # pulseRadius / barRadius
            "pulse_anim_start": round(10*46/58),
            "pulse_anim_end": round(20*46/58),
        },
        "medium": {
            "size": QSize(45, 45),
            "bar_ratio": 0.48,
            "handle_ratio": 0.20,
            "pulse_ratio": 1.5,
            "pulse_anim_start": 10,
            "pulse_anim_end": 20,
        },
    }

    def __init__(
        self,
        parent=None,
        size: str = "medium",
        color_checked: str = "#1976D2",
        color_unchecked: str = "#BDBDBD",
        handle_color: str = "#FFFFFF",
        **kwargs
    ):
        super().__init__(parent)

        self._key = None
        self._color = "color"
        self._size = size
        self._value = None

        self._size_key = size
        self._cfg = self.SIZE_MAP[self._size_key]

        # ---- BRUSHES ----
        self._bar_brush = QBrush(QColor(color_unchecked))
        self._bar_checked_brush = QBrush(QColor(color_checked))
        self._handle_brush = QBrush(QColor(handle_color))
        self._handle_checked_brush = QBrush(QColor(handle_color))

        self._pulse_unchecked_brush = QBrush(QColor(0, 0, 0, 40))
        self._pulse_checked_brush = QBrush(QColor(color_checked).lighter(160))

        # ---- STATE ----
        self._handle_position = 0.0
        self._pulse_radius = 0.0

        # ---- ANIMATION ----
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(180)

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(300)
        
        self.anim_group = QSequentialAnimationGroup(self)
        self.anim_group.addAnimation(self.animation)
        self.anim_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self._setup_animation)

        self.setCursor(Qt.PointingHandCursor)
        self.setContentsMargins(4, 0, 4, 0)

    # ------------------------------------------------------------
    # SIZE / HIT
    # ------------------------------------------------------------

    def sizeHint(self) -> QSize:
        return self._cfg["size"]

    def hitButton(self, pos: QPoint) -> bool:
        return self.contentsRect().contains(pos)

    # ------------------------------------------------------------
    # ANIMATION
    # ------------------------------------------------------------

    @Slot(int)
    def _setup_animation(self, value: int):
        self.anim_group.stop()

        self.animation.setStartValue(self._handle_position)
        self.animation.setEndValue(1.0 if value else 0.0)

        bar_radius = (self._cfg["bar_ratio"] * self.contentsRect().height()) / 2
        self.pulse_anim.setStartValue(bar_radius * 0.6)
        self.pulse_anim.setEndValue(bar_radius * self._cfg["pulse_ratio"])

        self.anim_group.start()

    # ------------------------------------------------------------
    # PAINT
    # ------------------------------------------------------------

    def paintEvent(self, e: QPaintEvent):
        contRect = self.contentsRect()

        bar_height = self._cfg["bar_ratio"] * contRect.height()
        bar_radius = bar_height / 2
        handle_radius = self._cfg["handle_ratio"] * contRect.height()

        p = QPainter(self)
        p.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        p.setPen(self._transparent_pen)

        # ---- BAR RECT ----
        barRect = QRectF(
            contRect.x(),
            0,
            contRect.width(),
            bar_height,
        )
        barRect.moveCenter(contRect.center())

        # ---- HANDLE POS (MUI LOGIC) ----
        left_x = barRect.left() + bar_radius
        right_x = barRect.right() - bar_radius
        xPos = left_x + (right_x - left_x) * self._handle_position
        yPos = barRect.center().y()

        # ---- PULSE ----
        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_brush
                if self.isChecked()
                else self._pulse_unchecked_brush
            )
            p.drawEllipse(
                QPointF(xPos, yPos),
                self._pulse_radius,
                self._pulse_radius,
            )

        # ---- BAR ----
        p.setBrush(
            self._bar_checked_brush
            if self.isChecked()
            else self._bar_brush
        )
        p.drawRoundedRect(barRect, bar_radius, bar_radius)

        # ---- HANDLE ----
        p.setBrush(
            self._handle_checked_brush
            if self.isChecked()
            else self._handle_brush
        )
        p.drawEllipse(
            QPointF(xPos, yPos),
            handle_radius,
            handle_radius,
        )

        p.end()

    # ------------------------------------------------------------
    # PROPERTIES (ANIMATED)
    # ------------------------------------------------------------

    @Property(float)
    def handle_position(self) -> float:
        return self._handle_position

    @handle_position.setter
    def handle_position(self, v: float):
        self._handle_position = v
        self.update()

    @Property(float)
    def pulse_radius(self) -> float:
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, v: float):
        self._pulse_radius = v
        self.update()
