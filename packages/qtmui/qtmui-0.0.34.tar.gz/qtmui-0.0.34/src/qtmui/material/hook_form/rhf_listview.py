from typing import Any, Callable
import uuid
from PySide6.QtWidgets import QLabel
from qtmui.material.section import Section
from ...common.ui_functions import clear_layout
from ..qss_name import *

# from ...material._common.widget_model import WidgetModel
from ...material.box import Box

from ...material.typography.typography import Typography

from ..qss_name import *
from qtmui.material.styles import useTheme


class RHFListView(Section):

    def __init__(
            self,
            name: str,
            compornent: object = None,
            renderProps: Callable = None,
            minimumWidth: int=None,
            model: Any = None,
            onItemClicked: Callable = None,
        ):
        super().__init__()

        self._value = []
        self._name = name
        self._compornent = compornent
        self._renderProps = renderProps
        self._minimumWidth = minimumWidth

        self._model = model
        self._onItemClicked = onItemClicked

        self._stateSignal = None

        if self._minimumWidth:
            self.setMinimumWidth(self._minimumWidth)

        if self._model is not None:
            self._model.dataChanged.connect(self.render_ui)
            self.render_ui()

    def render_compornent(self, config):
        return config.get("compornent")(**config.get("kwargs"))

    def render_ui(self):
        clear_layout(self.layout())
        # lambda config=item: self._renderProps(config)
        self.layout().addWidget(Typography(text="Selected: 0"))

        self._value = []
        for item in self._model.data:
            self._value.append(item.get("value"))


        self.lbl_helper_text = QLabel(self)
        self.lbl_helper_text.setStyleSheet('padding-left: 8px;')
        self.lbl_helper_text.setText("")

        self.add_widget(Box(
            children=[
                self._compornent(**self._renderProps(item))
                for item in self._model.data
            ]
        ))
        self.layout().addWidget(self.lbl_helper_text)


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