import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..stack import Stack

class ListItemSecondaryAction(QFrame):
    """
    A component that renders secondary actions within a ListItem, styled like Material-UI ListItemSecondaryAction.

    The `ListItemSecondaryAction` component is used to display secondary actions (typically an IconButton or selection control)
    at the end of a ListItem, with customizable styles and alignment.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically an IconButton or selection control. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop is typically an IconButton or selection control but can be any QWidget or list of QWidgets.
    - The component uses a QHBoxLayout to align the secondary action to the right, consistent with Material-UI.

    Demos:
    - ListItemSecondaryAction: https://qtmui.com/material-ui/qtmui-listitemsecondaryaction/

    API Reference:
    - ListItemSecondaryAction API: https://qtmui.com/material-ui/api/list-item-secondary-action/
    """

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"ListItemSecondaryAction-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_sx(sx)

        self._init_ui()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.listitemsecondaryaction", param_name="children", supported_signatures=Union[State, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.listitemsecondaryaction", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.listitemsecondaryaction", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def _init_ui(self):
        # Tạo layout QVBoxLayout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight) # ra giữa theo chiều ngang và cả chiều dọc

        # self.setAttribute(Qt.WA_TransparentForMouseEvents) # Điều này cho phép các sự kiện chuột (bao gồm hover) có thể đi qua và được lắng nghe bởi QPushButton.
        
        for widget in self._get_children():
            if widget is not None:
                self.layout().addWidget(widget)
            
