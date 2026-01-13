import asyncio
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QGroupBox
from PySide6.QtCore import Signal, Qt, QTimer
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.hooks import State

from .py_input import MuiInput

class MuiFilledInput(MuiInput):

    def __init__(
        self,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        if kwargs.get("size"):
            self._size = kwargs.get("size")

        if kwargs.get("InputProps"):
            self._InputProps = kwargs.get("InputProps")
    
    def _set_stylesheet(self):
        super()._set_stylesheet()
        if not hasattr(self, "theme"):
            self.theme = useTheme()

        MuiFilledInput = self.theme.components["MuiFilledInput"].get("styles")
        MuiFilledInput_root = MuiFilledInput.get("root")
        MuiFilledInput_root_qss = get_qss_style(MuiFilledInput_root)
        MuiFilledInput_root_slot_hovered_qss = get_qss_style(MuiFilledInput_root["slots"]["hover"])
        MuiFilledInput_root_slot_focused_qss = get_qss_style(MuiFilledInput_root["slots"]["focus"])
        
        MuiFilledInput_title = MuiFilledInput.get("title")
        MuiFilledInput_title_qss = get_qss_style(MuiFilledInput_title)
        MuiFilledInput_title_prop_hasStartAdornment_qss = get_qss_style(MuiFilledInput_title["props"]["hasStartAdornment"])

        MuiFilledInput_inputField_root = MuiFilledInput.get("inputField")["root"]
        MuiFilledInput_inputField_root_qss = get_qss_style(MuiFilledInput_inputField_root)
        MuiFilledInput_inputField_root_prop_hasValue_qss = get_qss_style(MuiFilledInput_inputField_root["props"]["hasValue"][f"{self._size}"])
        MuiFilledInput_root_prop_hasStartAdornment_qss = get_qss_style(MuiFilledInput_inputField_root["props"]["hasStartAdornment"])

        self.setProperty("variant", "filled")

        self.setStyleSheet(
            self.styleSheet() + 
            f"""
                #{self.objectName()}[variant=filled] {{
                    {MuiFilledInput_root_qss}
                }}
                #{self.objectName()}[variant=filled]:title {{
                    {MuiFilledInput_title_qss}
                }}
                #{self.objectName()}[hasStartAdornment=true]:title  {{
                    {MuiFilledInput_title_prop_hasStartAdornment_qss}
                }}
                #{self.objectName()}[variant=filled] QLineEdit, QPlainTextEdit, QTextEdit  {{
                    {MuiFilledInput_inputField_root_qss}
                }}
                #{self.objectName()}[hasStartAdornment=true] QLineEdit, QPlainTextEdit, QTextEdit  {{
                    {MuiFilledInput_root_prop_hasStartAdornment_qss}
                }}

                #{self.objectName()}[filledHasValue=true] QLineEdit, QPlainTextEdit, QTextEdit  {{
                    {MuiFilledInput_inputField_root_prop_hasValue_qss}
                }}
                #{self.objectName()}[hovered=true] {{
                    {MuiFilledInput_root_slot_hovered_qss}
                }}
                #{self.objectName()}[focused=true] {{
                    {MuiFilledInput_root_slot_focused_qss}
                }}
            """
        )

    def _set_filled_has_value_prop(self, state:bool):
        self.setProperty("filledHasValue", state)
        self._set_stylesheet()

    def _set_filled_foucusin_prop(self, state:bool):
        self.setProperty("filledHasValue", state)
        self._set_stylesheet()

    def _set_prop_has_start_adornment(self, state:bool):
        self.setProperty("hasStartAdornment", state)
        self._set_stylesheet()

        
