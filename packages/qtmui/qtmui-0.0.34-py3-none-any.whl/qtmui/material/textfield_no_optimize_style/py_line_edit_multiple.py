import asyncio
from functools import lru_cache
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QLineEdit, QLabel
from PySide6.QtCore import Qt, QEvent, QTimer
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.utils.translator import getTranslatedText
from  .py_input_base import MuiInputBase
from ..widget_base import PyWidgetBase

from qtmui.material.styles import useTheme
from qtmui.hooks import State

from qtmui.i18n.use_translation import i18n

class PyLineEditMultiple(QLineEdit, PyWidgetBase):
    def __init__(
        self,
        textField=None,
        label: Optional[Union[str, State, Callable]] = None,
        placeholder: Optional[Union[str, State, Callable]] = None,
        selectedKeys: State = None,
        onChange: Optional[Callable] = None,
        children: Optional[list] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        sx: Optional[Union[Dict, Callable, str]] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        variant: str = "outlined",
        size: str = "medium",  # Kích thước của thành phần ('medium' hoặc 'small').
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        self._setUpUi(**kwargs)

        self._children = children
        self._label = label
        self._placeholder = placeholder
        self._onChange = onChange
        self._sx = sx
        self._variant = variant
        self._size = size
        self._selectedKeys = selectedKeys
        self._textField = textField
        
        self._init_ui()
        
    def _init_ui(self):
        self.theme = useTheme()
        
        i18n.langChanged.connect(self._set_placer_holder_text)
        self._selectedKeys.valueChanged.connect(self._onSelectedkeysChanged)

        self.placeholder_label = QLabel("", self)
        self.setStyleSheet("min-height: 20px;padding-left: 0px;padding-top:3px;")
        # self.placeholder_label.setStyleSheet(f"color: gray;border: 1px solid green;min-height: 20px;font-size: 13px;font-weight: 600;")
        self.placeholder_label.setStyleSheet(f"color: gray;min-height: 20px;font-size: 13px;font-weight: 600;")
        self.placeholder_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.textChanged.connect(self._update_placeholder_visibility)
        self.installEventFilter(self)
        self._update_placeholder_visibility()

        if isinstance(self._placeholder, State):
            self._placeholder.valueChanged.connect(self._set_placer_holder_text)
        self._set_placer_holder_text()

        self.textChanged.connect(self._onChange)

    def _set_placer_holder_text(self):
        # nếu chưa chọn gì và cũng không có focus thì hiển thị placeholder là label
        # print('_set_placer_holder_text')
        
        if len(self._selectedKeys.value) == 0 and not self.hasFocus():
            self.placeholder_label.setText(getTranslatedText(self._label))
            self.setMinimumWidth(self.placeholder_label.sizeHint().width() + 10)
            return
        self.placeholder_label.setText(getTranslatedText(self._placeholder))
        
    def _onSelectedkeysChanged(self):
        print('_onSelectedkeysChanged', self._selectedKeys.value, self._placeholder)

        self.placeholder_label.setText(getTranslatedText(self._placeholder))
        QTimer.singleShot(0, lambda: self.setFocus(Qt.OtherFocusReason))
        

    def enterEvent(self, event):
        PyWidgetBase.enterEvent(self, event)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        PyWidgetBase.leaveEvent(self, event)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        PyWidgetBase.mousePressEvent(self, event)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        PyWidgetBase.mouseReleaseEvent(self, event)
        super().mouseReleaseEvent(event)
    
    def focusInEvent(self, event) -> None:
        self.placeholder_label.setText(getTranslatedText(self._placeholder))
        PyWidgetBase.focusInEvent(self, event)
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        if self.text() == "":
            self._set_placer_holder_text()
        PyWidgetBase.focusOutEvent(self, event)
        super().focusOutEvent(event)
    
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.placeholder_label.resize(self.size())

    def _update_placeholder_visibility(self):
        """Ẩn label khi có text, hiện khi trống."""
        self.placeholder_label.setVisible(self.text() == "")

    def eventFilter(self, obj, event):
        """Không ẩn placeholder khi focus vào."""
        if event.type() in (QEvent.FocusIn, QEvent.FocusOut):
            self._update_placeholder_visibility()
        return super().eventFilter(obj, event)