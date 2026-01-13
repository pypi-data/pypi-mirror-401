from typing import Callable, Optional, Union
import uuid
from PySide6.QtCore import Qt, Property, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel, QHBoxLayout, QFrame

from qtmui.hooks import State

from ..autocomplete.complete import Autocomplete
from qtmui.material.styles import useTheme

from ..qss_name import *

class RHFAutocompleteGroup(QWidget):
    def __init__(
            self,
            label: Optional[Union[str, State, Callable]]=None,
            name: str = None,
            value: object = None,
            onValueChanged: Callable = None,
            direction: str = "row",
            children: list = None,
            ):
        super().__init__()
        
        

        self._name = name
        self._value = value
        self._onValueChanged = onValueChanged

        self._stateSignal = None

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self.frm_content = QFrame()
        
        if direction == "row":
            self.lo_frm_content = QHBoxLayout(self.frm_content)
        else: # column
            self.lo_frm_content = QVBoxLayout(self.frm_content)

        self.lo_frm_content.setContentsMargins(0,0,0,0)

        if children is not None:
            if isinstance(children, list):
                for item in children:
                    self.lo_frm_content.addWidget(item)

        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setFixedHeight(14)
        self.lbl_helper_text.setStyleSheet('padding-left: 8px;')
        self.lbl_helper_text.setText("")
        self.layout().addWidget(self.frm_content)
        self.layout().addWidget(self.lbl_helper_text)

        self.setup_ui()

    def setup_ui(self):
        # kiểm tra selected của các RHFAutocomplete, thông báo lỗi nếu tìm thấy có nhiều hơn 1 field có trường này == True
        selected_item_count = 0
        for item in self.findChildren(Autocomplete):
            item.valueChanged.connect(lambda value, item_name=item.objectName(): self._onValueChanged(item_name))
            item.valueChanged.connect(lambda value, item=item: self.on_fields_value_changed(value, item))
            if item._selected:
                self._value = item._value
                selected_item_count += 1
            else:
                item._value = None
                
        # xem lai
        # if selected_item_count > 1:
        #     raise AttributeError("Only one child element of RHFAutocompleteGroup is allowed to have the attribute selected set to True.")
        # if selected_item_count == 0:
        #     raise AttributeError("At least one AutoComplete must have the selected attribute set to True.")

    def unselected_all_field(self):
        for item in self.findChildren(Autocomplete):
            item.selected = False

    def on_fields_value_changed(self, value, item):
        print('item____________',value,  item)
        self._value = value
        self.unselected_all_field()
        item.selected = True

    def set_value(self, value):
        print('show_even  ===> set_value')
        self._value = value

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
                self.set_state({"status": "invalid", "message": state.get("error_message")})
                self.lbl_helper_text.setText(str(state.get("error_message")))
                self.lbl_helper_text.setStyleSheet(f'padding-left: 8px;color: {theme.palette.error.main};')