from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QTextEdit, QWidget
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State
from ..utils.validate_params import _validate_param

class AlertTitle(QTextEdit):
    """
    A component that displays the title of an Alert with customizable typography.

    The `AlertTitle` component is used to render the title text of an `Alert`, typically
    displayed above the main message. It inherits from `QTextEdit` and supports all props
    of the Material-UI `Typography` component, including alignment and gutter spacing.
    It provides customizable styling through `classes` and `sx` props, consistent with
    Material-UI's `AlertTitle`.

    Parameters
    ----------
    text : State or str, optional
        The text content of the title. If provided, it is used as the default content
        unless `children` is specified. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the text. Supports "primary", "secondary", "error", "info",
        "success", "warning", or custom colors. Default is "primary".
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The typography variant to use. Valid values include "h1", "h2", "h3", "h4",
        "h5", "h6", "subtitle1", "subtitle2", "body1", "body2", "caption", "button",
        "overline". Default is "body2".
        Can be a `State` object for dynamic updates.
    children : State, str, QWidget, list[QWidget], or None, optional
        The content of the component, overriding `text` if provided. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        The system prop that allows defining system overrides as well as additional CSS
        styles. Can be a CSS-like string, a dictionary of style properties, a callable
        returning styles, or a `State` object for dynamic styling. Default is None.
    align : State or str, optional
        The text alignment. Valid values: "left", "center", "right", "justify",
        "inherit". Default is "inherit".
        Can be a `State` object for dynamic updates.
    gutterBottom : State or bool, optional
        If True, adds a bottom margin to the title. Default is False.
        Can be a `State` object for dynamic updates.

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["h1", "h2", "h3", "h4", "h5", "h6",
        "subtitle1", "subtitle2", "body1", "body2", "caption", "button", "overline"].
    VALID_ALIGNS : list[str]
        Valid values for the `align` parameter: ["left", "center", "right", "justify",
        "inherit"].

    Notes
    -----
    - Props of the `Typography` component are supported (e.g., `color`, `variant`,
      `align`, `gutterBottom`).
    - The `text` parameter is a fallback for `children` and is not part of the standard
      Material-UI `AlertTitle` props but is retained for compatibility.

    Demos:
    - AlertTitle: https://qtmui.com/material-ui/qtmui-alert-title/

    API Reference:
    - AlertTitle API: https://qtmui.com/material-ui/api/alert-title/
    """

    VALID_VARIANTS = [
        "h1", "h2", "h3", "h4", "h5", "h6",
        "subtitle1", "subtitle2", "body1", "body2",
        "caption", "button", "overline"
    ]
    VALID_ALIGNS = ["left", "center", "right", "justify", "inherit"]

    def __init__(
        self,
        text: Optional[Union[str, State, Callable]] = None,
        color: Optional[Union[State, str]] = "primary",
        variant: Union[State, str] = "body2",
        children: Optional[Union[State, str, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        align: Union[State, str] = "inherit",
        gutterBottom: Union[State, bool] = False
    ):
        super().__init__()
        self.setObjectName("PyAlertTitle")
        self.setReadOnly(True)

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_text(text)
        self._set_color(color)
        self._set_variant(variant)
        self._set_children(children)
        self._set_classes(classes)
        self._set_sx(sx)
        self._set_align(align)
        self._set_gutterBottom(gutterBottom)

        self._init_ui()
        self._set_stylesheet()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )

    @_validate_param(file_path="qtmui.material.alert_title", param_name="text", supported_signatures=Union[State, str, type(None)])
    def _set_text(self, value):
        """Assign value to text."""
        self._text = value

    def _get_text(self):
        """Get the text value."""
        return self._text.value if isinstance(self._text, State) else self._text

    @_validate_param(file_path="qtmui.material.alert_title", param_name="color", supported_signatures=Union[State, str, type(None)])
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.alert_title", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.alert_title", param_name="children", supported_signatures=Union[State, str, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.alert_title", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.alert_title", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.alert_title", param_name="align", supported_signatures=Union[State, str], valid_values=VALID_ALIGNS)
    def _set_align(self, value):
        """Assign value to align."""
        self._align = value

    def _get_align(self):
        """Get the align value."""
        return self._align.value if isinstance(self._align, State) else self._align

    @_validate_param(file_path="qtmui.material.alert_title", param_name="gutterBottom", supported_signatures=Union[State, bool])
    def _set_gutterBottom(self, value):
        """Assign value to gutterBottom."""
        self._gutterBottom = value

    def _get_gutterBottom(self):
        """Get the gutterBottom value."""
        return self._gutterBottom.value if isinstance(self._gutterBottom, State) else self._gutterBottom

    def _init_ui(self):
        """Initialize the UI with content from children or text."""
        self.setStyleSheet("background: transparent; border: none;")
        self.setContentsMargins(0, 0, 0, 0)

        # Set content from children or text
        children = self._get_children()
        if children:
            if isinstance(children, str):
                self.setText(children)
            elif isinstance(children, (list, tuple)):
                self.setText("")  # Clear default text
                for child in children:
                    if isinstance(child, QWidget):
                        self.layout().addWidget(child)  # Note: QTextEdit doesn't use layout, this is for future compatibility
                    elif isinstance(child, str):
                        self.append(child)
            elif isinstance(children, QWidget):
                self.setText("")  # Clear default text
                # QTextEdit can't directly add widgets, so we append as text or handle separately
                if hasattr(children, "text"):
                    self.setText(children.text())
        elif self._get_text():
            self.setText(self._get_text())

    def _set_stylesheet(self):
        """Apply styles based on theme, variant, color, sx, classes, align, and gutterBottom."""
        theme = useTheme()
        component_styles = theme.components.get("PyAlertTitle", {})
        root_style = get_qss_style(component_styles.get("root", {}).get(self._get_color() or "primary", {}))

        # Map variant to typography styles
        variant_styles = {
            "h1": {"font-size": "2rem", "font-weight": "bold"},
            "h2": {"font-size": "1.5rem", "font-weight": "bold"},
            "h3": {"font-size": "1.17rem", "font-weight": "bold"},
            "h4": {"font-size": "1rem", "font-weight": "bold"},
            "h5": {"font-size": "0.83rem", "font-weight": "bold"},
            "h6": {"font-size": "0.67rem", "font-weight": "bold"},
            "subtitle1": {"font-size": "1rem", "font-weight": "normal"},
            "subtitle2": {"font-size": "0.875rem", "font-weight": "normal"},
            "body1": {"font-size": "1rem", "font-weight": "normal"},
            "body2": {"font-size": "0.875rem", "font-weight": "normal"},
            "caption": {"font-size": "0.75rem", "font-weight": "normal"},
            "button": {"font-size": "0.875rem", "font-weight": "medium", "text-transform": "uppercase"},
            "overline": {"font-size": "0.75rem", "font-weight": "normal", "text-transform": "uppercase"},
        }
        variant_style = get_qss_style(variant_styles.get(self._get_variant(), variant_styles["body2"]))

        # Apply color
        color_style = f"color: {self._get_color()};" if self._get_color() else ""

        # Apply align
        align_style = f"text-align: {self._get_align()};" if self._get_align() != "inherit" else ""

        # Apply gutterBottom
        gutter_style = "margin-bottom: 8px;" if self._get_gutterBottom() else ""

        # Apply sx
        sx_style = get_qss_style(self._get_sx()) if self._get_sx() else ""

        # Apply classes
        classes_style = get_qss_style(self._get_classes()) if self._get_classes() else ""

        # Combine styles
        stylesheet = f"""
            #{self.objectName()} {{
                {root_style}
                {variant_style}
                {color_style}
                {align_style}
                {gutter_style}
                {sx_style}
                {classes_style}
                background: transparent;
                border: none;
                padding: 0;
            }}
        """
        self.setStyleSheet(stylesheet)