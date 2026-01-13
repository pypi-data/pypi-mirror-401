from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject


class TableBody(QWidget):
    def __init__(
                self,
                children: object = None
                ):
        super().__init__()
        self._children = children

        self._init_ui()

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        for widget in self._children:
            if widget is not None:
                self.layout().addWidget(widget)