from PySide6.QtWidgets import QWidget, QVBoxLayout

from ..box import Box
from ..spacer import HSpacer

class Timeline(QWidget):
    def __init__(self, 
                 children=None, 
                 classes=None, 
                 className="", 
                 position="right", 
                 sx=None, 
                 parent=None
                 ):
        super().__init__(parent)

        # Thuộc tính của component với _ theo convention
        self._children = children  # Nội dung bên trong Timeline
        self._classes = classes  # CSS classes ghi đè hoặc mở rộng cho component
        self._className = className  # className gán cho root element
        self._position = position  # Vị trí của TimelineContent so với trục thời gian
        self._sx = sx  # Thuộc tính ghi đè hệ thống hoặc bổ sung CSS styles

        # Thiết lập layout cho Timeline
        self.setLayout(QVBoxLayout())
        # self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # self.layout().setAlignment(Qt.AlignCenter)

        # Thiết lập các thuộc tính cho root element (QWidget)
        self.setObjectName(self._className)
        self._apply_styles()

        # Thêm các thành phần con vào timeline
        self._add_children()

    # @is_list
    def _add_children(self):
        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                if child:
                    if self._position == "alternate":
                        self.layout().addWidget(
                            Box(
                                direction="row",
                                children=[
                                    HSpacer(),
                                    child,
                                    HSpacer()
                                ]
                            )
                        )
                    else:
                        self.layout().addWidget(child)

    def _apply_styles(self):
        """
        Áp dụng CSS styles từ `classes` và `sx`.
        """
        # Áp dụng CSS classes nếu có
        if self._classes:
            for key, value in self._classes.items():
                self.setStyleSheet(f'{key}: {value};')

        # Xử lý các overrides từ hệ thống qua prop `sx`
        if isinstance(self._sx, list):
            for style in self._sx:
                # Áp dụng các style nếu là dict hoặc gọi hàm nếu là func
                if isinstance(style, dict):
                    for key, value in style.items():
                        self.setStyleSheet(f'{key}: {value};')
                elif callable(style):
                    style(self)

    def set_position(self, position):
        """
        Cập nhật vị trí của TimelineContent so với trục thời gian.
        """
        valid_positions = ['alternate-reverse', 'alternate', 'left', 'right']
        if position in valid_positions:
            self._position = position
        else:
            raise ValueError(f"Position {position} is not valid. Valid positions are {valid_positions}.")

    def add_child(self, child):
        """
        Thêm một thành phần con mới vào Timeline.
        """
        self._children.append(child)
        self.layout().addWidget(child)
