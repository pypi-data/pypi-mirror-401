from typing import Optional, Any
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout
from PySide6.QtCore import QObject


class TableRow(QWidget):
    def __init__(
                self,
                children: object = None,
                data: object = None,
                hover: bool = False,
                key: str = None,
                selected: bool = False,
                sx: Optional[Any] = None,
                **kwargs
                ):
        super().__init__()

        self._children = children
        self._data = data

        self._init_ui()

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        if self._children:
            for widget in self._children:
                if widget is not None:
                    self.layout().addWidget(widget)

    def add_children(self, children: list):
        if children:
            for widget in children:
                if widget is not None:
                    self.layout().addWidget(widget)

