from typing import Callable, Optional, Union
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Qt

from qtmui.hooks import State
from .button import Button
# from .arc_widget import ArcWidget
from .loading_icon import LoadingIcon
from ..py_svg_widget import PySvgWidget

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

class LoadingButton(Button):
    """
    LoadingButton
    Base Button

    Args:
        loading?: True | False
        loadingPosition?: "start" | "center" | "end"
        loadingIndicator?: "Loading..." | any str

    Returns:
        new instance of LoadingButton
    """
    def __init__(self,
                type: str = None,
                loading: bool = False,
                loadingPosition: str = "start",
                loadingIndicator: Optional[Union[str, State, Callable]] = None,
                color: str = None,
                 *args, **kwargs):
        if loading:
            super().__init__(disabled=True, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)

        self._type = type
        self._loading = loading
        self._loadingPosition = loadingPosition
        self._loadingIndicator = loadingIndicator

        self._init_ui()

    def _init_ui(self):

        if self._loading:
            # Tạo layout để quản lý icon và text
            self.hbox = QHBoxLayout(self)
            self.hbox.setContentsMargins(0, 0, 0, 0)
            self.hbox.setSpacing(5)  # Khoảng cách giữa icon và text
            self.setLayout(self.hbox)

            if self._loadingIndicator is not None:
                self.setText(self._loadingIndicator)
            else:
                # self.setLayout(QHBoxLayout())
                # self.layout().setContentsMargins(0,0,0,0)
                self.loadingSvgWidget = PySvgWidget(key="eos-icons:loading")

                # if self._loadingPosition == "start":
                #     self.layout().addWidget(self.loadingSvgWidget, alignment=Qt.AlignLeft)
                # else:
                #     self.layout().addWidget(self.loadingSvgWidget, alignment=Qt.AlignRight)
                #     # self.setLayoutDirection(Qt.RightToLeft)

                if self._loadingPosition == "start":
                    self.hbox.addWidget(self.loadingSvgWidget, alignment=Qt.AlignLeft)
                    self.hbox.addStretch()
                    self.hbox.addWidget(self)
                elif self._loadingPosition == "end":
                    self.hbox.addWidget(self)
                    self.hbox.addStretch()
                    self.hbox.addWidget(self.loadingSvgWidget, alignment=Qt.AlignRight)

        theme = useTheme()
        theme.state.valueChanged.connect(self.__set_stylesheet)
        self.__set_stylesheet()

    def __set_stylesheet(self, _theme=None):
        self.theme = useTheme()
        component_styles = self.theme.components

        ownerState = {
            "size": self._size
        }
        PyLoadingButton_root = component_styles["PyLoadingButton"].get("styles")["root"](ownerState)
        PyLoadingButton_root_prop_softVariant_loadingIndicatorStart_left = PyLoadingButton_root["props"]["softVariant"]["loadingIndicatorStart"]["left"]
        PyLoadingButton_root_prop_softVariant_loadingIndicatorEnd_right = PyLoadingButton_root["props"]["softVariant"]["loadingIndicatorEnd"]["right"]
        PyLoadingButton_root_prop_smallSize_loadingIndicatorStart_left = PyLoadingButton_root["props"]["smallSize"]["loadingIndicatorStart"]["left"]
        PyLoadingButton_root_prop_smallSize_loadingIndicatorEnd_right = PyLoadingButton_root["props"]["smallSize"]["loadingIndicatorEnd"]["right"]
