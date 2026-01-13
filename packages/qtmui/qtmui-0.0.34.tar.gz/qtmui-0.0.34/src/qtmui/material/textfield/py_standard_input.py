import asyncio
import uuid
from typing import Optional, Callable, Any, Dict, Union

from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QGroupBox
from PySide6.QtCore import Signal, Qt, QTimer
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.hooks import State

from .py_input import MuiInput

class MuiStandardInput(MuiInput):

    def __init__(
        self,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
    
    # async def __set_stylesheet(self):
    def _set_stylesheet(self):
        super()._set_stylesheet()
        if not hasattr(self, "theme"):
            self.theme = useTheme()

        MuiStandardInput = self.theme.components["MuiStandardInput"].get("styles")
        MuiStandardInput_root = MuiStandardInput.get("root")
        MuiStandardInput_root_qss = get_qss_style(MuiStandardInput_root)
        MuiStandardInput_root_slot_hovered_qss = get_qss_style(MuiStandardInput_root["slots"]["hover"])
        MuiStandardInput_root_slot_focused_qss = get_qss_style(MuiStandardInput_root["slots"]["focus"])
        
        MuiStandardInput_title = MuiStandardInput.get("title")
        MuiStandardInput_title_qss = get_qss_style(MuiStandardInput_title)

        MuiStandardInput_inputField_root = MuiStandardInput.get("inputField")["root"]
        MuiStandardInput_inputField_root_qss = get_qss_style(MuiStandardInput_inputField_root)

        MuiStandardInput_root_prop_hasStartAdornment_qss = ""
        # MuiStandardInput_root_prop_hasStartAdornment_qss = get_qss_style(MuiStandardInput_inputField_root["props"]["hasStartAdornment"])

        self.setProperty("variant", "standard")

        self.setStyleSheet(
            self.styleSheet() + 
            f"""
                #{self.objectName()}[variant=standard] {{
                    {MuiStandardInput_root_qss}
                }}
                #{self.objectName()}[variant=standard]:title {{
                    {MuiStandardInput_title_qss}
                }}
                #{self.objectName()}[variant=standard]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiStandardInput_inputField_root_qss}
                }}
                #{self.objectName()}[standardHasStartAdornment=true]  QLineEdit, QPlainTextEdit, QTextEdit {{
                    {MuiStandardInput_root_prop_hasStartAdornment_qss}
                }}
                #{self.objectName()}[hovered=true] {{
                    {MuiStandardInput_root_slot_hovered_qss}
                }}
                #{self.objectName()}[focused=true] {{
                    {MuiStandardInput_root_slot_focused_qss}
                }}
            """
        )

    def _set_prop_has_start_adornment(self, state:bool):
        self.setProperty("standardHasStartAdornment", state)
        self._set_stylesheet()

