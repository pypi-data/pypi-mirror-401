from typing import Optional, Union, Callable, Dict
import uuid

from PySide6.QtWidgets import QToolButton
from PySide6.QtGui import QPalette, QIcon
from PySide6.QtCore import QSize, QEvent

from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.i18n.use_translation import i18n, translate

from ..py_iconify import PyIconify, Iconify

from ..widget_base import PyWidgetBase

class PyToolButton(QToolButton, PyWidgetBase):
    def __init__(
                self, 
                parent=None, 
                color: str = "default", 
                icon: Optional[Union[State, PyIconify, Iconify]] = None,
                iconKey: str = None,
                size: Optional[Union[QSize, str]] = "medium", 
                iconSize: QSize = QSize(16, 16), 
                tooltip=None,
                text: str=None,
                width: int=None,
                sx: Optional[Union[Callable, str, Dict]]= None,
                **kwargs
                ):
        super().__init__(parent, **kwargs)

        self._color = color
        self._icon = icon
        self._iconKey = iconKey
        self._iconSize = iconSize
        self._size = size
        self._tooltip = tooltip
        self._text = text
        self._sx = sx

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        if self._size:
            if isinstance(self._size, QSize):
                self.setFixedSize(self._size)


        PyWidgetBase._installTooltipFilter(self)
        if self._tooltip:
            self.setToolTip(self._tooltip)

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()

        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()
        
        self._setup_icon()
        
        # self.destroyed.connect(self._on_destroyed)
        # self.destroyed.connect(self._py_svg_widget_destroy)

    def _py_svg_widget_destroy(self):
        self.theme.state.valueChanged.disconnect(self._setup_ui)


    def _setup_icon(self):
        if isinstance(self._icon, Iconify):
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            self._icon._color = color.name()
            self.setIcon(self._icon.qIcon())#"#919eab"
            
        if self._iconSize and isinstance(self._iconSize, QSize):
            self.setIconSize(self._iconSize)

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        PyToolButton_root = component_styled["PyToolButton"].get("styles")["root"][self._color]
        PyToolButton_root_qss = get_qss_style(PyToolButton_root)
        PyToolButton_root_slot_hover_qss = get_qss_style(PyToolButton_root["slots"]["hover"])

        PyToolButtonSize_qss = ""
        if self._size in ["small", "medium"]:
            PyToolButtonSize_qss = get_qss_style(component_styled["PyToolButtonSize"].get("styles")[self._size])

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

        self._stylesheet = f"""
                #{self.objectName()} {{
                    {PyToolButton_root_qss}
                    {PyToolButtonSize_qss}
                }}
                #{self.objectName()}:hover {{
                    {PyToolButton_root_slot_hover_qss}
                }}

                {sx_qss}

            """

        self.setStyleSheet(self._stylesheet)
        
        

    def reTranslation(self, value=None):
        if value:
            if isinstance(value, Callable):
                self.setText(translate(value))
            else:
                self.setText(value)
        else:
            if isinstance(self._text, State):
                if isinstance(self._text, Callable):
                    self.setText(translate(self._text.value))
                else:
                    self.setText(self._text)
            else:
                if isinstance(self._text, Callable):
                    self.setText(translate(self._text))
                else:
                    self.setText(self._text)

    def changeEvent(self, event: QEvent):
        if event.type() == event.Type.StyleChange:
            self._setup_icon()
        super().changeEvent(event)
        

    def _set_text_color(self, color):
        if hasattr(self, "_stylesheet"):
            self.setStyleSheet(self._stylesheet + 
                f"""
                    #{self.objectName()} {{
                        color: {color};
                    }}
                """)

    def _set_icon(self, key):
        self._icon.changeSvg(key)