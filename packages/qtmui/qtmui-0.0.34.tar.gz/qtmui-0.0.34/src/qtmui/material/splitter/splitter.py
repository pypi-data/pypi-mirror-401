from typing import Callable, Dict, Optional, Union
import uuid
from PySide6.QtWidgets import QSplitter, QTextEdit, QSizePolicy
from PySide6.QtCore import Qt

from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class Splitter(QSplitter):
    def __init__(
                self, 
                orientation=Qt.Horizontal, 
                parent=None, 
                min_width=None, 
                max_width=None, 
                min_height=None, 
                max_height=None,
                handleWidth: int = 0,
                children: list= None,
                sx: Optional[Union[Callable, str, Dict]]= None
                ):
        super().__init__(orientation, parent)

        self._handleWidth = handleWidth
        self._childrend = children
        self._min_width = min_width
        self._max_width = max_width
        self._min_height = min_height
        self._max_height = max_height
        self._sx = sx

        self._init_ui()


    def _init_ui(self):
        self.setObjectName("PySplitter")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # self.setMinimumWidth(QSizePolicy.Maximum, QSizePolicy.Expanding)

        self.setHandleWidth(self._handleWidth)
        
        self.set_min_width(self._min_width)
        self.set_max_width(self._max_width)
        self.set_min_height(self._min_height)
        self.set_max_height(self._max_height)

        if self._childrend is not None:
            for item in self._childrend:
                item.get("widget").setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred))
                # item.get("widget").setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
                if item.get("sizePolicy") == "expanding":
                    item.get("widget").setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
                if item.get("maximumWidth") is not None:
                    item.get("widget").setMaximumWidth(item.get("maximumWidth"))
                if item.get("minimumWidth") is not None:
                    item.get("widget").setMinimumWidth(item.get("minimumWidth"))
                self.addWidget(item.get("widget"))


        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PySplitter_root = component_styles[f"PySplitter"].get("styles")["root"]
        PySplitter_root_qss = get_qss_style(PySplitter_root)

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
                #PySplitter {{
                    {PySplitter_root_qss}
                    {sx_qss}
                }}
            """
        )


    def set_min_width(self, min_width):
        if min_width is not None:
            self.setMinimumWidth(min_width)

    def set_max_width(self, max_width):
        if max_width is not None:
            self.setMaximumWidth(max_width)

    def set_min_height(self, min_height):
        if min_height is not None:
            self.setMinimumHeight(min_height)

    def set_max_height(self, max_height):
        if max_height is not None:
            self.setMaximumHeight(max_height)

    def add_pages(self, num_pages):
        for _ in range(num_pages):
            text_edit = QTextEdit()
            self.addWidget(text_edit)

