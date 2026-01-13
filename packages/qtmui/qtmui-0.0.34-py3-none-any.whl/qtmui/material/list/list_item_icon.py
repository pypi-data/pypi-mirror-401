import asyncio
from functools import lru_cache

import threading
from typing import Callable, Dict, Optional, Union
from qtmui.material.styles import useTheme
from PySide6.QtWidgets import QHBoxLayout, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Signal, QTimer

from qtmui.utils.data import deep_merge
from ..styles.create_theme.components.get_qss_styles import get_qss_style

from ..py_svg_widget import PySvgWidget
from ..widget_base.widget_base import PyWidgetBase

from qtmui.hooks import State


class ListItemIcon(QFrame, PyWidgetBase):
    updateStyleSheet = Signal(object)
    
    def __init__(self, 
                 children=None,
                sx: Optional[Union[State, Callable, str, Dict]] = None,
                asynRenderQss: Optional[Union[State, bool]] = False,
                 **kwargs
                ):
        super().__init__()
        self.setObjectName(str(id(self)))
        
        self._sx = sx
        
        if sx:
            self._setSx(sx)
        
        self._kwargs = kwargs.copy()
        self._setKwargs(kwargs)
        
        self._setUpUi()

        # Gán các prop thành thuộc tính của class
        self.kwargs = kwargs

        self._children = children

        self._asynRenderQss = asynRenderQss

        self._init_ui()


    def _init_ui(self):

        # Layout cơ bản cho icon
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # self.setFixedWidth(24)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True) # Điều này cho phép các sự kiện chuột (bao gồm hover) có thể đi qua và được lắng nghe bởi QPushButton.
        self.theme = useTheme()

        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            for child in self._children:
                self.layout().addWidget(child)
        else:
            # self.layout().addWidget(PySvgWidget(color=self.theme.palette.primary.main, **self.kwargs))
            self.layout().addWidget(PySvgWidget(**self.kwargs))


        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        if self._asynRenderQss:
            self.updateStyleSheet.connect(self._updateStylesheet)
        else:
            self._setStyleSheet()
        
        self.destroyed.connect(lambda obj: self._onDestroy())


    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_setStyleSheet())

    async def _lazy_setStyleSheet(self):
        self._setStyleSheet()

    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheet(cls, objectName: str, styledConfig: str="ListItemIcon"):
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components
            
        PyListItemIcon_root = themeComponent["PyListItemIcon"].get("styles")["root"](cls.ownerState)
        PyListItemIcon_root_qss = get_qss_style(PyListItemIcon_root, class_name=f"#{objectName}")
        
        return PyListItemIcon_root_qss
    
    def _renderStylesheet(self):
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyListItemIcon", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet()
            
        sxQss = ""
        if self._sx:
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"ListItemIcon")

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """
        
        self.updateStyleSheet.emit(stylesheet)
        
    @classmethod
    def _setSx(cls, sx: dict = {}):
        cls.sxDict = sx
        
    @classmethod
    def _setKwargs(cls, kwargs: dict = {}):
        cls.ownerState = kwargs

    @classmethod
    @lru_cache(maxsize=128)
    def _getSxQss(cls, sxStr: str = "", className: str = "PyWidgetBase"):
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss
        
    def _updateStylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)
    
    def _setStyleSheet(self):
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyListItemIcon", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(objectName=self.objectName(), styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet(objectName=self.objectName())
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"ListItemIcon")

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """

        self.setStyleSheet(stylesheet)

        
    def showEvent(self, event):
        if self._asynRenderQss:
            threading.Thread(target=self._renderStylesheet, args=(), daemon=True).start()
        return super().showEvent(event)