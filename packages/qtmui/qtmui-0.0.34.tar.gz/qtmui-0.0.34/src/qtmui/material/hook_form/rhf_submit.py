from typing import Optional, Union, Callable
from PySide6.QtWidgets import QSizePolicy, QHBoxLayout, QFrame
from PySide6.QtCore import Signal

from qtmui.hooks import State
from qtmui.common.ui_functions import clear_layout

from ..button.button import Button
from ..button.loading_button import LoadingButton
from ..qss_name import *

class SubmitButton(QFrame):
    clicked = Signal()
    def __init__(
            self,
            type: str = "submit",
            loading: Optional[State] = None,
            **kwargs
            ):
        super().__init__()
        self._kwargs = kwargs
        self._type = type
        self._loading = loading
        self._text = self._kwargs.get("text")
        self._onClick = self._kwargs.pop("onClick") if "onClick" in self._kwargs else None
        
        self._initUi()
        
        
    def _initUi(self):

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout().setContentsMargins(0,0,0,0)
        self._loadingButton = LoadingButton(loading=True, onClick=self.__onClick, **self._kwargs)
        # self._kwargs.pop("variant")
        self._button = Button(onClick=self.__onClick, **self._kwargs)
        self.layout().addWidget(self._loadingButton)
        self.layout().addWidget(self._button)
        
        if isinstance(self._loading, State):
            self._loading.valueChanged.connect(self._updateLoading)
            
        self._updateLoading()

    def _updateLoading(self, value=None):
        if isinstance(self._loading, State):
            if self._loading.value:
                self._loadingButton.setVisible(True)
                self._button.setVisible(False)
            else:
                self._loadingButton.setVisible(False)
                self._button.setVisible(True)
                
    def __onClick(self):
        self.clicked.emit()
        if isinstance(self._onClick, Callable):
            self._onClick()
