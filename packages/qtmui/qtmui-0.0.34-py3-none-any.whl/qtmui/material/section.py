from typing import Callable, Dict, Union
import uuid

from qtmui.hooks import State
from PySide6.QtWidgets import QVBoxLayout, QWidget, QSizePolicy, QFrame
from PySide6.QtCore import Qt, Signal, QSize
from qtmui.material.widget_base import PyWidgetBase
from .utils.validate_params import _validate_param
from .styles.create_theme.components.get_qss_styles import get_qss_style
from .styles import useTheme
# from ..hooks._effect_context import register_component_cleanup

class Section(QFrame, PyWidgetBase):

    sizeChanged = Signal(QSize)

    def __init__(self, key=None, children=None, sx=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setObjectName(str(uuid.uuid4()))
        PyWidgetBase._setUpUi(self)

        self._key = key

        self._set_sx(sx)

        # from PyWidgetBase
        self._setup_sx_position(sx)  # Gán sx và khởi tạo các thuộc tính định vị

        self.setLayout(QVBoxLayout())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self._set_stylesheet()

        if children:
            if isinstance(children, list):
                for widget in children:
                    if isinstance(widget, QWidget):
                        self.layout().addWidget(widget)
            if isinstance(children, QWidget):
                self.layout().addWidget(children)

    def add_widget(self, element: QWidget):
        """Thêm một phần tử giao diện vào trang."""
        if isinstance(element, QWidget):
            self.layout().addWidget(element)
        else:
            print(f"Opp!! element must have type QWidget")

    @_validate_param(file_path="qtmui.material.section", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value"""
        self._sx = value

    def _set_stylesheet(self):
        """Set the stylesheet for the Box."""
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, State):
                sx = self._sx.value
            elif isinstance(self._sx, Callable):
                sx = self._sx()
            else:
                sx = self._sx

            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        stylesheet = f"""
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def showEvent(self, e):
        """ fade in """
        PyWidgetBase.showEvent(self)
        super().showEvent(e)

    def resizeEvent(self, event):
        self.sizeChanged.emit(self.size())
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)

