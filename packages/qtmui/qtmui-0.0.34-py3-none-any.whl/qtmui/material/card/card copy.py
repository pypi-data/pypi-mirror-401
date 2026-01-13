import asyncio
from functools import lru_cache
from typing import Optional, Union, Callable, Any, List, Dict
import uuid

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QRunnable, QThreadPool

from qtmui.material.styles import useTheme
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ..utils.validate_params import _validate_param
from ..widget_base import PyWidgetBase

from qtmui.configs import LOAD_WIDGET_ASYNC


class Card(QFrame, PyWidgetBase):
    """
    A component that displays content in a card layout with customizable styling and elevation.

    The `Card` component is used to group content with a paper-like appearance, supporting
    elevation, outlined variants, and custom layouts. It supports all props of the Material-UI
    `Card` and `Paper` components, as well as additional props for direction, full width,
    click events, and spacing. Props of the `Paper` component are supported via `**kwargs`.

    Parameters
    ----------
    children : State, Any, List[Any], or None, optional
        The content of the component, either a single widget or a list of widgets.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    direction : State or str, optional
        Direction of the layout ("column" or "row"). Default is "column".
        Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        Shadow depth of the card, from 0 to 24. Default is 1.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the card expands to full width. Default is True.
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        Unique key for the component, used for internal purposes. Default is None.
        Can be a `State` object for dynamic updates.
    onClick : State or Callable, optional
        Function to call when the card is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    raised : State or bool, optional
        If True, uses raised styling (sets elevation to 4 if not specified).
        Default is False. Can be a `State` object for dynamic updates.
    square : State or bool, optional
        If True, the card has sharp corners (no border-radius). Default is False.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Variant of the card ("elevation" or "outlined"). Default is "elevation".
        Can be a `State` object for dynamic updates.
    spacing : State or int, optional
        Spacing between child elements in pixels. Default is 6.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the `Paper` component (e.g., style, className).

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["elevation", "outlined"].
    VALID_DIRECTIONS : list[str]
        Valid values for the `direction` parameter: ["column", "row"].

    Notes
    -----
    - Props of the `Paper` component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `raised` prop sets `elevation` to 4 if `elevation` is not explicitly set.
    - Additional props (`direction`, `fullWidth`, `key`, `onClick`, `spacing`) are specific
      to this implementation and not part of Material-UI `Card` or `Paper`.

    Demos:
    - Card: https://qtmui.com/material-ui/qtmui-card/

    API Reference:
    - Card API: https://qtmui.com/material-ui/api/card/
    - Paper API: https://qtmui.com/material-ui/api/paper/
    """

    VALID_VARIANTS = ["elevation", "outlined"]
    VALID_DIRECTIONS = ["column", "row"]

    def __init__(
        self,
        children: Optional[Union[State, Any, List[Any]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, Any]] = None,
        direction: Union[State, str] = "column",
        elevation: Union[State, int] = 1,
        fullWidth: Union[State, bool] = True,
        key: Optional[Union[State, str]] = None,
        onClick: Optional[Union[State, Callable]] = None,
        raised: Union[State, bool] = False,
        square: Union[State, bool] = False,
        variant: Union[State, str] = "elevation",
        spacing: Union[State, int] = 6,
        sizePolicy: QSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum),
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__()
        
        self.setObjectName(str(uuid.uuid4()))
        
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_direction(direction)
        self._set_elevation(elevation)
        self._set_fullWidth(fullWidth)
        self._set_key(key)
        self._set_onClick(onClick)
        self._set_raised(raised)
        self._set_square(square)
        self._set_variant(variant)
        self._set_spacing(spacing)
        self._set_sx(sx)
        
        self._sizePolicy = sizePolicy

        self._init_ui()


    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.card", param_name="children", supported_signatures=Union[State, Any, List[Any], type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.card", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.card", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.card", param_name="direction", supported_signatures=Union[State, str], valid_values=VALID_DIRECTIONS)
    def _set_direction(self, value):
        self._direction = value

    def _get_direction(self):
        return self._direction.value if isinstance(self._direction, State) else self._direction

    @_validate_param(file_path="qtmui.material.card", param_name="elevation", supported_signatures=Union[State, int])
    def _set_elevation(self, value):
        if not (0 <= value <= 24):
            raise ValueError("elevation must be between 0 and 24")
        self._elevation = value

    def _get_elevation(self):
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(file_path="qtmui.material.card", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        self._fullWidth = value

    def _get_fullWidth(self):
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.card", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.card", param_name="onClick", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClick(self, value):
        self._onClick = value

    def _get_onClick(self):
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    @_validate_param(file_path="qtmui.material.card", param_name="raised", supported_signatures=Union[State, bool])
    def _set_raised(self, value):
        self._raised = value

    def _get_raised(self):
        return self._raised.value if isinstance(self._raised, State) else self._raised

    @_validate_param(file_path="qtmui.material.card", param_name="square", supported_signatures=Union[State, bool])
    def _set_square(self, value):
        self._square = value

    def _get_square(self):
        return self._square.value if isinstance(self._square, State) else self._square

    @_validate_param(file_path="qtmui.material.card", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.card", param_name="spacing", supported_signatures=Union[State, int])
    def _set_spacing(self, value):
        if value < 0:
            raise ValueError("spacing must be non-negative")
        self._spacing = value

    def _get_spacing(self):
        return self._spacing.value if isinstance(self._spacing, State) else self._spacing

    @_validate_param(file_path="qtmui.material.card", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx


    def _init_ui(self):

        if self._direction == "column":
            self.setLayout(QVBoxLayout())
            self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        else:
            self.setLayout(QHBoxLayout())
        
        if isinstance(self._sizePolicy, QSizePolicy):
            self.setSizePolicy(self._sizePolicy)

        if self._onClick:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(self._spacing)

        # Xử lý phần tử con
        if self._children:
            if isinstance(self._children, list):
                for child in self._children:
                    if child is not None:
                        if LOAD_WIDGET_ASYNC:
                            self._do_task_async(lambda child=child: self.layout().addWidget(child))
                        else:
                            self.layout().addWidget(child)

        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()

    @classmethod
    @lru_cache(maxsize=128)
    def _get_stylesheet(cls, _theme_mode: str):
        
        theme = useTheme()
        PyCard_root = theme.components[f"PyCard"].get("styles")["root"]
        PyCard_root_qss = get_qss_style(PyCard_root)

        _________object_name_______ = "_________object_name_______"

        stylesheet = f"""
            #{_________object_name_______}{{
                {PyCard_root_qss}
            }}
        """

        return stylesheet

    def _set_stylesheet(self, component_styled=None):
        _theme_mode = useTheme().palette.mode
        stylesheet = self._get_stylesheet(_theme_mode)
        stylesheet = stylesheet.replace("_________object_name_______", self.objectName())

        sx_qss = ""

        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        self.setStyleSheet(stylesheet + sx_qss)


    def mouseReleaseEvent(self, event):
        if self._onClick:
            self._onClick()
        return super().mouseReleaseEvent(event)

    def paintEvent(self, arg__1):
        PyWidgetBase.paintEvent(self, arg__1)
        return super().paintEvent(arg__1)

    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)