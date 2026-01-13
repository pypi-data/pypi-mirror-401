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
from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter, QEnterEvent

from qtmui.material.styles import useTheme

from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param


class Switch(QCheckBox):
    _transparent_pen = QPen(Qt.transparent)

    VALID_COLORS = ['default', 'primary', 'secondary', 'error', 'info', 'success', 'warning']
    VALID_SIZES = ['small', 'medium']
    VALID_EDGES = ['start', 'end', False]
    SIZE_MAP = {
        "small": {
            "size": QSize(46, int(46 * 45 / 58)),
            "bar_ratio": 0.48,
            "handle_ratio": 0.18,
        },
        "medium": {
            "size": QSize(58, 45),
            "bar_ratio": 0.48,
            "handle_ratio": 0.20,
        },
    }

    def __init__(
        self,
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

        # Set properties with validation
        self._set_label(label)
        self._set_disabled(disabled)
        self._set_defaultChecked(defaultChecked)
        self._set_checked(checked)
        self._set_onChange(onChange)
        self._set_highlight(highlight)
        self._set_left(left)
        self._set_color(color)
        self._set_size(size)
        self._set_onClick(onClick)
        self._set_checkedIcon(checkedIcon)
        self._set_icon(icon)
        self._set_classes(classes)
        self._set_sx(sx)
        self._set_disableRipple(disableRipple)
        self._set_edge(edge)
        self._set_id(id)
        self._set_inputProps(inputProps)
        self._set_inputRef(inputRef)
        self._set_required(required)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_value(value)

        self._init_ui()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.switch", param_name="label", supported_signatures=Union[State, str, type(None)])
    def _set_label(self, value):
        self._label = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_label(self):
        return self._label.value if isinstance(self._label, State) else self._label

    @_validate_param(file_path="qtmui.material.switch", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        self._disabled = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_disabled(self):
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.switch", param_name="defaultChecked", supported_signatures=Union[State, bool])
    def _set_defaultChecked(self, value):
        self._defaultChecked = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_defaultChecked(self):
        return self._defaultChecked.value if isinstance(self._defaultChecked, State) else self._defaultChecked

    # @_validate_param(file_path="qtmui.material.switch", param_name="checked", supported_signatures=Union[State, bool])
    def _set_checked(self, value):
        self._checked = value

    def _get_checked(self):
        return self._checked.value if isinstance(self._checked, State) else self._checked

    @_validate_param(file_path="qtmui.material.switch", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        self._onChange = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_onChange(self):
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.switch", param_name="highlight", supported_signatures=Union[State, bool])
    def _set_highlight(self, value):
        self._highlight = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_highlight(self):
        return self._highlight.value if isinstance(self._highlight, State) else self._highlight

    @_validate_param(file_path="qtmui.material.switch", param_name="left", supported_signatures=Union[State, bool])
    def _set_left(self, value):
        self._left = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_left(self):
        return self._left.value if isinstance(self._left, State) else self._left

    @_validate_param(file_path="qtmui.material.switch", param_name="color", supported_signatures=Union[State, str, type(None)], valid_values=VALID_COLORS)
    def _set_color(self, value):
        self._color = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_color(self):
        color = self._color.value if isinstance(self._color, State) else self._color
        return color if color in self.VALID_COLORS or isinstance(color, str) else 'primary'

    @_validate_param(file_path="qtmui.material.switch", param_name="size", supported_signatures=Union[State, str, type(None)], valid_values=VALID_SIZES)
    def _set_size(self, value):
        self._size = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_size(self):
        size = self._size.value if isinstance(self._size, State) else self._size
        return size if size in self.VALID_SIZES else 'small'

    @_validate_param(file_path="qtmui.material.switch", param_name="onClick", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClick(self, value):
        self._onClick = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_onClick(self):
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    @_validate_param(file_path="qtmui.material.switch", param_name="checkedIcon", supported_signatures=Union[State, QWidget, type(None)])
    def _set_checkedIcon(self, value):
        self._checkedIcon = value
        if isinstance(value, QWidget):
            self._widget_references.append(value)
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_checkedIcon(self):
        return self._checkedIcon.value if isinstance(self._checkedIcon, State) else self._checkedIcon

    @_validate_param(file_path="qtmui.material.switch", param_name="icon", supported_signatures=Union[State, QWidget, type(None)])
    def _set_icon(self, value):
        self._icon = value
        if isinstance(value, QWidget):
            self._widget_references.append(value)
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_icon(self):
        return self._icon.value if isinstance(self._icon, State) else self._icon

    @_validate_param(file_path="qtmui.material.switch", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.switch", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
    def _set_sx(self, value):
        self._sx = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.switch", param_name="disableRipple", supported_signatures=Union[State, bool])
    def _set_disableRipple(self, value):
        self._disableRipple = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_disableRipple(self):
        return self._disableRipple.value if isinstance(self._disableRipple, State) else self._disableRipple

    @_validate_param(file_path="qtmui.material.switch", param_name="edge", supported_signatures=Union[State, str, bool, type(None)], valid_values=VALID_EDGES)
    def _set_edge(self, value):
        self._edge = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_edge(self):
        edge = self._edge.value if isinstance(self._edge, State) else self._edge
        return edge if edge in self.VALID_EDGES else False

    @_validate_param(file_path="qtmui.material.switch", param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        self._id = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_id(self):
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path="qtmui.material.switch", param_name="inputProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_inputProps(self, value):
        self._inputProps = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_inputProps(self):
        return self._inputProps.value if isinstance(self._inputProps, State) else self._inputProps

    # @_validate_param(file_path="qtmui.material.switch", param_name="inputRef", supported_signatures=Union[State, type(None)])
    def _set_inputRef(self, value):
        self._inputRef = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_inputRef(self):
        return self._inputRef.value if isinstance(self._inputRef, State) else self._inputRef

    @_validate_param(file_path="qtmui.material.switch", param_name="required", supported_signatures=Union[State, bool])
    def _set_required(self, value):
        self._required = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_required(self):
        return self._required.value if isinstance(self._required, State) else self._required

    @_validate_param(file_path="qtmui.material.switch", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.switch", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.switch", param_name="value", supported_signatures=Union[State, type(None)])
    def _set_value(self, value):
        self._value = value
        if isinstance(value, State):
            value.valueChanged.connect(self._init_ui)

    def _get_value(self):
        return self._value.value if isinstance(self._value, State) else self._value
    
    def _init_ui(self):
        
        self._cfg = self.SIZE_MAP[self._size]

        # STATE
        self._handle_position = 0.0
        self._pulse_radius = 0.0
        self._hover_opacity = 0.0

        # ANIMATIONS
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(300)

        self.hover_anim = QPropertyAnimation(self, b"hover_opacity", self)
        self.hover_anim.setDuration(160)
        self.hover_anim.setEasingCurve(QEasingCurve.OutCubic)

        self.anim_group = QSequentialAnimationGroup(self)
        self.anim_group.addAnimation(self.animation)
        self.anim_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self._setup_animation)
        
        self.setCursor(Qt.PointingHandCursor)
        self.setContentsMargins(4, 0, 4, 0)
        self.setMouseTracking(True)
        
        self._set_stylesheet()
        
        # tạo con trỏ chuột hình bàn tay khi hover chuột qua Button
        if self._disabled == True:
            self.setEnabled(False)
        else:
            self.setCursor(Qt.PointingHandCursor)

        if self._defaultChecked:
            self.setChecked(True)

        if self._checked:
            self.setChecked(True)

        # gán sau khi đã setChecked ban đầu nếu có
        if self._get_onChange():
            self.stateChanged.connect(self._get_onChange())
            
        

    # --------------------------------------------------
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

        self._handle_brush = QBrush(QColor(handleColor))
        self._handle_checked_brush = QBrush(QColor(handleColor))

        # self._pulse_unchecked_brush = QBrush(QColor(self.theme.palette.grey._100))
        self._pulse_unchecked_brush = QBrush(QColor(self.theme.palette.grey._500).lighter(120))
        self._pulse_checked_brush = QBrush(QColor(pulseCheckedColor))
        
        self._hover_unchecked_brush = QBrush(QColor(self.theme.palette.grey._500).lighter(120))
        self._hover_checked_brush = QBrush(QColor(pulseCheckedColor).lighter(120))


    # --------------------------------------------------
    def sizeHint(self):
        return self._cfg["size"] if hasattr(self, "_cfg") else QSize(58, 45)


    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @Slot(int)
    def _setup_animation(self, value):

        self.anim_group.stop()

        contRect = self.contentsRect()
        handle_radius = self._cfg["handle_ratio"] * contRect.height()

        self.animation.setEndValue(1.0 if value else 0.0)

        # if self._init_done:
        if hasattr(self, "_hovered"):
            self.pulse_anim.setStartValue(handle_radius * 1.1)
            self.pulse_anim.setEndValue(min(contRect.height() / 2, handle_radius * 2.2))

        self.anim_group.start()

    # --------------------------------------------------
    def enterEvent(self, event: QEnterEvent):
        self._hovered = True
        self.hover_anim.stop()
        self.hover_anim.setEndValue(1.0)
        self.hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover_anim.stop()
        self.hover_anim.setEndValue(0.0)
        self.hover_anim.start()
        super().leaveEvent(event)

    # --------------------------------------------------
    def paintEvent(self, e: QPaintEvent):
        if not hasattr(self, "_bar_brush"):
            return
        
        contRect = self.contentsRect()

        bar_height = self._cfg["bar_ratio"] * contRect.height()
        bar_radius = bar_height / 2
        handle_radius = self._cfg["handle_ratio"] * contRect.height()

        # 👉 SAFE RADIUS: bảo đảm hover không tràn
        hover_radius = handle_radius * 2.2

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(self._transparent_pen)

        # ---- BAR (TRACK) ----
        bar_left = contRect.x() + handle_radius
        bar_width = contRect.width() - 2 * handle_radius

        barRect = QRectF(bar_left, 0, bar_width, bar_height)
        barRect.moveCenter(contRect.center())

        # ---- HANDLE TRACK (CHUẨN MUI) ----
        left_x = barRect.left() + bar_radius
        right_x = barRect.right() - bar_radius

        xPos = left_x + (right_x - left_x) * self._handle_position
        yPos = barRect.center().y()

        # ---- HOVER SOFT ----
        if self._hover_opacity > 0:
            if self.isChecked():
                p.setBrush(self._hover_checked_brush)
            else:
                p.setBrush(self._hover_unchecked_brush)
                
            p.setOpacity(self._hover_opacity * 0.35)
            p.drawEllipse(QPointF(xPos, yPos), hover_radius, hover_radius)
            p.setOpacity(1.0)

        # ---- PULSE ----
        if self.pulse_anim.state() == QPropertyAnimation.Running and hasattr(self, "_hovered"):
            p.setBrush(
                self._pulse_checked_brush
                if self.isChecked()
                else self._pulse_unchecked_brush
            )
            p.drawEllipse(QPointF(xPos, yPos), self._pulse_radius, self._pulse_radius)

        # ---- BAR ----
        p.setBrush(self._bar_checked_brush if self.isChecked() else self._bar_brush)
        p.drawRoundedRect(barRect, bar_radius, bar_radius)

        # ---- HANDLE ----
        p.setBrush(self._handle_checked_brush if self.isChecked() else self._handle_brush)
        p.drawEllipse(QPointF(xPos, yPos), handle_radius, handle_radius)

        p.end()

    # --------------------------------------------------
    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, v):
        self._handle_position = v
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, v):
        self._pulse_radius = v
        self.update()

    @Property(float)
    def hover_opacity(self):
        return self._hover_opacity

    @hover_opacity.setter
    def hover_opacity(self, v):
        self._hover_opacity = v
        self.update()
