from typing import TYPE_CHECKING, Callable, Union, Optional
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

from ...typography import Typography
from ...avatar import Avatar
from ...label import Label
from qtmui.hooks import useState, State

if TYPE_CHECKING:
    from .table import TableWidget


class TableViewCell(QFrame):
    indexRow = Signal(int)
    def __init__(
                self,
                key: str = None,
                data: object = None,
                padding: str = "checkbox",
                align: str = "left",
                children: object = None,
                colSpan: int = None,
                onClick: Callable=None,
                sx: Optional[Union[dict, State]] = None,
                text: str = None
                ):
        super().__init__()
        self.data = data

        self._align = align
        self._children = children
        self._text = text
        self._sx = sx

        self._indexRow = None

        # self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        
        if self._align == "left":
            self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif self._align == "right":
            self.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            

        if self._text:
                self.layout().addWidget(Typography(text=self._text, variant="body2"))

        elif self._children:
            if isinstance(self._children, list):
                for widget in self._children:
                    if widget is not None:
                        self.layout().addWidget(widget)
            elif isinstance(self._children, QWidget):
                self.layout().addWidget(self._children)
            elif isinstance(self._children, str):
                cell_widget = Typography(text=self._children, variant="body2", align=self._align)
                self.layout().addWidget(cell_widget)

    
    def enterEvent(self, event):
        try:
            # self.parent().parent()._setHoverRow(self._indexRow)
            # self.parent()._setHoverRow(self._indexRow)
            self.indexRow.emit(self._indexRow)
        except Exception as e:
            print('eeeeeeeee', e)
            pass
        # return super().enterEvent(event)