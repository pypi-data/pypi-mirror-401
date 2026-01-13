from functools import lru_cache
import uuid
from typing import Optional, Union, Callable, List
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QApplication, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

class Portal(QFrame, PyWidgetBase):
    """
    A component that renders children into a container, styled like Material-UI Portal.

    The `Portal` component renders its children into a specified container or the application's main window,
    optionally keeping them within the DOM hierarchy of the parent component. It integrates with the `qtmui`
    framework, retaining the existing `children` parameter and adding `container` and `disablePortal` to align
    with MUI props.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The children to render into the container. Default is None.
        Can be a `State` object for dynamic updates.
    container : State, QWidget, Callable, or None, optional
        The container widget to render the children into. Default is None (uses QApplication.instance().mainWindow).
        Can be a `State` object for dynamic updates or a Callable returning a QWidget.
    disablePortal : State or bool, optional
        If True, children are rendered in the parent component's hierarchy instead of a portal.
        Default is False.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class.

    Notes
    -----
    - The existing `children` parameter is retained.
    - New parameters `container` and `disablePortal` are added to align with MUI Portal props.
    - MUI classes applied: `MuiPortal-root`.
    - Integrates with `qtmui` theme for styling.

    Demos:
    - Portal: https://qtmui.com/material-ui/qtmui-portal/

    API Reference:
    - Portal API: https://qtmui.com/material-ui/api/portal/
    """

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        container: Optional[Union[State, QWidget, Callable]] = None,
        disablePortal: Union[State, bool] = False,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"Portal-{str(uuid.uuid4())}")
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_container(container)
        self._set_disablePortal(disablePortal)

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
        file_path="qtmui.material.portal",
        param_name="children",
        supported_signatures=Union[State, QWidget, List, type(None)]
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
        elif isinstance(children, QWidget):
            self._widget_references.append(children)
        elif children is not None:
            raise TypeError(f"children must be a State, QWidget, List[QWidget], or None, got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        children = self._children.value if isinstance(self._children, State) else self._children
        return children if isinstance(children, list) else [children] if isinstance(children, QWidget) else []

    @_validate_param(
        file_path="qtmui.material.portal",
        param_name="container",
        supported_signatures=Union[State, QWidget, Callable, type(None)]
    )
    def _set_container(self, value):
        """Assign value to container."""
        self._container = value

    def _get_container(self):
        """Get the container value."""
        container = self._container
        if isinstance(container, State):
            container = container.value
        if callable(container):
            container = container()
        return container if isinstance(container, QWidget) else QApplication.instance().mainWindow

    @_validate_param(
        file_path="qtmui.material.portal",
        param_name="disablePortal",
        supported_signatures=Union[State, bool]
    )
    def _set_disablePortal(self, value):
        """Assign value to disablePortal."""
        self._disablePortal = value

    def _get_disablePortal(self):
        """Get the disablePortal value."""
        return self._disablePortal.value if isinstance(self._disablePortal, State) else self._disablePortal

    def _init_ui(self):
        """Initialize the UI based on props."""
        # Clear previous widgets
        self._widget_references.clear()
        if hasattr(self, 'layout') and self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().setParent(None)

        # Set layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.theme.spacing(1))

        # Set size policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set parent based on disablePortal
        if not self._get_disablePortal():
            self.setParent(self._get_container())
        else:
            self.setParent(None)  # Keep in parent's hierarchy

        # Add children
        children = self._get_children()
        for child in children:
            child.setParent(self if self._get_disablePortal() else self._get_container())
            self.layout().addWidget(child)

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the Portal."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        portal_styles = component_styled.get("Portal", {}).get("styles", {})
        root_styles = portal_styles.get("root", {})
        root_qss = get_qss_style(root_styles)

        # Apply MUI classes
        mui_classes = ["MuiPortal-root"]

        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                background: {self.theme.palette.background.default};
            }}
        """
        self.setStyleSheet(stylesheet)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._container, State):
            self._container.valueChanged.connect(self._on_container_changed)
        if isinstance(self._disablePortal, State):
            self._disablePortal.valueChanged.connect(self._on_disablePortal_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._init_ui()

    def _on_container_changed(self):
        """Handle changes to container."""
        self._set_container(self._container)
        self._init_ui()

    def _on_disablePortal_changed(self):
        """Handle changes to disablePortal."""
        self._set_disablePortal(self._disablePortal)
        self._init_ui()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)
        if isinstance(self._container, State):
            self._container.valueChanged.disconnect(self._on_container_changed)
        if isinstance(self._disablePortal, State):
            self._disablePortal.valueChanged.disconnect(self._on_disablePortal_changed)