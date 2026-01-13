from typing import Callable, Optional, Union
import uuid
from PySide6.QtCore import Qt, Property, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from qtmui.hooks import State

from ...material.masonry.masonry import Masonry

from qtmui.hooks import useState

from ..controller import Controller
from ..form_control_label import FormControlLabel
from ..box import Box
from ..form_control import FormControl
from ..form_label import FormLabel
from ..radio import Radio
from ..radio_group import RadioGroup

from qtmui.material.styles import useTheme

from ..qss_name import *

class RHFRadioGroup(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            key: Optional[str] = None,
            value: object = None,
            orientation: str = "horizontal",
            label: Optional[Union[str, State, Callable]]=None,
            options: object = None,
            spacing: int = None,
            helperText: str = None,
            row: bool = False,
            ):
        super().__init__()


        self._name = name
        self._key = key

        self._state, self._setState = useState(None)

        self._value = value
        self._row = row
        self._label = label

        self._options = options

        # self._isOptionEqualToValue = isOptionEqualToValue

        self._stateSignal = None

        self._control = False

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        if self._row:
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "border: none;background: #ffeaa7;")) # str multi line

        self.lbl_helper_text = QLabel(self)

        self._radio_group = RadioGroup(value=self._value, options=self._options, orientation="horizontal", onChange=self._on_change)


        self.layout().addWidget(
            Controller(
                name=self._name,
                control=self._control,
                render=FormControl(
                    component="fieldset",
                    children=[
                        Box(
                            direction="column",
                            children=[
                                FormLabel(component="legend", label=self._label) if self._label else None,
                                self._radio_group,
                                self.lbl_helper_text
                            ]
                        )
                    ]
                )
            )
        )

    def set_value(self, value):
        self._value = value

        if self._key == "webglMetadatakeyyyyyyyyyyyyy":
            print('set_valuewebglMetadatakeyyyyyyyyyyyyy___________', self._value)

        self.valueChanged.emit(self._value)
        self._radio_group._set_checked(self._value)
        
        self._setState(self._value)
        # print('RHFRadioGroup_set_value_________________________', self._state.value)

    def _on_change(self, value):
        self._value = value
        print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(value)
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
