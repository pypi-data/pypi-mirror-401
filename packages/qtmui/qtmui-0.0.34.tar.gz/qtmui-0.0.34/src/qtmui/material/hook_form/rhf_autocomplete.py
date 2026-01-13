from typing import Callable, Optional, Sequence, Union
from PySide6.QtCore import Qt, Property, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel

from qtmui.material.styles import useTheme

from qtmui.hooks import useState
from qtmui.hooks import State
from ...material.controller import Controller
from ..textfield.textfield import TextField
from ...material.autocomplete.complete import Autocomplete

class RHFAutocomplete(QFrame):
    valueChanged = Signal(object)

    def __init__(
            self,
            name,
            key: Optional[str] = None,
            label: Optional[Union[str, State, Callable]]=None,
            selected: bool = False,
            onChange: Optional[Callable] = None,
            helperText: str = None,
            **kwargs
            ):
        super().__init__()
        self._key = key

        self._state, self._setState = useState("None")

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)

        # if not multiple:
        #     self.setFixedHeight(60)

        self._name = name
        self._label = label
        self._value = None
        self._selected = selected
        self._helperText = helperText
        self._onChange = onChange


        # if self._defaultValue is not None:
        #     if self._multiple:
        #         _value = []
        #         for item in self._defaultValue:
        #             _value.append(item.get("value"))
        #         self.set_value(_value)
        #     else:
        #         self.set_value(self._defaultValue.get("value"))

        self._stateSignal = None

        control = False

        self._complete = Autocomplete(
            key=self._key,
            name=self._name,
            selected=self._selected,
            onChange=lambda newValue:
                self.set_value(newValue)
            ,
            renderInput=lambda params:
                TextField(
                    label=self._label,
                    **params
                )
            ,
            **kwargs
        )

        self.layout().addWidget(
            Controller(
            name=name,
            control=control,
            render=self._complete
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

        self._complete.valueChanged.connect(self.set_value)

        # if self._onValueChanged is not None:
        #     self.valueChanged.connect(self._onValueChanged)


    def set_value(self, value=None):
        if isinstance(value, dict):
            value = value.get("value")
        self._value = value
        if self._value == []:
            self._value = None
        if isinstance(self._selected, State):
            self._selected.value = True

        if self._onChange:
            self._onChange(value)
        self.valueChanged.emit(value)

        if self._key == "Resolution_keyyyyyyyyyyyyy":
            print("Resolution_keyyyyyyyyyyyyy", self._value)
            
        if hasattr(self, "_complete"):
            self._complete._inputField._set_data(value=self._value, valueChanged=False)
        
        self._setState(self._value)
        # print(f"RHFAutocomplete {self._name}: {self._value}")


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
                self._complete._inputField._set_slot({"slot": "error", "message": state.get("error_message")})
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
                self._complete._inputField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()


