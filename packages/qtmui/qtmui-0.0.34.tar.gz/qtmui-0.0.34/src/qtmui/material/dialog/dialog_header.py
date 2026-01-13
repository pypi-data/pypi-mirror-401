from typing import Callable, Optional, Union
from PySide6.QtWidgets import QHBoxLayout, QFrame, QSpacerItem, QSizePolicy

from qtmui.hooks import State

from ..typography.typography import Typography
from ..button import IconButton

class DialogHeader(QFrame):
    def __init__(
            self,
            parent=None,
            title: Optional[Union[State, str, Callable]] = "Information",
            align: str = "right"
        ):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        
        if align == "left":
            self.layout().addWidget(IconButton(onClick=parent.hide_dialog, icon=":/round/resource_qtmui/round/close.svg", variant="soft"))
            self.layout().addItem(QSpacerItem(448, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        else:
            self.layout().addWidget(Typography(text=title, variant="h3"))
            self.layout().addItem(QSpacerItem(448, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            self.layout().addWidget(IconButton(onClick=parent.hide_dialog, icon=":/round/resource_qtmui/round/close.svg", variant="soft"))