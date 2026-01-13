import uuid
from PySide6.QtWidgets import QVBoxLayout, QFrame
from typing import Union, List, Callable

class TimelineSeparator(QFrame):
    def __init__(self, 
                 children=None,  # Nội dung của component (node)
                 classes: dict = None,  # Ghi đè hoặc mở rộng các styles áp dụng cho component (dict)
                 sx: Union[List[Union[Callable, dict, bool]], Callable, dict] = None  # Thuộc tính hệ thống, thêm CSS bổ sung (array | func | object)
                 ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet(f"#{self.objectName()} {{background-color: green;}}")

        self._children = children
        self._classes = classes if classes is not None else {}
        self._sx = sx if sx is not None else []

        self._initUI()

    def _initUI(self):
        """Khởi tạo giao diện của TimelineItem."""
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(2,2,2,2)
        
        self._add_children()

    # @is_list
    def _add_children(self):
        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                if child:
                    self.layout().addWidget(child)
