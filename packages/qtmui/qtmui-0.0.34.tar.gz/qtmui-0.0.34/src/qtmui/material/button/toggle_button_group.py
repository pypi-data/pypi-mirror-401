import asyncio
import uuid
from typing import Optional, List, Callable, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor

from qtmui.hooks import State

from .toggle_button import ToggleButton

class ToggleButtonGroup(QFrame):
    valueChanged = Signal(object)  # Tín hiệu được phát khi giá trị thay đổi

    def __init__(
        self,
        children: List[ToggleButton],  # Thay đổi từ buttons thành children
        exclusive: bool = False,
        key: Optional[str] = None,
        color: str = 'default',
        size: str = 'medium',
        orientation: str = 'horizontal',
        fullWidth: bool = False,
        disabled: bool = False,
        value: Optional[Any] = None,
        onChange: Optional[Callable[[Any], None]] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.setObjectName(str(uuid.uuid4()))

        self._children = children  # Đổi từ _buttons thành _children
        self._exclusive = exclusive
        self._color = color
        self._size = size
        self._orientation = orientation
        self._fullWidth = fullWidth
        self._disabled = disabled
        self._state = value

        if isinstance(self._state, State):
            self._value = self._state.value
            self._state.valueChanged.connect(self._on_state_changed)
            self._set_state(self._state.value)

        self._onChange = onChange

        # Tạo ButtonGroup cho chức năng chọn độc quyền (exclusive)
        self._button_group = QButtonGroup(self)
        if self._exclusive:
            self._button_group.setExclusive(True)

        # Thiết lập layout dựa trên orientation
        if self._orientation == 'horizontal':
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())

        self.layout().setContentsMargins(4,4,4,4)
        self.layout().setSpacing(5)
        self.layout().setAlignment(Qt.AlignCenter)

        # Thêm các nút vào nhóm và thiết lập sự kiện
        for button in self._children:  # Thay đổi thành _children
            self._add_button(button)

        border_color = "rgba(145, 158, 171, 0.1)"
        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    background-color: white;
                    border: 1px solid {border_color};
                    border-radius: 8px;
                }}

            """
        )

    def _on_state_changed(self, newValue):
        self._value = newValue
        self.valueChanged.emit(self._value)
        self._set_state(newValue)

    def _add_button(self, button: ToggleButton):
        """Thêm một nút vào ToggleButtonGroup."""
        if self._fullWidth:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        else:
            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        button.clicked.connect(self._on_button_clicked)
        if self._color:
            button._color = self._color
        if self._size:
            button._size = self._size

        if self._disabled:
            self.setEnabled(not self._disabled)

        QTimer.singleShot(0, button._scheduleSetStyleSheet)

        self.layout().addWidget(button)

    def _on_button_clicked(self):
        """Hàm xử lý khi một nút được click."""
        clicked_button: ToggleButton = self.sender()
        # Phát tín hiệu thay đổi giá trị
        if self._exclusive:
            if self._onChange:
                self._onChange(clicked_button._key)
        else:
            if self._onChange:
                if clicked_button._key in self._value:
                    self._value.remove(clicked_button._key)
                else:
                    self._value.append(clicked_button._key)
                self._onChange(self._value)

    def _set_state(self, value: Any):
        """Đặt giá trị hiện tại cho ToggleButtonGroup."""
        if self._exclusive:
            # Chỉ chọn một nút
            for button in self._children:
                button.set_selected(button._key == value)
        else:
            # Có thể chọn nhiều nút
            for button in self._children:
                button.set_selected(button._key in value)

    def get_value(self):
        """Trả về giá trị hiện tại của ToggleButtonGroup."""
        return self._state

    def set_disabled(self, disabled: bool):
        """Vô hiệu hóa tất cả các nút trong ToggleButtonGroup."""
        self._disabled = disabled
        for button in self._children:
            button.setDisabled(disabled)


