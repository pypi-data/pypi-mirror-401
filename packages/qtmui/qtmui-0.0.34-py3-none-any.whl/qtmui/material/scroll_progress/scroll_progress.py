from typing import Callable, Dict, Optional, List, Union
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QProgressBar, QLabel
from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPropertyAnimation, QEasingCurve
from ..widget_base import PyWidgetBase
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.material.styles import useTheme

class ScrollProgress(QWidget, PyWidgetBase):
    # Tín hiệu cập nhật thanh tiến trình
    scrollChanged = Signal(int)

    def __init__(
                self,
                children: Optional[List] = None,
                maxHeight: int = None,
                sx: Optional[Union[Callable, str, Dict]]= None,
                ):
        super().__init__()
        self._maxHeight = maxHeight
        self._children = children
        self._progress_animation = None # Property animation instance
        self._sx = sx

        self.init_ui()

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def init_ui(self):
        if self._maxHeight:
            self.setFixedHeight(self._maxHeight)


        layout = QVBoxLayout()

        # Tạo QProgressBar để hiển thị tiến trình
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setRange(0, 100)  # Giới hạn từ 0 đến 100
        self.progress_bar.setValue(0)  # Bắt đầu với giá trị 0
        self.progress_bar.setTextVisible(False)  # Bắt đầu với giá trị 0
        layout.addWidget(self.progress_bar)

        self.scrollChanged.connect(self.start_smooth_progress_bar)  # Connect to the new function

        # Tạo nội dung bên trong QScrollArea
        self.scroll_content = QWidget(self)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        QTimer.singleShot(300, self._set_children)


        # Tạo QScrollArea và thêm vào layout chính
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)  # Làm cho nội dung thay đổi kích thước theo diện tích của QScrollArea
        layout.addWidget(self.scroll_area)

        # Thêm QProgressBar vào layout
        self.setLayout(layout)

        # Kết nối tín hiệu cuộn chuột với slot
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_progress)



    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

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

        self.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 1px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {self.theme.palette.primary.light}, stop:1 {self.theme.palette.primary.dark});
                border-radius: 1px;
            }}

            {sx_qss}

        """)

    def _set_children(self):
        for widget in self._children:
            self.scroll_layout.addWidget(widget)
        self.update()

    def update_progress(self, scroll_value):
        if not self.isVisible():
            return
        """Cập nhật giá trị của thanh tiến trình khi thanh cuộn thay đổi."""
        scroll_max = self.scroll_area.verticalScrollBar().maximum()
        # print(scroll_max)
        
        # Tính toán tỷ lệ cuộn và cập nhật giá trị thanh tiến trình
        if scroll_max != 0:  # Đảm bảo không chia cho 0
            scroll_percentage = int((scroll_value / scroll_max) * 100)  # Tính toán tỷ lệ cuộn
            self.scrollChanged.emit(scroll_percentage)  # Phát tín hiệu cập nhật thanh tiến trình

    @Slot()
    def start_smooth_progress_bar(self, value):
        if self._progress_animation and self._progress_animation.state() == QPropertyAnimation.Running:
            self._progress_animation.stop()


        self._progress_animation = QPropertyAnimation(self.progress_bar, b"value", self)
        self._progress_animation.setDuration(500) # Adjust to your liking
        self._progress_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._progress_animation.setStartValue(self.progress_bar.value())
        self._progress_animation.setEndValue(value)
        self._progress_animation.start()


# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication, QLabel
#     app = QApplication(sys.argv)

#     # Create dummy content
#     labels = [QLabel(f"Item {i}") for i in range(30)]


#     scroll_progress = ScrollProgress(children=labels, maxHeight=300)

#     scroll_progress.show()
#     sys.exit(app.exec())