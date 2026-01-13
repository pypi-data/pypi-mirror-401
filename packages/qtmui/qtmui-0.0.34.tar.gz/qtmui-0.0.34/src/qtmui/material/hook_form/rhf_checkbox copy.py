from PySide6.QtCore import Qt, Property, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from qtmui.hooks import State

from ..flow_layout import FlowLayout
from qtmui.material.styles import useTheme

from ..controller import Controller
from ..textfield import TextField
from ..autocomplete.complete import Autocomplete
from ..form_control_label import FormControlLabel
from ..checkbox import Checkbox, MultiCheckbox
from ..form_control import FormControl
from ..form_label import FormLabel
from ..box import Box
from ..form_group import FormGroup
from ..form_helper_text import FormHelperText

from ..qss_name import *

class RHFCheckbox(QFrame):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            value: object = None,
            checked: bool = False,
            label: str = None,
            error: bool = False,
            helperText: str = None,
            ):
        super().__init__()

        self._name = name
        self._value = value

        self._stateSignal = None

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        # self.setStyleSheet('background: red;')

        field = {
            "value": "checkbox value demooooooo"
        }

        control = False

        if checked:
            self._value = True
        else:
            self._value = False


        self.lbl_helper_text = QLabel(self)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=Box(
                    children=[
                        FormControlLabel(
                            label=label, 
                            # hightLight=True,
                            checked=field.get("value"),
                            control=Checkbox(
                                checked=checked, onChange=self.onChange,
                            )
                        ),
                        self.lbl_helper_text
                    ]
                )

            )
        )

    def onChange(self, value):
        self._value = value
        print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(self._value)

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


class RHFMultiCheckbox(QFrame):
    valueChanged = Signal(object)

    def __init__(
            self,
            row: bool = False,
            name: str = None,
            label: str = None,
            options: object = None,
            spacing: int = None,
            helperText: str = None,
            value: object = None,
            sx: dict = None,
            *other
            ):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self._name = name
        self._value = value
        control = False
        error = False

        self._stateSignal = None

        self.lbl_helper_text = QLabel(self)

        self.multiCheckbox = MultiCheckbox(options=options, value=value, onChange=self._on_change)

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=FormControl(
                    children=[
                        FormLabel(component="legend", label=label or ""),
                        FormGroup(
                            children=[
                                self.multiCheckbox
                            ]
                        ),
                        self.lbl_helper_text
                    ]
                )
            )
        )


    def _set_value(self, value: list):
        for option in self.findChildren(Checkbox):
            option.setChecked(option.text() in value)

    def _on_change(self, value):
        self._value = value
        print(f"Field width name {self._name} has value {self._value}")
        self.valueChanged.emit(value)

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


class RHFMultiCheckboxNew(QWidget):
    def __init__(
            self,
            row: bool = False,
            flowLayout: bool = False,
            name: str = None,
            label: str = None,
            options: object = None,
            spacing: int = None,
            helperText: str = None,
            sx: dict = None,
            *other
            ):
        super().__init__()

        if flowLayout:
            self.flow_layout = FlowLayout(self)
            self.setLayout(self.flow_layout)
        else:
            if row:
                self.setLayout(QHBoxLayout())
            else:
                self.setLayout(QVBoxLayout())

        field = {
            "value": "multi checkbox value"
        }
        control = False
        error = False

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=FormControl(
                    children=[
                        FormLabel(component="legend",  label=label),
                        FormGroup(
                            row=row,
                            # sx={{
                            # ...(row && {
                            #     flexDirection: 'row',
                            # }),
                            # [`& .${formControlLabelClasses.root}`]: {
                            #     '&:not(:last-of-type)': {
                            #     mb: spacing || 0,
                            #     },
                            #     ...(row && {
                            #     mr: 0,
                            #     '&:not(:last-of-type)': {
                            #         mr: spacing || 2,
                            #     },
                            #     }),
                            # },
                            # ...sx,
                            # }}
                            children=[
                                FormControlLabel(
                                    key=option["value"],
                                    control=Checkbox(
                                        checked=option["value"] in field["value"],
                                        onChange=lambda: field.on_change(self.get_selected(field["value"], option["value"]))
                                    ),
                                    label=option["label"],
                                    *other
                                ) for option in options
                            ]
                        ),
                        FormHelperText(error=bool(error), sx={'mx': 0}, children=error.message if error else helperText) if error or helperText else None

                    ]
                )
            )
        )

    def get_selected(self, field_value, option_value):
        pass
