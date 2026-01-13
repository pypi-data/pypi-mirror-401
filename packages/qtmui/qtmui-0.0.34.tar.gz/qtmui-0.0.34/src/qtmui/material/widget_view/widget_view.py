from typing import Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from ...common.ui_functions import clear_layout
from qtmui.hooks import State



class WidgetView(QWidget):
    def __init__(
                self,
                direction="column",
                renderView: Callable = None,
                renderViewProps: Callable = None,
                children: State = None,
                view: State = None
                ):
        super().__init__()
        if direction == "column":
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self._children = children
        if not self._children:
            self._children = view
        
        if isinstance(children, State):
            children.valueChanged.connect(self._render_ui)
            self._render_ui(children.value)

    def _render_ui(self, widget):
        if self.layout().count():
            clear_layout(self.layout())
        if widget:
            self.layout().addWidget(widget)

QPushButton