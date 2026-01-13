from typing import Optional, Union, Callable, Dict, Any, List
from PySide6.QtCore import QSize, Qt, Signal, QPoint, QRectF, QPointF, QPropertyAnimation, Property
from PySide6.QtGui import QColor, QPainter, QPainterPath, QMouseEvent
from PySide6.QtWidgets import QProxyStyle, QSlider, QWidget, QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy

from ...common.style_sheet import FluentStyleSheet, themeColor
from ...common.overload import singledispatchmethod

from .sliders import (
    DoubleSlider, 
    RangeSlider, 
    DoubleRangeSlider, 
    MultiHandleRangeSlider, 
    LabeledSlider, 
    LabeledRangeSlider, 
    LabeledDoubleSlider, 
    LabeledDoubleRangeSlider
)

from qtmui.hooks import State
from qtmui.material.styles import useTheme




class Slider(QFrame):
    """
    A slider component, styled like Material-UI Slider.

    The `Slider` component allows users to select a value or range by dragging handles along a track.
    It supports single or range sliders, marks, and accessibility features, aligning with MUI Slider props.
    Inherits from native component props.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget. Default is None.
    orientation : State or str, optional
        Orientation of the slider ('horizontal' or 'vertical'). Default is 'horizontal'.
        Can be a `State` object for dynamic updates.
    valueLabelDisplay : State or str, optional
        Controls value label display ('auto', 'on', 'off'). Default is 'auto'.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides (replaces style). Default is None.
        Can be a `State` object for dynamic updates.
    ariaLabel : State or str, optional
        The label of the slider for accessibility. Default is None.
        Can be a `State` object for dynamic updates.
    ariaLabelledby : State or str, optional
        The id of the element containing a label for the slider. Default is None.
        Can be a `State` object for dynamic updates.
    ariaValuetext : State or str, optional
        A user-friendly name for the current value. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        Color of the component ('primary', 'secondary', etc., or hex). Default is 'primary'.
        Can be a `State` object for dynamic updates.
    defaultValue : State, List[int], int, or None, optional
        Default value of the slider. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableSwap : State or bool, optional
        If True, prevents thumb swapping in range slider. Default is False.
        Can be a `State` object for dynamic updates.
    getAriaLabel : State or Callable, optional
        Function to format thumb labels. Default is None.
        Can be a `State` object for dynamic updates.
    getAriaValueText : State or Callable, optional
        Function to format value text. Default is None.
        Can be a `State` object for dynamic updates.
    marks : State, List[Dict], or bool, optional
        Marks on the slider. Default is False.
        Can be a `State` object for dynamic updates.
    max : State or int, optional
        Maximum value of the slider. Default is 100.
        Can be a `State` object for dynamic updates.
    min : State or int, optional
        Minimum value of the slider. Default is 0.
        Can be a `State` object for dynamic updates.
    name : State or str, optional
        Name of the hidden input element. Default is None.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback when value changes. Default is None.
        Can be a `State` object for dynamic updates.
    onChangeCommitted : State or Callable, optional
        Callback when mouseup occurs. Default is None.
        Can be a `State` object for dynamic updates.
    scale : State or Callable, optional
        Transformation function for slider values. Default is lambda x: x.
        Can be a `State` object for dynamic updates.
    shiftStep : State or int, optional
        Step size for Page Up/Down or Shift + Arrow. Default is 10.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        Size of the slider ('small', 'medium'). Default is 'medium'.
        Can be a `State` object for dynamic updates.
    slotProps : State or Dict, optional
        Props for slot components. Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or Dict, optional
        Components for slots. Default is None.
        Can be a `State` object for dynamic updates.
    step : State or int, optional
        Step size for the slider. Default is 1.
        Can be a `State` object for dynamic updates.
    tabIndex : State or int, optional
        Tab index of the hidden input. Default is None.
        Can be a `State` object for dynamic updates.
    track : State, str, or bool, optional
        Track presentation ('normal', 'inverted', False). Default is 'normal'.
        Can be a `State` object for dynamic updates.
    value : State, List[int], int, or None, optional
        Current value of the slider. Default is None.
        Can be a `State` object for dynamic updates.
    valueLabelFormat : State or Callable, optional
        Format function for value label. Default is lambda x: x.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QSlider, supporting native component props.

    Signals
    -------
    clicked : Signal(int)
        Emitted when the slider is clicked, with the current value.
    valueChanged : Signal(int)
        Emitted when the slider value changes.

    Notes
    -----
    - Existing parameters (4) are retained; 27 new parameters added to align with MUI Slider.
    - Supports range sliders with multiple thumbs.
    - MUI classes applied: `MuiSlider-root`.
    - Integrates with `SliderHandle` for dragging and marks.

    Demos:
    - Slider: https://qtmui.com/material-ui/qtmui-slider/

    API Reference:
    - Slider API: https://qtmui.com/material-ui/api/slider/
    """


    clicked = Signal(int)

    # Signals tương tự MUI behavior
    valueChanged = Signal(object)
    changeCommitted = Signal(object)

    VALID_COLORS = ['primary', 'secondary', 'error', 'info', 'success', 'warning']
    VALID_SIZES = ['small', 'medium']
    VALID_ORIENTATIONS = ['horizontal', 'vertical']
    VALID_TRACKS = ['normal', 'inverted', False]
    VALID_VALUE_LABEL_DISPLAY = ['auto', 'off', 'on']

    def __init__(
        self,
        ariaLabel: Optional[str] = None,
        ariaLabelledby: Optional[str] = None,
        ariaValuetext: Optional[str] = None,
        classes: Optional[Dict[str, Any]] = None,
        color: Optional[str] = "primary",
        components: Optional[Dict[str, Any]] = None,
        componentsProps: Optional[Dict[str, Any]] = None,
        defaultValue: Optional[Union[int, float, List[Union[int, float]]]] = None,
        disabled: Optional[bool] = False,
        disableSwap: Optional[bool] = False,
        getAriaLabel: Optional[Callable[[int], str]] = None,
        getAriaValueText: Optional[Callable[[Union[int, float], int], str]] = None,
        marks: Optional[Union[bool, List[Dict[str, Any]]]] = False,
        max: Optional[Union[int, float]] = 100,
        min: Optional[Union[int, float]] = 0,
        name: Optional[str] = None,
        onChange: Optional[Callable[[Any, Any, int], None]] = None,
        onChangeCommitted: Optional[Callable[[Any, Any], None]] = None,
        orientation: Optional[str] = "horizontal",
        scale: Optional[Callable[[Any], Any]] = None,
        shiftStep: Optional[Union[int, float]] = 10,
        size: Optional[str] = "medium",
        slotProps: Optional[Dict[str, Any]] = None,
        slots: Optional[Dict[str, Any]] = None,
        step: Optional[Union[int, float, None]] = 1,
        sx: Optional[Union[Dict, Callable, str, List[Any]]] = None,
        tabIndex: Optional[int] = None,
        track: Optional[Union[str, bool]] = "normal",
        value: Optional[Union[int, float, List[Union[int, float]]]] = None,
        valueLabelDisplay: Optional[str] = "off",
        valueLabelFormat: Optional[Union[str, Callable[[Union[int, float], int], Any]]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # Gán toàn bộ props vào self
        self._ariaLabel = ariaLabel
        self._ariaLabelledby = ariaLabelledby
        self._ariaValuetext = ariaValuetext
        self._classes = classes
        self._color = color
        self._components = components
        self._componentsProps = componentsProps
        self._defaultValue = defaultValue
        self._disabled = disabled
        self._disableSwap = disableSwap
        self._getAriaLabel = getAriaLabel
        self._getAriaValueText = getAriaValueText
        self._marks = marks
        self._max = max
        self._min = min
        self._name = name
        self._onChange = onChange
        self._onChangeCommitted = onChangeCommitted
        self._orientation = orientation
        self._scale = scale
        self._shiftStep = shiftStep
        self._size = size
        self._slotProps = slotProps
        self._slots = slots
        self._step = step
        self._sx = sx
        self._tabIndex = tabIndex
        self._track = track
        self._value = value
        self._valueLabelDisplay = valueLabelDisplay
        self._valueLabelFormat = valueLabelFormat
        
        if self._orientation == 'horizontal':
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        # self.setStyleSheet("border: 1px solid red;")
        
        # MUI - Continuous sliders
        if isinstance(self._value, State):
            if isinstance(self._value.value, int):
                if self._valueLabelDisplay == 'on':
                    self.layout().addWidget(
                        LabeledSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._value.value,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                elif self._valueLabelDisplay == 'auto':
                    self.layout().addWidget(
                        LabeledSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._value.value,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                else: # off
                    self.layout().addWidget(
                        DoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._value.value,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
            elif isinstance(self._value.value, float):
                if self._valueLabelDisplay == 'on':
                    self.layout().addWidget(
                        LabeledDoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._value.value,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                elif self._valueLabelDisplay == 'auto':
                    self.layout().addWidget(
                        LabeledDoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._value.value,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                else: # off
                    self.layout().addWidget(
                        DoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._value.value,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
            elif isinstance(self._value.value, tuple) and len(self._value.value) == 2:
                if all(isinstance(x, int) for x in self._value.value):
                    self.layout().addWidget(
                        RangeSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                elif all(isinstance(x, float) for x in self._value.value):
                    self.layout().addWidget(
                        DoubleRangeSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
            elif isinstance(self._value.value, tuple) and len(self._value.value) > 2: # multi-handle range slider
                self.layout().addWidget(
                    MultiHandleRangeSlider(
                        color=self._color,
                        min=self._min,
                        max=self._max,
                        value=self._defaultValue,
                        onChange=self._onChange,
                        orientation=self._orientation,
                        step=self._step,
                        disabled=self._disabled
                    )
                )
            else: 
                print("Unsupported value type for Slider: Stateeeeeeeeeee", type(self._value.value))
        else:
            if isinstance(self._defaultValue, int):
                if self._valueLabelDisplay == 'on':
                    self.layout().addWidget(
                        LabeledSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                elif self._valueLabelDisplay == 'auto':
                    self.layout().addWidget(
                        LabeledSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                else: # off
                    self.layout().addWidget(
                        DoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
            elif isinstance(self._defaultValue, float):
                if self._valueLabelDisplay == 'on':
                    self.layout().addWidget(
                        LabeledDoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                elif self._valueLabelDisplay == 'auto':
                    self.layout().addWidget(
                        LabeledDoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
                else: # off
                    self.layout().addWidget(
                        DoubleSlider(
                            color=self._color,
                            min=self._min,
                            max=self._max,
                            value=self._defaultValue,
                            onChange=self._onChange,
                            orientation=self._orientation,
                            step=self._step,
                            disabled=self._disabled
                        )
                    )
            elif isinstance(self._defaultValue, tuple) and len(self._defaultValue) == 2:
                if all(isinstance(x, int) for x in self._defaultValue):
                    if self._valueLabelDisplay == 'on':
                        self.layout().addWidget(
                            LabeledRangeSlider(
                                color=self._color,
                                min=self._min,
                                max=self._max,
                                value=self._defaultValue,
                                onChange=self._onChange,
                                orientation=self._orientation,
                                step=self._step,
                                disabled=self._disabled
                            )
                        )
                    elif self._valueLabelDisplay == 'auto':
                        self.layout().addWidget(
                            LabeledRangeSlider(
                                color=self._color,
                                min=self._min,
                                max=self._max,
                                value=self._defaultValue,
                                onChange=self._onChange,
                                orientation=self._orientation,
                                step=self._step,
                                disabled=self._disabled
                            )
                        )
                    else: # off
                        self.layout().addWidget(
                            RangeSlider(
                                color=self._color,
                                min=self._min,
                                max=self._max,
                                value=self._defaultValue,
                                onChange=self._onChange,
                                orientation=self._orientation,
                                step=self._step,
                                disabled=self._disabled
                            )
                        )
                elif all(isinstance(x, float) for x in self._defaultValue):
                    if self._valueLabelDisplay == 'on':
                        self.layout().addWidget(
                            LabeledDoubleRangeSlider(
                                color=self._color,
                                min=self._min,
                                max=self._max,
                                value=self._defaultValue,
                                onChange=self._onChange,
                                orientation=self._orientation,
                                step=self._step,
                                disabled=self._disabled
                            )
                        )
                    elif self._valueLabelDisplay == 'auto':
                        self.layout().addWidget(
                            LabeledDoubleRangeSlider(
                                color=self._color,
                                min=self._min,
                                max=self._max,
                                value=self._defaultValue,
                                onChange=self._onChange,
                                orientation=self._orientation,
                                step=self._step,
                                disabled=self._disabled
                            )
                        )
                    else: # off
                        # Không hiển thị nhãn
                        self.layout().addWidget(
                            DoubleRangeSlider(
                                color=self._color,
                                min=self._min,
                                max=self._max,
                                value=self._defaultValue,
                                onChange=self._onChange,
                                orientation=self._orientation,
                                step=self._step,
                                disabled=self._disabled
                            )
                        )
            elif isinstance(self._defaultValue, tuple) and len(self._defaultValue) > 2: # multi-handle range slider
                self.layout().addWidget(
                    MultiHandleRangeSlider(
                        color=self._color,
                        min=self._min,
                        max=self._max,
                        value=self._defaultValue,
                        onChange=self._onChange,
                        orientation=self._orientation,
                        step=self._step,
                        disabled=self._disabled
                    )
                ) 
            else:
                print("Unsupported value type for Slider:", type(self._defaultValue))
        


class SliderHandle(QWidget):
    """ Slider handle """

    pressed = Signal()
    released = Signal()

    def __init__(self, parent: QSlider):
        super().__init__(parent=parent)
        self.setFixedSize(22, 22)
        self._radius = 5
        self.radiusAni = QPropertyAnimation(self, b'radius', self)
        self.radiusAni.setDuration(100)

    @Property(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.update()

    def enterEvent(self, e):
        self._startAni(6)

    def leaveEvent(self, e):
        self._startAni(5)

    def mousePressEvent(self, e):
        self._startAni(4)
        self.pressed.emit()

    def mouseReleaseEvent(self, e):
        self._startAni(6)
        self.released.emit()

    def _startAni(self, radius):
        self.radiusAni.stop()
        self.radiusAni.setStartValue(self.radius)
        self.radiusAni.setEndValue(radius)
        self.radiusAni.start()

    def paintEvent(self, e):
        if not hasattr(self, "theme"):
            self.theme = useTheme()
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # draw outer circle
        painter.setPen(QColor(0, 0, 0, 90 if self.theme.palette.mode == "dark" else 25))
        painter.setBrush(QColor(69, 69, 69) if self.theme.palette.mode == "dark" else Qt.GlobalColor.white)
        painter.drawEllipse(self.rect().adjusted(1, 1, -1, -1))

        # draw innert circle
        painter.setBrush(themeColor())
        painter.drawEllipse(QPoint(11, 11), self.radius, self.radius)


class ClickableSlider(QSlider):
    """ A slider can be clicked """

    clicked = Signal(int)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        if self.orientation() == Qt.Orientation.Horizontal:
            value = int(e.pos().x() / self.width() * self.maximum())
        else:
            value = int((self.height()-e.pos().y()) /
                        self.height() * self.maximum())

        self.setValue(value)
        self.clicked.emit(self.value())



class HollowHandleStyle(QProxyStyle):
    """ Hollow handle style """

    def __init__(self, config: dict = None):
        """
        Parameters
        ----------
        config: dict
            style config
        """
        super().__init__()
        self.config = {
            "groove.height": 3,
            "sub-page.color": QColor(255, 255, 255),
            "add-page.color": QColor(255, 255, 255, 64),
            "handle.color": QColor(255, 255, 255),
            "handle.ring-width": 4,
            "handle.hollow-radius": 6,
            "handle.margin": 4
        }
        config = config if config else {}
        self.config.update(config)

        # get handle size
        w = self.config["handle.margin"]+self.config["handle.ring-width"] + \
            self.config["handle.hollow-radius"]
        self.config["handle.size"] = QSize(2*w, 2*w)

    def subControlRect(self, cc, opt, sc, widget):
        """ get the rectangular area occupied by the sub control """
        if cc != self.ComplexControl.CC_Slider or opt.orientation != Qt.Orientation.Horizontal or \
                sc == self.SubControl.SC_SliderTickmarks:
            return super().subControlRect(cc, opt, sc, widget)

        rect = opt.rect

        if sc == self.SubControl.SC_SliderGroove:
            h = self.config["groove.height"]
            grooveRect = QRectF(0, (rect.height()-h)//2, rect.width(), h)
            return grooveRect.toRect()

        elif sc == self.SubControl.SC_SliderHandle:
            size = self.config["handle.size"]
            x = self.sliderPositionFromValue(
                opt.minimum, opt.maximum, opt.sliderPosition, rect.width())

            # solve the situation that the handle runs out of slider
            x *= (rect.width()-size.width())/rect.width()
            sliderRect = QRectF(x, 0, size.width(), size.height())
            return sliderRect.toRect()

    def drawComplexControl(self, cc, opt, painter, widget):
        """ draw sub control """
        if cc != self.ComplexControl.CC_Slider or opt.orientation != Qt.Orientation.Horizontal:
            return super().drawComplexControl(cc, opt, painter, widget)

        grooveRect = self.subControlRect(cc, opt, self.SubControl.SC_SliderGroove, widget)
        handleRect = self.subControlRect(cc, opt, self.SubControl.SC_SliderHandle, widget)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # paint groove
        painter.save()
        painter.translate(grooveRect.topLeft())

        # paint the crossed part
        w = handleRect.x()-grooveRect.x()
        h = self.config['groove.height']
        painter.setBrush(self.config["sub-page.color"])
        painter.drawRect(0, 0, w, h)

        # paint the uncrossed part
        x = w+self.config['handle.size'].width()
        painter.setBrush(self.config["add-page.color"])
        painter.drawRect(x, 0, grooveRect.width()-w, h)
        painter.restore()

        # paint handle
        ringWidth = self.config["handle.ring-width"]
        hollowRadius = self.config["handle.hollow-radius"]
        radius = ringWidth + hollowRadius

        path = QPainterPath()
        path.moveTo(0, 0)
        center = handleRect.center() + QPoint(1, 1)
        path.addEllipse(QPointF(center), radius, radius)
        path.addEllipse(QPointF(center), hollowRadius, hollowRadius)

        handleColor = self.config["handle.color"]  # type:QColor
        handleColor.setAlpha(255 if opt.activeSubControls !=
                             self.SubControl.SC_SliderHandle else 153)
        painter.setBrush(handleColor)
        painter.drawPath(path)

        # press handle
        if widget.isSliderDown():
            handleColor.setAlpha(255)
            painter.setBrush(handleColor)
            painter.drawEllipse(handleRect)
