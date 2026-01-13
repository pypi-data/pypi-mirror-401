from typing import Callable, Optional, Union
import uuid

from PySide6.QtWidgets import QHBoxLayout, QFrame, QPushButton

from qtmui.hooks import State

from ...material.styles import useTheme

from ..widget_base import PyWidgetBase

class Option(QFrame, PyWidgetBase):
    def __init__(self,
                 key: str = None,
                 value: object = None,
                 enabled: bool = True,
                label: Optional[Union[str, State, Callable]] = None,
                 
                 selected: bool = None,
                 children: object = None,
                 *args, **kwargs
                 ):
        super().__init__(*args, **kwargs)

        self._enabled = enabled
        self._children = children
        self._key = key
        self._label = label
        self._value = value
        self._selected = value

        self.__init_ui()

        PyWidgetBase._installTooltipFilter(self)

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()


    def __init_ui(self):

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        if self._children is not None:
            if isinstance(self._children, list):
                for item in self._children:
                    self.layout().addWidget(item)
            else:
                self.layout().addWidget(self._children)
        else:
            self.button = QPushButton(text=self._label if self._label else "")

            self.layout().addWidget(self.button)
            self.clicked = self.button.clicked


    def _set_stylesheet(self):
        theme = useTheme()

        self.button.setStyleSheet(f"""
            QPushButton {{
                padding: 10px;
                border-radius: {theme.shape.borderRadius}px;
                background-color: transparent;
                color: {theme.palette.text.secondary};
                text-align: left;
                font-weight: {theme.typography.button.fontWeight};
                line-height: {theme.typography.button.lineHeight};
                font-size: {theme.typography.button.fontSize};
            }}
            QPushButton:hover {{
                padding: 10px;
                border-radius: {theme.shape.borderRadius}px;
                background-color: {theme.palette.action.selected};
                color: {theme.palette.text.secondary};
            }}
        """)

    def set_selected(self, state):
        self._selected = state
        self._set_selected(state)

    def _set_selected(self, selected):
        theme = useTheme()

        if selected:
            self.button.setStyleSheet(f"""
                QPushButton {{
                    padding: 10px;
                    border-radius: {theme.shape.borderRadius}px;
                    background-color: {theme.palette.action.selected};
                    color: {theme.palette.text.secondary};
                    text-align: left;
                    font-weight: {theme.typography.button.fontWeight};
                    line-height: {theme.typography.button.lineHeight};
                    font-size: {theme.typography.button.fontSize};
                }}
                QPushButton:hover {{
                    padding: 10px;
                    border-radius: {theme.shape.borderRadius}px;
                    background-color: {theme.palette.action.selected};
                    color: {theme.palette.text.secondary};
                }}
            """)
        else:
            self.button.setStyleSheet(f"""
                QPushButton {{
                    padding: 10px;
                    border-radius: {theme.shape.borderRadius}px;
                    background-color: transparent;
                    color: {theme.palette.text.secondary};
                    text-align: left;
                    font-weight: {theme.typography.button.fontWeight};
                    line-height: {theme.typography.button.lineHeight};
                    font-size: {theme.typography.button.fontSize};
                }}
                QPushButton:hover {{
                    padding: 10px;
                    border-radius: {theme.shape.borderRadius}px;
                    background-color: {theme.palette.action.selected};
                    color: {theme.palette.text.secondary};
                }}
            """)

    def set_menu_item_visible(self, state):
        self.button.set_menu_item_visible(state)
        # if state == True:
        #     self.parent().setMaximumHeight(self.parent().height() + self._height)
        # else:
        #     self.parent().setMaximumHeight(self.parent().height() - self._height)

