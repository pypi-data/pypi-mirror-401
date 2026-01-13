from typing import TYPE_CHECKING, Union, Callable
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, Property, Slot, Signal

from ..controller import Controller
from ..slider import Slider
from ..box import Box
from ..form_helper_text import FormHelperText
from qtmui.material.styles import useTheme
from qtmui.hooks import useState

from ..qss_name import *


class RHFSlider(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            control: QWidget = None,
            onChange: Callable = None,
            helperText: str = None,
            ):
        super().__init__()

        self._name = name
        if isinstance(control.value(), tuple):
            self._value = list(control.value())
        else:
            self._value = control.value()
            
        self._control = control
        self._onChange = onChange
        self._helperText = helperText
        
        self._state, self._setState = useState(None)

        self._stateSignal = None

        if control._orientation == "vertical":
            self.setLayout(QVBoxLayout())
            self._direction = "column"
        else:
            self.setLayout(QHBoxLayout())
            self._direction = "row"

        control.valueChanged.connect(self.set_value)

        self.layout().setContentsMargins(0,0,0,0)

        self.lbl_helper_text = QLabel(self)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Box(
                    direction=self._direction,
                    children=[
                        control,
                        self.lbl_helper_text
                    ]
                )
            )
        )

    def set_value(self, value=None):
        print('typpeeeeeeeeeeee', type(value))
        if isinstance(value, tuple):
            self._value = list(value)
        else:
            self._value = value
        print(f"RHFSlider {self._name}: {self._value}")
        self.valueChanged.emit(self._value)
        if self._onChange:
            self._onChange(value)
            
        self._setState(self._value)


    @Property(bool)
    def stateSignal(self):
        return self._stateSignal

    @stateSignal.setter
    def stateSignal(self, value):
        self._stateSignal = value
        self._stateSignal.connect(self.state)


    @Slot(object)
    def state(self, state):
        theme = useTheme()
        if self._name == state.get("field"):
            if state.get("error"):
                # self._complete._inputField._set_slot({"slot": "error", "message": state.get("error_message")})
                self.lbl_helper_text.setText(str(state.get("error_message")[0]))
                self.lbl_helper_text.setStyleSheet(f'''
                    padding-left: 8px;
                    font-size: {theme.typography.caption.fontSize};
                    font-weight: {theme.typography.caption.fontWeight};
                    color: {theme.palette.error.main};
                ''')
                if not self.lbl_helper_text.isVisible():
                    self.lbl_helper_text.show()
            else:
                # self._complete._inputField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()
