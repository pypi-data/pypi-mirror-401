import uuid
from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from ..typography import Typography
from ..utils.validate_params import _validate_param

class DialogContent(QWidget):
    """
    A component that renders the main content of a dialog.

    The `DialogContent` component is used to display the primary content of a dialog,
    supporting all props of the Material-UI `DialogContent` component, as well as additional
    props for customization.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically text or sub-components. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    dividers : State or bool, optional
        If True, displays top and bottom dividers. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    text : State, str, or None, optional
        Text content to be rendered via Typography (custom feature, not part of Material-UI).
        Default is None. Can be a `State` object for dynamic updates.
    ref : State, object, or None, optional
        A reference to the root element (custom feature, not part of Material-UI). Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class, supporting
        props of the native component (e.g., style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `text` and `ref` parameters are custom features, not part of Material-UI's `DialogContent`.
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - DialogContent: https://qtmui.com/material-ui/qtmui-dialog-content/

    API Reference:
    - DialogContent API: https://qtmui.com/material-ui/api/dialog-content/
    """

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        dividers: Union[State, bool] = False,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        text: Optional[Union[State, str, Callable]] = None,
        ref: Optional[Union[State, object]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(str(uuid.uuid4()))

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_dividers(dividers)
        self._set_sx(sx)
        self._set_text(text)
        self._set_ref(ref)

        # Setup UI
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
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
    # @_validate_param(file_path="qtmui.material.dialog_content", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children and store widget references."""
        self._widget_references.clear()
        self._children = value
        children = self._get_children()

        if isinstance(children, QWidget):
            self._widget_references.append(children)
            children.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        elif isinstance(children, list):
            for child in children:
                if child is None:
                    continue
                if isinstance(child, QWidget):
                    self._widget_references.append(child)
                    child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
                else:
                    raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
        elif children is not None:
            raise TypeError(f"children must be a State, QWidget, or list of QWidgets, but got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.dialog_content", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.dialog_content", param_name="dividers", supported_signatures=Union[State, bool])
    def _set_dividers(self, value):
        """Assign value to dividers."""
        self._dividers = value

    def _get_dividers(self):
        """Get the dividers value."""
        return self._dividers.value if isinstance(self._dividers, State) else self._dividers

    @_validate_param(file_path="qtmui.material.dialog_content", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.dialog_content", param_name="text", supported_signatures=Union[State, str, Callable, type(None)])
    def _set_text(self, value):
        """Assign value to text (custom feature)."""
        self._text = value

    def _get_text(self):
        """Get the text value."""
        return self._text.value if isinstance(self._text, State) else self._text

    @_validate_param(file_path="qtmui.material.dialog_content", param_name="ref", supported_signatures=Union[State, object, type(None)])
    def _set_ref(self, value):
        """Assign value to ref (custom feature)."""
        self._ref = value

    def _get_ref(self):
        """Get the ref value."""
        return self._ref.value if isinstance(self._ref, State) else self._ref

    def forward_ref(self, ref):
        """Set the reference to the root element (custom feature)."""
        self._set_ref(ref)

    def _init_ui(self):
        """Initialize the UI with dividers, text, and children."""
        self.layout().setContentsMargins(16, 16, 16, 16)  # Default MUI padding
        self.layout().setSpacing(8)  # Default MUI spacing

        # Add top divider
        if self._get_dividers():
            top_divider = QFrame()
            top_divider.setObjectName(f"top-divider-{self.objectName()}")
            top_divider.setFrameShape(QFrame.HLine)
            top_divider.setFrameShadow(QFrame.Sunken)
            self._widget_references.append(top_divider)
            self.layout().addWidget(top_divider)

        # Add text
        text = self._get_text()
        if text:
            typography = Typography(wrap=True, text=text, variant="body1")
            self._widget_references.append(typography)
            self.layout().addWidget(typography)

        # Add children
        self._add_children_to_layout()

        # Add bottom divider
        if self._get_dividers():
            bottom_divider = QFrame()
            bottom_divider.setObjectName(f"bottom-divider-{self.objectName()}")
            bottom_divider.setFrameShape(QFrame.HLine)
            bottom_divider.setFrameShadow(QFrame.Sunken)
            self._widget_references.append(bottom_divider)
            self.layout().addWidget(bottom_divider)

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
        dialog_content_styles = component_styled.get("DialogContent", {}).get("styles", {})
        root_styles = dialog_content_styles.get("root", {})
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
        mui_classes = ["MuiDialogContent-root"]
        if self._get_dividers():
            mui_classes.append("MuiDialogContent-dividers")

        # Divider styles
        divider_qss = ""
        if self._get_dividers():
            divider_qss = f"""
                #{self.objectName()} > QFrame {{
                    background-color: {self.theme.palette.divider};
                    height: 1px;
                    margin: 0 16px;
                }}
            """

        stylesheet = f"""
            #{self.objectName()} {{
                padding: 16px;
                {root_qss}
                {classes_qss}
            }}
            {divider_qss}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._dividers, State):
            self._dividers.valueChanged.connect(self._on_dividers_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._text, State):
            self._text.valueChanged.connect(self._on_text_changed)
        if isinstance(self._ref, State):
            self._ref.valueChanged.connect(self._on_ref_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._clear_layout()
        self._init_ui()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_dividers_changed(self):
        """Handle changes to dividers."""
        self._set_dividers(self._dividers)
        self._clear_layout()
        self._init_ui()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_text_changed(self):
        """Handle changes to text."""
        self._set_text(self._text)
        self._clear_layout()
        self._init_ui()

    def _on_ref_changed(self):
        """Handle changes to ref."""
        self._set_ref(self._ref)

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
        if isinstance(self._dividers, State):
            self._dividers.valueChanged.disconnect(self._on_dividers_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._text, State):
            self._text.valueChanged.disconnect(self._on_text_changed)
        if isinstance(self._ref, State):
            self._ref.valueChanged.disconnect(self._on_ref_changed)