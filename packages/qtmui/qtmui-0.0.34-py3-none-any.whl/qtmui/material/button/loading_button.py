import asyncio
import uuid
from typing import Optional, Union, Callable, Dict
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtWidgets import QHBoxLayout, QFrame
from .button import Button
# from .arc_widget import ArcWidget
# from .loading_icon import LoadingIcon
from qtmui.hooks import State
from functools import lru_cache

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n

from ..py_svg_widget import PySvgWidget
from ..typography import Typography

class LoadingButton(QFrame):
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
    def __init__(
                self,
                loading: Optional[State] = None,
                loadingPosition: str = "start",
                loadingIndicator: Optional[Union[str, State, Callable]] = None,
                color: str = "primary",
                variant: str = "contained",
                size: str = "medium",
                sx: Optional[Union[State, Callable, str, Dict]] = None,
                **kwargs
                ):
        super().__init__()
        self.setObjectName(f"LoadingButton_{str(uuid.uuid4())}")
        
        self._kwargs = kwargs
        
        self._text = self._kwargs.get("text")
        
        self._variant = variant
        self._size = size   
        self._color = color
        self._sx = sx
        

        self._loading = loading
        self._loadingPosition = loadingPosition
        self._loadingIndicator = loadingIndicator
        
        # self.loadingWidget = PySvgWidget(key="line-md:loading-loop", color="#555555")
        self.loadingWidget = PySvgWidget(key="eos-icons:loading", color="palette.grey._500")
        self.label = Typography(text=self._text or self._loadingIndicator, variant="button", sx={"color": "palette.text.disabled"})

        self._init_ui()
        
    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.loadingWidget)
        self.connectSignalSlot()
        self._update_loading()

        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        self._set_stylesheet()
        
        self.destroyed.connect(lambda obj: self._onDestroy())

    def _onDestroy(self, obj=None):
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_set_stylesheet())

    async def _lazy_set_stylesheet(self):
        self._set_stylesheet()

    def connectSignalSlot(self):
        if isinstance(self._loading, State):
            self._loading.valueChanged.connect(self._update_loading)

    def _update_loading(self, value=None):
        if isinstance(self._loading, State):
            if self._loading.value:
                if self._loadingPosition == "start":
                    self.layout().insertWidget(0, self.loadingWidget)
                else: # end
                    self.layout().insertWidget(1, self.loadingWidget)
                self.loadingWidget.setVisible(True)
            else:
                self.loadingWidget.setVisible(False)
        else:
            if self._loading:
                if self._loadingPosition == "start":
                    self.layout().insertWidget(0, self.loadingWidget)
                else: # end
                    self.layout().insertWidget(1, self.loadingWidget)
                self.loadingWidget.setVisible(True)
            else:
                self.loadingWidget.setVisible(False)

    @classmethod
    @lru_cache(maxsize=128)
    def _get_stylesheet(cls, _variant: str, _size: str, _color: str, _theme_mode: str):
        theme = useTheme()
        MuiButton_root = theme.components["MuiButton"].get("styles")["root"]
        MuiButton_root_size_qss = get_qss_style(MuiButton_root["size"]({})[_size])
        MuiButton_root_size_textVariant_qss = get_qss_style(MuiButton_root["size"]({})[_size]["textVariant"])
        MuiButton_root_colorStyle_prop_variant_qss = get_qss_style(
            MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]
        )
        MuiButton_root_colorStyle_prop_variant_slot_hover_qss = get_qss_style(
            MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]["slots"]["hover"]
        )
        MuiButton_root_colorStyle_prop_variant_slot_checked_qss = get_qss_style(
            MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]["slots"]["checked"]
        )

        _________object_name_______ = "_________object_name_______"

        stylesheet = f"""
            #{_________object_name_______}{{
                {MuiButton_root_size_qss}
                {MuiButton_root_size_textVariant_qss}
                {MuiButton_root_colorStyle_prop_variant_qss}
            }}
            #{_________object_name_______}:hover {{
                {MuiButton_root_colorStyle_prop_variant_slot_hover_qss}
            }}
            #{_________object_name_______}[selected=true] {{
                {MuiButton_root_colorStyle_prop_variant_slot_checked_qss}
            }}
        """

        return stylesheet

    def _set_stylesheet(self, component_styled=None):
        _theme_mode = useTheme().palette.mode
        self.setProperty("variant", self._variant)
        if self._color == "inherit":
            self._color = "default"

        self._variant = self._variant.replace("Extended", "").replace("extended", "contained")

        stylesheet = ""
        # stylesheet = self._get_stylesheet(self._variant, self._size, self._color, _theme_mode)
        stylesheet = stylesheet.replace("_________object_name_______", self.objectName())
        sx_qss = ""

        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        self.setStyleSheet(stylesheet + sx_qss)