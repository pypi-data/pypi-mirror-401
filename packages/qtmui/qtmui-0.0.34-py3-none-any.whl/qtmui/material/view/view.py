from typing import Callable, Dict, Optional, Union
import uuid
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from qtmui.hooks import State
from ...common.ui_functions import clear_layout
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from qtmui.material.widget_base import PyWidgetBase

class View(QFrame, PyWidgetBase):
    def __init__(
            self,
            hidden: Optional[Union[State, bool]] = None,
            content: State = None,
            hightLight: bool = False,
            alignment: str = None, # "top-left"
            sx: Optional[Union[Callable, str, Dict]]= None,
            *args,
            **kwargs
            ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self._hidden = hidden
        self._alignment = alignment
        self._sx = sx
        
        if self._hidden:
            self._updateHidden()

        if hightLight:
            self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background-color: orange;"))
        self._content = content

        self.setLayout(QVBoxLayout())
        
        if self._alignment == "top-left":
            self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        elif self._alignment == "center-right":
            self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        else:
            self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.destroyed.connect(lambda obj: self._onDestroyed())

        self.layout().setContentsMargins(0,0,0,0)
        self._content.valueChanged.connect(self._render_ui)
        self._render_ui()
        # self.destroyed.connect(self._on_destroyed)
        self.slot_set_stylesheet()
        
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        
        self._setupStates()

    def _setupStates(self):
        if isinstance(self._hidden, State):
            self._hidden.valueChanged.connect(self._updateHidden)

    def _updateHidden(self, val=None):
        if isinstance(self._hidden, State):
            self.setVisible(self._hidden.value)
        elif isinstance(self._hidden, bool):
            self.setVisible(self._hidden.value)

    def _onDestroyed(self, obj=None):
        # print('Viewdestroyed_________________________')
        pass
        
        # self._content.valueChanged.disconnect(self._render_ui)
        
    def _deleteChildren(self):
        for widget in self.findChildren(QWidget):
            widget.setParent(None)
            widget.deleteLater() 
    
    def _render_ui(self):
        try:
            clear_layout(self.layout())

            # for widget in self.findChildren(QWidget):
            #     widget.hide()
                
            # QTimer.singleShot(200, self._deleteChildren)

            if self._content.value is not None:
                if isinstance(self._content.value, list):
                    for widget in self._content.value:
                        if isinstance(widget, QWidget):
                            self.layout().addWidget(widget)
                elif isinstance(self._content.value, QWidget):
                    self.layout().addWidget(self._content.value)
                    # print('self._content.value_________________________', self._content.value)
                elif isinstance(self._content.value, Callable):
                    content = self._content.value()
                    if isinstance(content, QWidget):
                        self.layout().addWidget(content)
        except Exception as e: # tranh loi bat dong bo
            pass
        
    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        stylesheet = f"""

                {sx_qss}

            """
        
        # print('stylesheet___________', stylesheet)

        self.setStyleSheet(stylesheet)