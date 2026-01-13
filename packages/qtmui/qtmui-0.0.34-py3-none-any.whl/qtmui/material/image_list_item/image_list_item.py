# src/qtmui/material/image_list_item.py
from typing import Optional, Union, Callable, Dict, List
from functools import lru_cache
from typing import TYPE_CHECKING
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State

if TYPE_CHECKING:
    from ..image import Image
    from ..image_list_item_bar import ImageListItemBar

class ImageListItem(QFrame):
    def __init__(
        self,
        children=None,
        cols=1,
        rows=1,
        title=None,
        subtitle=None,
        actionIcon=None,
        titlePosition="bottom",  # top, bottom, below
        sx: Optional[Union[State, Callable, str, Dict]] = None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(f"ImageListItem{str(id(self))}")
        if sx:
            self._setSx(sx)
            
        self._kwargs = {
            "cols": cols,
            "rows": rows,
            "title": title,
            "subtitle": subtitle,
            "actionIcon": actionIcon,
            "titlePosition": titlePosition,
            **kwargs
        }
        self._setKwargs(self._kwargs)
        
        self.cols = cols
        self.rows = rows
        self._sx = sx

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container cho image + overlay
        self.image_container = QFrame()
        # self.image_container.setStyleSheet("background: #000; border-radius: 8px; overflow: hidden;")
        self.image_container.setStyleSheet("background: #000; border-radius: 8px")
        container_layout = QVBoxLayout(self.image_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        if children:
            for child in children:
                # if isinstance(child, Image):
                #     child.setStyleSheet("border-radius: 8px;")
                container_layout.addWidget(child)

        layout.addWidget(self.image_container)

        # Thêm titlebar nếu có
        if title or subtitle or actionIcon:
            bar = ImageListItemBar(
                title=title or "",
                subtitle=subtitle,
                actionIcon=actionIcon,
                position=titlePosition,
            )
            if titlePosition in ["top", "bottom"]:
                # Overlay vào trong image
                container_layout.addWidget(bar)
                bar.setStyleSheet(bar.styleSheet() + "position: absolute; width: 100%;")
                bar.setAttribute(Qt.WA_TransparentForMouseEvents, titlePosition == "bottom")
            else:
                # Below image
                layout.addWidget(bar)

        self.setLayout(layout)
        
        self._setStyleSheet()
        
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
        
    def _setStyleSheet(self):
        
        # stylesheet = ""
        # if hasattr(self, "styledDict"):
        #     root = self.styledDict.get("PyBox", {}).get("styles", {}).get("root", None)(self._kwargs)
        #     if root:
        #         stylesheet = self._getStyleSheet(styledConfig=str(root))
        # else:
        #     stylesheet = self._getStyleSheet()
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")

        stylesheet = f"""
            {sxQss}
        """
        
        self.setStyleSheet(stylesheet)