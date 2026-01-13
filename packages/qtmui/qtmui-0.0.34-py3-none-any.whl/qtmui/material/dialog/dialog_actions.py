import uuid
from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param

class DialogActions(QWidget):
    """
    A component that renders action buttons or content for dialogs, typically at the bottom.

    The `DialogActions` component is used to group action buttons (e.g., OK, Cancel) in a dialog,
    supporting all props of the Material-UI `DialogActions` component, as well as additional
    props for customization.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically action buttons. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    disableSpacing : State or bool, optional
        If True, removes additional margin and spacing between actions. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    ref : State, object, or None, optional
        A reference to the root element (custom feature, not part of Material-UI). Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class, supporting
        props of the native component (e.g., style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `ref` parameter is a custom feature, not part of Material-UI's `DialogActions`.
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - DialogActions: https://qtmui.com/material-ui/qtmui-dialog-actions/

    API Reference:
    - DialogActions API: https://qtmui.com/material-ui/api/dialog-actions/
    """

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        disableSpacing: Union[State, bool] = False,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
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
        self._set_disableSpacing(disableSpacing)
        self._set_sx(sx)
        self._set_ref(ref)

        # Setup UI
        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignRight)
        self._update_spacing()
        self._add_children_to_layout()

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
    # @_validate_param(file_path="qtmui.material.dialog_actions", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
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

    @_validate_param(file_path="qtmui.material.dialog_actions", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.dialog_actions", param_name="disableSpacing", supported_signatures=Union[State, bool])
    def _set_disableSpacing(self, value):
        """Assign value to disableSpacing."""
        self._disableSpacing = value

    def _get_disableSpacing(self):
        """Get the disableSpacing value."""
        return self._disableSpacing.value if isinstance(self._disableSpacing, State) else self._disableSpacing

    @_validate_param(file_path="qtmui.material.dialog_actions", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.dialog_actions", param_name="ref", supported_signatures=Union[State, object, type(None)])
    def _set_ref(self, value):
        """Assign value to ref (custom feature)."""
        self._ref = value

    def _get_ref(self):
        """Get the ref value."""
        return self._ref.value if isinstance(self._ref, State) else self._ref

    def forward_ref(self, ref):
        """Set the reference to the root element (custom feature)."""
        self._set_ref(ref)

    def _update_spacing(self):
        """Update layout spacing based on disableSpacing."""
        if self._get_disableSpacing():
            self.layout().setSpacing(0)
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            self.layout().setSpacing(8)  # Default MUI spacing
            self.layout().setContentsMargins(8, 8, 8, 8)  # Default MUI padding

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
        dialog_actions_styles = component_styled.get("DialogActions", {}).get("styles", {})
        root_styles = dialog_actions_styles.get("root", {})
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
        mui_classes = ["MuiDialogActions-root"]
        if self._get_disableSpacing():
            mui_classes.append("MuiDialogActions-spacingDisabled")

        stylesheet = f"""
            #{self.objectName()} {{
                padding: 8px;
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
        if isinstance(self._disableSpacing, State):
            self._disableSpacing.valueChanged.connect(self._on_disableSpacing_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._ref, State):
            self._ref.valueChanged.connect(self._on_ref_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._clear_layout()
        self._add_children_to_layout()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_disableSpacing_changed(self):
        """Handle changes to disableSpacing."""
        self._set_disableSpacing(self._disableSpacing)
        self._update_spacing()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_ref_changed(self):
        """Handle changes to ref."""
        self._set_ref(self._ref)

    def _clear_layout(self):
        """Remove all widgets from the layout."""
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._disableSpacing, State):
            self._disableSpacing.valueChanged.disconnect(self._on_disableSpacing_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._ref, State):
            self._ref.valueChanged.disconnect(self._on_ref_changed)