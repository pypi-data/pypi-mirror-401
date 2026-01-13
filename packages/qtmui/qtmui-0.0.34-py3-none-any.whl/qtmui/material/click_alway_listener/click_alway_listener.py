import uuid
from typing import Callable, Union, List, Optional, Literal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QApplication
from PySide6.QtCore import QEvent, Qt, QObject
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param

class ClickAwayListener(QWidget):
    """
    A component that listens for click or touch events outside of its children and triggers a callback.

    The `ClickAwayListener` component wraps a widget or a list of widgets and detects click or touch
    events that occur outside of its boundaries, triggering the `onClickAway` callback. It supports
    all props of the Material-UI `ClickAwayListener` component.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The wrapped element(s), which must be able to hold a reference (QWidget or list of QWidgets).
        Default is None. Can be a `State` object for dynamic updates.
    onClickAway : State, Callable, or None, optional
        Callback fired when a click or touch event is detected outside the children.
        Signature: function(event: QEvent) -> None
        Default is None. Can be a `State` object for dynamic updates.
    disableReactTree : State or bool, optional
        If True, only the DOM tree is considered, ignoring the React tree. In Qt, this limits event
        checking to the widget's direct children. Default is False.
        Can be a `State` object for dynamic updates.
    mouseEvent : State, str, or Literal[False], optional
        The mouse event to listen to. Supported values: "onClick", "onMouseDown", "onMouseUp",
        "onPointerDown", "onPointerUp", or False to disable. Default is "onClick".
        Can be a `State` object for dynamic updates.
    touchEvent : State, str, or Literal[False], optional
        The touch event to listen to. Supported values: "onTouchEnd", "onTouchStart", or False to
        disable. Default is "onTouchEnd".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class.

    Attributes
    ----------
    VALID_MOUSE_EVENTS : list[Union[str, bool]]
        Valid values for the `mouseEvent` parameter: ["onClick", "onMouseDown", "onMouseUp",
        "onPointerDown", "onPointerUp", False].
    VALID_TOUCH_EVENTS : list[Union[str, bool]]
        Valid values for the `touchEvent` parameter: ["onTouchEnd", "onTouchStart", False].

    Notes
    -----
    - The `children` prop must be a `QWidget` or a list of `QWidget` instances that can hold a reference.
    - The `onClickAway` callback receives a `QEvent` object as its argument.
    - The `disableReactTree` prop limits event checking to the widget's direct children when True.

    Demos:
    - ClickAwayListener: https://qtmui.com/material-ui/qtmui-click-away-listener/

    API Reference:
    - ClickAwayListener API: https://qtmui.com/material-ui/api/click-away-listener/
    """

    VALID_MOUSE_EVENTS = ["onClick", "onMouseDown", "onMouseUp", "onPointerDown", "onPointerUp", False]
    VALID_TOUCH_EVENTS = ["onTouchEnd", "onTouchStart", False]

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        onClickAway: Optional[Union[State, Callable]] = None,
        disableReactTree: Union[State, bool] = False,
        mouseEvent: Union[State, str, Literal[False]] = "onClick",
        touchEvent: Union[State, str, Literal[False]] = "onTouchEnd",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))

        # Set properties with validation
        self._set_children(children)
        self._set_onClickAway(onClickAway)
        self._set_disableReactTree(disableReactTree)
        self._set_mouseEvent(mouseEvent)
        self._set_touchEvent(touchEvent)

        self._init_ui()

    # Setter and Getter methods for all parameters
    @_validate_param(file_path="qtmui.material.click_away_listener", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        if isinstance(value, list) and not all(isinstance(item, QWidget) for item in value):
            raise ValueError("children must be a QWidget or a list of QWidgets")
        if value is not None and not isinstance(value, (QWidget, list, State)):
            raise ValueError("children must be a QWidget, list of QWidgets, or State")
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.click_away_listener", param_name="onClickAway", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClickAway(self, value):
        self._onClickAway = value

    def _get_onClickAway(self):
        return self._onClickAway.value if isinstance(self._onClickAway, State) else self._onClickAway

    @_validate_param(file_path="qtmui.material.click_away_listener", param_name="disableReactTree", supported_signatures=Union[State, bool])
    def _set_disableReactTree(self, value):
        self._disableReactTree = value

    def _get_disableReactTree(self):
        return self._disableReactTree.value if isinstance(self._disableReactTree, State) else self._disableReactTree

    @_validate_param(file_path="qtmui.material.click_away_listener", param_name="mouseEvent", supported_signatures=Union[State, str, Literal[False]], valid_values=VALID_MOUSE_EVENTS)
    def _set_mouseEvent(self, value):
        self._mouseEvent = value

    def _get_mouseEvent(self):
        return self._mouseEvent.value if isinstance(self._mouseEvent, State) else self._mouseEvent

    @_validate_param(file_path="qtmui.material.click_away_listener", param_name="touchEvent", supported_signatures=Union[State, str, Literal[False]], valid_values=VALID_TOUCH_EVENTS)
    def _set_touchEvent(self, value):
        self._touchEvent = value

    def _get_touchEvent(self):
        return self._touchEvent.value if isinstance(self._touchEvent, State) else self._touchEvent

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }};'''.format(self.objectName(), "background-color: red"))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        # self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        if isinstance(self._children, list):
            for widget in self._children:
                if isinstance(widget, QWidget):
                    self.layout().addWidget(widget)

        self.installEventFilter(QApplication.instance().mainWindow)

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton and not self.underMouse():
                if self._onClickAway:
                    self._onClickAway()

        return super().eventFilter(obj, event)