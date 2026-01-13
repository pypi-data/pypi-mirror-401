import asyncio
from typing import Optional, Union, Dict, Callable, List
import uuid
from PySide6.QtWidgets import QGridLayout, QFrame, QWidget, QSizePolicy, QApplication
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
    It allows for responsive layouts with customizable columns, spacing, and properties.

    Parameters
    ----------
    children : State, str, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the component (text, widget, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    columns : State, int, Dict[str, int], or List[int], optional
        The number of columns (e.g., 12). Default is None (inherits from parent or 12).
        Can be a `State` object or responsive dict/list for breakpoints.
    columnSpacing : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Horizontal space between items. Default is None (uses spacing or inherits).
        Can be a `State` object or responsive dict/list.
    container : State or bool, optional
        If True, the component acts as a container. Default is False.
        Can be a `State` object for dynamic updates.
    direction : State, str, Dict[str, str], or List[str], optional
        Direction ("row", "row-reverse"). Default is "row".
        Can be a `State` object or responsive dict/list.
    offset : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Offset for items. Default is None.
        Can be a `State` object or responsive dict/list.
    rowSpacing : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Vertical space between items. Default is None (uses spacing or inherits).
        Can be a `State` object or responsive dict/list.
    size : State, int, str, Dict[str, Union[int, str]], List[Union[int, str]], or None, optional
        Size of items per breakpoint ("grow", "auto", or int). Default is None.
        Can be a `State` object or responsive dict/list.
    spacing : State, int, str, Dict[str, Union[int, str]], or List[Union[int, str]], optional
        Space between items. Default is None (inherits or 0).
        Can be a `State` object or responsive dict/list.
    wrap : State or str, optional
        Wrap style ("wrap", "nowrap", "wrap-reverse"). Default is "wrap".
        Can be a `State` object for dynamic updates.
    key : State, str, or None, optional
        Unique identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class.

    Attributes
    ----------
    VALID_DIRECTIONS = ["row", "row-reverse"]
    VALID_WRAP = ["wrap", "nowrap", "wrap-reverse"]

    Notes
    -----
    - Direction "column" and "column-reverse" not supported; use Stack for vertical.
    - Size "grow" shares remaining space equally among grow items in row.
    - Size "auto" sizes based on content, with Maximum policy.
    - Offset "auto" pushes item to end of row.
    - Wrap "nowrap" may cause overflow; "wrap-reverse" reverses row order.

    Demos:
    - Grid: https://qtmui.com/material-ui/qtmui-grid/

    API Reference:
    - Grid API: https://qtmui.com/material-ui/api/grid/
    """

    VALID_DIRECTIONS = ["row", "row-reverse"]
    VALID_WRAP = ["wrap", "nowrap", "wrap-reverse"]

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        container: Optional[Union[bool, State]] = False,
        key: Optional[Union[str, State]] = None,
        columns: Optional[Union[int, Dict, List, State]] = None,
        columnSpacing: Optional[Union[int, str, Dict, List, State]] = None,
        direction: Optional[Union[str, Dict, List, State]] = "row",
        offset: Optional[Union[int, str, Dict, List, State]] = None,
        spacing: Optional[Union[int, str, Dict, List, State]] = None,
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

    @_validate_param(file_path="qtmui.material.grid", param_name="columns", supported_signatures=Union[int, Dict, List, State, type(None)], validator=lambda x: x > 0 if isinstance(x, int) else True)
    def _set_columns(self, value):
        self._columns = value

    def _get_columns(self):
        columns = self._columns.value if isinstance(self._columns, State) else self._columns
        """✅ NESTED GRID: Kế thừa columns từ parent nếu không khai báo"""
        if columns is None and self._get_container():
            parent = self.parent()
            if parent and isinstance(parent, Grid):
                return parent._get_columns()
            return 12
        if isinstance(columns, dict):
            return self._resolve_breakpoint_value(columns, self._get_breakpoint())
        elif isinstance(columns, list):
            return columns[0] if columns else 12
        return columns

    @_validate_param(file_path="qtmui.material.grid", param_name="columnSpacing", supported_signatures=Union[int, str, Dict, List, State, type(None)], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else True)
    def _set_columnSpacing(self, value):
        self._columnSpacing = value

    def _get_columnSpacing(self):
        """✅ NESTED GRID: Kế thừa columnSpacing từ parent nếu không khai báo"""
        if self._columnSpacing is None and self._get_container():
            parent = self.parent()
            if parent and isinstance(parent, Grid):
                return parent._get_columnSpacing()
            return self._get_spacing()
        return self._compute_spacing(self._columnSpacing)

    @_validate_param(file_path="qtmui.material.grid", param_name="direction", supported_signatures=Union[str, Dict, List, State], valid_values=VALID_DIRECTIONS)
    def _set_direction(self, value):
        self._direction = value

    def _get_direction(self):
        direction = self._direction.value if isinstance(self._direction, State) else self._direction
        if isinstance(direction, dict):
            return self._resolve_breakpoint_value(direction, self._get_breakpoint())
        elif isinstance(direction, list):
            return direction[0] if direction else "row"
        return direction

    def _set_offset(self, value):
        self._offset = value

    def _get_offset(self):
        return self._offset.value if isinstance(self._offset, State) else self._offset

    @_validate_param(file_path="qtmui.material.grid", param_name="spacing", supported_signatures=Union[int, float, str, Dict, State, type(None)], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else True)
    def _set_spacing(self, value):
        self._spacing = value

    def _compute_spacing(self, spacing):
        spacing_value = spacing.value if isinstance(spacing, State) else spacing
        
        if isinstance(spacing_value, dict):
            spacing_value = self._resolve_breakpoint_value(spacing_value, self._get_breakpoint())
        elif isinstance(spacing_value, list):
            spacing_value = spacing_value[0] if spacing_value else 0
        
        if isinstance(spacing_value, (int, float)):
            spacing_value = int(spacing_value * self.theme.spacing.default_spacing)
        elif isinstance(spacing_value, str) and spacing_value.endswith("px"):
            spacing_value = int(spacing_value.replace("px", ""))
            
        return spacing_value

    def _get_spacing(self):
        """✅ NESTED GRID: Kế thừa spacing từ parent nếu không khai báo"""
        if self._spacing is None and self._get_container():
            parent = self.parent()
            if parent and isinstance(parent, Grid):
                return parent._get_spacing()
            return 0
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
        """✅ NESTED GRID: Kế thừa rowSpacing từ parent nếu không khai báo"""
        if self._rowSpacing is None and self._get_container():
            parent = self.parent()
            if parent and isinstance(parent, Grid):
                return parent._get_rowSpacing()
            return self._get_spacing()
        return self._compute_spacing(self._rowSpacing)

    # @_validate_param(file_path="qtmui.material.grid", param_name="size", supported_signatures=Union[int, str, bool, Dict[str, Union[int, str, bool]], List[Union[int, str, bool]], type(None)], validator=lambda x: x > 0 if isinstance(x, (int, float)) else True)
    def _set_size(self, value):
        self._size = value

    def _get_size(self):
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.grid", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _setup_sx_position(self, sx):
        pass

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

    def _setup_layout(self):
        if self.layout() is None:
            self.setLayout(QGridLayout())
            self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self.layout().setVerticalSpacing(self._get_rowSpacing() or 0)
        self.layout().setHorizontalSpacing(self._get_columnSpacing() or 0)
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

        stylesheet = f"""
            #{self.objectName()} {{
                {PyGrid_root_qss}
            }}
            
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

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

    def _add_columns_by_breakpoint(self, breakpoint: str, size: Union[int, str, bool, Dict, List]) -> Union[int, str]:
        if size is None:
            return "auto"
        if isinstance(size, dict):
            value = self._resolve_breakpoint_value(size, breakpoint)
        elif isinstance(size, list):
            value = size[0] if size else "auto"
        elif isinstance(size, bool):
            value = 'grow' if size else None
        else:
            value = size
        return value
    

    def _get_offset_by_breakpoint(self, breakpoint: str, offset: Union[int, str, Dict, List]) -> Union[int, str]:
        if offset is None:
            return 0
        if isinstance(offset, dict):
            value = self._resolve_breakpoint_value(offset, breakpoint)
        elif isinstance(offset, list):
            value = offset[0] if offset else 0
        else:
            value = offset
        return value

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

    def _arrange_children(self):
        # ===========================================
        # BƯỚC 0: KHỞI TẠO THÔNG TIN CƠ BẢN
        # ===========================================
        self.breakpoint = self._get_breakpoint()  # Lấy breakpoint hiện tại (xs, sm, md...)
        is_container = self._get_container()      # Grid này có phải container không?
        columns = self._get_columns()             # Số cột tổng (4, 8, 12...)
        columns = self._get_columns_by_breakpoint(self.breakpoint, columns)
        
        direction = self._get_direction()         # Hướng sắp xếp (row/column)
        wrap = self._get_wrap()                   # Cách wrap (wrap/nowrap...)
        children = self._get_children()
        if not isinstance(children, list):
            children = [children] if children else []

        # ===========================================
        # BƯỚC 1: XỬ LÝ GRID ITEM (container=False)
        # ===========================================
        if not is_container:
            if not columns:
                columns = 1
            # ✅ ITEM MODE: Đơn giản, xếp children theo lưới cố định
            row = 0
            col = 0
            for child in children:
                if isinstance(child, QWidget):
                    self.layout().addWidget(child, row, col)
                elif isinstance(child, str):
                    self.layout().addWidget(Typography(text=child), row, col)
                col += 1
                if col >= columns:  # Hết cột → xuống hàng mới
                    col = 0
                    row += 1
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
            return

        # ===========================================
        # BƯỚC 2: RESET TẤT CẢ COLUMN STRETCH = 0
        # ===========================================
        # ✅ Quan trọng: Reset stretch về 0 để tính toán lại từ đầu
        for c in range(columns):
            self.layout().setColumnStretch(c, 0)

        # ===========================================
        # BƯỚC 3: TENTATIVE PLACEMENT - XÁC ĐỊNH CÁC HÀNG
        # ===========================================
        # Mục đích: Thử đặt các item để biết chúng thuộc hàng nào
        rows = []           # Danh sách các hàng
        current_row = []    # Hàng hiện tại đang xây dựng
        col = 0 if direction == "row" else columns  # Vị trí bắt đầu
        
        for child in children:
            # Lấy size và offset của child
            if not isinstance(child, Grid):
                size_value = "auto"    # Non-Grid = auto
                offset_value = 0
            else:
                size_value = self._add_columns_by_breakpoint(self.breakpoint, child._get_size())
                offset_value = self._get_offset_by_breakpoint(self.breakpoint, child._get_offset())

            # Tính toán vị trí thử nghiệm
            tentative_offset = 0 if offset_value == "auto" else int(offset_value) if isinstance(offset_value, (int, float)) else 0
            # tentative_span = 1 if isinstance(size_value, str) or size_value is None else int(size_value)
            tentative_span = 1 if isinstance(size_value, str) or size_value is None else int(size_value)

            if direction == "row":  # Từ trái sang phải
                new_col = col + tentative_offset + tentative_span
                if wrap == "wrap" and new_col > columns:  # Không đủ chỗ → xuống hàng mới
                    rows.append(current_row)
                    current_row = []
                    col = 0
                    new_col = tentative_offset + tentative_span
                current_row.append((child, offset_value, size_value))  # Lưu thông tin item
                col = new_col
            # ... (column direction tương tự nhưng từ phải sang trái)

        if current_row:  # Thêm hàng cuối nếu còn
            rows.append(current_row)

        if wrap == "wrap-reverse":  # Đảo ngược thứ tự hàng
            rows = rows[::-1]

        # ===========================================
        # BƯỚC 4: XỬ LÝ TỪNG HÀNG - TÍNH TOÁN SPAN THỰC TẾ
        # ===========================================
        row_index = 0
        has_size_auto = False
        has_size_grow = False
        for row_items in rows:
            # 4.1: Lần 1 - Tính span cơ bản và tổng span của fixed items
            item_infos = []  # (child, offset, size_value, span)
            row_span_total = 0  # Tổng span của items có offset != auto
            
            for child, offset_value, size_value in row_items:
                span = 1 if isinstance(size_value, str) or size_value is None else int(size_value)
                if size_value == "auto":
                    span = 1  # Auto luôn chiếm 1 cột tối thiểu
                offset = 0 if offset_value == "auto" else int(offset_value) if isinstance(offset_value, (int, float)) else 0
                item_infos.append((child, offset, size_value, span))
                if offset_value != "auto":  # Chỉ tính fixed items
                    row_span_total += span

            # 4.2: Xử lý offset="auto" - Đẩy item về cuối hàng
            for i in range(len(item_infos)):
                if row_items[i][1] == "auto":  # Item có offset auto
                    push_offset = columns - row_span_total - item_infos[i][3]
                    item_infos[i] = (item_infos[i][0], max(0, push_offset), item_infos[i][2], item_infos[i][3])
                    has_size_auto = True

            # 4.3: Lần 2 - Tính toán grow spans
            total_fixed = 0
            num_grow = 0
            for child, offset, size_value, span in item_infos:
                total_fixed += offset
                if size_value == "grow":
                    num_grow += 1  # Đếm số item grow
                    has_size_grow = True
                else:
                    total_fixed += span
            
            remaining = columns - total_fixed  # Không gian còn lại
            if num_grow > 0 and remaining > 0:
                grow_span = remaining // num_grow      # Span cơ bản cho mỗi grow
                extra = remaining % num_grow           # Phần dư
                grow_idx = 0
                new_item_infos = []
                for child, offset, size_value, span in item_infos:
                    if size_value == "grow":
                        # Phân bổ đều + thêm 1 cho các item đầu
                        new_span = grow_span + (1 if grow_idx < extra else 0)
                        new_item_infos.append((child, offset, size_value, new_span))
                        grow_idx += 1
                    else:
                        new_item_infos.append((child, offset, size_value, span))
                item_infos = new_item_infos

            # ===========================================
            # BƯỚC 5: ĐẶT CÁC ITEM VÀO LAYOUT THỰC TẾ
            # ===========================================
            col = 0 if direction == "row" else columns
            for child, offset, size_value, span in item_infos:
                if direction == "row":
                    # 5.1: Áp dụng offset (khoảng trống trước item)
                    offset_start = col
                    col += offset
                    for o in range(offset_start, col):  # ✅ Stretch offset columns
                        self.layout().setColumnStretch(o, 1)
                    start_col = col
                    col += span

                # 5.2: Thêm widget vào layout
                if isinstance(child, str):
                    widget = Typography(text=child)
                else:
                    widget = child

                # print("Adding widget:", 'widget', "at row", row_index, "col", start_col, "span", span, "columns", columns)
                self.layout().addWidget(widget, row_index, start_col, 1, span)
                
                if isinstance(child, Grid):
                    child._setup_layout()  # Trigger layout của child Grid

                # 5.3: QUAN TRỌNG - Set SizePolicy & ColumnStretch
                if size_value == "auto" or not isinstance(child, Grid) or size_value is None:
                    # ✅ AUTO: Theo nội dung + KHÔNG stretch
                    widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
                    for s in range(span):
                        self.layout().setColumnStretch(start_col + s, 0)
                else:
                    # ✅ FIXED/GROW: Chiếm đều không gian + STRETCH
                    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    if not has_size_grow and not has_size_auto:
                        for s in range(span):
                            self.layout().setColumnStretch(start_col + s, 0)
                    else:
                        for s in range(span):
                            self.layout().setColumnStretch(start_col + s, 1)

            row_index += 1

        # ===========================================
        # BƯỚC CUỐI: HOÀN THIỆN LAYOUT
        # ===========================================
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)


    def resizeEvent(self, event):
        if self._get_breakpoint() != self.breakpoint:
            self._setup_layout()
        return super().resizeEvent(event)

    def _on_destroyed(self):
        pass