from typing import Callable, Optional, Union
import uuid
from PySide6.QtCore import Qt, Property, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel

from qtmui.hooks import useState
from qtmui.hooks import State
from ...material.spacer.hspacer import HSpacer
from ...material.form_label.form_label import FormLabel
from ...material.button.button import Button

from ..controller import Controller
from ..form_control_label import FormControlLabel
from ..box import Box
from ..form_helper_text import FormHelperText
from ..switch import Switch

from qtmui.material.styles import useTheme

from ..qss_name import *

class RHFListView(QWidget):
    def __init__(
            self,
            name: str,
            value: bool = False,
            hightLight: bool = None,
            row: bool = False,
            label: Optional[Union[str, State, Callable]]=None,
            list_view: object = None,
            spacing: int = None,
            helperText: str = None,
            ):
        super().__init__()

        self._name = name
        self._value = value

        self._state, self._setState = useState(None)

        self._list_view = list_view

        self._stateSignal = None

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        if hightLight:
            self.setObjectName(str(uuid.uuid4()))
            self.setStyleSheet('''#{} {{ {} }}'''.format(self.objectName(), "background: red;"))

        control = False

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Box(
                    hightLight=True,
                    direction="column",
                    children=[
                        FormLabel(component="legend", label=label),
                        FormControlLabel(
                            control=self._list_view
                        )
                        # FormHelperText(error=error.message if error and hasattr(error, 'message') else helperText)
                    ]
                )
            )
        )

        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setStyleSheet('padding-left: 8px;')
        self.lbl_helper_text.setText("")
        self.layout().addWidget(self.lbl_helper_text)
        self.layout().addWidget(
            Box(
                direction="row",
                children=[
                    HSpacer(),
                    Button(text="Add language", variant="outlined", onClick=self.add_new_item)
                ]
            )
        )

        self.setup_ui()

    def add_new_item(self):
        pass

    def setup_ui(self):
        for item in self.findChildren(Switch):
            # item.switch_icon.clicked.connect(lambda checked, value=item.switch_icon: self.set_value(value))
            item._switch_icon.checkStateChanged.connect(lambda checked, value=item._switch_icon.isChecked(): self.set_value(value))

    def set_state(self, state):
        if state.get("status") == "invalid":
            # self._inputField._lineEdit.setStyleSheet(self._inputField._lineEdit.styleSheet() + f"border: 1px solid {self._theme.error.main};")
            self.lbl_helper_text.setStyleSheet(f'padding-left: 8px;color: {useTheme().palette.error.main};')
            self.lbl_helper_text.setText(str(state.get("message")))
        elif state.get("status") == "validate":
            # self._inputField._lineEdit.setStyleSheet(self._inputField._lineEdit.styleSheet() + f"border: 1px solid {self._theme.grey.grey_500};")
            self.lbl_helper_text.setStyleSheet(f'padding-left: 8px;')
            self.lbl_helper_text.setText("")
        elif state.get("status") == "helper":
            # self._inputField._lineEdit.setStyleSheet(self._inputField._lineEdit.styleSheet() + f"border: 1px solid {self._theme.grey.grey_500};")
            self.lbl_helper_text.setStyleSheet(f'padding-left: 8px;')
            self.lbl_helper_text.setText(str(state.get("message")))

    def set_value(self, value):
        if int(value) == 0:
            self._value = False
        else:
            self._value = True
            
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
        if self._name == state.get("field"):
            if state.get("error"):
                self.set_state({"status": "invalid", "message": state.get("error_message")})