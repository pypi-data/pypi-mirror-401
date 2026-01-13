import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase
from ..typography import Typography
from ..utils.validate_params import _validate_param

class Paper(QFrame, PyWidgetBase):
    """
    A component that renders a paper-like surface, styled like Material-UI Paper.

    The `Paper` component provides a container with elevation, rounded corners, and customizable styles,
    suitable for cards, dialogs, or other surfaces. It integrates with `Typography` and other components
    in the `qtmui` framework, retaining all existing parameters and aligning with MUI props.

    Parameters
    ----------
    children : State, str, QWidget, List[QWidget], or None, optional
        The content of the component. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, type, str, or None, optional
        The component used for the root node (e.g., QFrame). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    direction : State or str, optional
        Layout direction ("column" or "row"). Default is "column".
        Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        Shadow depth (0-24). Default is 1.
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        Identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    square : State or bool, optional
        If True, rounded corners are disabled. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Variant of the component ("elevation" or "outlined"). Default is "elevation".
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the component takes full width. Default is True.
        Can be a `State` object for dynamic updates.
    spacing : State or int, optional
        Spacing between children (in theme.spacing units). Default is 6.
        Can be a `State` object for dynamic updates.
    onClick : State or Callable, optional
        Callback fired when the component is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    width : State or int, optional
        Fixed width in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    height : State or int, optional
        Fixed height in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    borderRadius : State or int, optional
        Border radius in pixels. Default is None (uses theme.shape.borderRadius).
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., id, className).

    Signals
    -------
    themeChanged : Signal
        Emitted when the theme changes.
    clicked : Signal
        Emitted when the component is clicked.

    Notes
    -----
    - All existing parameters from the previous implementation are retained.
    - Props of the native component are supported via `**kwargs`.
    - The `elevation` prop uses MUI's box-shadow spec (0-24 levels).
    - MUI classes applied: `MuiPaper-root`, `MuiPaper-elevation`, `MuiPaper-outlined`.
    - Integrates with `Typography` for string children and other `qtmui` components.

    Demos:
    - Paper: https://qtmui.com/material-ui/qtmui-paper/

    API Reference:
    - Paper API: https://qtmui.com/material-ui/api/paper/
    """

    themeChanged = Signal()
    clicked = Signal()

    VALID_DIRECTIONS = ["column", "row"]
    VALID_VARIANTS = ["elevation", "outlined"]

    # MUI box-shadow spec (simplified for Qt stylesheet)
    SHADOWS = {
        0: "none",
        1: "0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12)",
        2: "0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12)",
        3: "0px 3px 3px -2px rgba(0,0,0,0.2), 0px 3px 4px 0px rgba(0,0,0,0.14), 0px 1px 8px 0px rgba(0,0,0,0.12)",
        4: "0px 2px 4px -1px rgba(0,0,0,0.2), 0px 4px 5px 0px rgba(0,0,0,0.14), 0px 1px 10px 0px rgba(0,0,0,0.12)",
        # ... (up to 24, simplified here for brevity)
        24: "0px 11px 15px -7px rgba(0,0,0,0.2), 0px 24px 38px 3px rgba(0,0,0,0.14), 0px 9px 46px 8px rgba(0,0,0,0.12)"
    }

    def __init__(
        self,
        children: Optional[Union[State, str, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, type, str]] = None,
        direction: Union[State, str] = "column",
        elevation: Union[State, int] = 1,
        key: Optional[Union[State, str]] = None,
        square: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        variant: Union[State, str] = "elevation",
        fullWidth: Union[State, bool] = True,
        spacing: Union[State, int] = 6,
        onClick: Optional[Union[State, Callable]] = None,
        width: Optional[Union[State, int]] = None,
        height: Optional[Union[State, int]] = None,
        borderRadius: Optional[Union[State, int]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"Paper-{str(uuid.uuid4())}")
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_direction(direction)
        self._set_elevation(elevation)
        self._set_key(key)
        self._set_square(square)
        self._set_sx(sx)
        self._set_variant(variant)
        self._set_fullWidth(fullWidth)
        self._set_spacing(spacing)
        self._set_onClick(onClick)
        self._set_width(width)
        self._set_height(height)
        self._set_borderRadius(borderRadius)

        self._init_ui()
        self._set_stylesheet()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._connect_signals()

    # Setter and Getter methods
    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="children",
        supported_signatures=Union[State, str, QWidget, List, type(None)]
    )
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._widget_references.clear()
        self._children = value
        children = value.value if isinstance(value, State) else value

        if isinstance(children, list):
            for child in children:
                if not isinstance(child, QWidget):
                    raise TypeError(f"Each element in children must be a QWidget, got {type(child)}")
                self._widget_references.append(child)
        elif isinstance(children, (QWidget, str)):
            if isinstance(children, str):
                typography = Typography(text=children, variant="body1")
                self._widget_references.append(typography)
            else:
                self._widget_references.append(children)
        elif children is not None:
            raise TypeError(f"children must be a State, str, QWidget, List[QWidget], or None, got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        children = self._children.value if isinstance(self._children, State) else self._children
        if isinstance(children, str):
            return [Typography(text=children, variant="body1")]
        return children if isinstance(children, list) else [children] if isinstance(children, QWidget) else []

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="classes",
        supported_signatures=Union[State, Dict, type(None)]
    )
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="component",
        supported_signatures=Union[State, type, str, type(None)]
    )
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component or QFrame

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="direction",
        supported_signatures=Union[State, str],
        valid_values=VALID_DIRECTIONS
    )
    def _set_direction(self, value):
        """Assign value to direction."""
        self._direction = value

    def _get_direction(self):
        """Get the direction value."""
        return self._direction.value if isinstance(self._direction, State) else self._direction

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="elevation",
        supported_signatures=Union[State, int],
        validator=lambda x: 0 <= x <= 24 if isinstance(x, int) else True
    )
    def _set_elevation(self, value):
        """Assign value to elevation."""
        self._elevation = value

    def _get_elevation(self):
        """Get the elevation value."""
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="key",
        supported_signatures=Union[State, str, type(None)]
    )
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="square",
        supported_signatures=Union[State, bool]
    )
    def _set_square(self, value):
        """Assign value to square."""
        self._square = value

    def _get_square(self):
        """Get the square value."""
        return self._square.value if isinstance(self._square, State) else self._square

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="sx",
        supported_signatures=Union[State, List, Dict, Callable, str, type(None)]
    )
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="variant",
        supported_signatures=Union[State, str],
        valid_values=VALID_VARIANTS
    )
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value
        self.setProperty("variant", self._get_variant())

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="fullWidth",
        supported_signatures=Union[State, bool]
    )
    def _set_fullWidth(self, value):
        """Assign value to fullWidth."""
        self._fullWidth = value

    def _get_fullWidth(self):
        """Get the fullWidth value."""
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="spacing",
        supported_signatures=Union[State, int],
        validator=lambda x: x >= 0 if isinstance(x, int) else True
    )
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value

    def _get_spacing(self):
        """Get the spacing value."""
        return self._spacing.value if isinstance(self._spacing, State) else self._spacing

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="onClick",
        supported_signatures=Union[State, Callable, type(None)]
    )
    def _set_onClick(self, value):
        """Assign value to onClick."""
        self._onClick = value

    def _get_onClick(self):
        """Get the onClick value."""
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="width",
        supported_signatures=Union[State, int, type(None)],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_width(self, value):
        """Assign value to width."""
        self._width = value

    def _get_width(self):
        """Get the width value."""
        return self._width.value if isinstance(self._width, State) else self._width

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="height",
        supported_signatures=Union[State, int, type(None)],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_height(self, value):
        """Assign value to height."""
        self._height = value

    def _get_height(self):
        """Get the height value."""
        return self._height.value if isinstance(self._height, State) else self._height

    @_validate_param(
        file_path="qtmui.material.paper",
        param_name="borderRadius",
        supported_signatures=Union[State, int, type(None)],
        validator=lambda x: x >= 0 if isinstance(x, int) else True
    )
    def _set_borderRadius(self, value):
        """Assign value to borderRadius."""
        self._borderRadius = value

    def _get_borderRadius(self):
        """Get the borderRadius value."""
        return self._borderRadius.value if isinstance(self._borderRadius, State) else self._borderRadius

    def _init_ui(self):
        """Initialize the UI based on props."""
        component = self._get_component()
        if not isinstance(self, component):
            # Re-instantiate with the correct component class
            self.__class__ = type("DynamicPaper", (component, PyWidgetBase), {})
        PyWidgetBase._setUpUi(self)

        # Set layout
        self.setLayout(QVBoxLayout() if self._get_direction() == "column" else QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setSpacing(self.theme.spacing(self._get_spacing()))

        # Apply size policy
        width_policy = QSizePolicy.Expanding if self._get_fullWidth() else QSizePolicy.Preferred
        self.setSizePolicy(width_policy, QSizePolicy.Preferred)

        # Apply fixed dimensions
        if self._get_width():
            self.setFixedWidth(self._get_width())
        if self._get_height():
            self.setFixedHeight(self._get_height())

        # Clear previous widgets
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Apply children
        children = self._get_children()
        for child in children:
            self.layout().addWidget(child)

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the Paper."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        paper_styles = component_styled.get("Paper", {}).get("styles", {})
        root_styles = paper_styles.get("root", {})
        outlined_styles = paper_styles.get("outlined", {})
        root_qss = get_qss_style(root_styles)
        outlined_qss = get_qss_style(outlined_styles)

        # Handle sx
        sx = self._get_sx()
        sx_qss = ""
        if sx:
            if isinstance(sx, (list, dict)):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, Callable):
                sx_result = sx()
                if isinstance(sx_result, (list, dict)):
                    sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
                elif isinstance(sx_result, str):
                    sx_qss = sx_result
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        # Handle classes
        classes = self._get_classes()
        classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

        # Apply MUI classes
        mui_classes = ["MuiPaper-root"]
        if self._get_variant() == "elevation":
            mui_classes.append(f"MuiPaper-elevation{self._get_elevation()}")
        else:
            mui_classes.append("MuiPaper-outlined")

        # Apply elevation
        elevation = min(max(self._get_elevation(), 0), 24)
        shadow = self.SHADOWS.get(elevation, self.SHADOWS[1])

        # Apply border radius
        border_radius = 0 if self._get_square() else (self._get_borderRadius() or self.theme.shape.borderRadius)
        border_radius_qss = f"border-radius: {border_radius}px;"

        # Apply variant
        variant_qss = f"border: 1px solid {self.theme.palette.divider};" if self._get_variant() == "outlined" else ""

        # stylesheet = f"""
        #     #{self.objectName()} {{
        #         {root_qss}
        #         {classes_qss}
        #         background-color: {self.theme.palette.background.paper};
        #         box-shadow: {shadow};
        #         {border_radius_qss}
        #         {variant_qss}
        #     }}
        #     #{self.objectName()}[variant=outlined] {{
        #         {outlined_qss}
        #     }}
        #     {sx_qss}
        # """
        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                {classes_qss}
                background-color: {self.theme.palette.background.paper};
                {border_radius_qss}
                {variant_qss}
            }}
            #{self.objectName()}[variant=outlined] {{
                {outlined_qss}
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release event."""
        if event.button() == Qt.LeftButton and self._get_onClick():
            self._get_onClick()(event)
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        """Handle paint event."""
        PyWidgetBase.paintEvent(self, event)
        super().paintEvent(event)

    def resizeEvent(self, event):
        """Handle resize event."""
        PyWidgetBase.resizeEvent(self, event)
        super().resizeEvent(event)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.connect(self._on_component_changed)
        if isinstance(self._direction, State):
            self._direction.valueChanged.connect(self._on_direction_changed)
        if isinstance(self._elevation, State):
            self._elevation.valueChanged.connect(self._on_elevation_changed)
        if isinstance(self._key, State):
            self._key.valueChanged.connect(self._on_key_changed)
        if isinstance(self._square, State):
            self._square.valueChanged.connect(self._on_square_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.connect(self._on_variant_changed)
        if isinstance(self._fullWidth, State):
            self._fullWidth.valueChanged.connect(self._on_fullWidth_changed)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.connect(self._on_spacing_changed)
        if isinstance(self._onClick, State):
            self._onClick.valueChanged.connect(self._on_onClick_changed)
        if isinstance(self._width, State):
            self._width.valueChanged.connect(self._on_width_changed)
        if isinstance(self._height, State):
            self._height.valueChanged.connect(self._on_height_changed)
        if isinstance(self._borderRadius, State):
            self._borderRadius.valueChanged.connect(self._on_borderRadius_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._init_ui()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_component_changed(self):
        """Handle changes to component."""
        self._set_component(self._component)
        self._init_ui()

    def _on_direction_changed(self):
        """Handle changes to direction."""
        self._set_direction(self._direction)
        self._init_ui()

    def _on_elevation_changed(self):
        """Handle changes to elevation."""
        self._set_elevation(self._elevation)
        self._set_stylesheet()

    def _on_key_changed(self):
        """Handle changes to key."""
        self._set_key(self._key)

    def _on_square_changed(self):
        """Handle changes to square."""
        self._set_square(self._square)
        self._set_stylesheet()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_variant_changed(self):
        """Handle changes to variant."""
        self._set_variant(self._variant)
        self._set_stylesheet()

    def _on_fullWidth_changed(self):
        """Handle changes to fullWidth."""
        self._set_fullWidth(self._fullWidth)
        self._init_ui()

    def _on_spacing_changed(self):
        """Handle changes to spacing."""
        self._set_spacing(self._spacing)
        self._init_ui()

    def _on_onClick_changed(self):
        """Handle changes to onClick."""
        self._set_onClick(self._onClick)

    def _on_width_changed(self):
        """Handle changes to width."""
        self._set_width(self._width)
        self._init_ui()

    def _on_height_changed(self):
        """Handle changes to height."""
        self._set_height(self._height)
        self._init_ui()

    def _on_borderRadius_changed(self):
        """Handle changes to borderRadius."""
        self._set_borderRadius(self._borderRadius)
        self._set_stylesheet()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.disconnect(self._on_component_changed)
        if isinstance(self._direction, State):
            self._direction.valueChanged.disconnect(self._on_direction_changed)
        if isinstance(self._elevation, State):
            self._elevation.valueChanged.disconnect(self._on_elevation_changed)
        if isinstance(self._key, State):
            self._key.valueChanged.disconnect(self._on_key_changed)
        if isinstance(self._square, State):
            self._square.valueChanged.disconnect(self._on_square_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.disconnect(self._on_variant_changed)
        if isinstance(self._fullWidth, State):
            self._fullWidth.valueChanged.disconnect(self._on_fullWidth_changed)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.disconnect(self._on_spacing_changed)
        if isinstance(self._onClick, State):
            self._onClick.valueChanged.disconnect(self._on_onClick_changed)
        if isinstance(self._width, State):
            self._width.valueChanged.disconnect(self._on_width_changed)
        if isinstance(self._height, State):
            self._height.valueChanged.disconnect(self._on_height_changed)
        if isinstance(self._borderRadius, State):
            self._borderRadius.valueChanged.disconnect(self._on_borderRadius_changed)