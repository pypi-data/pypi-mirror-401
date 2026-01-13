import uuid
from typing import Callable, Optional, Union
from PySide6.QtCore import Qt, Signal, Slot, Property
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qtmui.hooks import useState
from qtmui.hooks import State

from ..controller import Controller
from ..textfield import TextField

from qtmui.material.styles import useTheme

from qtmui.qss_name import *

class RHFTextField(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            key: str=None,
            label: Optional[Union[str, State, Callable]]=None,
            value: str = None,
            defaultValue: str = None,
            type: object = None,
            field: object = None,
            multiline: bool = False,
            options: object = None,
            spacing: int = None,
            InputProps: object = None,
            helperText: str = None,
            # textChanged: object = None,
            placeholder: str = None,
            *args,
            **kwargs
            ):
        super().__init__()

        self._name = name
        self._key = key
        self._value = value
        self._InputProps = InputProps
        self._placeholder = placeholder

        self._state, self._setState = useState(None)

        self._label = label
        self._defaultValue = defaultValue
        
        if self._defaultValue is not None:
            self._value = self._defaultValue
            
        self._stateSignal = None

        self._field = field
        control = False
        error = None
        self._type = type

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "border: none;background: pink;")) # str multi line

        if not multiline:
            self.setFixedHeight(60)


        self.textField = TextField(
                    key=self._key,
                    label=self._label,
                    value=self._value,
                    type=self._type,
                    defaultValue=self._defaultValue,
                    multiline=multiline,
                    InputProps=self._InputProps,
                    placeholder=self._placeholder,
                    # value="" if self._type == "number" and field.value == 0 else field.value,
                    # textChanged=lambda event: field.textChanged(int(event.target.value)) if type == "number" else field.textChanged(event.target.value),
                    # onChange=textChanged,
                    error=not error,
                    # helperText=error.message if error and hasattr(error, 'message') else helperText
                    *args,
                    **kwargs
                )

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=self.textField
            )
        )

        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setFixedHeight(14)
        self.lbl_helper_text.setStyleSheet(f'''
            padding-left: 8px;
            {useTheme().typography.caption.to_qss_props()}
            font-size: 11px;
        ''')
        self.lbl_helper_text.setText("")
        self.layout().addWidget(self.lbl_helper_text)

        self.textField.valueChanged.connect(self.set_only_value_not_change_text)


    def set_only_value_not_change_text(self, value):
        if self._type == "int":
            self._value = int(value)
        elif self._type == "float":
            self._value = float(value)
        else:
            self._value = value

        self.valueChanged.emit(self._value)
        self._setState(self._value)
        # print('RHFTextField_setState_________________________1111111111', self._state.value, self._value)
        

    def set_value(self, value, setText=True):
        if self._type == "int":
            self._value = int(value)
        elif self._type == "float":
            self._value = float(value)
        else:
            self._value = value

        self.valueChanged.emit(self._value)

        self.textField._set_data(value=self._value, valueChanged=False)
        
        self._setState(self._value)
        # print('RHFTextField_setState_________________________222222222', self._state.value, self._value)


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
                self.textField._set_slot({"slot": "error", "message": state.get("error_message")})
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
                self.textField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()
