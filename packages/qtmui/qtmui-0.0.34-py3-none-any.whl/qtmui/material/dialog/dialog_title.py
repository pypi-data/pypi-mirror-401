import uuid
from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from ..typography import Typography
from ..utils.validate_params import _validate_param

class DialogTitle(QFrame):
    """
    A component that renders the title of a dialog.

    The `DialogTitle` component is used to display the title of a dialog, supporting all props
    of the Material-UI `DialogTitle` component, as well as props inherited from `Typography`
    and additional custom props.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically text or sub-components. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    text : State, str, or None, optional
        Text content to be rendered via Typography (custom feature, not part of Material-UI).
        Default is None. Can be a `State` object for dynamic updates.
    align : State, str, or None, optional
        Text alignment ("left", "center", "right", "justify"). Default is None.
        Can be a `State` object for dynamic updates.
    color : State, str, or None, optional
        Text color (e.g., "primary", "secondary", or a color code). Default is None.
        Can be a `State` object for dynamic updates.
    gutterBottom : State or bool, optional
        If True, adds margin below the text. Default is False.
        Can be a `State` object for dynamic updates.
    noWrap : State or bool, optional
        If True, prevents text wrapping. Default is False.
        Can be a `State` object for dynamic updates.
    variant : State, str, or None, optional
        Typography variant ("h1" to "h6", "subtitle1", "subtitle2", "body1", "body2",
        "caption", "button", "overline"). Default is "h6".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_ALIGN : list[str]
        Valid values for `align`: ["left", "center", "right", "justify"].
    VALID_VARIANT : list[str]
        Valid values for `variant`: ["h1", "h2", "h3", "h4", "h5", "h6", "subtitle1",
        "subtitle2", "body1", "body2", "caption", "button", "overline"].

    Notes
    -----
    - Props of the `Typography` component (e.g., `align`, `color`, `gutterBottom`, `noWrap`, `variant`)
      and native component are supported.
    - The `text` parameter is a custom feature, not part of Material-UI's `DialogTitle`.
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - DialogTitle: https://qtmui.com/material-ui/qtmui-dialog-title/

    API Reference:
    - DialogTitle API: https://qtmui.com/material-ui/api/dialog-title/
    - Typography API: https://qtmui.com/material-ui/api/typography/
    """

    VALID_ALIGN = ["left", "center", "right", "justify"]
    VALID_VARIANT = [
        "h1", "h2", "h3", "h4", "h5", "h6",
        "subtitle1", "subtitle2", "body1", "body2",
        "caption", "button", "overline"
    ]

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        text: Optional[Union[State, str, Callable]] = None,
        align: Optional[Union[State, str]] = None,
        color: Optional[Union[State, str]] = None,
        gutterBottom: Union[State, bool] = False,
        noWrap: Union[State, bool] = False,
        variant: Optional[Union[State, str]] = "h6",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_sx(sx)
        self._set_text(text)
        self._set_align(align)
        self._set_color(color)
        self._set_gutterBottom(gutterBottom)
        self._set_noWrap(noWrap)
        self._set_variant(variant)

        # Setup UI
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._init_ui()

        # Apply styles
        self._set_stylesheet()

        # Connect signals
        self._connect_signals()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self.destroyed.connect(self._on_destroyed)

    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.dialog_title", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children and store widget references."""
        self._widget_references.clear()
        self._children = value
        children = self._get_children()

        if isinstance(children, QWidget):
            self._widget_references.append(children)
            children.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        elif isinstance(children, list):
            for child in children:
                if child is None:
                    continue
                if isinstance(child, QWidget):
                    self._widget_references.append(child)
                    child.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                else:
                    raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
        elif children is not None:
            raise TypeError(f"children must be a State, QWidget, or list of QWidgets, but got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="text", supported_signatures=Union[State, str, Callable, type(None)])
    def _set_text(self, value):
        """Assign value to text (custom feature)."""
        self._text = value

    def _get_text(self):
        """Get the text value."""
        return self._text.value if isinstance(self._text, State) else self._text

    # @_validate_param(file_path="qtmui.material.dialog_title", param_name="align", supported_signatures=Union[State, str, type(None)], valid_values=VALID_ALIGN)
    def _set_align(self, value):
        """Assign value to align."""
        self._align = value

    def _get_align(self):
        """Get the align value."""
        return self._align.value if isinstance(self._align, State) else self._align

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="color", supported_signatures=Union[State, str, type(None)])
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color or "textPrimary"

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="gutterBottom", supported_signatures=Union[State, bool])
    def _set_gutterBottom(self, value):
        """Assign value to gutterBottom."""
        self._gutterBottom = value

    def _get_gutterBottom(self):
        """Get the gutterBottom value."""
        return self._gutterBottom.value if isinstance(self._gutterBottom, State) else self._gutterBottom

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="noWrap", supported_signatures=Union[State, bool])
    def _set_noWrap(self, value):
        """Assign value to noWrap."""
        self._noWrap = value

    def _get_noWrap(self):
        """Get the noWrap value."""
        return self._noWrap.value if isinstance(self._noWrap, State) else self._noWrap

    @_validate_param(file_path="qtmui.material.dialog_title", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANT)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    def _init_ui(self):
        """Initialize the UI with text or children."""
        # self.layout().setContentsMargins(24, 20, 24, 20)  # Default MUI padding for DialogTitle
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(8)  # Default MUI spacing

        # Add text
        text = self._get_text()
        if text:
            typography = Typography(
                text=text,
                variant=self._get_variant() or "h6",
                align=self._get_align(),
                color=self._get_color(),
                gutterBottom=self._get_gutterBottom(),
                noWrap=self._get_noWrap()
            )
            self._widget_references.append(typography)
            self.layout().addWidget(typography)
        else:
            # Add children
            self._add_children_to_layout()

    def _add_children_to_layout(self):
        """Add children to the layout."""
        children = self._get_children()
        if children is None:
            return

        if isinstance(children, QWidget):
            self.layout().addWidget(children)
        elif isinstance(children, list):
            for child in children:
                if child is not None:
                    self.layout().addWidget(child)
        else:
            raise TypeError(f"children must be a State, QWidget, or list of QWidgets, but got {type(children)}")

    def _set_stylesheet(self, component_styled=None):
        """Apply styles based on theme, classes, and sx."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        dialog_title_styles = component_styled.get("DialogTitle", {}).get("styles", {})
        root_styles = dialog_title_styles.get("root", {})
        root_qss = get_qss_style(root_styles)

        # Handle sx
        sx = self._get_sx()
        sx_qss = ""
        if sx:
            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, Callable):
                sx_result = sx()
                if isinstance(sx_result, dict):
                    sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
                elif isinstance(sx_result, str):
                    sx_qss = sx_result
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        # Handle classes
        classes = self._get_classes()
        classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

        # Apply MUI classes
        mui_classes = ["MuiDialogTitle-root"]

        stylesheet = f"""
            #{self.objectName()} {{
                padding: 20px 24px;
                {root_qss}
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
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._text, State):
            self._text.valueChanged.connect(self._on_text_changed)
        if isinstance(self._align, State):
            self._align.valueChanged.connect(self._on_align_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.connect(self._on_color_changed)
        if isinstance(self._gutterBottom, State):
            self._gutterBottom.valueChanged.connect(self._on_gutterBottom_changed)
        if isinstance(self._noWrap, State):
            self._noWrap.valueChanged.connect(self._on_noWrap_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.connect(self._on_variant_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._clear_layout()
        self._init_ui()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_text_changed(self):
        """Handle changes to text."""
        self._set_text(self._text)
        self._clear_layout()
        self._init_ui()

    def _on_align_changed(self):
        """Handle changes to align."""
        self._set_align(self._align)
        self._clear_layout()
        self._init_ui()

    def _on_color_changed(self):
        """Handle changes to color."""
        self._set_color(self._color)
        self._clear_layout()
        self._init_ui()

    def _on_gutterBottom_changed(self):
        """Handle changes to gutterBottom."""
        self._set_gutterBottom(self._gutterBottom)
        self._clear_layout()
        self._init_ui()

    def _on_noWrap_changed(self):
        """Handle changes to noWrap."""
        self._set_noWrap(self._noWrap)
        self._clear_layout()
        self._init_ui()

    def _on_variant_changed(self):
        """Handle changes to variant."""
        self._set_variant(self._variant)
        self._clear_layout()
        self._init_ui()

    def _clear_layout(self):
        """Remove all widgets from the layout."""
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
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._text, State):
            self._text.valueChanged.disconnect(self._on_text_changed)
        if isinstance(self._align, State):
            self._align.valueChanged.disconnect(self._on_align_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.disconnect(self._on_color_changed)
        if isinstance(self._gutterBottom, State):
            self._gutterBottom.valueChanged.disconnect(self._on_gutterBottom_changed)
        if isinstance(self._noWrap, State):
            self._noWrap.valueChanged.disconnect(self._on_noWrap_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.disconnect(self._on_variant_changed)