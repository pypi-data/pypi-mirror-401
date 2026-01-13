from typing import Union, Optional, Dict, List, Callable
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from qtmui.hooks import State
from ..py_iconify import PyIconify
from qtmui.material.styles import useTheme
from ..typography import Typography
from ..utils.validate_params import _validate_param
import uuid

class InputAdornment(QWidget):
    """
    A component that adds adornments to an input, such as icons or buttons, styled like Material-UI InputAdornment.

    The `InputAdornment` component is used to enhance inputs with additional content, typically placed at the start or
    end of the input field, supporting icons, buttons, or text.

    Parameters
    ----------
    position : State or str
        The position of the adornment relative to the input ("start" or "end"). Required.
        Can be a `State` object for dynamic updates.
    children : State, str, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the adornment (text, widget, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "QWidget"). Default is None (uses QWidget).
        Can be a `State` object for dynamic updates.
    disablePointerEvents : State or bool, optional
        If True, disables pointer events on the root. Default is False.
        Can be a `State` object for dynamic updates.
    disableTypography : State or bool, optional
        If True, disables wrapping string children in a Typography component. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The variant to use ("filled", "outlined", "standard"). Default is None.
        Can be a `State` object for dynamic updates.
    icon : State, QIcon, PyIconify, or None, optional
        The icon to display in the adornment (integrated into children). Default is None.
        Can be a `State` object for dynamic updates.
    text : State, str, or None, optional
        The text to display in the adornment (integrated into children). Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_POSITIONS : list[str]
        Valid values for `position`: ["start", "end"].
    VALID_VARIANTS : list[str]
        Valid values for `variant`: ["filled", "outlined", "standard"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop takes precedence over `icon` and `text` if provided.
    - The `variant` prop is typically set by a parent `TextField` or `FormControl` component.

    Demos:
    - InputAdornment: https://qtmui.com/material-ui/qtmui-inputadornment/

    API Reference:
    - InputAdornment API: https://qtmui.com/material-ui/api/input-adornment/
    """

    VALID_POSITIONS = ["start", "end"]
    VALID_VARIANTS = ["filled", "outlined", "standard"]

    def __init__(
        self,
        position: Union[State, str] = None,
        children: Optional[Union[State, str, QWidget, List[Union[QWidget, str]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, str]] = None,
        disablePointerEvents: Union[State, bool] = False,
        disableTypography: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        variant: Optional[Union[State, str]] = None,
        icon: Optional[Union[State, QIcon, PyIconify]] = None,
        text: Optional[Union[State, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"InputAdornment-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_position(position)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_disablePointerEvents(disablePointerEvents)
        self._set_disableTypography(disableTypography)
        self._set_sx(sx)
        self._set_variant(variant)
        self._set_icon(icon)
        self._set_text(text)

        self._init_ui()

    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.inputadornment", param_name="position", supported_signatures=Union[State, str], valid_values=VALID_POSITIONS)
    def _set_position(self, value):
        """Assign value to position."""
        self._position = value

    def _get_position(self):
        """Get the position value."""
        return self._position.value if isinstance(self._position, State) else self._position

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="children", supported_signatures=Union[State, str, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="disablePointerEvents", supported_signatures=Union[State, bool])
    def _set_disablePointerEvents(self, value):
        """Assign value to disablePointerEvents."""
        self._disablePointerEvents = value
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, self._get_disablePointerEvents())

    def _get_disablePointerEvents(self):
        """Get the disablePointerEvents value."""
        return self._disablePointerEvents.value if isinstance(self._disablePointerEvents, State) else self._disablePointerEvents

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="disableTypography", supported_signatures=Union[State, bool])
    def _set_disableTypography(self, value):
        """Assign value to disableTypography."""
        self._disableTypography = value

    def _get_disableTypography(self):
        """Get the disableTypography value."""
        return self._disableTypography.value if isinstance(self._disableTypography, State) else self._disableTypography

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.inputadornment", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="icon", supported_signatures=Union[State, QIcon, PyIconify, type(None)])
    def _set_icon(self, value):
        """Assign value to icon."""
        self._icon = value

    def _get_icon(self):
        """Get the icon value."""
        return self._icon.value if isinstance(self._icon, State) else self._icon

    @_validate_param(file_path="qtmui.material.inputadornment", param_name="text", supported_signatures=Union[State, str, type(None)])
    def _set_text(self, value):
        """Assign value to text."""
        self._text = value

    def _get_text(self):
        """Get the text value."""
        return self._text.value if isinstance(self._text, State) else self._text

    def _init_ui(self):

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        theme = useTheme()

        if self._children and isinstance(self._children, list):
            for widget in self._children:
                self.layout().addWidget(widget)
        else:
            self.button = QPushButton()
            if self._text:
                self.button.setText(self._text)
            if isinstance(self._icon, PyIconify):
                self.button.setIcon(self._icon)

            self.button.setFixedSize(24, 24)
            self.button.setIconSize(QSize(16, 16))
            self.layout().addWidget(self.button)
            self.button.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    color: {theme.palette.grey._500};
                    font-size: {theme.typography.button.fontSize};
                    line-height: {theme.typography.button.lineHeight};
                    font-weight: {theme.typography.button.fontWeight};
                }}
                QPushButton:hover {{
                    background-color: transparent;
                }}
            """)

        