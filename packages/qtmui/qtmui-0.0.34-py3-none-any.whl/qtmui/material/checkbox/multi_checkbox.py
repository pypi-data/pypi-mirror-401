from typing import Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPainter, QPen, QIcon
from PySide6.QtCore import Qt, QSize, Signal

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from ..system.color_manipulator import hex_string_to_qcolor
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from .checkbox import Checkbox
from ..form_control_label import FormControlLabel

from qtmui.hooks import State, useEffect

from qtmui.material.styles import useTheme


class MultiCheckbox(QWidget):

    valueChanged = Signal(bool)

    """
    LoadingButton
    Base Button

    Args:
        loading?: True | False
        loadingPosition?: "start" | "center" | "end"
        loadingIndicator?: "Loading..." | any str

    Returns:
        new instance of LoadingButton
    """
    def __init__(self,
                value: object = None,
                orientation: str = "vertical",
                options: bool = False,
                onChange: Callable = None,
                *args, **kwargs
                ):
        super().__init__()
        
        self._value = value
        self._options = options
        self._orientation = orientation
        self._onChange = onChange
        self._selected_values = []  # Lưu giá trị được chọn

        self._init_ui()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )

        self._set_stylesheet()
    
    def _init_ui(self):
        self.setObjectName("PyMultiCheckbox")
        self.setLayout(QVBoxLayout() if self._orientation == "vertical" else QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        if self._options:
            for option in self._options:
                self.layout().addWidget(
                        FormControlLabel(
                            label=option.get("label"), 
                            control=Checkbox(
                                checked=option.get("value") == self._value, value=option.get("value"), onChange=self._on_field_value_change,
                            )
                        ),
                )

    def _set_stylesheet(self):
        pass

    def _on_field_value_change(self, data):
        value, checked = data[0], data[1]
        """Cập nhật danh sách giá trị đã chọn và phát tín hiệu."""
        if checked:
            if value not in self._selected_values:
                self._selected_values.append(value)  # Thêm giá trị nếu được chọn
        else:
            if value in self._selected_values:
                self._selected_values.remove(value)  # Loại bỏ giá trị nếu bỏ chọn

        print("Updated selected values:", self._selected_values)
        self.valueChanged.emit(self._selected_values)  # Phát tín hiệu với danh sách mới

        if self._onChange:
            self._onChange(self._selected_values)

        self._value = self._selected_values