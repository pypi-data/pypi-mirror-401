import threading, time
from PySide6.QtWidgets import QVBoxLayout, QWidget, QSizePolicy, QFrame
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QPoint, QRect, Signal, QTimer
from .view import View
from qtmui.hooks import useState

class Page(QFrame):
    renderView = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    def _wait_for_3s(self):
        time.sleep(2)
        self.renderView.emit()


    def add_widget(self, element: QWidget):
        """Thêm một phần tử giao diện vào trang."""
        if isinstance(element, QWidget):
            self.layout().addWidget(element)
        else:
            print(f"Opp!! element must have type QWidget")
        
  