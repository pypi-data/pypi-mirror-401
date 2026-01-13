import asyncio
import json
import uuid
from typing import Optional, Union, Dict, Callable

from PySide6.QtWidgets import QVBoxLayout, QFrame, QWidget, QApplication
from PySide6.QtCore import Qt, QEvent
from qtmui.hooks import State
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class Container(QFrame, PyWidgetBase):
    """
    A component that centers and constrains the width of its content based on breakpoints.

    The `Container` component is used to wrap content and apply responsive width constraints
    based on Material-UI breakpoints. It supports all props of the Material-UI `Container`
    component, including native component props via `**kwargs`.

    Parameters
    ----------
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, str, or None, optional
        The component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If True, removes left and right padding. Default is False.
        Can be a `State` object for dynamic updates.
    fixed : State or bool, optional
        If True, sets max-width to match the min-width of the current breakpoint.
        Default is False. Can be a `State` object for dynamic updates.
    maxWidth : State, str, or bool, optional
        Determines the max-width of the container ("xs", "sm", "md", "lg", "xl", False, or custom string).
        Default is "lg". Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The child elements to be contained. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_MAX_WIDTH : list[Union[str, bool]]
        Valid values for the `maxWidth` parameter: ["xs", "sm", "md", "lg", "xl", False].
    MAX_WIDTHS : dict[str, int]
        Maximum widths for breakpoints: {"xs": 0, "sm": 600, "md": 900, "lg": 1200, "xl": 1536}.
    MIN_WIDTHS : dict[str, int]
        Minimum widths for breakpoints: {"xs": 0, "sm": 600, "md": 900, "lg": 1200, "xl": 1536}.

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - Container: https://qtmui.com/material-ui/qtmui-container/

    API Reference:
    - Container API: https://qtmui.com/material-ui/api/container/
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
        key: str =  None,
        disableGutters: Optional[Union[bool, State]] = False,  # Remove left/right padding if True
        fixed: Optional[Union[bool, State]] = False,           # If True, maxWidth matches minWidth of current breakpoint
        maxWidth: Optional[Union[str, bool, State]] = "lg",    # Maximum width limit
        sx: Optional[Union[State, Callable, str, Dict]] = None,  # Custom styles
        children: Optional[Union[State, list]] = None,         # List of child elements (only accepts State or list)
        **kwargs
    ):
        # Initialize parent QFrame
        super().__init__(**kwargs)
        self.setObjectName(str(uuid.uuid4()))
        PyWidgetBase._setUpUi(self)
        
        self._key = key

        self.theme = useTheme()
        
        self._current_breakpoint = None  # Cache breakpoint hiện tại
        self._marginLeft = 0

        # List to hold references to child widgets to prevent Qt from deleting them
        self._widget_references = []

        # Assign values to properties
        self._set_disableGutters(disableGutters)
        self._set_fixed(fixed)
        self._set_maxWidth(maxWidth)
        self._set_children(children)
        self._set_sx(sx)

        # from PyWidgetBase
        self._setup_sx_position(sx)  # Gán sx và khởi tạo các thuộc tính định vị

        # Initialize UI
        self._init_ui()


    def eventFilter(self, obj, event):
        """Monitor events of the parent to track size changes."""
        if obj == self.parent() and event.type() == QEvent.Resize:
            print(f"Parent resizeEvent: parent_rect={self.parent().rect() if self.parent() else 'N/A'}, parent_width={self.parent().width() if self.parent() else 'N/A'}, parent_height={self.parent().height() if self.parent() else 'N/A'}")
        return super().eventFilter(obj, event)

    @_validate_param(file_path="qtmui.material.container", param_name="disableGutters", supported_signatures=Union[bool, State])
    def _set_disableGutters(self, value):
        """Assign value to disableGutters."""
        self._disableGutters = value

    def _get_disableGutters(self):
        """Get the disableGutters value."""
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    @_validate_param(file_path="qtmui.material.container", param_name="fixed", supported_signatures=Union[bool, State])
    def _set_fixed(self, value):
        """Assign value to fixed."""
        self._fixed = value

    def _get_fixed(self):
        """Get the fixed value."""
        return self._fixed.value if isinstance(self._fixed, State) else self._fixed

    @_validate_param(file_path="qtmui.material.container", param_name="maxWidth", supported_signatures=Union[str, bool, State], valid_values=VALID_MAX_WIDTH)
    def _set_maxWidth(self, value):
        """Assign value to maxWidth."""
        self._maxWidth = value

    def _get_maxWidth(self):
        """Get the maxWidth value."""
        return self._maxWidth.value if isinstance(self._maxWidth, State) else self._maxWidth

    @_validate_param(file_path="qtmui.material.container", param_name="children", supported_signatures=Union[State, list, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references to prevent Qt deletion."""
        self._widget_references.clear()
        self._children = value
        children = self._get_children()

        # Validate and store references to child widgets
        if isinstance(children, list):
            for child in children:
                if child is None:
                    continue
                if isinstance(child, QWidget):
                    self._widget_references.append(child)
                    # Ensure child widgets expand to fill the width of widgetContents
                    # child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
                elif isinstance(child, list):
                    for sub_child in child:
                        if isinstance(sub_child, QWidget):
                            self._widget_references.append(sub_child)
                            # sub_child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
                else:
                    raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
        elif children is not None:
            raise TypeError(f"children must be a State or list, but got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.container", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value"""
        self._sx = value

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

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
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
        """Handle changes to disableGutters."""
        self._set_disableGutters(self._disableGutters)
        self._update_margins()

    def _on_fixed_changed(self):
        """Handle changes to fixed."""
        self._set_fixed(self._fixed)

    def _on_maxWidth_changed(self):
        """Handle changes to maxWidth."""
        self._set_maxWidth(self._maxWidth)

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)  # Sử dụng set_sx từ PyWidgetBase
        self._set_stylesheet()

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._clear_layout()
        self._add_children_to_layout()

    def _clear_layout(self):
        """Remove all widgets from the layout."""
        while self.contentLayout.count():
            item = self.contentLayout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                if widget in self._child_abs:
                    self._child_abs.remove(widget)
                    widget._relative_to = None

    def _init_ui(self):
        QApplication.instance().mainWindow.installEventFilter(self)
        
        """Initialize the Container UI."""
        # Use QVBoxLayout to center content horizontally
        self.setLayout(QVBoxLayout())
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)  # Ensure no margins interfere with centering

        # Update margins and maxWidth
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
        """Add child components to the layout."""
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
                            self.layout().addWidget(child)
                        else:
                            self.layout().addWidget(child)
                    else:
                        raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
            else:
                raise TypeError(f"children must be a State or list, but got {type(children)}")

    def _update_margins(self):
        """Update margins based on disableGutters."""
        disable_gutters = self._get_disableGutters()
        if disable_gutters:
            self.layout().setContentsMargins(0, 0, 0, 0)
        else:
            self.layout().setContentsMargins(16, 0, 16, 0)  # Default padding of 16px on left/right

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


    # Hàm helper: cố gắng center trong parent layout, fallback move()
    def _center_in_parent(self, new_width):
        parent = self.parentWidget()
        if parent is None:
            return
        parent_width = parent.width()
        parent_layout = parent.layout()

        # Try set alignment on parent layout for this widget
        if parent_layout is not None:
            try:
                # Try direct widget alignment (works on many PySide/PyQt)
                parent_layout.setAlignment(self, Qt.AlignHCenter | Qt.AlignTop)
                return
            except Exception:
                # If direct setAlignment(widget, ...) not supported, try find QLayoutItem
                try:
                    for i in range(parent_layout.count()):
                        item = parent_layout.itemAt(i)
                        if item is not None and item.widget() is self:
                            parent_layout.setAlignment(item, Qt.AlignHCenter | Qt.AlignTop)
                            return
                except Exception:
                    pass

        # Fallback: manually move widget to center (when no layout controlling it)
        x = max((parent_width - new_width) // 2, 0)
        # Keep current y
        y = self.y() if hasattr(self, 'y') else 0
        self.move(x, y)

    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)

    # Thay thế adjustWidth hoàn chỉnh:
    def adjustWidth(self):
        """Adjust the container width based on parent width and breakpoints,
        and center it. Only update stylesheet when breakpoint changes.
        """
        # parent = self.parentWidget()
        # parent_width = parent.width() if parent is not None else self.width()
        parent_width = self.parent().width()
        
        # Determine new width and breakpoint
        if parent_width < 576:
            new_width = parent_width
            bp = "xs"
        elif parent_width < 768:
            new_width = 540
            bp = "sm"
        elif parent_width < 992:
            new_width = 720
            bp = "md"
        elif parent_width < 1200:
            new_width = 960
            bp = "lg"
        elif parent_width < 1400:
            new_width = 1140
            bp = "xl"
        else:
            new_width = 1320
            bp = "xxl"

        # Ensure not wider than parent
        if new_width > parent_width:
            new_width = parent_width

        # Enforce width so layouts/widgets will respect it
        # Use setFixedWidth to avoid layout stretching; if you prefer flexible, use setMaximumWidth
        self.setFixedWidth(int(new_width))

        # # Only update container-level stylesheet when breakpoint changes
        # if bp != self._current_breakpoint:
        #     self._current_breakpoint = bp
        #     self._set_stylesheet()

        # Center container in parent (prefer layout alignment, fallback to move)
        self._center_in_parent(new_width)
 


    # Dùng một eventFilter duy nhất (thay thế cặp eventFilter cũ)
    def eventFilter(self, obj, event):
        # If parent (or mainWindow) resized, adjust width
        if event.type() == QEvent.Type.Resize:
            # If the event is from our parent or from the installed mainWindow, do adjust
            # We consider both parentWidget() and the mainWindow where this container lives.
            sender = obj
            if sender is self.parent() or sender is QApplication.instance().mainWindow:
                # small debounce: use singleShot 0 to ensure layouts updated before measuring
                # QTimer.singleShot(0, self.adjustWidth)
                self.adjustWidth()
        return super().eventFilter(obj, event)
        
        