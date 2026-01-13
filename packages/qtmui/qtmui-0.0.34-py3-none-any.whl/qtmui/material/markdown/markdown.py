# qtmui/material/masonry.py
import asyncio
from typing import Optional, Union, Dict, Callable
import uuid

from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from qtmui.hooks import State
from ...common.ui_functions import clear_layout
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class Markdown(QFrame, PyWidgetBase):

    def __init__(
        self,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))  # Gán objectName trước khi gọi set_sx
        PyWidgetBase._setUpUi(self)
