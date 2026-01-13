import uuid
from PySide6.QtWidgets import QVBoxLayout, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from typing import Optional, Union, List, Callable

from qtmui.hooks import State

from ..typography import Typography

class TimelineOppositeContent(QFrame):
    def __init__(self,
                 children=None,  # Nội dung của component (node)
                 classes: dict = None,  # Ghi đè hoặc mở rộng các styles áp dụng cho component (dict)
                 sx: Union[List[Union[Callable, dict, bool]], Callable, dict] = None,  # Hệ thống prop cho phép ghi đè hệ thống hoặc thêm CSS styles
                text: Optional[Union[str, State, Callable]] = None,
                 ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet(f"#{self.objectName()} {{background-color: orange;}}")

        self._children = children
        self._classes = classes if classes is not None else {}
        self._sx = sx
        self._text = text

        # Khởi tạo giao diện
        self._initUI()

    def _initUI(self):
        """Khởi tạo giao diện của TimelineContent."""
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().setAlignment(Qt.AlignTop)

        if self._text:
            self.content_widget = Typography(variant="body2", text=self._text)
            self.layout().addWidget(self.content_widget)

        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for widget in self._children:
                if widget:
                    self.layout().addWidget(widget)