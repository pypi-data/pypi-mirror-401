import sys
import uuid
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor

class Item(QWidget):
    def __init__(self, content:QWidget):
        super().__init__()
        # self.setFixedSize(QSize(100, 20))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        if isinstance(content, QWidget):
            raise TypeError(f"Argument 'content' has incorrect type (expected QWidget, got {type(content)})")
        self.layout().addWidget(content)
        