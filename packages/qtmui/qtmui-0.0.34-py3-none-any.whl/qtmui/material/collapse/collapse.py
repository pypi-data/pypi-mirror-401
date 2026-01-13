import asyncio
import uuid
from typing import Optional, Union, Dict, Callable, List, Literal
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Property, Slot, QRunnable, QThreadPool, QTimer
from qtmui.hooks import State, useEffect
from ..py_iconify import PyIconify
from ..spacer import HSpacer
from ..typography import Typography
from ...qtmui_assets import QTMUI_ASSETS
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param

class WidgetSetter(QRunnable):
    def __init__(self):
        super().__init__()

    async def run(self, cls, widget):
        cls.layout().addWidget(widget)


class Collapse(QFrame):
    """
    A component that transitions its children in and out by collapsing or expanding its size.

    The `Collapse` component animates the visibility of its children by changing its height or width,
    supporting vertical or horizontal orientation. It supports all props of the Material-UI `Collapse`
    and `Transition` components, as well as additional props for customization.

    Parameters
    ----------
    addEndListener : State, Callable, or None, optional
        Custom transition end trigger. Called with the transitioning widget and a done callback.
        Default is None. Can be a `State` object for dynamic updates.
    child : State, QWidget, or None, optional
        A single child widget to be collapsed. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The content node(s) to be collapsed. Takes precedence over `child`. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    collapsedSize : State, int, or str, optional
        The size (height for vertical, width for horizontal) when collapsed. Default is "0px".
        Can be a `State` object for dynamic updates.
    component : State, str, or None, optional
        The component used for the root node (e.g., HTML element or custom component). Default is None.
        Can be a `State` object for dynamic updates.
    easing : State, str, dict, or None, optional
        The transition timing function (e.g., "ease", or {enter: "ease-in", exit: "ease-out"}).
        Default is None. Can be a `State` object for dynamic updates.
    id : State, str, or None, optional
        The identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    isIn : State, bool, or None, optional
        If True, the component transitions in. Default is False.
        Can be a `State` object for dynamic updates.
    maximumHeight : State, int, or None, optional
        The maximum height of the component. Default is None.
        Can be a `State` object for dynamic updates.
    minimumHeight : State, int, or None, optional
        The minimum height of the component. Default is None.
        Can be a `State` object for dynamic updates.
    orientation : State or str, optional
        The transition orientation ("horizontal" or "vertical"). Default is "vertical".
        Can be a `State` object for dynamic updates.
    showToogleButton : State or bool, optional
        If True, displays a toggle button with title and icon. Default is True.
        Can be a `State` object for dynamic updates.
    startActionWidget : State, QWidget, or None, optional
        A widget to display at the start of the toggle button. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    timeout : State, str, int, dict, or None, optional
        The duration for the transition (ms, "auto", or {appear, enter, exit}). Default is "auto".
        Can be a `State` object for dynamic updates.
    title : State or str, optional
        The title displayed in the toggle button. Default is "Page".
        Can be a `State` object for dynamic updates.
    unmountOnExit : State, bool, or None, optional
        If True, removes children from the layout when collapsed. Default is None.
        Can be a `State` object for dynamic updates.
    vExpanding : State, bool, or None, optional
        If True, sets expanding size policy (vertical or horizontal based on orientation).
        Default is None. Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class.

    Attributes
    ----------
    is_in_signal : Signal
        Signal emitted when the `isIn` state changes, carrying the new state.
    VALID_ORIENTATIONS : list[str]
        Valid values for the `orientation` parameter: ["horizontal", "vertical"].

    Notes
    -----
    - Props of the `Transition` component are supported (e.g., `addEndListener`).
    - The `children` prop takes precedence over `child`.
    - The `id`, `vExpanding`, `unmountOnExit`, `showToogleButton`, `title`, `minimumHeight`,
      `maximumHeight`, and `startActionWidget` props are specific to this implementation.

    Demos:
    - Collapse: https://qtmui.com/material-ui/qtmui-collapse/

    API Reference:
    - Collapse API: https://qtmui.com/material-ui/api/collapse/
    - Transition API: https://qtmui.com/material-ui/api/transition/
    """

    is_in_signal = Signal(bool)
    VALID_ORIENTATIONS = ["horizontal", "vertical"]

    def __init__(
        self,
        addEndListener: Optional[Union[State, Callable]] = None,
        child: Optional[Union[State, QWidget]] = None,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        collapsedSize: Union[State, int, str] = "0px",
        component: Optional[Union[State, str]] = None,
        easing: Optional[Union[State, str, Dict[str, str]]] = None,
        id: Optional[Union[State, str]] = None,
        isIn: Optional[Union[State, bool]] = False,
        maximumHeight: Optional[Union[State, int]] = None,
        minimumHeight: Optional[Union[State, int]] = None,
        orientation: Union[State, str] = "vertical",
        showToogleButton: Union[State, bool] = True,
        startActionWidget: Optional[Union[State, QWidget]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        timeout: Optional[Union[State, str, int, Dict[str, int]]] = "auto",
        title: Optional[Union[State, str, Callable]] = "Page",
        unmountOnExit: Optional[Union[State, bool]] = None,
        vExpanding: Optional[Union[State, bool]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Set properties with validation
        self._set_addEndListener(addEndListener)
        self._set_child(child)
        self._set_children(children)
        self._set_classes(classes)
        self._set_collapsedSize(collapsedSize)
        self._set_component(component)
        self._set_easing(easing)
        self._set_id(id)
        self._set_isIn(isIn)
        self._set_maximumHeight(maximumHeight)
        self._set_minimumHeight(minimumHeight)
        self._set_orientation(orientation)
        self._set_showToogleButton(showToogleButton)
        self._set_startActionWidget(startActionWidget)
        self._set_sx(sx)
        self._set_timeout(timeout)
        self._set_title(title)
        self._set_unmountOnExit(unmountOnExit)
        self._set_vExpanding(vExpanding)

        self._animation = None
        
        self._thread_pool = QThreadPool.globalInstance()  # Sử dụng thread pool toàn cục
        
        self._init_ui()


    # Setter and Getter methods for all parameters
    @_validate_param(file_path="qtmui.material.collapse", param_name="addEndListener", supported_signatures=Union[State, Callable, type(None)])
    def _set_addEndListener(self, value):
        self._addEndListener = value

    def _get_addEndListener(self):
        return self._addEndListener.value if isinstance(self._addEndListener, State) else self._addEndListener

    @_validate_param(file_path="qtmui.material.collapse", param_name="child", supported_signatures=Union[State, QWidget, type(None)])
    def _set_child(self, value):
        self._child = value

    def _get_child(self):
        return self._child.value if isinstance(self._child, State) else self._child

    # @_validate_param(file_path="qtmui.material.collapse", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        if isinstance(value, list) and not all(isinstance(item, QWidget) for item in value):
            raise ValueError("children must be a QWidget or a list of QWidgets")
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.collapse", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.collapse", param_name="collapsedSize", supported_signatures=Union[State, int, str])
    def _set_collapsedSize(self, value):
        if isinstance(value, str) and not value.endswith(("px", "%")):
            raise ValueError("collapsedSize as string must end with 'px' or '%'")
        self._collapsedSize = value

    def _get_collapsedSize(self):
        return self._collapsedSize.value if isinstance(self._collapsedSize, State) else self._collapsedSize

    @_validate_param(file_path="qtmui.material.collapse", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    # @_validate_param(file_path="qtmui.material.collapse", param_name="easing", supported_signatures=Union[State, str, Dict[str, str], type(None)])
    def _set_easing(self, value):
        self._easing = value

    def _get_easing(self):
        return self._easing.value if isinstance(self._easing, State) else self._easing

    @_validate_param(file_path="qtmui.material.collapse", param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        self._id = value

    def _get_id(self):
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path="qtmui.material.collapse", param_name="isIn", supported_signatures=Union[State, bool, type(None)])
    def _set_isIn(self, value):
        self._isIn = value

    def _get_isIn(self):
        return self._isIn.value if isinstance(self._isIn, State) else self._isIn

    @_validate_param(file_path="qtmui.material.collapse", param_name="maximumHeight", supported_signatures=Union[State, int, type(None)])
    def _set_maximumHeight(self, value):
        self._maximumHeight = value

    def _get_maximumHeight(self):
        return self._maximumHeight.value if isinstance(self._maximumHeight, State) else self._maximumHeight

    @_validate_param(file_path="qtmui.material.collapse", param_name="minimumHeight", supported_signatures=Union[State, int, type(None)])
    def _set_minimumHeight(self, value):
        self._minimumHeight = value

    def _get_minimumHeight(self):
        return self._minimumHeight.value if isinstance(self._minimumHeight, State) else self._minimumHeight

    @_validate_param(file_path="qtmui.material.collapse", param_name="orientation", supported_signatures=Union[State, str], valid_values=VALID_ORIENTATIONS)
    def _set_orientation(self, value):
        self._orientation = value

    def _get_orientation(self):
        return self._orientation.value if isinstance(self._orientation, State) else self._orientation

    @_validate_param(file_path="qtmui.material.collapse", param_name="showToogleButton", supported_signatures=Union[State, bool])
    def _set_showToogleButton(self, value):
        self._showToogleButton = value

    def _get_showToogleButton(self):
        return self._showToogleButton.value if isinstance(self._showToogleButton, State) else self._showToogleButton

    @_validate_param(file_path="qtmui.material.collapse", param_name="startActionWidget", supported_signatures=Union[State, QWidget, type(None)])
    def _set_startActionWidget(self, value):
        self._startActionWidget = value

    def _get_startActionWidget(self):
        return self._startActionWidget.value if isinstance(self._startActionWidget, State) else self._startActionWidget

    @_validate_param(file_path="qtmui.material.collapse", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.collapse", param_name="timeout", supported_signatures=Union[State, str, int, Dict[str, int], type(None)])
    def _set_timeout(self, value):
        if isinstance(value, dict) and not all(k in ["appear", "enter", "exit"] for k in value):
            raise ValueError("timeout dict must contain 'appear', 'enter', or 'exit' keys")
        self._timeout = value

    def _get_timeout(self):
        return self._timeout.value if isinstance(self._timeout, State) else self._timeout

    @_validate_param(file_path="qtmui.material.collapse", param_name="title", supported_signatures=Union[State, str, Callable])
    def _set_title(self, value):
        self._title = value

    def _get_title(self):
        return self._title.value if isinstance(self._title, State) else self._title

    @_validate_param(file_path="qtmui.material.collapse", param_name="unmountOnExit", supported_signatures=Union[State, bool, type(None)])
    def _set_unmountOnExit(self, value):
        self._unmountOnExit = value

    def _get_unmountOnExit(self):
        return self._unmountOnExit.value if isinstance(self._unmountOnExit, State) else self._unmountOnExit

    @_validate_param(file_path="qtmui.material.collapse", param_name="vExpanding", supported_signatures=Union[State, bool, type(None)])
    def _set_vExpanding(self, value):
        self._vExpanding = value

    def _get_vExpanding(self):
        return self._vExpanding.value if isinstance(self._vExpanding, State) else self._vExpanding


    def _init_ui(self):
        if self._id is not None:
            self.setObjectName(self._id)
        else:
            self.setObjectName(str(uuid.uuid4()))

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.btn_toogle = QPushButton()
        self.btn_toogle.setMinimumHeight(40)

        if self._minimumHeight is not None:
            self.setMinimumHeight(self._minimumHeight)

        if self._maximumHeight is not None:
            self.setMaximumHeight(self._maximumHeight)


        self.btn_toogle.setLayout(QHBoxLayout())
        self.btn_toogle.layout().setSpacing(0)

        if self._startActionWidget is not None:
            self.btn_toogle.layout().addWidget(self._startActionWidget)

        self.btn_toogle.layout().addWidget(Typography(text=self._title, variant="h6"))
        self.btn_toogle.layout().addWidget(HSpacer())
        self.btn_icon = QPushButton()
        # self.btn_icon.setIcon(FluentIconBase().icon_(path=":/IconLight/resources/IconLight/Arrow - Down 2.svg", color=self._theme.grey.grey_500))
        self.btn_toogle.layout().addWidget(self.btn_icon)
        self.layout().addWidget(self.btn_toogle)

        if self._children is not None:
            for child in self._children:
                self.layout().addWidget(child)
                # self._add_child_fast(child)
        elif isinstance(self._child, QWidget):
            self.layout().addWidget(self._child)
            # self._add_child_fast(self._child)
            

        if not self._showToogleButton:
            self.btn_toogle.hide()

        self.btn_toogle.clicked.connect(self.set_visible)

        if self._vExpanding:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        # self.is_in_signal.emit(self.__isIn)

        if isinstance(self._isIn, State):
            self._isIn.valueChanged.connect(self.set_visible)
            # self.__isIn = isIn.data
            self.__isIn = self._isIn.value
            self.set_visible(self.__isIn)
        else:
            self.__isIn = self._isIn
            self.is_in_signal.connect(self.set_visible)
            self.is_in_signal.emit(self.__isIn)

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _add_child_fast(self, widget):
        worker = WidgetSetter()
        self._thread_pool.start(QTimer.singleShot(0, lambda widget=widget: asyncio.ensure_future(worker.run(self, widget))))  # Chạy setIndexWidget trong thread riêng
     

    def _set_stylesheet(self):
        theme = useTheme()
        self.btn_toogle.setStyleSheet(f"background-color: {theme.palette.background.main};border: 1px solid transparent;border-radius: 5px;")
        self.btn_icon.setStyleSheet("background-color: transparent; border: none;")


    @Slot(bool)
    def set_visible(self, isIn=None):
        if not isIn:
            self.btn_icon.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_DOWN))
            if self._child is not None:
                self._child.hide()
            if self._children is not None:
                for widget in self._children:
                    widget.hide()
        else:
            self.btn_icon.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_UP))
            if self._child is not None:
                self._child.show()
            if self._children is not None:
                for widget in self._children:
                    widget.show()

