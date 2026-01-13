import asyncio
import json
import uuid
from typing import Optional, Union, Dict, Callable

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QWidget, QApplication, QSizePolicy
from PySide6.QtCore import Qt, QEvent
from qtmui.hooks import State
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class Container(QFrame, PyWidgetBase):
    """
    A component that centers and constrains the width of its content based on breakpoints.
    """

    # Valid values for maxWidth
    VALID_MAX_WIDTH = ["xs", "sm", "md", "lg", "xl", False]

    # Define max-width based on breakpoints (from MUI)
    MAX_WIDTHS = {
        "xs": 0,    # No limit
        "sm": 600,
        "md": 900,
        "lg": 1200,
        "xl": 1536,
    }

    # Define min-width based on breakpoints (used when fixed=True)
    MIN_WIDTHS = {
        "xs": 0,
        "sm": 600,
        "md": 900,
        "lg": 1200,
        "xl": 1536,
    }

    def __init__(
        self,
        key: str = None,
        disableGutters: Optional[Union[bool, State]] = False,
        fixed: Optional[Union[bool, State]] = False,
        maxWidth: Optional[Union[str, bool, State]] = "lg",
        sx: Optional[Union[State, Callable, str, Dict]] = None,
        children: Optional[Union[State, list]] = None,
        **kwargs
    ):
        # Initialize parent QFrame
        super().__init__(**kwargs)
        self.setObjectName(str(uuid.uuid4()))
        PyWidgetBase._setUpUi(self)
        
        self._key = key
        self.theme = useTheme()
        self._current_breakpoint = None

        # List to hold references to child widgets to prevent Qt from deleting them
        self._widget_references = []

        # Assign values to properties
        self._set_disableGutters(disableGutters)
        self._set_fixed(fixed)
        self._set_maxWidth(maxWidth)
        self._set_children(children)
        self._set_sx(sx)

        # from PyWidgetBase
        self._setup_sx_position(sx)

        # Initialize UI
        self._init_ui()

    # ...existing validation and getter methods...
    @_validate_param(file_path="qtmui.material.container", param_name="disableGutters", supported_signatures=Union[bool, State])
    def _set_disableGutters(self, value):
        self._disableGutters = value

    def _get_disableGutters(self):
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    @_validate_param(file_path="qtmui.material.container", param_name="fixed", supported_signatures=Union[bool, State])
    def _set_fixed(self, value):
        self._fixed = value

    def _get_fixed(self):
        return self._fixed.value if isinstance(self._fixed, State) else self._fixed

    @_validate_param(file_path="qtmui.material.container", param_name="maxWidth", supported_signatures=Union[str, bool, State], valid_values=VALID_MAX_WIDTH)
    def _set_maxWidth(self, value):
        self._maxWidth = value

    def _get_maxWidth(self):
        return self._maxWidth.value if isinstance(self._maxWidth, State) else self._maxWidth

    @_validate_param(file_path="qtmui.material.container", param_name="children", supported_signatures=Union[State, list, type(None)])
    def _set_children(self, value):
        self._widget_references.clear()
        self._children = value
        children = self._get_children()

        if isinstance(children, list):
            for child in children:
                if child is None:
                    continue
                if isinstance(child, QWidget):
                    self._widget_references.append(child)
                elif isinstance(child, list):
                    for sub_child in child:
                        if isinstance(sub_child, QWidget):
                            self._widget_references.append(sub_child)
                else:
                    raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
        elif children is not None:
            raise TypeError(f"children must be a State or list, but got {type(children)}")

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.container", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        self._sx = value

    # ...existing signal methods...
    def _connect_signals(self):
        if isinstance(self._disableGutters, State):
            self._disableGutters.valueChanged.connect(self._on_disableGutters_changed)
        if isinstance(self._fixed, State):
            self._fixed.valueChanged.connect(self._on_fixed_changed)
        if isinstance(self._maxWidth, State):
            self._maxWidth.valueChanged.connect(self._on_maxWidth_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)

    def _on_disableGutters_changed(self):
        self._set_disableGutters(self._disableGutters)
        self._update_margins()

    def _on_fixed_changed(self):
        self._set_fixed(self._fixed)
        self.adjustWidth()

    def _on_maxWidth_changed(self):
        self._set_maxWidth(self._maxWidth)
        self.adjustWidth()

    def _on_sx_changed(self):
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_children_changed(self):
        self._set_children(self._children)
        self._clear_layout()
        self._add_children_to_layout()

    def _init_ui(self):
        """Initialize the Container UI with QHBoxLayout and widgetContents."""
        # Use QHBoxLayout for Container to center the content widget
        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Create a content widget to hold children - this will have responsive width
        self.widgetContents = QFrame()
        self.widgetContents.setObjectName(str(uuid.uuid4()))
        self.contentLayout = QVBoxLayout(self.widgetContents)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)

        # Add the content widget to the main layout - this auto-centers it
        self.layout().addWidget(self.widgetContents)

        # Update margins based on disableGutters
        self._update_margins()

        # Add child components
        self._add_children_to_layout()

        # Update positions of child components with position: absolute
        self.update_absolute_children()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()
        self.destroyed.connect(self._on_destroyed)

        # Connect signals for State parameters
        self._connect_signals()

    def _add_children_to_layout(self):
        """Add child components to the contentLayout."""
        if self._children is not None:
            children = self._get_children()
            if isinstance(children, list):
                for child in children:
                    if child is None:
                        continue
                    if isinstance(child, QWidget):
                        # Check if the widget has position: absolute
                        sx = getattr(child, '_sx', None)
                        if sx and isinstance(sx, dict) and sx.get("position") == "absolute":
                            self._child_abs.append(child)
                            child._relative_to = self
                            self.contentLayout.addWidget(child)
                        else:
                            self.contentLayout.addWidget(child)
                    else:
                        raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")

    def _update_margins(self):
        """Update margins based on disableGutters."""
        if hasattr(self, 'contentLayout'):
            disable_gutters = self._get_disableGutters()
            if disable_gutters:
                self.contentLayout.setContentsMargins(0, 0, 0, 0)
            else:
                self.contentLayout.setContentsMargins(16, 0, 16, 0)  # Default padding of 16px on left/right

    def _clear_layout(self):
        """Remove all widgets from the contentLayout."""
        if hasattr(self, 'contentLayout'):
            while self.contentLayout.count():
                item = self.contentLayout.takeAt(0)
                if item.widget():
                    widget = item.widget()
                    widget.setParent(None)
                    if hasattr(self, '_child_abs') and widget in self._child_abs:
                        self._child_abs.remove(widget)
                        widget._relative_to = None

    def adjustWidth(self):
        """Adjust the widgetContents width based on parent size, fixed, and maxWidth settings."""
        if not hasattr(self, 'widgetContents'):
            return
            
        if not self.parent():
            return
            
        parent_width = self.parent().width()
        
        # Get current settings
        fixed = self._get_fixed()
        max_width_setting = self._get_maxWidth()
        
        # Determine current MUI breakpoint based on parent width
        if parent_width < 600:  # xs
            current_breakpoint = "xs"
        elif parent_width < 900:  # sm
            current_breakpoint = "sm"
        elif parent_width < 1200:  # md
            current_breakpoint = "md"
        elif parent_width < 1536:  # lg
            current_breakpoint = "lg"
        else:  # xl
            current_breakpoint = "xl"
        
        # Default behavior: widgetContents equals parent width
        new_width = parent_width
        
        # Apply maxWidth constraint first
        if max_width_setting != False and max_width_setting in self.MAX_WIDTHS:
            max_width_limit = self.MAX_WIDTHS[max_width_setting]
            if max_width_limit > 0:  # 0 means no limit (xs case)
                new_width = min(new_width, max_width_limit)
        
        # Apply fixed constraint - use width of previous breakpoint
        if fixed:
            if current_breakpoint == "xl":
                fixed_width = self.MIN_WIDTHS["lg"]  # 1200
            elif current_breakpoint == "lg":
                fixed_width = self.MIN_WIDTHS["md"]  # 900
            elif current_breakpoint == "md":
                fixed_width = self.MIN_WIDTHS["sm"]  # 600
            elif current_breakpoint == "sm":
                fixed_width = self.MIN_WIDTHS["xs"]  # 0 (full width)
            else:  # xs
                fixed_width = 0  # Full width for xs
                
            if fixed_width > 0:
                new_width = fixed_width
        
        # Final constraint: ensure not wider than parent
        new_width = min(new_width, parent_width)
        
        # Set the width on widgetContents - this automatically centers due to QHBoxLayout
        self.widgetContents.setMaximumWidth(int(new_width))
        
        print(f"Container width: parent={parent_width}, breakpoint={current_breakpoint}, fixed={fixed}, maxWidth={max_width_setting}, final_width={new_width}")

    def eventFilter(self, obj, event):
        """Monitor events of the parent to track size changes."""
        if obj == self.parent() and event.type() == QEvent.Resize:
            self.adjustWidth()
        return super().eventFilter(obj, event)

    def _on_destroyed(self):
        """Disconnect signals when the object is destroyed."""
        if isinstance(self._disableGutters, State):
            self._disableGutters.valueChanged.disconnect(self._on_disableGutters_changed)
        if isinstance(self._fixed, State):
            self._fixed.valueChanged.disconnect(self._on_fixed_changed)
        if isinstance(self._maxWidth, State):
            self._maxWidth.valueChanged.disconnect(self._on_maxWidth_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the Container."""
        self.theme = useTheme()

        ownerState = {}
        if not component_styled:
            component_styled = self.theme.components
        PyContainer_root = component_styled["PyContainer"].get("styles")["root"]
        PyContainer_root_qss = get_qss_style(PyContainer_root)

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, State):
                sx = self._sx.value
            elif isinstance(self._sx, Callable):
                sx = self._sx()
            else:
                sx = self._sx

            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        # Apply classes corresponding to MUI
        classes = ["MuiContainer-root"]
        disable_gutters = self._get_disableGutters()
        fixed = self._get_fixed()
        max_width = self._get_maxWidth()

        if disable_gutters:
            classes.append("MuiContainer-disableGutters")
        if fixed:
            classes.append("MuiContainer-fixed")
        if max_width in self.VALID_MAX_WIDTH:
            classes.append(f"MuiContainer-maxWidth{max_width.capitalize()}")

        class_styles = " ".join(classes)

        stylesheet = f"""
            #{self.objectName()} {{
                {PyContainer_root_qss}
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def showEvent(self, e):
        """ fade in """
        self.adjustWidth()
        PyWidgetBase.showEvent(self)
        super().showEvent(e)

    def paintEvent(self, arg__1):
        """Handle paint events."""
        PyWidgetBase.paintEvent(self, arg__1)
        return super().paintEvent(arg__1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustWidth()
        PyWidgetBase.resizeEvent(self, event)