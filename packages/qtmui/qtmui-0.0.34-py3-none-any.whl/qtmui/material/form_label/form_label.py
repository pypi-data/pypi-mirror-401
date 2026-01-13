from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
import uuid
from qtmui.hooks import State
from ...material.styles import useTheme
from ..typography import Typography
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class FormLabel(QFrame):
    """
    A component that provides a label for form controls.

    The `FormLabel` component is used to display labels for form controls, supporting all
    props of the Material-UI `FormLabel` component.

    Parameters
    ----------
    children : State, str, QWidget, List[QWidget], or None, optional
        The content of the component, typically text or a widget. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component ("error", "info", "primary", "secondary", "success", "warning",
        or custom color). Default is "primary".
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "label"). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the label is displayed in a disabled state. Default is False.
        Can be a `State` object for dynamic updates.
    error : State or bool, optional
        If True, the label is displayed in an error state. Default is False.
        Can be a `State` object for dynamic updates.
    filled : State or bool, optional
        If True, the label uses filled classes key. Default is False.
        Can be a `State` object for dynamic updates.
    focused : State or bool, optional
        If True, the label uses focused classes key. Default is False.
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the label indicates that the input is required (adds *). Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for `color`: ["error", "info", "primary", "secondary", "success", "warning"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - If `children` is a string, it is rendered using `Typography` with variant="button".
    - If `children` is a `QWidget` or list of `QWidget`, it is added directly to the layout.

    Demos:
    - FormLabel: https://qtmui.com/material-ui/qtmui-formlabel/

    API Reference:
    - FormLabel API: https://qtmui.com/material-ui/api/form-label/
    """

    VALID_COLORS = ["error", "info", "primary", "secondary", "success", "warning"]

    def __init__(
        self,
        children: Optional[Union[State, str, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        color: Union[State, str] = "primary",
        component: Optional[Union[State, str]] = None,
        disabled: Union[State, bool] = False,
        label: Optional[Union[State, str, Callable]] = None,
        error: Union[State, bool] = False,
        filled: Union[State, bool] = False,
        focused: Union[State, bool] = False,
        required: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"MuiFormLabel-{str(uuid.uuid4())}")

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_color(color)
        self._set_component(component)
        self._set_disabled(disabled)
        self._set_error(error)
        self._set_label(label)
        self._set_filled(filled)
        self._set_focused(focused)
        self._set_required(required)
        self._set_sx(sx)

        # Setup UI
        self._init_ui()


    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.formlabel", param_name="children", supported_signatures=Union[State, str, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.formlabel", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.formlabel", param_name="color", supported_signatures=Union[State, str])
    def _set_color(self, value):
        """Assign value to color."""
        if value not in self.VALID_COLORS and not isinstance(value, str):
            raise ValueError(f"color must be one of {self.VALID_COLORS} or a custom string, got {value}")
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.formlabel", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.formlabel", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value
        self._update_enabled_state()

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.formlabel", param_name="error", supported_signatures=Union[State, bool])
    def _set_error(self, value):
        """Assign value to error."""
        self._error = value

    def _get_error(self):
        """Get the error value."""
        return self._error.value if isinstance(self._error, State) else self._error
    
    @_validate_param(file_path="qtmui.material.formlabel", param_name="label", supported_signatures=Union[State, str])
    def _set_label(self, value):
        """Assign value to error."""
        self._label = value

    def _get_label(self):
        """Get the error value."""
        return self._label.value if isinstance(self._label, State) else self._label

    @_validate_param(file_path="qtmui.material.formlabel", param_name="filled", supported_signatures=Union[State, bool])
    def _set_filled(self, value):
        """Assign value to filled."""
        self._filled = value

    def _get_filled(self):
        """Get the filled value."""
        return self._filled.value if isinstance(self._filled, State) else self._filled

    @_validate_param(file_path="qtmui.material.formlabel", param_name="focused", supported_signatures=Union[State, bool])
    def _set_focused(self, value):
        """Assign value to focused."""
        self._focused = value

    def _get_focused(self):
        """Get the focused value."""
        return self._focused.value if isinstance(self._focused, State) else self._focused

    @_validate_param(file_path="qtmui.material.formlabel", param_name="required", supported_signatures=Union[State, bool])
    def _set_required(self, value):
        """Assign value to required."""
        self._required = value

    def _get_required(self):
        """Get the required value."""
        return self._required.value if isinstance(self._required, State) else self._required

    @_validate_param(file_path="qtmui.material.formlabel", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def _init_ui(self):
        """Initialize the UI based on props."""
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        children = self._get_children()
        component = self._get_component() or "label"

        # Clear previous widgets
        self._clear_layout()

        if isinstance(children, str):
            text = children + (" *" if self._get_required() else "")
            typography = Typography(variant="button", text=text)
            typography.setEnabled(not self._get_disabled())
            self.layout().addWidget(typography)
            self._widget_references.append(typography)
        elif isinstance(children, QWidget):
            children.setEnabled(not self._get_disabled())
            self.layout().addWidget(children)
            self._widget_references.append(children)
        elif isinstance(children, list):
            for child in children:
                if child is None:
                    continue
                if not isinstance(child, QWidget):
                    raise TypeError(f"Each element in children must be a QWidget, got {type(child)}")
                child.setEnabled(not self._get_disabled())
                self.layout().addWidget(child)
                self._widget_references.append(child)
        elif children is None:
            pass  # No content

        # Apply styles
        self._set_stylesheet()

        # Connect signals
        self._connect_signals()
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)


    def _update_enabled_state(self):
        """Update the enabled state of child widgets."""
        for widget in self._widget_references:
            widget.setEnabled(not self._get_disabled())

    def _set_stylesheet(self, component_styled=None):
        """Apply styles based on theme, classes, and sx."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        form_label_styles = component_styled.get("FormLabel", {}).get("styles", {})
        root_styles = form_label_styles.get("root", {})
        root_qss = get_qss_style(root_styles)

        # Handle color
        color = self._get_color()
        if color in self.VALID_COLORS:
            color_value = getattr(getattr(self.theme.palette, color, {}), "main")
        else:
            color_value = color
        if self._get_error():
            color_value = self.theme.palette.error.main
        elif self._get_disabled():
            color_value = self.theme.palette.text.disabled
        color_qss = f"color: {color_value};"

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
        mui_classes = ["MuiFormLabel-root"]
        if self._get_disabled():
            mui_classes.append("Mui-disabled")
        if self._get_error():
            mui_classes.append("Mui-error")
        if self._get_filled():
            mui_classes.append("MuiFormLabel-filled")
        if self._get_focused():
            mui_classes.append("Mui-focused")
        if self._get_required():
            mui_classes.append("MuiFormLabel-required")

        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                {color_qss}
                {classes_qss}
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.connect(self._on_color_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.connect(self._on_component_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.connect(self._on_disabled_changed)
        if isinstance(self._error, State):
            self._error.valueChanged.connect(self._on_error_changed)
        if isinstance(self._filled, State):
            self._filled.valueChanged.connect(self._on_filled_changed)
        if isinstance(self._focused, State):
            self._focused.valueChanged.connect(self._on_focused_changed)
        if isinstance(self._required, State):
            self._required.valueChanged.connect(self._on_required_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._init_ui()
        self._set_stylesheet()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_color_changed(self):
        """Handle changes to color."""
        self._set_color(self._color)
        self._set_stylesheet()

    def _on_component_changed(self):
        """Handle changes to component."""
        self._set_component(self._component)
        self._init_ui()
        self._set_stylesheet()

    def _on_disabled_changed(self):
        """Handle changes to disabled."""
        self._set_disabled(self._disabled)
        self._set_stylesheet()

    def _on_error_changed(self):
        """Handle changes to error."""
        self._set_error(self._error)
        self._set_stylesheet()

    def _on_filled_changed(self):
        """Handle changes to filled."""
        self._set_filled(self._filled)
        self._set_stylesheet()

    def _on_focused_changed(self):
        """Handle changes to focused."""
        self._set_focused(self._focused)
        self._set_stylesheet()

    def _on_required_changed(self):
        """Handle changes to required."""
        self._set_required(self._required)
        self._init_ui()
        self._set_stylesheet()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _clear_layout(self):
        """Remove all widgets from the layout."""
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            self._widget_references.clear()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.disconnect(self._on_color_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.disconnect(self._on_component_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.disconnect(self._on_disabled_changed)
        if isinstance(self._error, State):
            self._error.valueChanged.disconnect(self._on_error_changed)
        if isinstance(self._filled, State):
            self._filled.valueChanged.disconnect(self._on_filled_changed)
        if isinstance(self._focused, State):
            self._focused.valueChanged.disconnect(self._on_focused_changed)
        if isinstance(self._required, State):
            self._required.valueChanged.disconnect(self._on_required_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)