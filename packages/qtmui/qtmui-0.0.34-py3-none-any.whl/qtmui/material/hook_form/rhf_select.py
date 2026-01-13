import uuid
from typing import Callable, Optional, Sequence, Union

from PySide6.QtCore import Property, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qtmui.hooks import useState

from qtmui.material.styles import useTheme
from qtmui.hooks import State

from ..controller import Controller
from ..textfield import TextField
from ..form_control import FormControl
from ..select import Select
from ..box import Box
from ..chip import Chip


from ..qss_name import *

class RHFSelect(QWidget):
    valueChanged = Signal(object)

    def __init__(
            self,
            name: str,
            label: Optional[Union[str, State, Callable]]=None,
            native: bool = None,
            maxHeight: int = 220,
            onChange: Optional[Callable] = None,
            PaperPropsSx: object = None,
            helperText: str = None,
            children: object = None,
            selected: bool = False,
            **kwargs
            ):
        super().__init__()

        self._name = name
        self._label = label
        self._native = native
        self._maxHeight = maxHeight
        self._onChange = onChange
        self._children = children
        self._PaperPropsSx = PaperPropsSx
        self._helperText = helperText
        self._selected = selected
        self._value = None

        self._state, self._setState = useState(None)


        self.setLayout(QVBoxLayout())
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet("background: green;") # str multi line
        control = False
        error = {}

        self._stateSignal = None

        self._select = Select(
            name=self._name,
            # selected=self._selected,
            onChange=lambda newValue:
                self.set_value(newValue)
            ,
            label=self._label,
            children=children,
            **kwargs
        )

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=self._select
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


    def set_value(self, value=None):
        self._value = value
        if self._value == []:
            self._value = None
        # print(f"RHFAutocomplete {self._name}: {self._value}")
        if isinstance(self._selected, State):
            self._selected.value = True

        if self._onChange:
            self._onChange(value)
        self.valueChanged.emit(value)

        self._select._inputField._set_value(value=self._value, valueChanged=False)
        
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
                self._select._inputField._set_slot({"slot": "error", "message": state.get("error_message")})
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
                self._select._inputField._set_slot({"slot": "valid"})
                self.lbl_helper_text.hide()


class RHFMultiSelect(QWidget):
    def __init__(
            self,
            name: str = None,
            chip: object = None,
            label: str = None,
            options: object = None,
            checkbox: object = None,
            placeholder: str = None,
            helperText: str = None,
            sx: dict = None
            ):
        super().__init__()
        self.setLayout(QVBoxLayout())
        # self.layout().setContentsMargins(0,0,0,0)
        self.setObjectName(str(uuid.uuid4()))
        # self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "background: green;")) # str multi line
        self.setStyleSheet("background: green;") # str multi line

        control = False
        error = {
            "message": "ksjdkl"
        }
        field = {
            "value": "option 1"
        }

        self.layout().addWidget(
            Controller(
                name=name,
                control=control,
                render=FormControl(
                    sx=sx,
                    children=[
                        # InputLabel(label=label) if label else None,
                        # Select(
                        #     # **field,
                        #     multiple=True,
                        #     displayEmpty=not placeholder,
                        #     labelId=name,
                        #     input=OutlinedInput(fullWidth=True, select=True, label=label, error=not error),
                        #     renderValue=self.render_values,
                        #     children=[
                        #         MenuItem(enabled=False, value="", children=[QLabel('nnnnnnnnnnnnnnnnnnnnnnnnnnnn')]), # Typography(text=placeholder, variant="h6")
                        #         *[
                        #             MenuItem(
                        #                 text=option["label"],
                        #                 key=option["value"], 
                        #                 value=option["value"], 
                        #                 children=[
                        #                     Checkbox(size="small", disableRipple=True, checked=option["value"] in field["value"]) 
                        #                 ]
                        #             ) for option in options
                        #         ]
                        #     ]
                        # ),
                        # FormHelperText(error=error.get("message") if error and hasattr(error, 'message') else helperText)
                    ]
                ),
            )
        )

    def render_values(self, selected_ids, options, placeholder=None, chip=False):
        selected_items = [item for item in options if item['value'] in selected_ids]

        if not selected_items and placeholder:
            return Box(component='em', children=[QLabel(placeholder)])

        if chip:
            chips = []
            for item in selected_items:
                chips.append(Chip(item['label']))
            return Box(children=chips)

        return ', '.join(item['label'] for item in selected_items)
