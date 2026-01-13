import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..typography import Typography
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class ListSubheader(QFrame):
    """
    A component that renders a subheader within a List, styled like Material-UI ListSubheader.

    The `ListSubheader` component is used to display a subheader in a List, with support for custom colors,
    indentation, gutter control, and styling overrides.

    Parameters
    ----------
    children : State, str, QWidget, List[Union[str, QWidget]], or None, optional
        The content of the component. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component ("default", "inherit", "primary"). Default is "default".
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "QFrame"). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If True, removes gutters (padding). Default is False.
        Can be a `State` object for dynamic updates.
    disableSticky : State or bool, optional
        If True, the subheader will not stick to the top during scroll. Default is False.
        Can be a `State` object for dynamic updates.
    id : State or str, optional
        The identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    inset : State or bool, optional
        If True, the subheader is indented. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the subheader ("small", "medium", "large"). Default is "medium".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for `color`: ["default", "inherit", "primary"].
    VALID_SIZES : list[str]
        Valid values for `size`: ["small", "medium", "large"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `disableSticky` prop may require additional logic in Qt to emulate sticky behavior during scroll.
    - The `color` prop maps to theme palette: "default" uses `text.disabled`, "primary" uses `primary.main`, "inherit" retains parent color.

    Demos:
    - ListSubheader: https://qtmui.com/material-ui/qtmui-listsubheader/

    API Reference:
    - ListSubheader API: https://qtmui.com/material-ui/api/list-subheader/
    """

    VALID_COLORS = ["default", "inherit", "primary"]
    VALID_SIZES = ["small", "medium", "large"]

    def __init__(
        self,
        children: Optional[Union[State, str, QWidget, List[Union[str, QWidget]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        color: Union[State, str] = "default",
        component: Optional[Union[State, str]] = None,
        disableGutters: Union[State, bool] = False,
        disableSticky: Union[State, bool] = False,
        id: Optional[Union[State, str]] = None,
        inset: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        size: Union[State, str] = "medium",
        **kwargs
    ):
        super().__init__()
        self.setObjectName(f"ListSubheader-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_color(color)
        self._set_component(component)
        self._set_disableGutters(disableGutters)
        self._set_disableSticky(disableSticky)
        self._set_id(id)
        self._set_inset(inset)
        self._set_sx(sx)
        self._set_size(size)

        self._init_ui()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.listsubheader", param_name="children", supported_signatures=Union[State, str, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="color", supported_signatures=Union[State, str], valid_values=VALID_COLORS)
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="disableGutters", supported_signatures=Union[State, bool])
    def _set_disableGutters(self, value):
        """Assign value to disableGutters."""
        self._disableGutters = value

    def _get_disableGutters(self):
        """Get the disableGutters value."""
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="disableSticky", supported_signatures=Union[State, bool])
    def _set_disableSticky(self, value):
        """Assign value to disableSticky."""
        self._disableSticky = value

    def _get_disableSticky(self):
        """Get the disableSticky value."""
        return self._disableSticky.value if isinstance(self._disableSticky, State) else self._disableSticky

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        """Assign value to id."""
        self._id = value

    def _get_id(self):
        """Get the id value."""
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="inset", supported_signatures=Union[State, bool])
    def _set_inset(self, value):
        """Assign value to inset."""
        self._inset = value

    def _get_inset(self):
        """Get the inset value."""
        return self._inset.value if isinstance(self._inset, State) else self._inset

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.listsubheader", param_name="size", supported_signatures=Union[State, str], valid_values=VALID_SIZES)
    def _set_size(self, value):
        """Assign value to size."""
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size

    def _init_ui(self):
        # Thêm nội dung children (nếu có)
        if self._children:
            # Tạo layout cho ListSubHeader
            self._layout = QVBoxLayout(self)
            self.setLayout(self._layout)
            self._layout.setContentsMargins(0, 0, 0, 0 if self._disableGutters else 10)
            if self._component:
                label = self._component(self)
            else:
                label = QLabel(self)
                
            label.setText(self._children)
            self._layout.addWidget(label)

        # Nếu inset=True, thêm padding bên trái
        if self._inset:
            self._layout.setContentsMargins(20, 0, 0, 0)

        padding = {
            "small": "4px 8px", # top-bottom left-right
            "medium": "8px 16px",
            "large": "12px 24px"
        }[self._size]

        self.setStyleSheet(self.styleSheet() + f"""
            QLabel {{
                font-size: 12px;
                padding: {padding}px;
                margin-left: 9px;
                color: {useTheme().palette.text.disabled};
            }}
        """)



      