from typing import Callable, Optional, Union
import uuid
from PySide6.QtWidgets import  QFrame, QHBoxLayout, QSizePolicy, QWidget
from PySide6.QtCore import  Qt, Signal, QEvent

from qtmui.hooks import State, useEffect

from ..system.color_manipulator import alpha

from .li_base import LiBase

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from ..widget_base import PyWidgetBase
from ..typography import Typography

class Li(LiBase, PyWidgetBase):

    selectedChange = Signal(object)

    def __init__(self, 
                 alignItems='center',  # Căn chỉnh items
                 autoFocus=False,  # Tự động focus khi mount
                 children=None,  # Nội dung của MenuItem
                 classes=None,  # Ghi đè hoặc mở rộng các style
                 component=QFrame,  # Thành phần dùng cho root node
                 dense=False,  # Sử dụng padding dọc nhỏ gọn
                 disabled=False,  # Vô hiệu hóa component
                 disableGutters=False,  # Loại bỏ padding trái/phải
                 divider=False,  # Thêm viền dưới
                 focusVisibleClassName=None,  # Lớp CSS khi focus
                 key = None,
                 minHeight=None,
                 onChange: Callable = None,
                 onClick: Callable = None,
                 selected=False,  # Sử dụng style khi được chọn
                 sx=None,  # Hệ thống prop cho overrides và styles
                 visible: bool = True,  # Hệ thống prop cho overrides và styles
                 size="medium",  # Hệ thống prop cho overrides và styles
                 parent=None,  # Parent widget
                 selectedKey: State=None,  # Parent widget
                text: Optional[Union[State, str, Callable]] = None,
                 textAlign: str = 'left',  # Parent widget
                 **kwargs):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self._alignItems = alignItems
        self._autoFocus = autoFocus
        self._children = children
        self._classes = classes
        self._component = component
        self._dense = dense
        self._disabled = disabled
        self._disableGutters = disableGutters
        self._divider = divider
        self._minHeight = minHeight
        self._onChange = onChange or print
        self._focusVisibleClassName = focusVisibleClassName
        self._selected = selected
        self._sx = sx

        self._visible = visible
        self._size = size
        self._text = text
        self._textAlign = textAlign

        self._key = key
        self._onListItemButtonClick = onClick
        self._selectedKeys = selectedKey
        self._searchdKeys = None

        self.__init_ui()


    def __init_ui(self):

        self.setDisabled(self._disabled)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if self._selected:
            self.setProperty("selected", "true")

        if self._textAlign in ["left", "center", "right"]:
            self._textAlign = f"text-align: {self._textAlign};"

        if self._minHeight:
            self.setMinimumHeight(self._minHeight)

        if self._selectedKeys:
            if isinstance(self._selectedKeys, State):
                self._selectedKeys.valueChanged.connect(self._set_selected)

        if self._children:
            self.setLayout(QHBoxLayout())
            # self.layout().setContentsMargins(6,6,6,6)
            self.layout().setContentsMargins(0,0,0,0)
            self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
  
            if isinstance(self._children, list):
                for child in self._children:
                    self.layout().addWidget(child)
            elif isinstance(self._children, QWidget):
                self.layout().addWidget(self._children)
            if self._text:
                self.layout().addWidget(Typography(text=self._text, variant="button"))
        else:
            self.setText(self._text)

        PyWidgetBase._installTooltipFilter(self)

        for widget in self.findChildren(QWidget):
            widget.installEventFilter(self)  # Bắt sự kiện từ con

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _set_on_changed(self, onChange: Callable):
        self._onChange = onChange
        self.selectedChange.connect(self._onChange)

    def _set_selected_keys(self, selectedKeys: State):
        self._selectedKeys = selectedKeys
        self._selectedKeys.valueChanged.connect(self._set_selected)
        self._set_selected(selectedKeys.value)

    # def _set_search_keys(self, _searchKeys: State):
    #     self._searchKeys = _searchKeys
    #     self._searchKeys.valueChanged.connect(self._set_search_results)

    def _set_selected(self, keys):
        if isinstance(keys, list):
            if self._key in keys:
                self.setProperty("selected", "true")
            else:
                self.setProperty("selected", "false")
        else:
            # print('kkeys____________', keys)
            if self._key == keys:
                self.setProperty("selected", "true")
            else:
                self.setProperty("selected", "false")
        self._set_stylesheet()

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyMenuItem = component_styles[f"PyMenuItem"].get("styles")
        PyMenuItem_root_qss = get_qss_style(PyMenuItem["root"])
        PyMenuItem_root_slot_hover_qss = get_qss_style(PyMenuItem["root"]["slots"]["hover"])
        PyMenuItem_root_slot_selected_qss = get_qss_style(PyMenuItem["root"]["slots"]["selected"])
        PyMenuItem_root_slot_selected_hover_qss = get_qss_style(PyMenuItem["root"]["slots"]["selected"]["hover"])

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx


        stylesheet = f"""
            #{self.objectName()} {{
                {PyMenuItem_root_qss}
            }}
            #{self.objectName()}::hover {{
                {PyMenuItem_root_slot_hover_qss}
            }}
            #{self.objectName()}[selected=true] {{
                {PyMenuItem_root_slot_selected_qss}
            }}
            #{self.objectName()}[selected=true]::hover {{
                {PyMenuItem_root_slot_selected_hover_qss}
            }}

            {sx_qss}
        """

        self.setStyleSheet(stylesheet)


    # def _set_search_results(self, keys):
    #     if isinstance(keys, list):
    #         if self._key in keys:
    #             self.setProperty("search", "true")
    #         else:
    #             self.setProperty("search", "false")
    #     else:
    #         if self._key == keys:
    #             self.setProperty("search", "true")
    #         else:
    #             self.setProperty("search", "false")
    #     self._set_stylesheet()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            # print("🖱️ Mouse click on child:", obj)
            # Thực hiện logic ở đây, ví dụ chọn dòng, đổi màu...
            if self._onListItemButtonClick:
                self._onListItemButtonClick({"label": self._text or self._key, "value": self._key})
            self.selectedChange.emit({"label": self._text or self._key, "value": self._key})
            return False  # cho sự kiện đi tiếp (QCheckBox vẫn nhận)
        # elif event.type() == QEvent.Enter:
        #     print("🟩 Mouse entered child:", obj)
        # elif event.type() == QEvent.Leave:
        #     print("🟥 Mouse left child:", obj)
        return super().eventFilter(obj, event)
    