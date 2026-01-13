import uuid
from typing import Optional, Union, Callable, Dict

from PySide6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import useEffect

class TableContainer(QFrame):
    def __init__(
                self,
                children: object = None,
                data: object = None,
                sx: Optional[Union[Callable, str, Dict]]= None
                ):
        super().__init__()

        self._children = children
        self._data = data
        self._sx = sx

        self._children = children

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        if self._children:
            for widget in self._children:
                if widget is not None:
                    self.layout().addWidget(widget)


        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        # PyBox_root = component_styles[f"PyBox"].get("styles")["root"]
        # PyBox_root_qss = get_qss_style(PyBox_root)
        
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {sx_qss}
                }}
            """
        )
