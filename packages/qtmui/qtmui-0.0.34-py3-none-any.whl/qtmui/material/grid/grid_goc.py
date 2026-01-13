import asyncio
from typing import Optional, Union, Dict, Callable, List
import uuid
from PySide6.QtWidgets import QGridLayout, QFrame, QHBoxLayout, QWidget, QSizePolicy, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer
from qtmui.hooks import State
from ..typography import Typography
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class Grid(QFrame, PyWidgetBase):
    """
    A component that provides a flexible grid layout for arranging child components.

    The `Grid` component implements the Material-UI Grid system, supporting both container and item behaviors.
    It allows for responsive layouts with customizable columns, spacing, and flex properties.

    Parameters
    ----------
    children : State, str, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the component (text, widget, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    columns : State, int, Dict[str, int], or List[int], optional
        The number of columns (e.g., 12). Default is 12.
        Can be a `State` object or responsive dict/list for breakpoints.
    columnSpacing : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Horizontal space between items. Default is None (uses spacing).
        Can be a `State` object or responsive dict/list.
    container : State or bool, optional
        If True, the component acts as a flex container. Default is False.
        Can be a `State` object for dynamic updates.
    direction : State, str, Dict[str, str], or List[str], optional
        Flex direction ("row", "row-reverse", "column", "column-reverse"). Default is "row".
        Can be a `State` object or responsive dict/list.
    offset : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Offset for items. Default is None.
        Can be a `State` object or responsive dict/list.
    rowSpacing : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Vertical space between items. Default is None (uses spacing).
        Can be a `State` object or responsive dict/list.
    size : State, int, str, bool, Dict[str, Union[int, str, bool]], List[Union[int, str, bool]], or None, optional
        Size of items per breakpoint. Default is None.
        Can be a `State` object or responsive dict/list.
    spacing : State, int, str, Dict[str, Union[int, str]], or List[Union[int, str]], optional
        Space between items. Default is 0.
        Can be a `State` object or responsive dict/list.
    wrap : State or str, optional
        Flex wrap style ("wrap", "nowrap", "wrap-reverse"). Default is "wrap".
        Can be a `State` object for dynamic updates.
    key : State, str, or None, optional
        Unique identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_DIRECTIONS : list[str]
        Valid values for `direction`: ["row", "row-reverse", "column", "column-reverse"].
    VALID_WRAP : list[str]
        Valid values for `wrap`: ["wrap", "nowrap", "wrap-reverse"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - When `container` is True, the Grid acts as a container, arranging children in a grid layout.
    - When `container` is False, the Grid acts as an item, occupying space defined by `size` and `offset`.

    Demos:
    - Grid: https://qtmui.com/material-ui/qtmui-grid/

    API Reference:
    - Grid API: https://qtmui.com/material-ui/api/grid/
    """

    VALID_DIRECTIONS = ["row", "row-reverse", "column", "column-reverse"]
    VALID_WRAP = ["wrap", "nowrap", "wrap-reverse"]

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        container: Optional[Union[bool, State]] = False,
        key: Optional[Union[str, State]] = None,
        columns: Optional[Union[int, Dict, List, State]] = 12,
        columnSpacing: Optional[Union[int, str, Dict, List, State]] = None,
        direction: Optional[Union[str, Dict, List, State]] = "row",
        offset: Optional[Union[int, str, Dict, List, State]] = None,
        spacing: Optional[Union[int, str, Dict, List, State]] = 0,
        wrap: Optional[Union[str, State]] = "wrap",
        children: Optional[Union[str, Callable, list, State]] = None,
        rowSpacing: Optional[Union[int, str, Dict, List, State]] = None,
        size: Optional[Union[int, str, Dict, List, State]] = None,
        sx: Optional[Union[State, Callable, str, Dict]] = None,
        **kwargs
    ):
        super().__init__(parent)
        self.setObjectName(str(uuid.uuid4()))
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()
        self._is_resizing = False
        self.breakpoint = None
        self._spacing_mark = 5
        self._widget_references = []

        self._set_container(container)
        self._set_key(key)
        self._set_columns(columns)
        self._set_columnSpacing(columnSpacing)
        self._set_direction(direction)
        self._set_offset(offset)
        self._set_spacing(spacing)
        self._set_wrap(wrap)
        self._set_children(children)
        self._set_rowSpacing(rowSpacing)
        self._set_size(size)
        self._set_sx(sx)

        self._setup_sx_position(sx)
        self._init_ui()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()
        self.destroyed.connect(self._on_destroyed)

        self._connect_signals()

    @_validate_param(file_path="qtmui.material.grid", param_name="container", supported_signatures=Union[bool, State])
    def _set_container(self, value):
        self._container = value
        self._item = not value if isinstance(value, bool) else not value.value

    def _get_container(self):
        return self._container.value if isinstance(self._container, State) else self._container

    @_validate_param(file_path="qtmui.material.grid", param_name="key", supported_signatures=Union[str, State, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.grid", param_name="columns", supported_signatures=Union[int, Dict, List, State], validator=lambda x: x > 0 if isinstance(x, int) else True)
    def _set_columns(self, value):
        self._columns = value

    def _get_columns(self):
        return self._columns.value if isinstance(self._columns, State) else self._columns

    @_validate_param(file_path="qtmui.material.grid", param_name="columnSpacing", supported_signatures=Union[int, str, Dict, List, State, type(None)], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else True)
    def _set_columnSpacing(self, value):
        self._columnSpacing = value

    def _get_columnSpacing(self):
        return self._compute_spacing(self._columnSpacing)

    @_validate_param(file_path="qtmui.material.grid", param_name="direction", supported_signatures=Union[str, Dict, List, State], valid_values=VALID_DIRECTIONS)
    def _set_direction(self, value):
        self._direction = value

    def _get_direction(self):
        return self._direction.value if isinstance(self._direction, State) else self._direction

    # @_validate_param(file_path="qtmui.material.grid", param_name="offset", supported_signatures=Union[int, str, Dict, List, State, type(None)], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else x == "auto")
    def _set_offset(self, value):
        self._offset = value

    def _get_offset(self):
        return self._offset.value if isinstance(self._offset, State) else self._offset

    @_validate_param(file_path="qtmui.material.grid", param_name="spacing", supported_signatures=Union[int, float, str, Dict, State], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else True)
    def _set_spacing(self, value):
        self._spacing = value



    def _get_spacing(self):
        return self._compute_spacing(self._spacing)

    @_validate_param(file_path="qtmui.material.grid", param_name="wrap", supported_signatures=Union[str, State], valid_values=VALID_WRAP)
    def _set_wrap(self, value):
        self._wrap = value

    def _get_wrap(self):
        return self._wrap.value if isinstance(self._wrap, State) else self._wrap

    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.grid", param_name="rowSpacing", supported_signatures=Union[int, str, Dict, List, State, type(None)], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else True)
    def _set_rowSpacing(self, value):
        self._rowSpacing = value

    def _get_rowSpacing(self):
        return self._compute_spacing(self._rowSpacing)

    @_validate_param(file_path="qtmui.material.grid", param_name="size", supported_signatures=Union[int, str, Dict, List, State, type(None)], validator=lambda x: x > 0 if isinstance(x, (int, float)) else True)
    def _set_size(self, value):
        self._size = value
        size = value.value if isinstance(value, State) else value

        if not size:
            size_dict = {'xs': 1}
        elif isinstance(size, dict):
            size_dict = size
        elif isinstance(size, (int, str, list)):
            size_dict = {'xs': size}
        else:
            raise TypeError(f"size must be a dict, int, str, list, or None, but got {type(size)}")

        self.breakpoint_columns = {
            'xs': size_dict.get("xs"),
            'sm': size_dict.get("sm"),
            'md': size_dict.get("md"),
            'lg': size_dict.get("lg"),
            'xl': size_dict.get("xl")
        }

    def _get_size(self):
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.grid", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._setup_layout()

    def _connect_signals(self):
        if isinstance(self._container, State):
            self._container.valueChanged.connect(self._update_container)
        if isinstance(self._key, State):
            self._key.valueChanged.connect(self._set_key)
        if isinstance(self._columns, State):
            self._columns.valueChanged.connect(self._update_columns)
        if isinstance(self._columnSpacing, State):
            self._columnSpacing.valueChanged.connect(self._update_columnSpacing)
        if isinstance(self._direction, State):
            self._direction.valueChanged.connect(self._update_direction)
        if isinstance(self._offset, State):
            self._offset.valueChanged.connect(self._update_offset)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.connect(self._update_spacing)
        if isinstance(self._wrap, State):
            self._wrap.valueChanged.connect(self._update_wrap)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._update_children)
        if isinstance(self._rowSpacing, State):
            self._rowSpacing.valueChanged.connect(self._update_rowSpacing)
        if isinstance(self._size, State):
            self._size.valueChanged.connect(self._update_size)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._update_stylesheet)

    def _update_container(self):
        self._set_container(self._container)
        self._setup_layout()

    def _update_columns(self):
        self._set_columns(self._columns)
        self._setup_layout()

    def _update_columnSpacing(self):
        self._set_columnSpacing(self._columnSpacing)
        self._setup_layout()

    def _update_direction(self):
        self._set_direction(self._direction)
        self._setup_layout()

    def _update_offset(self):
        self._set_offset(self._offset)
        self._setup_layout()

    def _update_spacing(self):
        self._set_spacing(self._spacing)
        self._setup_layout()

    def _update_wrap(self):
        self._set_wrap(self._wrap)
        self._setup_layout()

    def _update_children(self):
        self._set_children(self._children)
        self._setup_layout()

    def _update_rowSpacing(self):
        self._set_rowSpacing(self._rowSpacing)
        self._setup_layout()

    def _update_size(self):
        self._set_size(self._size)
        if self.parent() and isinstance(self.parent(), Grid):
            self.parent()._setup_layout()



    def _setup_layout(self):
        if self.layout() is None:
            direction = self._get_direction()
            if isinstance(direction, dict):
                direction = direction.get(self._get_breakpoint(), "row")
            elif isinstance(direction, list):
                direction = direction[0] if direction else "row"

            if direction in ["row", "row-reverse"]:
                self.setLayout(QGridLayout())
            else:
                self.setLayout(QVBoxLayout())
                self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)


        if self._rowSpacing:
            if isinstance(self.layout(), QGridLayout):
                self.layout().setVerticalSpacing(self._get_rowSpacing())
            else:
                self.layout().setSpacing(self._get_rowSpacing())

        if self._columnSpacing:
            if isinstance(self.layout(), QGridLayout):
                self.layout().setHorizontalSpacing(self._get_columnSpacing())
            else:
                self.layout().setSpacing(self._get_columnSpacing()) 

        if not self._rowSpacing and not self._columnSpacing:
            self.layout().setSpacing(self._get_spacing())

        self._arrange_children()

    def _update_stylesheet(self):
        self._set_stylesheet()

    async def _async_update_stylesheet(self):
        self._set_stylesheet()

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()
        ownerState = {}
        if not component_styled:
            component_styled = self.theme.components

        PyGrid_root_qss = ""
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

        classes = ["MuiGrid-root"]
        if self._get_container():
            classes.append("MuiGrid-container")

        class_styles = " ".join(classes)
        stylesheet = f"""
            #{self.objectName()} {{
                {PyGrid_root_qss}
            }}
            
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def _compute_spacing(self, spacing):
        spacing_value = spacing.value if isinstance(spacing, State) else spacing
        
        if isinstance(spacing_value, dict):
            spacing_value = self._resolve_breakpoint_value(spacing_value, self._get_breakpoint())
        
        if (isinstance(spacing_value, int) or isinstance(spacing_value, float)):
            spacing_value = int(spacing_value * self.theme.spacing.default_spacing)
        elif isinstance(spacing_value, str) and spacing_value.endswith("px"):
            spacing_value = int(spacing_value.replace("px", ""))
            
        return spacing_value

    def _resolve_breakpoint_value(self, config_dict: dict, current_bp: str):
        if not isinstance(config_dict, dict):
            return config_dict

        breakpoints = ["xs", "sm", "md", "lg", "xl"]
        if current_bp not in breakpoints:
            current_bp = "xs"

        bp_index = breakpoints.index(current_bp)
        if current_bp in config_dict:
            return config_dict[current_bp]

        for i in range(bp_index - 1, -1, -1):
            bp = breakpoints[i]
            if bp in config_dict:
                return config_dict[bp]

        return 0

    def _get_breakpoint(self):
        width = QApplication.instance().mainWindow.width()
        if width >= 1536:
            return "xl"
        elif width >= 1200:
            return "lg"
        elif width >= 900:
            return "md"
        elif width >= 600:
            return "sm"
        else:
            return "xs"

    def _get_columns_by_breakpoint(self, breakpoint: str, columns: Union[int, Dict, List]) -> int:
        if isinstance(columns, dict):
            order = ["xs", "sm", "md", "lg", "xl"]
            index = order.index(breakpoint)
            while index >= 0:
                column = columns.get(order[index])
                if column is not None:
                    return column
                index -= 1
            return 12
        elif isinstance(columns, list):
            return columns[0] if columns else 12
        else:
            return columns

    def _add_columns_by_breakpoint(self, breakpoint: str, size: Union[int, Dict, List]) -> int:
        if isinstance(size, dict):
            order = ["xs", "sm", "md", "lg", "xl"]
            index = order.index(breakpoint)
            while index >= 0:
                columns = size.get(order[index])
                if columns is not None:
                    return columns
                index -= 1
            return 12
        elif isinstance(size, list):
            return size[0] if size else 12
        else:
            return size

    def _get_offset_by_breakpoint(self, breakpoint: str, offset: Union[int, Dict, List]) -> Union[int, str]:
        if isinstance(offset, dict):
            order = ["xs", "sm", "md", "lg", "xl"]
            index = order.index(breakpoint)
            while index >= 0:
                off = offset.get(order[index])
                if off is not None:
                    return off
                index -= 1
            return 0
        elif isinstance(offset, list):
            return offset[0] if offset else 0
        else:
            return offset if offset is not None else 0

    def _arrange_children(self):
        self.breakpoint = self._get_breakpoint()
        row = 0
        col = 0
        is_container = self._get_container()
        columns = self._get_columns()
        columns = self._get_columns_by_breakpoint(self.breakpoint, columns)

        if is_container:
            children = self._get_children()
            if not isinstance(children, list):
                children = [children] if children else []

            for child in children:
                if isinstance(child, Grid):
                    # Get size for the current breakpoint
                    child_size = child._get_size()
                    span_columns = self._add_columns_by_breakpoint(self.breakpoint, child_size) or 12
                    if span_columns == "grow":
                        span_columns = columns - col  # Occupy remaining space
                    elif span_columns == "auto":
                        span_columns = 1  # Minimal width for content

                    # Get offset for the current breakpoint
                    offset = child._get_offset()
                    offset_columns = self._get_offset_by_breakpoint(self.breakpoint, offset)
                    if offset_columns == "auto":
                        # Calculate auto offset to align to the end
                        offset_columns = max(0, columns - span_columns - col)
                    elif isinstance(offset_columns, (int, float)):
                        offset_columns = int(offset_columns)
                    else:
                        offset_columns = 0

                    # Apply offset
                    col += offset_columns

                    # Handle row wrapping
                    if col + span_columns > columns:
                        row += 1
                        col = offset_columns

                    # Add widget to layout
                    self.layout().addWidget(child, row, col, 1, span_columns)
                    child._setup_layout()
                    col += span_columns

                    # Move to next row if columns are fully occupied
                    if col >= columns:
                        row += 1
                        col = 0
                else:
                    # Handle non-Grid children (QWidget or str)
                    if isinstance(children, list):
                        for index, child_widget in enumerate(children):
                            if isinstance(child_widget, QWidget):
                                row = index // columns
                                col = index % columns
                                if child_widget.parent() is None:
                                    self.layout().addWidget(child_widget, row, col)
                            elif isinstance(child_widget, str):
                                self.layout().addWidget(Typography(text=child_widget), row, col)
                    elif isinstance(child, QWidget):
                        self.layout().addWidget(child, row, col)
                    elif isinstance(child, str):
                        self.layout().addWidget(Typography(text=child), row, col)

        else:
            children = self._get_children()
            if isinstance(children, list):
                for index, child in enumerate(children):
                    row = index // columns
                    col = index % columns
                    if isinstance(child, QWidget) and child.parent() is None:
                        self.layout().addWidget(child, row, col)
                    elif isinstance(child, str):
                        self.layout().addWidget(Typography(text=child), row, col)
                self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

    def resizeEvent(self, event):
        if self._get_breakpoint() != self.breakpoint:
            self._setup_layout()
        return super().resizeEvent(event)