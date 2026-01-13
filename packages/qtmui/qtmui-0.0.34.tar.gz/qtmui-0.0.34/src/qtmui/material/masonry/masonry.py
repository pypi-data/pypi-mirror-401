# qtmui/material/masonry.py
import asyncio
from typing import Optional, Union, Dict, Callable
import uuid

from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from qtmui.hooks import State, useEffect
from ...common.ui_functions import clear_layout
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.widget_base import PyWidgetBase
from qtmui.material.utils.validate_params import _validate_param
from qtmui.configs import LOAD_WIDGET_ASYNC


class Masonry(QFrame, PyWidgetBase):
    """
    A component that arranges children in a masonry grid layout, styled like Material-UI Masonry.

    The `Masonry` component arranges its children in a dynamic grid layout, distributing them across columns
    to balance heights or in sequential order, with customizable spacing and styling.

    Parameters
    ----------
    children : State, List[QWidget], or QWidget
        The content of the component (required). Can be a single widget or a list of widgets.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    columns : State, int, List[Union[int, str]], dict, or str, optional
        Number of columns. Default is 4.
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "QFrame"). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    defaultColumns : State or int, optional
        The default number of columns for server-side rendering. Default is None.
        Can be a `State` object for dynamic updates.
    defaultHeight : State or int, optional
        The default height in pixels for server-side rendering. Default is None.
        Can be a `State` object for dynamic updates.
    defaultSpacing : State or int, optional
        The default spacing for server-side rendering. Default is None.
        Can be a `State` object for dynamic updates.
    sequential : State or bool, optional
        If True, arranges children in sequential order rather than adding to the shortest column. Default is False.
        Can be a `State` object for dynamic updates.
    spacing : State, int, List[Union[int, str]], dict, or str, optional
        Defines the space between children, as a factor of the theme's spacing. Default is 1.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Notes
    -----
    - The `children` prop is required and must be a QWidget or a list of QWidgets.
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `defaultColumns`, `defaultHeight`, and `defaultSpacing` props are used for server-side rendering initialization.
    - The `sequential` prop changes the layout behavior to add children in order rather than balancing column heights.

    Demos:
    - Masonry: https://qtmui.com/material-ui/qtmui-masonry/

    API Reference:
    - Masonry API: https://qtmui.com/material-ui/api/masonry/
    """

    def __init__(
        self,
        columns: Optional[Union[int, State]] = 4,
        spacing: Optional[Union[int, State]] = 1,
        children: Optional[Union[list, State]] = None,
        sx: Optional[Union[Callable, str, Dict, State]] = None
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))  # Gán objectName trước khi gọi set_sx
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()

        # Gán giá trị ban đầu cho các thuộc tính bằng các hàm _set_*
        self._set_columns(columns)
        self._set_spacing(spacing)
        self._set_children(children)
        self._set_sx(sx)

        # from PyWidgetBase
        self._setup_sx_position(sx)  # Gán sx và khởi tạo các thuộc tính định vị

        self._init_ui()


    @_validate_param(file_path="qtmui.material.masonry", param_name="columns", supported_signatures=Union[int, State], validator=lambda x: x > 0 if isinstance(x, int) else True)
    def _set_columns(self, value):
        """Assign value to columns."""
        self._columns = value

    def _get_columns(self):
        """Get the columns value."""
        return self._columns.value if isinstance(self._columns, State) else self._columns

    @_validate_param(file_path="qtmui.material.masonry", param_name="spacing", supported_signatures=Union[int, State], validator=lambda x: x >= 0 if isinstance(x, (int, float)) else True)
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value

    def _get_spacing(self):
        """Get the spacing value."""
        spacing_value = self._spacing.value if isinstance(self._spacing, State) else self._spacing
        if (isinstance(spacing_value, int) or isinstance(spacing_value, float)) and (0 <= spacing_value <= 3):
            spacing_value = spacing_value * self.theme.spacing.default_spacing
        return spacing_value

    @_validate_param(file_path="qtmui.material.masonry", param_name="children", supported_signatures=Union[list, State, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.masonry", param_name="sx", supported_signatures=Union[Callable, str, Dict, State, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._columns, State):
            self._columns.valueChanged.connect(self._update_columns)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.connect(self._update_spacing)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._update_children)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._update_stylesheet)

    def _on_masonry_destroyed(self):
        if isinstance(self._columns, State):
            self._columns.valueChanged.disconnect(self._setup_layout)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.disconnect(self._setup_layout)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._update_children)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._update_stylesheet)

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        # Create a QVBoxLayout for each column
        self.column_layouts = []

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)

        self._setup_layout()

        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()
        self.destroyed.connect(self._on_destroyed)
        self.destroyed.connect(self._on_masonry_destroyed)

        # Connect signals for State parameters
        self._connect_signals()

    def _update_columns(self):
        """Xử lý khi columns thay đổi."""
        self._setup_layout()

    def _update_spacing(self):
        """Xử lý khi spacing thay đổi."""
        self._setup_layout()

    def _update_children(self):
        """Xử lý khi children thay đổi."""
        self._setup_layout()

    def _update_stylesheet(self):
        """Xử lý khi sx thay đổi."""
        self._set_stylesheet()

    def _setup_layout(self):
        columns = self._get_columns()
        spacing = self._get_spacing()
        children = self._get_children()

        # Xóa các cột hiện có trước khi tạo lại
        clear_layout(self.layout())
        self.column_layouts = []

        # Thiết lập lại spacing cho layout chính
        self.layout().setSpacing(spacing)

        # Tạo các cột mới
        for i in range(columns):
            column = QWidget()
            column.setObjectName(str(uuid.uuid4()))
            vlo_column = QVBoxLayout(column)
            vlo_column.setContentsMargins(0, 0, 0, 0)
            vlo_column.setAlignment(Qt.AlignmentFlag.AlignTop)
            vlo_column.setSpacing(spacing)
            column.setLayout(vlo_column)
            self.column_layouts.append(vlo_column)
            if LOAD_WIDGET_ASYNC:
                self._do_task_async(lambda column=column: self.layout().addWidget(column))
            else:
                self.layout().addWidget(column)

        # Thêm các phần tử con vào các cột
        if children:
            # Tính chiều cao của từng cột để phân phối phần tử
            column_heights = [0] * columns
            for child in children:
                # Tìm cột có tổng chiều cao nhỏ nhất để thêm phần tử vào
                min_height_col = column_heights.index(min(column_heights))
                # if LOAD_WIDGET_ASYNC: # còn có tính toán height liên quan nên chưa áp dụng được
                #     self._do_task_async(lambda min_height_col=min_height_col, child=child: self.column_layouts[min_height_col].addWidget(child))
                # else:
                #     self.column_layouts[min_height_col].addWidget(child)
                self.column_layouts[min_height_col].addWidget(child)
                # Cập nhật chiều cao của cột (ước lượng dựa trên chiều cao của phần tử)
                child_height = child.sizeHint().height() if child.sizeHint().isValid() else 0
                column_heights[min_height_col] += child_height + spacing
                
    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        PyMasonry_root = component_styled["PyMasonry"].get("styles")["root"]
        PyMasonry_root_qss = get_qss_style(PyMasonry_root)

        sx_qss = ""
        if self._sx:
            sx = self._get_sx()
            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, Callable):
                sx = sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        stylesheet = f"""
            #{self.objectName()} {{
                {PyMasonry_root_qss}
            }}
            
            {sx_qss}
        """

        self.setStyleSheet(stylesheet)