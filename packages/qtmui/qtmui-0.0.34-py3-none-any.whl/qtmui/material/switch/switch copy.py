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
    """
    A switch component, styled like Material-UI Switch.

    The `Switch` component provides a toggle switch with animations, supporting checked, disabled, and
    custom color states, aligning with MUI Switch props. Inherits from IconButton props.

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget. Default is None.
    label : State, str, or None, optional
        Label text for the switch (qtmui-specific). Default is None.
    disabled : State or bool, optional
        If True, disables the switch. Default is False.
        Can be a `State` object for dynamic updates.
    defaultChecked : State or bool, optional
        Default checked state. Default is False.
        Can be a `State` object for dynamic updates.
    checked : State or bool, optional
        If True, the switch is checked. Default is False.
        Can be a `State` object for dynamic updates.
    onChange : State, Callable, or None, optional
        Callback fired when the state changes. Default is None.
        Can be a `State` object for dynamic updates.
    highlight : State or bool, optional
        If True, highlights the switch (qtmui-specific). Default is False.
        Can be a `State` object for dynamic updates.
    left : State or bool, optional
        If True, positions the handle on the left when disabled (qtmui-specific). Default is True.
        Can be a `State` object for dynamic updates.
    color : State, str, or None, optional
        Color of the switch ('default', 'primary', 'secondary', 'error', 'info', 'success', 'warning', or custom).
        Default is 'primary'.
        Can be a `State` object for dynamic updates.
    size : State, str, or None, optional
        Size of the switch ('small' or 'medium'). Default is 'small'.
        Can be a `State` object for dynamic updates.
    onClick : State, Callable, or None, optional
        Callback for click events (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    checkedIcon : State, QWidget, or None, optional
        Icon to display when checked. Default is None.
        Can be a `State` object for dynamic updates.
    icon : State, QWidget, or None, optional
        Icon to display when unchecked. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If True, disables the ripple effect. Default is False.
        Can be a `State` object for dynamic updates.
    edge : State, str, bool, or None, optional
        Aligns the switch ('start', 'end', or False). Default is False.
        Can be a `State` object for dynamic updates.
    id : State, str, or None, optional
        ID of the input element. Default is None.
        Can be a `State` object for dynamic updates.
    inputProps : State or Dict, optional
        Attributes for the input element (deprecated, use slotProps.input). Default is None.
        Can be a `State` object for dynamic updates.
    inputRef : State, Any, or None, optional
        Ref for the input element (deprecated, use slotProps.input.ref). Default is None.
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the input is required. Default is False.
        Can be a `State` object for dynamic updates.
    slotProps : State or Dict, optional
        Props for each slot (input, root, switchBase, thumb, track). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or Dict, optional
        Components for each slot (input, root, switchBase, thumb, track). Default is None.
        Can be a `State` object for dynamic updates.
    value : State, Any, or None, optional
        Value of the component. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QCheckBox, supporting IconButton props.

    Signals
    -------
    stateChanged : Signal(int)
        Emitted when the checked state changes.

    Notes
    -----
    - Retains `left` and `highlight` as qtmui-specific features.
    - `inputProps` and `inputRef` are deprecated; use `slotProps.input` instead.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiSwitch-root`.

    Demos:
    - Switch: https://qtmui.com/material-ui/qtmui-switch/

    API Reference:
    - Switch API: https://qtmui.com/material-ui/api/switch/
    """

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    stateChanged = Signal(int)

    VALID_COLORS = ['default', 'primary', 'secondary', 'error', 'info', 'success', 'warning']
    VALID_SIZES = ['small', 'medium']
    VALID_EDGES = ['start', 'end', False]
    SIZE_MAP = {
        "small": (48, 32, 0.24),
        "medium": (70, 38, 0.24)
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
        size: Optional[Union[State, str, None]]="small",
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
        super().__init__(parent, **kwargs)
        PyWidgetBase._setUpUi(self)
        self.theme = useTheme()
        self._widget_references = []

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
            value.valueChanged.connect(self.update_ui)

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
            value.valueChanged.connect(self.update_ui)

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

        self.setMaximumWidth(36 if self._size == "small" else 48)

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        # print('self._color___________________', self._color)
        PySwitchRootColor = component_styled[f"PySwitch"].get("styles").get("root").get(self._color)
        if component_styled[f"PySwitch"].get("styleOverrides"):
            PySwitchOverrideRootColor = component_styled[f"PySwitch"].get("styleOverrides").get("root").get(self._color)

        barColor = PySwitchRootColor["barColor"]
        handleColor = PySwitchRootColor["handleColor"]
        checkedColor = PySwitchRootColor["checkedColor"]
        pulseCheckedColor = PySwitchRootColor["pulseCheckedColor"]
        pulseUncheckedColor = PySwitchRootColor["pulseUncheckedColor"]

        if self._disabled:
            barColor = self.theme.palette.grey._400 if self.theme.palette.mode == "light" else self.theme.palette.grey._600
        self._bar_brush = QBrush(barColor)
        self._bar_checked_brush = QBrush(checkedColor)
        # self._disabled = not self._disabled

        self._handle_brush = QBrush(handleColor)
        self._handle_checked_brush = QBrush(QColor(checkedColor))

        self._pulse_unchecked_animation = QBrush(QColor(self.theme.palette.grey._100))
        # self._pulse_unchecked_animation = QBrush(QColor(pulseUncheckedColor))
        self._pulse_checked_animation = QBrush(QColor(pulseCheckedColor))

        self.setContentsMargins(0, 0, 0, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # ms

        self._pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self._pulse_anim.setDuration(350)  # ms
        

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self._pulse_anim)

        self.stateChanged.connect(self.setup_animation)

        # tạo con trỏ chuột hình bàn tay khi hover chuột qua Button
        if self._disabled == True:
            self.setEnabled(False)
        else:
            self.setCursor(Qt.PointingHandCursor)

        if self._defaultChecked:
            self.setChecked(True)

        if self._checked:
            self.setChecked(True)

        self._size_data = self.SIZE_MAP.get(self._size, self.SIZE_MAP["medium"])

        self._pulse_anim.setStartValue(self._size_data[2] * self._size_data[1])
        self._pulse_anim.setEndValue(self._size_data[2] * self._size_data[1] * 2)
        


    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

        
    def sizeHint(self):
        return QSize(self._size_data[0], self._size_data[1])

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def mouseReleaseEvent(self, e):
        if self._onChange:
            if isinstance(self._checked, bool):
                self._onChange(self.isChecked())
        return super().mouseReleaseEvent(e)

    @Slot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        contRect = self.contentsRect()
        handleRadius = round(self._size_data[2] * contRect.height()) - (3 if self._size == "small" else 2)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)

        barRect = QRectF(
            0, 0, contRect.width() - 2* handleRadius, 0.50 * contRect.height() + 2
        )

        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        trailLength = contRect.width() - 2 * handleRadius 

        if self._disabled == False:
            if self.isChecked():
                xPos = (
                    contRect.x()
                    + handleRadius
                    + trailLength * self._handle_position
                    - (9 if self._size == "small" else 11)
                )
            else:
                xPos = (
                    contRect.x()
                    + handleRadius
                    + trailLength * self._handle_position
                    + (8 if self._size == "small" else 10)
                )

            if self._pulse_anim.state() == QPropertyAnimation.Running:
                p.setBrush(
                    self._pulse_checked_animation
                    if self.isChecked()
                    else self._pulse_unchecked_animation
                )
                p.drawEllipse(
                    QPointF(xPos, barRect.center().y()),
                    self._pulse_radius,
                    self._pulse_radius,
                )

            if self.isChecked():
                p.setBrush(self._bar_checked_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_brush)
                p.drawEllipse(
                    QPointF(xPos, barRect.center().y()), handleRadius, handleRadius
                )

            else:
                p.setBrush(self._bar_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_brush)
                p.drawEllipse(
                    QPointF(xPos, barRect.center().y()), handleRadius, handleRadius
                )

            p.end()

        else:
            xPos_1 = barRect.top() + 7 if self._size == "small" else 17
            xPos_2 = barRect.width()

            if self._left == True:
                p.setBrush(self._bar_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_brush)
                p.drawEllipse(
                    QPointF(xPos_1, barRect.center().y()), handleRadius, handleRadius
                )

            else:
                p.setBrush(self._bar_checked_brush)
                p.drawRoundedRect(barRect, rounding, rounding)
                p.setBrush(self._handle_brush)
                p.drawEllipse(
                    QPointF(xPos_2, barRect.center().y()),
                    handleRadius,
                    handleRadius,
                )

            p.end()

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()

