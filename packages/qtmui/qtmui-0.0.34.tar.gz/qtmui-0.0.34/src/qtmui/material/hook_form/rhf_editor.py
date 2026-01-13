from typing import Callable, Optional, Sequence
from PySide6.QtCore import Qt, Property, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel

from qtmui.material.styles import useTheme
from qtmui.hooks import useState

from qtmui.hooks import State
from ...material.controller import Controller
from ..editor import Editor

class RHFEditor(QFrame):
    valueChanged = Signal(object)
    def __init__(
            self,
            name,
            max: int = 5,
            value: int = 3,
            onChange: Optional[Callable] = None,
            simple: Optional[bool] = None,
            helperText: str = None,
            **kwargs
            ):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)

        self._name = name
        self._value = None
        
        self._state, self._setState = useState(None)
        
        self._onChange = onChange
        self._helperText = helperText

        self._stateSignal = None

        control = False

        self.layout().addWidget(
            Controller(
            name=name,
            control=control,
            render=Editor(onChange=self._set_value, simple=simple, **kwargs)
            )
        )

        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setStyleSheet(f'''
            padding-left: 8px;
            {useTheme().typography.caption.to_qss_props()}
            font-size: 11px;
        ''')
        self.lbl_helper_text.setText("")
        self.layout().addWidget(self.lbl_helper_text)

        # self._complete.valueChanged.connect(self.set_value)

        # if self._onValueChanged is not None:
        #     self.valueChanged.connect(self._onValueChanged)


    def _set_value(self, value=None):
        self._value = value
        if self._value == []:
            self._value = None
        print(f"RHFRating {self._name}: {self._value}")
        self.valueChanged.emit(value)

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


