from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import QObject


class TableHead(QWidget):
    def __init__(
                self,
                children: object = None
                ):
        super().__init__()
        self._children = children

        self._init_ui()

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        if self._children:
            for widget in self._children:
                self.layout().addWidget(widget)