from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Property, Slot

from ...material._common.widget_model import WidgetModel
from qtmui.material.styles import useTheme

from ..qss_name import *

class RHFHidden(QWidget):
    def __init__(
            self,
            name: str,
            id: str = None,
            model: WidgetModel = None,
            helperText: str = "",
            ):
        super().__init__()
        if id is not None:
            self.setObjectName(id)

        self._name = name
        self._model = model
        self._value = None

        if self._model is not None:
            self._value = model.data
            self._model.dataChanged.connect(self.on_model_data_changed)

        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setText(helperText)
        self.lbl_helper_text.setStyleSheet(f"padding-left: 8px;color: {useTheme().palette.text.primary}")
        self.lbl_helper_text.setText("")
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(self.lbl_helper_text)

    def on_model_data_changed(self):
        self._value = self._model.data
        print(f"Field width name {self._name} has value {self._value}")

    def set_value(self, value=None):
        self._value = value
        print(f"Field width name {self._name} has value {self._value}")

    def set_helper_text(self, text):
        self.lbl_helper_text.setText(text)
        self.lbl_helper_text.setStyleSheet(f"padding-left: 8px;color: {useTheme().palette.text.primary}")

    def set_error_text(self, text):
        self.lbl_helper_text.setText(text)
        self.lbl_helper_text.setStyleSheet(f"padding-left: 8px;color: {useTheme().palette.text.error}")

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
                self.set_error_text(str(state.get("message")))