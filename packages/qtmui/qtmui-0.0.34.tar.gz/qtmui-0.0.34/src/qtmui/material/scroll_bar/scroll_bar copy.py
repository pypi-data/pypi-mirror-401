from typing import Optional, List
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QProgressBar, QLabel
from PySide6.QtCore import Qt, Signal, Slot, QTimer

class Scrollbar(QWidget):
    # Tín hiệu cập nhật thanh tiến trình
    scrollChanged = Signal(int)

    def __init__(
                self,
                autoHide: Optional[bool] = False,
                children: Optional[List] = None,
                maxHeight: int = None,
                maximumHeight: int = None,
                fixedHeight: int = None,
                sx: object = None,
                ref: object = None,
                ):
        super().__init__()
        self._maxHeight = maxHeight
        self._maximumHeight = maximumHeight
        self._fixedHeight = fixedHeight
        self._children = children

        self.init_ui()

    def init_ui(self):
        if self._maxHeight:
            self.setFixedHeight(self._maxHeight)
        if self._maximumHeight:
            self.setFixedHeight(self._maximumHeight)
        if self._fixedHeight:
            self.setFixedHeight(self._fixedHeight)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        # Tạo QProgressBar để hiển thị tiến trình
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # Giới hạn từ 0 đến 100
        self.progress_bar.setValue(0)  # Bắt đầu với giá trị 0
        self.progress_bar.setTextVisible(False)  # Bắt đầu với giá trị 0
        layout.addWidget(self.progress_bar)

        # Tạo nội dung bên trong QScrollArea
        self.scroll_content = QWidget(self)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0,0,0,0)


        # Tạo QScrollArea và thêm vào layout chính
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)  # Làm cho nội dung thay đổi kích thước theo diện tích của QScrollArea
        layout.addWidget(self.scroll_area)
        
        # QTimer.singleShot(300, self._set_children)
        self._set_children()

        # Thêm QProgressBar vào layout
        self.setLayout(layout)

    def _set_children(self):
        if isinstance(self._children, list):
            for widget in self._children:
                if widget is not None:
                    self.scroll_layout.addWidget(widget)
        elif isinstance(self._children, QWidget):
            self.scroll_layout.addWidget(self._children)
        self.update()
