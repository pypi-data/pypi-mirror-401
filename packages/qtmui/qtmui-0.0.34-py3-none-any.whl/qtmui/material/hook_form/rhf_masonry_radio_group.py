from typing import Callable, Optional, Union
import uuid
from PySide6.QtWidgets import QWidget, QVBoxLayout

from qtmui.hooks import State
from ...material.masonry.masonry import Masonry

from ..controller import Controller
from ..form_control_label import FormControlLabel
from ..box import Box
from ..form_control import FormControl
from ..form_label import FormLabel
from ..radio import  Radio
from ..radio_group import RadioGroup

from ..qss_name import *

class RHFMasonryRadioGroup(QWidget):
    def __init__(
            self,
            name,
            id: str = None,
            value: object = None,
            row: str = "row",
            columns: int = None,
            checked: bool = False,
            isVisible: bool = False,
            label: Optional[Union[str, State, Callable]]=None,
            options: object = None,
            spacing: int = None,
            minWidth: int = None,
            helperText: str = None,
            color: str = "primary",
            isOptionEqualToValue: Optional[Callable] = lambda checked: False,
            ):
        super().__init__()
        self.setLayout(QVBoxLayout())
        # self.layout().setContentsMargins(0,0,0,0)
        self.setMinimumWidth(400)

        self._id = id
        self._name = name
        self._value = value

        self._isVisible = isVisible
        self._selected = False

        if self._id is not None:
            self.setObjectName(id)
        else:
            self.setObjectName(str(uuid.uuid4()))

        self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), "border: none;background: #ffeaa7;")) # str multi line

        self._row = row
        self._columns = columns
        self._options = options

        self._color = color

        # if isOptionEqualToValue:
        #     self._isOptionEqualToValue = isOptionEqualToValue
        # else:
        #     self._isOptionEqualToValue = lambda checked=False: checked

        self._isOptionEqualToValue = isOptionEqualToValue

        self._stateSignal = None

        field = {}
        control = False
        error = False


        if self._columns is None:
            self._columns = len(options)

        self._labelledby = f"{label}"  if label else ""

        if minWidth:
            self.setMinimumWidth(minWidth)

        self.layout().addWidget(
            Controller(
                control=control,
                render=FormControl(
                    component="fieldset",
                    children=[
                        Box(
                            direction="column",
                            children=[
                                FormLabel(component="legend",  label=label),
                                self.renderRadioGroup(),
                                # FormHelperText(error=error.get("message") if error and hasattr(error, 'message') else helperText)
                            ]
                        )
                    ]
                )
            )
        )

        self.setup_ui()


    def setup_ui(self):
        for item in self._radio_group.findChildren(Radio):
            # item.toggled.connect(lambda checked, value=item._value: self.set_value(value))
            if not item.checked:
                self._value = item._value
                break

        if isinstance(self._isVisible, State):
            self._isVisible.valueChanged.connect(self._set_visible)
            self._selected = self._isVisible.value
            self._set_hide(self._selected)
        else:
            self._selected = self._isVisible
            self._set_hide(self._selected)

    def renderRadioGroup(self):
        self._radio_group = RadioGroup(
            direction="column",
            # hightLight=True,
            ariaLabelledby=self._labelledby,
            row=self._row,
            children=[
                Masonry(
                    # hightLight=True,
                    columns=self._columns,
                    children=[
                        FormControlLabel(
                            # hightLight=True,
                            labelPlacement="end",
                            key=option["value"],
                            value=option["value"],
                            label=option["label"],
                            fullWidth=False,
                            control=Radio(text=option["label"], value=option["value"], color=self._color,  checked=self._isOptionEqualToValue(option)),
                            # label=option["label"],
                            # sx={
                            #     '&:not(:last-of-type)': {
                            #         mb: spacing || 0,
                            #     },
                            #     ...(row && {
                            #         mr: 0,
                            #         '&:not(:last-of-type)': {
                            #         mr: spacing || 2,
                            #         },
                            #     }),
                            # }
                        ) for option in self._options
                    ]
                ) 
            ]
        )
        self.valueChanged = self._radio_group.valueChanged
        self.valueChanged.connect(self.set_value)

        return self._radio_group

    def _set_hide(self, state):
        self._selected = state
        if not state:
            self.hide()

    def _set_visible(self, state):
        self._selected = state
        if state:
            if not self.isVisible():
                print('show___________________________')
                self.show()
        else:
            if self.isVisible():
                print('hide___________________________')
                self.hide()

    def set_value(self, value):
        self._value = value


    # def showEvent(self, event):
    #     self.valueChanged.emit(self._value)