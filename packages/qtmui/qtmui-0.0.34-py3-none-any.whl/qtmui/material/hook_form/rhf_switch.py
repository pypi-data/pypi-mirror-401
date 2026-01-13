from typing import Optional, Union, Callable, Dict
import uuid
from PySide6.QtCore import Property, Slot, Signal, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame, QVBoxLayout

from qtmui.hooks import State

from ..controller import Controller
from ..form_control_label import FormControlLabel
from ..box import Box
from ..switch import Switch
from qtmui.material.styles import useTheme

from qtmui.hooks import useState

from ..qss_name import *

class RHFSwitch(QFrame):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            key: Optional[str] = None,
            defaultChecked: Optional[bool] = None,
            value: bool = False,
            hightLight: bool = None,
            row: bool = False,
            checked: bool = False,
            label: Optional[Union[str, State, Callable]]=None,
            fullWidth: bool = False,
            labelPlacement: str = "end",
            options: object = None,
            spacing: int = None,
            helperText: str = None,
            sx: Optional[Union[Callable, str, Dict]]= None
            ):
        super().__init__()

        self._name = name
        self._key = key
        self._value = value
        self._checked = defaultChecked or checked
        self._fullWidth = fullWidth
        self._helperText = helperText

        self._state, self._setState = useState(None)

        self._stateSignal = None

        self.setLayout(QVBoxLayout())
        # self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)
        if not self._fullWidth:
            self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum) 
        self.layout().setContentsMargins(0,0,0,0)

        if hightLight:
            self.setObjectName(str(uuid.uuid4()))
            self.setStyleSheet('''#{} {{ {} }}'''.format(self.objectName(), "border: 1px solid red;"))

        control = False

        if self._checked:
            self._value = True
        else:
            self._value = False

        self.lbl_helper_text = QLabel(self)

        self._control = Switch(checked=self._checked, onChange=self._on_change)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Box(
                        direction="column",
                        # sx=sx,
                        # sx={"background-color": "red"},
                        children=[
                            FormControlLabel(
                                hightLight=True,
                                labelPlacement=labelPlacement,
                                label=label, 
                                control=self._control,
                                fullWidth=self._fullWidth
                            ),
                            # self.lbl_helper_text
                            # self._helperText and self.lbl_helper_text
                            # FormHelperText(error=error.message if error and hasattr(error, 'message') else helperText)
                        ]
                )

            )
        )

    def set_value(self, value):
        self._value = value

        self.valueChanged.emit(self._value)
        if self._key == "locationSwitch___________":
            print('set_value locationSwitch___________', self._value)
        self._control.setChecked(self._value)
        
        self._setState(self._value)

    def _on_change(self, value):
        if int(value) == 0:
            self._value = True
        else:
            self._value = False
        print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(self._value)
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