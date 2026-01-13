# qtmui/material/scrollbar.py
import uuid
from typing import Callable, Optional, Union, Dict

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QWidget, QScrollArea, QSizePolicy, QApplication, QLabel
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QEvent

from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..system.color_manipulator import alpha
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase

from ..utils.validate_params import _validate_param

class Scrollbar(QScrollArea, PyWidgetBase):
    """
    Demos:
    - Container: https://qtmui.com/material-ui/react-scrollbar/

    API Reference:
    - Container API: https://qtmui.com/material-ui/api/scrollbar/
    """

    def __init__(
        self,
        children: Optional[Union[State, list]] = None,         # List of child elements (only accepts State or list)
        sx: Optional[Union[State, Callable, str, Dict]] = None,  # Custom styles
    ):
        super().__init__()

        # Assign values to properties
        self._set_children(children)
        self._set_sx(sx)

        PyWidgetBase._setup_sx_position(self)
        PyWidgetBase._handle_float_and_percent_sx_value(self)

        self._init_ui()

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    @_validate_param(file_path="qtmui.material.scrollbar", param_name="children", supported_signatures=Union[State, list, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.scrollbar", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value to sx and handle width/height in percentage or 0-1 range."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value and process width/height if in percentage or 0-1 range."""
        sx = self._sx.value if isinstance(self._sx, State) else self._sx
        if isinstance(sx, Callable):
            sx = sx()
        if not isinstance(sx, dict):
            return sx

        # Convert sx to dict and pop width/height if they are in 0-1 range or percentage
        sx_dict = dict(sx)
        width = sx_dict.pop("width", None) # pop
        height = sx_dict.pop("height", None) # pop

        # Store width/height for later use in _apply_dimensions_from_sx
        self._sx_width = width
        self._sx_height = height

        return sx_dict


    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWidgetResizable(True)
        self.contentBox = QWidget()
        self.contentBox.setObjectName(str(uuid.uuid4()))
        self.contentBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.vlayout = QVBoxLayout(self.contentBox)
        self.vlayout.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.vlayout.setContentsMargins(0, 0, 0, 0)

        self.setWidget(self.contentBox)

        children = self._get_children()
        if isinstance(children, list) and len(children) > 0:
            for widget in children:
                if widget is not None:
                    self.vlayout.addWidget(widget)

    def _on_destroyed(self):
        """Disconnect signals when the object is destroyed."""
        try:
            self.theme.state.valueChanged.disconnect(self.slot_set_stylesheet)
        except TypeError:
            pass

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        sx_qss = ""
        if self._sx:
            sx = self._get_sx()
            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        stylesheet = f"""

            QScrollBar:horizontal {{
                border: none;
                background: transparent;
                height: 8px;
                margin: 0px 21px 0 21px;
                border-radius: 0px;
            }}

            QScrollBar::handle:horizontal {{
                background: {alpha(self.theme.palette.grey._500, 0.32)};
                min-width: 25px;
                border-radius: 2px;
                margin-bottom: 2px;
            }}

            QScrollBar::add-line:horizontal {{
                border: none;
                background: transparent;
                width: 20px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }}

            QScrollBar::sub-line:horizontal {{
                border: none;
                background: transparent;
                width: 20px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }}

            QScrollBar::up-arrow:horizontal,
            QScrollBar::down-arrow:horizontal {{
                background: none;
            }}

            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {{
                background: none;
            }}

            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 8px;
                margin: 21px 0 21px 0;
                border-radius: 0px;
            }}

            QScrollBar::handle:vertical {{
                background: {alpha(self.theme.palette.grey._500, 0.32)};
                min-height: 25px;
                border-radius: 2px;
                margin-right: 2px;
            }}

            QScrollBar::add-line:vertical {{
                border: none;
                background: transparent;
                height: 20px;
                border-bottom-left-radius: 0px; 
                border-bottom-right-radius: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}

            QScrollBar::sub-line:vertical {{
                border: none;
                background: transparent;
                height: 20px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}

            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {{
                background: none;
            }}

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
            }}

            {sx_qss}
            
        """

        self.setStyleSheet(stylesheet)

    def resizeEvent(self, event):
        """Handle resize events to update dimensions."""
        PyWidgetBase.resizeEvent(event)
        super().resizeEvent(event)