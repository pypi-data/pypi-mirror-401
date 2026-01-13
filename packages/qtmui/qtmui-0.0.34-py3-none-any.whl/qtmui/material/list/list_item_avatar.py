import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QSize
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class ListItemAvatar(QWidget):
    """
    A component that renders an avatar within a ListItem, styled like Material-UI ListItemAvatar.

    The `ListItemAvatar` component is used to display an avatar (typically an Avatar component)
    within a ListItem, with customizable styles and alignment.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically an Avatar. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class,
        supporting props of the native component (e.g., parent, style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop is typically an Avatar component but can be any QWidget or list of QWidgets.
    - The component uses a QHBoxLayout to align the avatar to the left, consistent with Material-UI.

    Demos:
    - ListItemAvatar: https://qtmui.com/material-ui/qtmui-listitemavatar/

    API Reference:
    - ListItemAvatar API: https://qtmui.com/material-ui/api/list-item-avatar/
    """

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"ListItemAvatar-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_sx(sx)

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.listitemavatar", param_name="children", supported_signatures=Union[State, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.listitemavatar", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.listitemavatar", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def _init_ui(self):
        # Layout cơ bản cho icon
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        # self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setFixedSize(QSize(32, 32))
        # self.setFixedWidth(32)
        self.setAttribute(Qt.WA_TransparentForMouseEvents) # Điều này cho phép các sự kiện chuột (bao gồm hover) có thể đi qua và được lắng nghe bởi QPushButton.

        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                self.layout().addWidget(child)


        # Áp dụng các styles thông qua sx
        if self._sx:
            self._apply_sx(self._sx)

        # Áp dụng các class styles thông qua classes
        if self._classes:
            self._apply_classes(self._classes)

    def _apply_sx(self, sx):
        """Áp dụng các overrides styles từ sx"""
        if isinstance(sx, dict):
            for key, value in sx.items():
                self.setStyleSheet(f"{key}: {value};")
        elif callable(sx):
            sx(self)

    def _apply_classes(self, classes):
        """Áp dụng class CSS từ classes"""
        if isinstance(classes, dict):
            styles = "; ".join([f"{k}: {v}" for k, v in classes.items()])
            self.setStyleSheet(styles)
