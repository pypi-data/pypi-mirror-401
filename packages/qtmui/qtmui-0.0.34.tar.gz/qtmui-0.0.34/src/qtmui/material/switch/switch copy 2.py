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

class Switch(QCheckBox, PyWidgetBase):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    SIZE_MAP = {
        "small": {
            "size": QSize(46, 46*45/58),
            "handle_ratio": 0.24,
            "bar_ratio": 0.40,
            "pulse_anim_start": round(10*46/58),
            "pulse_anim_end": round(20*46/58),
        },
        "medium": {
            "size": QSize(58, 45),
            "handle_ratio": 0.24, # handleRadius/contentHeight 24% => handleCircleDiameter/contentHeight = 0.48
            "bar_ratio": 0.40, # barHeight/contentHeight
            "pulse_anim_start": 10,
            "pulse_anim_end": 20,
        },
    }

    def __init__(self,
        parent=None,
        label: Optional[Union[str, State, Callable]] = None,
        disabled: Union[State, bool]=False,
        defaultChecked: Union[State, bool]=False,
        checked: Union[State, bool]=False,
        onChange: Optional[Union[State, Callable, None]]=None,
        highlight: Union[State, bool]=False,
        left: Union[State, bool]=True,
        color: Optional[Union[State, str, None]]="primary",
        size: Optional[Union[State, str, None]]="medium",
        onClick: Optional[Union[State, Callable, None]]=None,
        checkedIcon: Optional[Union[State, QWidget, None]]=None,
        icon: Optional[Union[State, QWidget, None]]=None,
        classes: Optional[Union[State, Dict, None]]=None,
        sx: Optional[Union[State, List, Dict, Callable, None]]=None,
        disableRipple: Union[State, bool]=False,
        edge: Optional[Union[State, str, bool, None]]=False,
        id: Optional[Union[State, str, None]]=None,
        inputProps: Optional[Union[State, Dict, None]]=None,
        inputRef: Optional[Union[State, Any, None]]=None,
        required: Union[State, bool]=False,
        slotProps: Optional[Union[State, Dict, None]]=None,
        slots: Optional[Union[State, Dict, None]]=None,
        value: Optional[Union[State, Any, None]]=None,
        **kwargs
        ):
        super().__init__(parent)
        
        self._key = None
        self._color = color
        self._size = size
        self._value = None
        
        self._init_ui()
        
    def _init_ui(self):
        
        self._cfg = self.SIZE_MAP[self._size]
        self._handle_ratio = self._cfg["handle_ratio"]
        self._bar_ratio = self._cfg["bar_ratio"]

        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        
        self._handle_position = 0
        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(self._cfg["pulse_anim_start"])
        self.pulse_anim.setEndValue(self._cfg["pulse_anim_end"])

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)
        
        self._set_stylesheet()


    def _set_stylesheet(self):
        self.theme = useTheme()

        theme_components = self.theme.components

        # print('self._color___________________', self._color)
        PySwitchRootColor = theme_components[f"PySwitch"].get("styles").get("root").get(self._color)
        if theme_components[f"PySwitch"].get("styleOverrides"):
            PySwitchOverrideRootColor = theme_components[f"PySwitch"].get("styleOverrides").get("root").get(self._color)

        barColor = PySwitchRootColor["barColor"]
        handleColor = PySwitchRootColor["handleColor"]
        checkedColor = PySwitchRootColor["checkedColor"]
        pulseCheckedColor = PySwitchRootColor["pulseCheckedColor"]
        pulseUncheckedColor = PySwitchRootColor["pulseUncheckedColor"]

        # if self._disabled:
        #     barColor = self.theme.palette.grey._400 if self.theme.palette.mode == "light" else self.theme.palette.grey._600
            
        self._bar_brush = QBrush(barColor)
        self._bar_checked_brush = QBrush(checkedColor)
        if self._color != "default":
            self._bar_checked_brush = QBrush(QColor(getattr(self.theme.palette, self._color).light))
        else:
            self._bar_checked_brush = QBrush(QColor(Qt.gray))

        self._handle_brush = QBrush(handleColor)
        self._handle_checked_brush = QBrush(QColor(checkedColor))

        self._pulse_unchecked_brush = QBrush(QColor(self.theme.palette.grey._100))
        self._pulse_checked_brush = QBrush(QColor(pulseCheckedColor))


    def sizeHint(self):
        return self._cfg["size"] if hasattr(self, "_cfg") else QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        if not hasattr(self, "_bar_brush"):
            return
        
        contRect = self.contentsRect()
        handleRadius = round(self._handle_ratio * contRect.height())
        
        # print("contRect", contRect)

        p = QPainter(self)
        p.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, self._bar_ratio * contRect.height()
        )
        print("barRect", barRect)
        
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_brush if
                self.isChecked() else self._pulse_unchecked_brush)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        print('pos', pos)
        self._handle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()