# qtmui/material/scrollbar.py
import asyncio
import uuid
from typing import Callable, Optional, Union, Dict

from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt, Signal, QTimer, Slot, QRunnable, QObject, QThreadPool

from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.widget_base import PyWidgetBase
from qtmui.configs import LOAD_WIDGET_ASYNC

from qtmui.material.system.color_manipulator import alpha
from qtmui.material.utils.validate_params import _validate_param


class Scrollbar(QScrollArea, PyWidgetBase):
    """
    Demos:
    - Container: https://qtmui.com/material-ui/react-scrollbar/

    API Reference:
    - Container API: https://qtmui.com/material-ui/api/scrollbar/
    """

    file_path = "qtmui.material.scrollbar"
    
    add_wg = Signal(int)
    
    def __init__(
        self,
        children: Optional[Union[State, list]] = None,         # List of child elements (only accepts State or list)
        spacing: Union[State, int] = 6,
        sx: Optional[Union[State, Callable, str, Dict]] = None,  # Custom styles
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))  # Gán objectName trước khi gọi set_sx
        PyWidgetBase._setUpUi(self)

        # Assign values to properties
        self._set_children(children)
        self._set_sx(sx)
        self._set_spacing(spacing)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # from PyWidgetBase
        self._setup_sx_position(sx)  # Gán sx và khởi tạo các thuộc tính định vị

        self._init_ui()


    # @_validate_param(file_path="qtmui.material.scrollbar", param_name="children", supported_signatures=Union[State, list, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children() if callable(self._children) else self._children

    @_validate_param(file_path="qtmui.material.scrollbar", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value"""
        self._sx = value
        

    @_validate_param(file_path="qtmui.material.scrollbar", param_name="spacing", supported_signatures=Union[State, int], validator=lambda x: x >= 0)
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value  # Chỉ gán, không cập nhật giao diện

    def _get_sx(self):
        """Get the sx value"""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._set_stylesheet)


    def _init_ui(self):
        
        # Connect signals for State parameters
        self._connect_signals()
        
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWidgetResizable(True)
        self.contentBox = QWidget()
        self.contentBox.setObjectName(str(uuid.uuid4()))
        self.contentBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.vlayout = QVBoxLayout(self.contentBox)
        self.vlayout.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(self._spacing)

        self.setWidget(self.contentBox)
        
        self._setup_children()

        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self._set_stylesheet()
        
    def _count_wg(self):
        print(len(self._children()))
        
    def _setup_children(self):
        for index, widget in enumerate(self._children() if callable(self._children) else self._children):
            if LOAD_WIDGET_ASYNC:
                self._do_task_async(lambda index=index, widget=widget: self.vlayout.insertWidget(index, widget))
            else:
                self.vlayout.insertWidget(index, widget)
                # self.vlayout.addWidget(widget)

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, State):
                sx = self._sx.value
            elif isinstance(self._sx, Callable):
                sx = self._sx()
            else:
                sx = self._sx

            if isinstance(sx, dict):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        stylesheet = f"""

            #{self.objectName()} {{
                background-color: transparent;
            }}
            
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

    def paintEvent(self, arg__1):
        PyWidgetBase.paintEvent(self, arg__1)
        return super().paintEvent(arg__1)

    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)