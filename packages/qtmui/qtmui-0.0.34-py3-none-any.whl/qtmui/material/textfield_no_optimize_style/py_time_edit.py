import asyncio
from functools import lru_cache
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QTimeEdit, QHBoxLayout
from PySide6.QtCore import QTimer
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from  .py_input_base import MuiInputBase

from qtmui.material.styles import useTheme
from qtmui.hooks import State
from qtmui.i18n.use_translation import translate

class PyTimeEdit(QTimeEdit, MuiInputBase):
    def __init__(
        self,
        parent=None,
        label: Optional[str] = None,
        onChange: Optional[Callable] = None,
        children: Optional[list] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        sx: Optional[Union[Dict, Callable, str]] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        variant: str = "outlined",
        size: str = "medium",  # Kích thước của thành phần ('medium' hoặc 'small').
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        # self._setUpUi(**kwargs)

        self._children = children
        self._label = label
        self._onChange = onChange
        self._sx = sx
        self._variant = variant
        self._size = size
        
        self._init_ui()
        
    def _init_ui(self):
        self.theme = useTheme()

        if isinstance(self._children, list):
            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(0,0,0,0)
            for widget in self._children:
                self.layout().addWidget(widget)

        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        self._set_stylesheet()
        
        self.destroyed.connect(lambda obj: self._onDestroy())

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_set_stylesheet())

    async def _lazy_set_stylesheet(self):
        self._set_stylesheet()

    @classmethod
    @lru_cache(maxsize=128)
    def _get_stylesheet(cls, _variant: str, _size: str, _theme_mode: str):
        
        theme = useTheme()
        PyTimeEdit_root = theme.components["PyTimeEdit"].get("styles").get("root")
        PyTimeEdit_root_qss = get_qss_style(PyTimeEdit_root)

        _________object_name_______ = "_________object_name_______"

        stylesheet = f"""
                #{_________object_name_______}[variant={_variant}] {{
                    {PyTimeEdit_root_qss}
                }}
            """
        return stylesheet
    
    def _set_stylesheet(self, component_styled=None):
        _theme_mode = useTheme().palette.mode
        self.setProperty("variant", self._variant)
        stylesheet = self._get_stylesheet(self._variant, self._size, _theme_mode)
        stylesheet = stylesheet.replace("_________object_name_______", self.objectName())
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

        # print('stylesheet___________', stylesheet)
        self.setStyleSheet(stylesheet + sx_qss)
        
    def enterEvent(self, event):
        MuiInputBase.enterEvent(self, event)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        MuiInputBase.leaveEvent(self, event)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        MuiInputBase.mousePressEvent(self, event)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        MuiInputBase.mouseReleaseEvent(self, event)
        super().mouseReleaseEvent(event)
    
    def focusInEvent(self, event) -> None:
        MuiInputBase.focusInEvent(self, event)
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        MuiInputBase.focusOutEvent(self, event)
        super().focusOutEvent(event)
    