import asyncio
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QGroupBox
from PySide6.QtCore import Signal, Qt, QTimer
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.hooks import State

from .py_input import MuiInput

class MuiOutlinedInput(MuiInput):

    def __init__(
        self,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

    
    def _set_stylesheet(self):
        super()._set_stylesheet()
        if not hasattr(self, "theme"):
            self.theme = useTheme()

        MuiOutlinedInput = self.theme.components["MuiOutlinedInput"].get("styles")
        MuiOutlinedInput_root = MuiOutlinedInput.get("root")
        MuiOutlinedInput_root_qss = get_qss_style(MuiOutlinedInput_root)
        MuiOutlinedInput_root_slot_hovered_qss = get_qss_style(MuiOutlinedInput_root["slots"]["hover"])
        MuiOutlinedInput_root_slot_focused_qss = get_qss_style(MuiOutlinedInput_root["slots"]["focus"])
        
        MuiOutlinedInput_inputField_root = MuiOutlinedInput.get("inputField")["root"]
        MuiOutlinedInput_inputField_root_qss = get_qss_style(MuiOutlinedInput_inputField_root)

        MuiOutlinedInput_root_prop_hasStartAdornment_qss = get_qss_style(MuiOutlinedInput_inputField_root["props"]["hasStartAdornment"])


        self.setProperty("variant", "outlined")


        self.setStyleSheet(
            self.styleSheet() + 
            f"""
                #{self.objectName()}[variant=outlined] {{
                    {MuiOutlinedInput_root_qss}
                }}
                #{self.objectName()}[variant=outlined]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiOutlinedInput_inputField_root_qss}
                }}
                #{self.objectName()}[outlinedHasStartAdornment=true]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiOutlinedInput_root_prop_hasStartAdornment_qss}
                }}
                #{self.objectName()}[hovered=true] {{
                    {MuiOutlinedInput_root_slot_hovered_qss}
                }}
                #{self.objectName()}[focused=true] {{
                    {MuiOutlinedInput_root_slot_focused_qss}
                }}
            """
        )


    def _set_prop_has_start_adornment(self, state:bool):
        self.setProperty("outlinedHasStartAdornment", state)
        self._set_stylesheet()

        
