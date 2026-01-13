import uuid
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from typing import Union, List, Callable

from ..box import Box
from ..spacer import HSpacer
from .timeline_content import TimelineContent, AlignBox
from .timeline_opposite_content import TimelineOppositeContent

class TimelineItem(QFrame):
    def __init__(self, 
                 children=None,  # Nội dung của component (node)
                 classes: dict = None,  # Ghi đè hoặc mở rộng styles cho component (dict)
                 position: str = 'right',  # Vị trí của item trên timeline ('alternate-reverse' | 'alternate' | 'left' | 'right')
                 key: Union[str, int] = None,  # Vị trí của item trên timeline ('alternate-reverse' | 'alternate' | 'left' | 'right')
                 sx: Union[List[Union[Callable, dict, bool]], Callable, dict] = None  # Thuộc tính hệ thống, thêm CSS bổ sung (array | func | object)
                 ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet(f"#{self.objectName()} {{background-color: blue;}}")
        
        self._children = children
        self._classes = classes if classes is not None else {}
        self._position = position
        self._key = key
        self._sx = sx

        # Thiết lập layout cơ bản cho item
        self._initUI()

    def _initUI(self):
        """Khởi tạo giao diện của TimelineItem."""
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        
        self._add_children()
        self._setup_layout()

    # @is_list
    def _add_children(self):
        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            if self._position == "alternate":
                self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                if self._key % 2 == 1:
                    spacer_w = 0
                    spacer_w_oppo = 0
                    for child in reversed(self._children):
                        if child:
                            if isinstance(child, TimelineOppositeContent):
                                spacer_w_oppo = child.sizeHint().width()
                            if isinstance(child, TimelineContent):
                                spacer_w = child.sizeHint().width()
                            self.layout().addWidget(child)

                    
                    if not len(self.findChildren(TimelineOppositeContent)):
                        self.layout().addWidget(HSpacer(width=spacer_w))
                    else:
                        max_size_content = spacer_w if (spacer_w - spacer_w_oppo) > 0 else spacer_w_oppo
                        max_size_content = max_size_content + 12
                        for index, child in enumerate(self.findChildren(QWidget), 0):
                            if index == 0:
                                if isinstance(child.content_widget, Box):
                                    child.content_widget.layout().setAlignment(Qt.AlignRight)
                                    for alignBox in child.content_widget.findChildren(AlignBox):
                                        alignBox.layout().insertWidget(0, HSpacer())
                                else:
                                    child.content_widget.setAlignment(Qt.AlignRight)

                            if isinstance(child, TimelineOppositeContent):
                                child.setFixedWidth(max_size_content)
                            if isinstance(child, TimelineContent):
                                child.setFixedWidth(max_size_content)

                else:
                    spacer_w = 0
                    spacer_w_oppo = 0
                    for child in self._children:
                        if child:
                            if isinstance(child, TimelineOppositeContent):
                                spacer_w_oppo = child.sizeHint().width()
                            if isinstance(child, TimelineContent):
                                spacer_w = child.sizeHint().width()
                            self.layout().addWidget(child)
                    if not len(self.findChildren(TimelineOppositeContent)):
                        self.layout().insertWidget(0, HSpacer(width=spacer_w))
                    else:
                        max_size_content = spacer_w if (spacer_w - spacer_w_oppo) > 0 else spacer_w_oppo
                        max_size_content = max_size_content + 12
                        for index, child in enumerate(self.findChildren(QWidget), 0):
                            if index == 0:
                                if isinstance(child.content_widget, Box):
                                    child.content_widget.layout().setAlignment(Qt.AlignRight)
                                    for alignBox in child.content_widget.findChildren(AlignBox):
                                        alignBox.layout().insertWidget(0, HSpacer())
                                else:
                                    child.content_widget.setAlignment(Qt.AlignRight)

                            if isinstance(child, TimelineOppositeContent):
                                child.setFixedWidth(max_size_content)
                            if isinstance(child, TimelineContent):
                                child.setFixedWidth(max_size_content)
            else:
                for child in reversed(self._children) if self._position == 'left' else self._children:
                    if child:
                        self.layout().addWidget(child)

    def _setup_layout(self):

        # Thiết lập vị trí cho timeline item dựa trên giá trị position
        if self._position == 'left':
            self.setAlignment(Qt.AlignLeft)
        elif self._position == 'right':
            self.setAlignment(Qt.AlignRight)
        elif self._position == 'alternate':
            self.setAlignment(Qt.AlignCenter)  # Giả định rằng alternate căn giữa
        elif self._position == 'alternate-reverse':
            self.setAlignment(Qt.AlignJustify)  # Hoặc xử lý khác tùy thuộc vào logic

    def setAlignment(self, alignment):
        """Phương thức để căn chỉnh item dựa trên vị trí."""
        self.layout().setAlignment(alignment)