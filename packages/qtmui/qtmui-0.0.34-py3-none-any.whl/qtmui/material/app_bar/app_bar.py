import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget, QSizePolicy, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State, useEffect
from ..utils.validate_params import _validate_param
from ..box import Box

class AppBar(QFrame):
    """
    A component that displays a top app bar with customizable positioning and styling.

    The `AppBar` component is used to render a navigation bar, typically at the top of
    the application. It supports customizable colors, positioning, and elevation, and
    inherits from `QFrame` and the Material-UI `Paper` component. It provides styling
    through `classes` and `sx` props, consistent with Material-UI's `AppBar`.

    Parameters
    ----------
    color : State or str, optional
        The color of the component. Valid values: "default", "inherit", "primary",
        "secondary", "transparent", "error", "info", "success", "warning", or custom
        colors. Default is "primary". Can be a `State` object for dynamic updates.
    enableColorOnDark : State or bool, optional
        If True, the color prop is applied in dark mode. Default is False.
        Can be a `State` object for dynamic updates.
    position : State or str, optional
        The positioning type. Valid values: "absolute", "fixed", "relative", "static",
        "sticky". Default is "fixed". Note: "sticky" falls back to "static" if not
        supported. Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        The system prop that allows defining system overrides as well as additional CSS
        styles. Can be a CSS-like string, a dictionary of style properties, a callable
        returning styles, or a `State` object for dynamic styling. Default is None.
    children : State, QWidget, list[QWidget], or None, optional
        The content of the component, such as navigation items or widgets.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        The elevation level of the component, affecting the shadow depth (0-24).
        Default is 4. Can be a `State` object for dynamic updates.
    square : State or bool, optional
        If True, the component has sharp corners (no border-radius). Default is False.
        Can be a `State` object for dynamic updates.
    *args
        Additional positional arguments passed to the parent `QFrame` class.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        all props of the Material-UI `Paper` component (e.g., `variant`).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for the `color` parameter: ["default", "inherit", "primary",
        "secondary", "transparent", "error", "info", "success", "warning"].
    VALID_POSITIONS : list[str]
        Valid values for the `position` parameter: ["absolute", "fixed", "relative",
        "static", "sticky"].

    Notes
    -----
    - Props of the `Paper` component are supported via `*args` and `**kwargs`.
    - The `sticky` position may fall back to `static` in environments where it is not
      supported.

    Demos:
    - AppBar: https://qtmui.com/material-ui/qtmui-appbar/

    API Reference:
    - AppBar API: https://qtmui.com/material-ui/api/appbar/
    """

    VALID_COLORS = ["default", "inherit", "primary", "secondary", "transparent", "error", "info", "success", "warning"]
    VALID_POSITIONS = ["absolute", "fixed", "relative", "static", "sticky"]

    def __init__(
        self,
        color: Union[State, str] = "primary",
        enableColorOnDark: Union[State, bool] = False,
        position: Union[State, str] = "fixed",
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        elevation: Optional[Union[State, int]] = 4,
        square: Union[State, bool] = False,
        *args,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_color(color)
        self._set_enableColorOnDark(enableColorOnDark)
        self._set_position(position)
        self._set_sx(sx)
        self._set_children(children)
        self._set_classes(classes)
        self._set_elevation(elevation)
        self._set_square(square)

        self._init_ui()
        self._set_stylesheet()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )

    @_validate_param(file_path="qtmui.material.appbar", param_name="color", supported_signatures=Union[State, str], valid_values=VALID_COLORS)
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.appbar", param_name="enableColorOnDark", supported_signatures=Union[State, bool])
    def _set_enableColorOnDark(self, value):
        """Assign value to enableColorOnDark."""
        self._enableColorOnDark = value

    def _get_enableColorOnDark(self):
        """Get the enableColorOnDark value."""
        return self._enableColorOnDark.value if isinstance(self._enableColorOnDark, State) else self._enableColorOnDark

    @_validate_param(file_path="qtmui.material.appbar", param_name="position", supported_signatures=Union[State, str], valid_values=VALID_POSITIONS)
    def _set_position(self, value):
        """Assign value to position."""
        self._position = value

    def _get_position(self):
        """Get the position value."""
        return self._position.value if isinstance(self._position, State) else self._position

    @_validate_param(file_path="qtmui.material.appbar", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.appbar", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.appbar", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.appbar", param_name="elevation", supported_signatures=Union[State, int, type(None)], valid_values=range(0, 25))
    def _set_elevation(self, value):
        """Assign value to elevation."""
        self._elevation = value

    def _get_elevation(self):
        """Get the elevation value."""
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(file_path="qtmui.material.appbar", param_name="square", supported_signatures=Union[State, bool])
    def _set_square(self, value):
        """Assign value to square."""
        self._square = value

    def _get_square(self):
        """Get the square value."""
        return self._square.value if isinstance(self._square, State) else self._square

    def _init_ui(self):
        """Initialize the UI with a horizontal layout and children."""
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(12, 12, 12, 12)  # Default padding from MUI AppBar
        self.layout().setSpacing(8)

        children = self._get_children()
        if children:
            self.layout().addWidget(
                Box(
                    direction="row",
                    children=children,
                    spacing=8,
                    alignItems="center"
                )
            )

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def _set_stylesheet(self):
        """Apply styles based on theme, color, position, sx, classes, elevation, and square."""
        theme = useTheme()
        component_styles = theme.components.get("PyAppBar", {})
        color_key = self._get_color() if self._get_enableColorOnDark() or not theme.palette.mode == "dark" else "default"
        root_style = get_qss_style(component_styles.get("root", {}).get(color_key, {}))

        # Apply color
        color_style = ""
        if color_key != "transparent":
            color_map = {
                "primary": theme.palette.primary.main,
                "secondary": theme.palette.secondary.main,
                "error": theme.palette.error.main,
                "info": theme.palette.info.main,
                "success": theme.palette.success.main,
                "warning": theme.palette.warning.main,
                "default": theme.palette.background.default,
                "inherit": "inherit",
            }
            color_value = color_map.get(color_key, color_key)
            color_style = f"background-color: {color_value};" if color_value != "inherit" else ""

        # Apply position
        position_style = ""
        position = self._get_position()
        if position in ["fixed", "absolute", "sticky"]:
            position_style = f"""
                position: {position};
                top: 0;
                left: 0;
                right: 0;
                z-index: 1100;
            """
            if position == "sticky" and not hasattr(self, "stickySupported"):  # Fallback for sticky
                position = "static"
        if position == "fixed":
            self.setFixedHeight(self.height())
        elif position == "absolute":
            self.setFixedHeight(self.height())
        else:
            self.setMinimumHeight(0)

        # Apply elevation
        elevation_style = ""
        elevation = self._get_elevation() or 4
        if elevation > 0:
            blur_radius = min(4 + elevation * 2, 24)
            offset_y = min(2 + elevation, 8)
            shadow_effect = QGraphicsDropShadowEffect(self)
            shadow_effect.setBlurRadius(blur_radius)
            shadow_effect.setOffset(0, offset_y)
            shadow_effect.setColor(QColor(0, 0, 0, 50))
            self.setGraphicsEffect(shadow_effect)
        else:
            self.setGraphicsEffect(None)

        # Apply square
        border_radius_style = "border-radius: 0;" if self._get_square() else "border-radius: 4px;"

        # Apply sx
        sx_style = get_qss_style(self._get_sx()) if self._get_sx() else ""

        # Apply classes
        classes_style = get_qss_style(self._get_classes()) if self._get_classes() else ""

        # Combine styles
        # stylesheet = f"""
        #     #{self.objectName()} {{
        #         {root_style}
        #         {color_style}
        #         {position_style}
        #         {elevation_style}
        #         {border_radius_style}
        #         {sx_style}
        #         {classes_style}
        #         min-height: 56px;
        #         padding: 12px;
        #     }}
        # """
        stylesheet = f"""
            #{self.objectName()} {{
                {root_style}
                {position_style}
                {elevation_style}
                {border_radius_style}
                {sx_style}
                {classes_style}
                min-height: 56px;
                padding: 12px;
            }}
        """
        self.setStyleSheet(stylesheet)
        