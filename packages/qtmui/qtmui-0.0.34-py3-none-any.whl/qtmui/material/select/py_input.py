import asyncio
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QGroupBox
from PySide6.QtCore import QTimer
from qtmui.i18n.use_translation import i18n, translate 
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.hooks import State

class MuiInput(QGroupBox):

    def __init__(
        self,
        disabled: Optional[Union[State, str]] = False,
        label: Optional[Union[State, str]] = False,
        hiddenLabel: bool = False,
        focused: Optional[Union[State, bool]] = False,
        hovered: Optional[Union[State, bool]] = False,
        children: Optional[list] = None,
        multiple: bool = False,
        multiline: bool = False,
        renderTags: Optional[Callable] = None,
        size: Optional[Union[str]] = "medium",
        sx: Optional[Union[Dict, Callable, str]] = None,  # Hỗ trợ định nghĩa ghi đè hệ thống cũng như các kiểu CSS bổ sung.
        value: Optional[Union[State, object]] = None,
        **kwargs
    ):
        super().__init__()
        
        self._children = children
        self._disabled = disabled
        self._multiple = multiple
        self._multiline = multiline
        self._renderTags = renderTags
        self._hovered = hovered
        self._hiddenLabel = hiddenLabel
        self._focused = focused
        self._label = label
        self._size = size
        self._sx = sx
        self._value = value
        self._init_ui()
        
    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        if not self._hiddenLabel:
            if isinstance(self._label, State):
                self._label.valueChanged.connect(self._set_translated_label)
            # self._set_translated_label()

        if isinstance(self._hovered, State):
            self._hovered.valueChanged.connect(self._set_hovered_prop)
        self._set_hovered_prop()
        
        if isinstance(self._focused, State):
            self._focused.valueChanged.connect(self._set_focused_prop)
        self._set_focused_prop()
        
        if isinstance(self._children, list):
            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(0,0,0,0)
            for widget in self._children:
                self.layout().addWidget(widget)


        i18n.langChanged.connect(self._set_translated_label)
        self.theme = useTheme()

        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        self._set_stylesheet()
        
        self.destroyed.connect(lambda obj: self._onDestroy())
        

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
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


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        if self._disabled:
            self.setProperty("disabled", True)

        MuiInput = component_styled["MuiInput"].get("styles")
        MuiInput_root = MuiInput.get("root")
        MuiInput_root_qss = get_qss_style(MuiInput_root)
        MuiInput_title = MuiInput.get("title")
        MuiInput_title_qss = get_qss_style(MuiInput_title)
        MuiInput_title_slot_focused_qss = get_qss_style(MuiInput_title["slots"]["focused"])
        MuiInput_title_slot_error_qss = get_qss_style(MuiInput_title["slots"]["error"])
        MuiInput_title_slot_disabled_qss = get_qss_style(MuiInput_title["slots"]["disabled"])
        MuiInput_inputField = MuiInput.get("inputField")
        MuiInput_inputField_qss = get_qss_style(MuiInput_inputField)
        MuiInput_inputField_prop_multiline_qss = get_qss_style(MuiInput_inputField["props"]["multiline"][f"{self._size}"])
        MuiInput_inputField_prop_multiple_qss = get_qss_style(MuiInput_inputField["props"]["multiple"])

        MuiInputSize = component_styled["MuiInputSize"]["styles"][f"{self._size}"]
        MuiInputSize_qss = get_qss_style(MuiInputSize)


        # MuiInputSize_not_multiline_qss = ""
        # if not self._multiline:
        #     MuiInputSize_not_multiline = MuiInputSize["notMultiline"]
        #     MuiInputSize_not_multiline_qss = get_qss_style(MuiInputSize_not_multiline)

        MuiInputSize_not_multiple_qss = get_qss_style(MuiInputSize["no-multiple"])
        MuiInputSize_no_multiple_height = MuiInputSize["no-multiple"]["height"]

        if (self._multiple and self._renderTags) or self._multiline:
            self.setMinimumHeight(MuiInputSize_no_multiple_height) # nếu setfixed (min-height, max-height) thì không tự giãn chiều

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

        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {MuiInput_root_qss}
                    {MuiInputSize_qss}
                    {MuiInputSize_not_multiple_qss if not (self._multiple and self._renderTags) and not self._multiline else ""}
                }}

                #{self.objectName()} QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox,
                QLineEdit, PyPlainTextEdit, QSpinBox, QTextEdit, QTimeEdit {{
                    {MuiInput_inputField_qss}
                }}
                #{self.objectName()}[multipleHasValue=true] QPlainTextEdit {{
                    {MuiInput_inputField_prop_multiple_qss}
                }}
                #{self.objectName()} PyPlainTextEdit, QTextEdit{{
                    {MuiInput_inputField_prop_multiline_qss}
                }}
                #{self.objectName()} QPlainTextEdit{{
                    min-height: 40px;
                }}
                #{self.objectName()}::title {{
                    {MuiInput_title_qss}
                }}
                #{self.objectName()}[focused=true]::title {{
                    {MuiInput_title_slot_focused_qss}
                }}
                #{self.objectName()}[error=true]::title {{
                    {MuiInput_title_slot_error_qss}
                }}
                #{self.objectName()}[disabled=true]::title {{
                    {MuiInput_title_slot_disabled_qss}
                }}

                {sx_qss}
            """
        )


    def _show_label(self):
        if not self._hiddenLabel:
            self._set_translated_label()

    def _set_translated_label(self):
        if not self._hiddenLabel:
            if isinstance(self._label, State):
                if isinstance(self._label.value, Callable):
                    self.setTitle(translate(self._label.value))
                elif isinstance(self._label.value, str):
                    self.setTitle(self._label.value)
            elif isinstance(self._label, str):
                self.setTitle(self._label)

    def _hide_label(self):
        self.setTitle("")

    def _set_hovered_prop(self):
        if self._disabled:
            return
        if isinstance(self._hovered, State):
            self.setProperty("hovered", self._hovered.value)
        elif isinstance(self._hovered, bool):
            self.setProperty("hovered", self._hovered)
        self.slot_set_stylesheet()
        
    def _set_focused_prop(self):
        if isinstance(self._focused, State):
            self.setProperty("focused", self._focused.value)
        elif isinstance(self._focused, bool):
            self.setProperty("focused", self._focused)
        self.slot_set_stylesheet()
        
    def _set_multiple_has_value_prop(self, state):
        # print('_set_multiple_has_value_prop_____________')
        self.setProperty("multipleHasValue", state)
        self.slot_set_stylesheet()
        
