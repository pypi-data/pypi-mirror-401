import asyncio
from functools import lru_cache
from typing import Callable, Optional, Union, Dict
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QToolButton
from PySide6.QtCore import Qt, QThreadPool, QTimer
import uuid


from qtmui.hooks.use_runable import useRunnable

from qtmui.hooks import State

# from ..py_tool_button.py_tool_button import PyToolButton

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor, TypeText
from qtmui.material.styles.create_theme.typography import TypographyStyle
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.i18n.use_translation import translate, i18n

from ..widget_base import PyWidgetBase
from ..py_iconify import PyIconify

from ...utils.data import convert_sx_params_to_str, convert_sx_params_to_dict


class Typography(QLabel, PyWidgetBase):

    def __init__(self,  
                 id=None,
                 align="left",
                 children=None,
                 text="",
                 color: str = "textPrimary",
                 value: object = None,
                 classes=None, 
                 gutterBottom=None,
                 wrap=False,
                 width: Optional[int]=None,
                 paragraph=None,
                 onClick: Callable = None,
                sx: Optional[Union[Callable, str, Dict]]= None,
                 variant:str="body1",
                 typography:str=None,
                 *args,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.setObjectName(str(uuid.uuid4()))

        self._align = align
        self._color = color
        self._children = children
        self._classes = classes
        self._wrap = wrap
        self._width = width
        self._gutterBottom = gutterBottom
        self._paragraph = paragraph
        self._sx = sx
        self._text = text
        self._value = value
        self._variant = variant
        self._onClick = onClick

        self._state = self._text
        
        self._init_ui()

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()

        self.theme = useTheme()
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._set_stylesheet()

    def _init_ui(self):

        if self._width:
            self.setFixedWidth(self._width)

        if isinstance(self._children, list) and all(isinstance(item, str) for item in self._children):
            children_widget = []
            for item in self._children:
                children_widget.append(QLabel(item))
            self._children = children_widget
        elif isinstance(self._children, str):
            self._children = [QLabel(self._children)]


        if self._children:
            # if not all(isinstance(item, PyToolButton) for item in children):
            #     print('children______', children, PyToolButton)
            #     raise ValueError("Opp!!!.Only accepts children where all elements are of type PyToolButton.")
            self.setLayout(QHBoxLayout())
            self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.layout().setContentsMargins(0,0,0,0)
            if isinstance(self._children, list):
                for widget in self._children:
                    if isinstance(widget, QWidget):
                        self.layout().addWidget(widget)
                    if isinstance(widget, PyIconify):
                        btn = QToolButton()
                        btn.setIcon(widget)
                        btn.setStyleSheet("background-color: none; border: none;")
                        self.layout().addWidget(btn)
                    else:
                        self.layout().addWidget(QLabel(widget))
            # elif isinstance(self._children, PyToolButton):
            #     self.layout().addWidget(self._children)

            self._lbl_text = QLabel(self)
            self._lbl_text.setObjectName('textContent')
            self.layout().addWidget(self._lbl_text)

            if self._wrap:
                self._lbl_text.setWordWrap(True)

                self._state.valueChanged.connect(self.reTranslation)

            if self._align == "left":
                self._lbl_text.setAlignment(Qt.AlignLeft)
            if self._align == "center":
                self._lbl_text.setAlignment(Qt.AlignCenter)
            if self._align == "right":
                self._lbl_text.setAlignment(Qt.AlignRight)

        else:
            if self._wrap:
                self.setWordWrap(True)

            if self._state:
                if isinstance(self._state, State):
                    self._state.valueChanged.connect(self.reTranslation)

            if self._align == "left":
                self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            if self._align == "center":
                self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            if self._align == "right":
                self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)


    def reTranslation(self):
        # print('vaoooooooooooooooooo________reTranslation')
        if hasattr(self, "_lbl_text"):
            if isinstance(self._state, State):
                if isinstance(self._state.value, Callable):
                    self._lbl_text.setText(translate(self._state.value))
                else:
                    self._lbl_text.setText(str(self._state.value))
            else:
                self._lbl_text.setText(str(self._state))

            total_children_w = 0
            if isinstance(self._children, list):
                for widget in self._children:
                    total_children_w += widget.sizeHint().width() if isinstance(widget, QWidget) else 0
                self.setMinimumWidth(total_children_w + self._lbl_text.sizeHint().width() + 16)
            else:
                self.setMinimumWidth(self._children.sizeHint().width() + self._lbl_text.sizeHint().width() + 16)

        else:
            if isinstance(self._state, State):
                if isinstance(self._state.value, Callable):
                    self.setText(translate(self._state.value))
                else:
                    self.setText(str(self._state.value))
            else:
                if isinstance(self._state, QWidget):
                    self.setLayout(QHBoxLayout())
                    self.layout().setContentsMargins(0,0,0,0)
                    self.layout().addWidget(self._state)
                elif isinstance(self._state, str):
                    self.setText(self._state)
                # else:
                #     raise ValueError(f"Unsuported text with type {type(self._state)}")
            # self.adjustSize()

    # def showEvent(self, e):
    #     """ fade in """
    #     PyWidgetBase.showEvent(self)
    #     super().showEvent(e)

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
            }}

            {sx_qss}

        """

        self.setStyleSheet(stylesheet)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if self._onClick:
            self._onClick()
        return super().mousePressEvent(ev)

            
