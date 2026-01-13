import asyncio
from functools import lru_cache
from typing import Callable, Optional, Union, Dict
from PySide6.QtGui import QCursor, QDesktopServices, QPalette
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QToolButton, QPushButton
from PySide6.QtCore import Qt, QUrl, QTimer
import uuid


from qtmui.hooks.use_runable import useRunnable

from qtmui.hooks import State, useEffect

# from ..py_tool_button.py_tool_button import PyToolButton

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor, TypeText
from qtmui.material.styles.create_theme.typography import TypographyStyle
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.i18n.use_translation import translate, i18n

from ..widget_base import PyWidgetBase
from ..py_iconify import Iconify

from ...utils.data import convert_sx_params_to_str, convert_sx_params_to_dict


class Link(QPushButton, PyWidgetBase):

    def __init__(self,  
                 align="left",
                 children=None,
                text: Optional[Union[str, State, Callable]] = None,
                 color: str = "textPrimary",
                 disabled: bool = False,
                 value: object = None,
                 classes=None, 
                 gutterBottom=None,
                 wrap=False,
                 icon: Iconify = None,
                 width: Optional[int]=None,
                 paragraph=None,
                 href: str = None,
                 underline: str = "hover", # "hover" | "always"
                 onClick: Callable = None,
                sx: Optional[Union[Callable, str, Dict]]= None,
                 variant:str="body1",
                 *args,
                 **kwargs
                 ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))
        
        self._align = align
        self._color = color
        self._children = children
        self._disabled = disabled
        self._classes = classes
        self._wrap = wrap
        self._icon = icon
        self._width = width
        self._gutterBottom = gutterBottom
        self._paragraph = paragraph
        self._sx = sx
        self._text = text
        self._value = value
        self._variant = variant
        self._underline = underline
        self._onClick = onClick
        self._href = href

        self._hovered = False

        self._init_ui()

        self.theme = useTheme()
        
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        
        self._set_stylesheet()

    def _get_text(self):
        return self._text.value if isinstance(self._text, State) else self._text

    def _init_ui(self):

        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.setText(self._get_text())
        
        QTimer.singleShot(0, self._setIcon)
        

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)



    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        typography_style: TypographyStyle = getattr(self.theme.typography, self._variant)
        typography_qss = typography_style.to_qss_props()

        PyTypography_root_qss = ""
        if self._color in ['primary', 'secondary', 'info', 'success', 'warning', 'error', 'textPrimary', 'textSecondary', 'textDisabled']:
            PyTypography_root = self.theme.components[f"PyTypography"].get("styles").get("root").get(self._color)
            PyTypography_root_qss = get_qss_style(PyTypography_root)

                
        underline = False
        if self._underline == "always":
            underline = True
        elif self._underline == "hover":
            underline = self._hovered

        decoration = "underline" if underline else "none"
                
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
            #{self.objectName()} {{
                {typography_qss}
                {PyTypography_root_qss}
                text-decoration: {decoration};
                text-align: left;
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def _setIcon(self):
        if isinstance(self._icon, Iconify):
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            self._icon._color = color.name()
            self.setIcon(self._icon.qIcon())#"#919eab"


    # ---------- Hover ----------
    def enterEvent(self, event):
        self._hovered = True
        self._set_stylesheet()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._set_stylesheet()
        super().leaveEvent(event)

    # ---------- Click ----------
    def mousePressEvent(self, event):
        if self._disabled:
            return

        if event.button() == Qt.LeftButton:
            # self.clicked.emit()

            if self._onClick:
                self._onClick()

            # if self.component == "a" and self._href:
            if self._href and self._href.startswith("http"):
                QDesktopServices.openUrl(QUrl(self._href))

        super().mousePressEvent(event)
            
