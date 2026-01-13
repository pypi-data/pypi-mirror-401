# qtmui/material/box/box.py
import asyncio
from functools import lru_cache
import json
import threading
import uuid

from typing import Optional, Union, Callable, Dict, List

from qtmui.utils.calc import timer
from PySide6.QtWidgets import (
    QFrame, 
    QWidget, 
    QBoxLayout,
)
from PySide6.QtCore import Qt, QTimer, Signal

from qtmui.hooks import State

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme

from qtmui.material.widget_base import PyWidgetBase
from qtmui.material.typography import Typography

from qtmui.utils.data import deep_merge

from qtmui.errors import PyMuiValidationError

# Biến global để xác định nguồn lỗi
FILE_PATH = "qtmui.material.box"

from ..utils.validate_params import _validate_param

class Box(QFrame, PyWidgetBase):
    """
    A flexible container widget for arranging child elements in a row or column.

    The `Box` widget is a versatile layout component that arranges its children
    either horizontally (row) or vertically (column) with customizable spacing
    and styling. It supports dynamic state management for properties like
    direction, visibility, and children.

    Parameters
    ----------
    key : str, optional
        A unique identifier for the widget, used for referencing or state management.
    direction : State or str, optional
        The arrangement direction of child elements. Must be one of "row" or "column".
        Default is "column". Can be a `State` object for dynamic updates.
    spacing : State or int, optional
        The spacing (in pixels) between child elements. Default is 0.
        Can be a `State` object for dynamic updates.
    children : State, list, or str, optional
        The child elements to be contained within the Box. Can be a list of widgets,
        a string (for text content), or a `State` object for dynamic child management.
    visible : State or bool, optional
        Whether the Box is visible. If None, defaults to True.
        Can be a `State` object for dynamic visibility control.
    sx : State, Callable, str, or dict, optional
        Custom styles for the Box. Can be a CSS-like string, a dictionary of style
        properties, a callable returning styles, or a `State` object for dynamic styling.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class.

    Attributes
    ----------
    VALID_DIRECTIONS : list[str]
        Valid values for the `direction` parameter: ["row", "column"].

    Demos:
    - Box: https://qtmui.com/material-ui/qtmui-box/

    API Reference:
    - Box API: https://qtmui.com/material-ui/api/box/
    """

    updateStyleSheet = Signal(object)

    VALID_DIRECTIONS = ["row", "column"]

    def __init__(
        self,
        key: Optional[str] = None,
        direction: Union[State, str] = "column",
        spacing: Union[State, int] = 0,
        children: Optional[Union[State, List, str]] = None,
        visible: Optional[Union[State, bool]] = None,
        sx: Optional[Union[State, Callable, str, Dict]] = None,
        asynRenderQss: Optional[Union[State, bool]] = False,
        **kwargs
    ):
        super().__init__()
        if sx:
            self._setSx(sx)
        self._setKwargs(kwargs)
        
        self._kwargs = kwargs.copy()
        self.setObjectName(str(uuid.uuid4()))  # Gán objectName trước khi gọi set_sx

        self.theme = useTheme()

        # List of child components with position: absolute
        self._child_abs = []
        self._relative_to = None

        # Khởi tạo layout ngay trong __init__ trước khi gọi các phương thức _set_*
        self._layout = QBoxLayout(QBoxLayout.LeftToRight)  # Hướng mặc định
        self.setLayout(self._layout)  # Gán layout ngay lập tức

        # Gán giá trị cho các thuộc tính bằng các hàm _set
        self._set_key(key)
        self._set_direction(direction)
        self._set_spacing(spacing)
        self._set_children(children)
        self._set_visible(visible)
        self._set_sx(sx)

        # from PyWidgetBase
        self._setup_sx_position(sx)  # Gán sx và khởi tạo các thuộc tính định vị

        # Initialize UI (các bước còn lại sau khi layout đã được khởi tạo)
        PyWidgetBase._setUpUi(self)
        
        self._asynRenderQss = asynRenderQss
        
        self._init_ui()

    @_validate_param(file_path=FILE_PATH, param_name="key", supported_signatures=Union[str, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key

    @_validate_param(file_path=FILE_PATH, param_name="direction", supported_signatures=Union[State, str], valid_values=VALID_DIRECTIONS)
    def _set_direction(self, value):
        """Assign value to direction."""
        self._direction = value  # Chỉ gán, không cập nhật giao diện

    def _get_direction(self):
        """Get the direction value."""
        return self._direction.value if isinstance(self._direction, State) else self._direction

    @_validate_param(file_path=FILE_PATH, param_name="spacing", supported_signatures=Union[State, int], validator=lambda x: x >= 0)
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value  # Chỉ gán, không cập nhật giao diện

    def _get_spacing(self):
        """Get the spacing value."""
        spacing_value = self._spacing.value if isinstance(self._spacing, State) else self._spacing
        if (isinstance(spacing_value, int) or isinstance(spacing_value, float)):
            spacing_value = spacing_value * self.theme.spacing.default_spacing
        return spacing_value
    
    # @_validate_param(file_path=FILE_PATH, param_name="children", supported_signatures=Union[State, list, str, type(None)])
    def _set_children(self, value):
        """Assign value to children and validate."""
        # Validate children đã được xử lý trong decorator, không cần kiểm tra lại ở đây
        self._children = value  # Chỉ gán, không cập nhật giao diện

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path=FILE_PATH, param_name="visible", supported_signatures=Union[State, bool, type(None)])
    def _set_visible(self, value):
        """Assign value to visible."""
        self._visible = value  # Chỉ gán, không cập nhật giao diện

    def _get_visible(self):
        """Get the visible value."""
        return self._visible.value if isinstance(self._visible, State) else self._visible

    @_validate_param(file_path=FILE_PATH, param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value"""
        self._sx = value

    def _validate_children(self, children: list) -> bool:
        """Validate the children parameter without using a loop for validation."""
        # Kiểm tra từng phần tử mà không dùng vòng for, sử dụng all() với generator expression
        if not all(isinstance(child, (QWidget, str)) or child is None for child in children):
            invalid_child = next((child for child in children if child is not None and not isinstance(child, (QWidget, str))), None)
            raise PyMuiValidationError(
                file_path=FILE_PATH,
                param_name="children",
                param_value=invalid_child,
                expected_types=[QWidget, str],
                error_type="INVALID_TYPE",
                message=f"Each element in list 'children' must be a QWidget or str, but got '{type(invalid_child)}'"
            )
        return True

    def _update_layout_direction(self):
        """Update layout direction and alignment."""
        self._layout.setDirection(self._get_direction_enum(self._direction))
        self._layout.setAlignment(self._get_align_enum(self._direction))
        self.update()

    def _update_layout_spacing(self):
        """Update layout spacing."""
        spacing_value = self._get_spacing()
        self._layout.setSpacing(spacing_value)
        self.update()

    def _update_layout_children(self):
        """Update layout children."""
        self._clear_layout()
        children_value = self._get_children()
        if children_value is not None:
            if isinstance(children_value, list):
                for content in children_value:  # Vòng for không thể tránh ở đây vì cần thêm widget vào layout
                    if content is None:
                        continue
                    if isinstance(content, QWidget):
                        sx = getattr(content, '_sx', None)
                        if sx and isinstance(sx, dict) and sx.get("position") == "absolute":
                            self._child_abs.append(content)
                            content._relative_to = self
                            self.layout().addWidget(content)
                        else:
                            self.layout().addWidget(content)
                    elif isinstance(content, str):
                        self.layout().addWidget(Typography(text=content))
            elif isinstance(children_value, str):
                self.layout().addWidget(Typography(text=children_value))

    def _update_layout_visible(self, init: bool=False):
        """Update layout visibility."""
        visible_value = self._get_visible()
        if visible_value is not None:
            if not visible_value:
                self.hide()
            elif visible_value and not self.isVisible() and not init:
                self.show()

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._key, State):
            self._key.valueChanged.connect(self._set_key)
        if isinstance(self._direction, State):
            self._direction.valueChanged.connect(self._update_layout_direction)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.connect(self._update_layout_spacing)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._update_layout_children)
        if isinstance(self._visible, State):
            self._visible.valueChanged.connect(lambda value:self._update_layout_visible(init=False))
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._setStyleSheet)

    def _get_direction_enum(self, direction):
        """Map direction to QBoxLayout direction."""
        direction = direction.value if isinstance(direction, State) else direction
        direction_map = {
            "row": QBoxLayout.LeftToRight,
            "column": QBoxLayout.TopToBottom,
        }
        return direction_map.get(direction, QBoxLayout.TopToBottom)
    
    def _get_align_enum(self, direction):
        """Map direction to QBoxLayout alignment."""
        direction = direction.value if isinstance(direction, State) else direction
        direction_map = {
            "row": Qt.AlignmentFlag.AlignLeft,
            "column": Qt.AlignmentFlag.AlignTop,
        }
        return direction_map.get(direction, Qt.AlignmentFlag.AlignTop)

    def _clear_layout(self):
        """Remove all widgets from the layout."""
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                if widget in self._child_abs:
                    self._child_abs.remove(widget)
                    widget._relative_to = None

    def _init_ui(self):
        """Initialize the Box UI."""
        # self._layout đã được khởi tạo trong __init__, không cần khởi tạo lại
        self.layout().setContentsMargins(0, 0, 0, 0)
        # Gọi các phương thức cập nhật giao diện để thiết lập giao diện ban đầu
        self._update_layout_direction()
        self._update_layout_spacing()
        self._update_layout_children()
        self._update_layout_visible(init=True)

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)

        # Update positions of child components with position: absolute
        PyWidgetBase.update_absolute_children(self)

        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        if self._asynRenderQss:
            self.updateStyleSheet.connect(self._update_stylesheet)
        else:
            self._setStyleSheet()
        
        self.destroyed.connect(lambda obj: self._onDestroy())

        # Connect signals for State parameters
        self._connect_signals()

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_setStyleSheet())

    async def _lazy_setStyleSheet(self):
        self._setStyleSheet()

    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheet(cls, styledConfig: str="Box"):
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components
            
        PyBox_root = themeComponent["PyBox"].get("styles")["root"](cls.ownerState)
        PyBox_root_qss = get_qss_style(PyBox_root)
        print('PyBox_root_qss_____________________')
        
        stylesheet = f"""
            Box {{
                {PyBox_root_qss}
            }}
        """

        return stylesheet
    
    # @classmethod
    # @lru_cache(maxsize=128)
    def _render_stylesheet(self):
        theme = useTheme()
        # if hasattr(cls, "styledFn"):
        #     themeComponent = deep_merge(useTheme().components, cls.styledFn)
        #     # print("themeComponent_____________________", themeComponent)
        #     MuiButton_root = themeComponent["MuiButton"].get("styles")["root"](cls.props)
        #     MuiButton_root_qss = get_qss_style(MuiButton_root)
        
        if not component_styled:
            component_styled = self.theme.components
            
        PyBox_root = component_styled["PyBox"].get("styles")["root"](self._kwargs)
        PyBox_root_qss = get_qss_style(PyBox_root)
        
        self.hover_qss = ""
        self.focus_qss = ""
        self.disabled_qss = ""
        self.enabled_qss = ""
        
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, State):
                sx = self._sx.value
            elif isinstance(self._sx, Callable):
                sx = self._sx()
            else:
                sx = self._sx

            if isinstance(sx, dict):
                self.setupPseudoClasses(sx)
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        stylesheet = f"""
            #{self.objectName()} {{
                {PyBox_root_qss}
            }}
            #{self.objectName()}:hover {{
                {self.hover_qss}
            }}
            #{self.objectName()}:focus {{
                {self.focus_qss}
            }}
            #{self.objectName()}:disabled {{
                {self.disabled_qss}
            }}
            #{self.objectName()}:enabled {{
                {self.enabled_qss}
            }}
            {sx_qss}
        """
        
        self.updateStyleSheet.emit(stylesheet)
        
    @classmethod
    def _setSx(cls, sx: dict = {}):
        cls.sxDict = sx
        
    @classmethod
    def _setKwargs(cls, kwargs: dict = {}):
        cls.ownerState = kwargs

    @classmethod
    @lru_cache(maxsize=128)
    def _getSxQss(cls, sxStr: str = "", className: str = "PyWidgetBase"):
        print("_getSxQss called with sxStr:_______________________________________________")
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss
        
    def _update_stylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)
    
    def _setStyleSheet(self):
        """Set the stylesheet for the Box."""
        
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyBox", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet()
            
        sxQss = ""
        if self._sx:
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"Box")

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """

        self.setStyleSheet(stylesheet)

    def _on_destroyed(self, ev):
        """Disconnect signals when the object is destroyed."""
        print('ondestroyyyyyyyyyyyyyyyy', ev)
        if isinstance(self._direction, State):
            self._direction.valueChanged.disconnect(self._update_layout_direction)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.disconnect(self._update_layout_spacing)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._update_layout_children)
        if isinstance(self._visible, State):
            self._visible.valueChanged.disconnect(self._update_layout_visible)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._set_sx)

    def paintEvent(self, arg__1):
        PyWidgetBase.paintEvent(self, arg__1)
        return super().paintEvent(arg__1)

    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)
    
    # def showEvent(self, e): # thêm ở đây sẽ làm nháy nav rất khó chịu
    #     """ fade in """
    #     PyWidgetBase.showEvent(self)
    #     super().showEvent(e)
    
    def enterEvent(self, event):
        self.setProperty("slot", "hover")
        self._setStyleSheet()
        return super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setProperty("slot", "leave")
        self._setStyleSheet()
        return super().leaveEvent(event)
    
    def showEvent(self, event):
        if self._asynRenderQss:
            threading.Thread(target=self._render_stylesheet, args=(), daemon=True).start()
        return super().showEvent(event)