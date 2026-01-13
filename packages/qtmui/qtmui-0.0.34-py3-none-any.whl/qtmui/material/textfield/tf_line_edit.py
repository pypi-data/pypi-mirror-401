import asyncio
from functools import lru_cache
import threading
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QLineEdit, QHBoxLayout
from PySide6.QtCore import QTimer, Signal

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.utils.translator import getTranslatedText
from .tf_input_base import TFInputBase

from qtmui.material.styles import useTheme
from qtmui.hooks import State

from qtmui.i18n.use_translation import i18n

class TFLineEdit(QLineEdit, TFInputBase):
    updateStyleSheet = Signal(object)
    
    def __init__(
        self,
        parent=None,
        label: Optional[Union[str, State, Callable]] = None,
        onChange: Optional[Callable] = None,
        children: Optional[list] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        sx: Optional[Union[Dict, Callable, str]] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        variant: str = "outlined",
        size: str = "medium",  # Kích thước của thành phần ('medium' hoặc 'small').
        asynRenderQss: Optional[Union[State, bool]] = False,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        self._setUpUi(**kwargs)

        self._children = children
        self._label = label
        self._onChange = onChange
        self._sx = sx
        self._variant = variant
        self._size = size
        
        self._asynRenderQss = asynRenderQss
        
        self._init_ui()
        
    def _init_ui(self):
        self.theme = useTheme()
        
        i18n.langChanged.connect(self._set_placer_holder_text)

        if isinstance(self._children, list):
            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(0,0,0,0)
            for widget in self._children:
                self.layout().addWidget(widget)

        if isinstance(self._label, State):
            self._label.valueChanged.connect(self._set_placer_holder_text)
        self._set_placer_holder_text()

        self.textChanged.connect(self._onChange)

    def _set_placer_holder_text(self):
        self.setPlaceholderText(getTranslatedText(self._label))

    def enterEvent(self, event):
        TFInputBase.enterEvent(self, event)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        TFInputBase.leaveEvent(self, event)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        TFInputBase.mousePressEvent(self, event)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        TFInputBase.mouseReleaseEvent(self, event)
        super().mouseReleaseEvent(event)
    
    def focusInEvent(self, event) -> None:
        self.setPlaceholderText("")
        print('focusInEvent___________________PyLineEdit')
        TFInputBase.focusInEvent(self, event)
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        print("focusoutEvent___________________PyLineEdit")
        if self.text() == "":
            self._set_placer_holder_text()
        TFInputBase.focusOutEvent(self, event)  # chỗ này nhấn Favorite xong nhấn btnSelect tạo đệ quy
        super().focusOutEvent(event)
    
