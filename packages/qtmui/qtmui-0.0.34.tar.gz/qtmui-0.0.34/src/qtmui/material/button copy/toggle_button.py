import asyncio
from typing import Optional, List, Callable, Any, Union
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from qtmui.hooks import State

from .button import Button
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme

class ToggleButton(Button):
    def __init__(
        self,
        icon: Optional[str] = ":/round/resource_qtmui/round/access_time.svg",
        text: Optional[Union[str, State, Callable]] = None,
        value: Optional[object] = None,
        selected: bool = False,
        *args, **kwargs
    ):
        super().__init__(text=text, startIcon=icon, value=value, *args, **kwargs)

        self._selected = selected

        self._init_ui()

    def _init_ui(self):
        self.setCheckable(True)  # Toggle button cần có trạng thái check/uncheck

        """Thiết lập trạng thái được chọn của ToggleButton."""
        if self._selected:
            super().set_selected(True)

    def _set_stylesheet(self, component_styled=None):
        super()._set_stylesheet()
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        ownerState = {
            "size": self._size
        }
        PyToggleButton_root = component_styled["PyToggleButton"].get("styles")["root"](ownerState)[self._color]
        if self._color in ['primary', 'secondary', 'info', 'success', 'warning', 'error']:
            PyToggleButton_root_slot_hover_qss = get_qss_style(PyToggleButton_root["slots"]["hover"])
            PyToggleButton_root_prop_disabled_selected_qss = get_qss_style(PyToggleButton_root["props"]["disabled"]["selected"])
        else:
            PyToggleButton_root_selected_qss = get_qss_style(PyToggleButton_root["selected"])

