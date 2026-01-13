from typing import Callable, Dict, Optional, Union
import uuid
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from qtmui.hooks import State

from .tf_line_edit_multiple import TFLineEditMultiple

class TagsView(QFrame):
    def __init__(
            self,
            hidden: Optional[Union[State, bool]] = None,
            content: State = None,
            sx: Optional[Union[Callable, str, Dict]]= None,
            *args,
            **kwargs
            ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self._hidden = hidden
        self._content = content
        self._sx = sx

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.layout().setContentsMargins(0,0,0,0)
        self._content.valueChanged.connect(self._render_ui)
        self._render_ui()
        
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            
            if widget is not None and not isinstance(widget, TFLineEditMultiple):
                widget.deleteLater()
        
    def _render_ui(self):
        try:
            if self.layout().count():
                self.clear_layout(self.layout())

            if self._content.value is not None:
                if isinstance(self._content.value, list):
                    for widget in self._content.value:
                        if isinstance(widget, QWidget):
                            self.layout().addWidget(widget)
                elif isinstance(self._content.value, QWidget):
                    self.layout().addWidget(self._content.value)
                elif isinstance(self._content.value, Callable):
                    if isinstance(self._content.value(), QWidget):
                        self.layout().addWidget(self._content.value())
        except Exception as e: # tranh loi bat dong bo
            pass
        