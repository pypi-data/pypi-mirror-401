from typing import Callable
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Signal

from qtmui.hooks import State

from ..checkbox.checkbox import Checkbox


class ListItemCheckbox(QFrame):

    themeChanged = Signal()

    def __init__(self, 
                 alignItems='center',  # Căn chỉnh items
                 autoFocus=False,  # Tự động focus khi mount
                 children=None,  # Nội dung của ListItemButton
                 classes=None,  # Ghi đè hoặc mở rộng các style
                 component=QFrame,  # Thành phần dùng cho root node
                 dense=False,  # Sử dụng padding dọc nhỏ gọn
                 disabled=False,  # Vô hiệu hóa component
                 disableGutters=False,  # Loại bỏ padding trái/phải
                 divider=False,  # Thêm viền dưới
                 focusVisibleClassName=None,  # Lớp CSS khi focus
                 key = None,
                 minHeight=None,
                 onClick: Callable=None,
                 selected=False,  # Sử dụng style khi được chọn
                 sx=None,  # Hệ thống prop cho overrides và styles
                 size="medium",  # Hệ thống prop cho overrides và styles
                 parent=None,  # Parent widget
                 selectedKey: State=None,  # Parent widget
                 **kwargs):
        super().__init__(**kwargs)

        # Gán các props thành thuộc tính của class
        self._alignItems = alignItems
        self._autoFocus = autoFocus
        self._children = children
        self._classes = classes
        self._component = component
        self._dense = dense
        self._disabled = disabled
        self._disableGutters = disableGutters
        self._divider = divider
        self._focusVisibleClassName = focusVisibleClassName
        self._selected = selected
        self._sx = sx

        self._size = size

        self._key = key
        self._onListItemButtonClick = onClick
        self._selectedKey = selectedKey

        # Thiết lập trạng thái ban đầu
        self.setDisabled(self._disabled)
        # self.setAutoDefault(self._autoFocus)

        # Thiết lập căn chỉnh
        # self.setStyleSheet(self._get_align_items_style(self._alignItems))

        # Áp dụng thêm styles từ sx nếu có
        if self._sx:
            self._apply_sx(self._sx)

        self.setLayout(QHBoxLayout())
        # self.layout().setContentsMargins(9,9,9,9)
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        if minHeight:
            self.setMinimumHeight(minHeight)

        self._checkbox = Checkbox(disableRipple=True, disableGutters=True, size="small", color="primary")
        self.layout().addWidget(self._checkbox)

        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            
            for child in self._children:
                if hasattr(child, '_secondary'):
                    if getattr(child, '_secondary'):
                        self.setFixedHeight(48)
                self.layout().addWidget(child)


    def _get_align_items_style(self, alignItems):
        """Thiết lập style cho align-items"""
        if alignItems == 'center':
            return "text-align: center;"
        elif alignItems == 'flex-start':
            return "text-align: left;"
        return ""

    def _apply_sx(self, sx):
        """Áp dụng hệ thống overrides cho styles."""
        if isinstance(sx, dict):
            for key, value in sx.items():
                self.setStyleSheet(f"{key}: {value};")
        elif callable(sx):
            sx(self)  # sx có thể là hàm áp dụng style

    def focusInEvent(self, event):
        """Quản lý lớp khi element được focus"""
        super().focusInEvent(event)
        if self._focusVisibleClassName:
            self.setStyleSheet(self.styleSheet() + f" {self._focusVisibleClassName} {{ outline: 1px solid #000; }}")

    def mouseReleaseEvent(self, event):
        if self._onListItemButtonClick:
            self._onListItemButtonClick(self._key)
            
        return super().mouseReleaseEvent(event)
