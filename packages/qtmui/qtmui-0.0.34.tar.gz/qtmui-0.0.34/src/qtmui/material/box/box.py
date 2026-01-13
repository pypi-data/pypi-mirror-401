# qtmui/material/box/box.py
import asyncio
from functools import lru_cache
import uuid

from typing import Optional, Union, Callable, Dict, List

from PySide6.QtWidgets import QFrame, QWidget, QBoxLayout
from PySide6.QtCore import Qt, QTimer, Signal

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.utils.data import deep_merge

from qtmui.material.styles import useTheme
from qtmui.hooks import useEffect, State
from qtmui.utils.calc import timer

from qtmui.material.widget_base import PyWidgetBase
from qtmui.material.widget_base.anim_manager import AnimManager
from qtmui.material.typography import Typography

from qtmui.errors import PyMuiValidationError
from qtmui.material.utils.validate_params import _validate_param
from qtmui.configs import LOAD_WIDGET_ASYNC

FILE_PATH = "qtmui.material.box"

class Box(QFrame, PyWidgetBase, AnimManager):
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
        key: Optional[Union[str, int]] = None,
        direction: Union[State, str] = "column",
        spacing: Union[State, int] = 0,
        children: Optional[Union[State, List, str]] = None,
        visible: Optional[Union[State, bool]] = None,
        sx: Optional[Union[State, Callable, str, Dict]] = None,
        asynRenderQss: Optional[Union[State, bool]] = False,
        **kwargs
    ):
        super().__init__()
        self.destroyed.connect(lambda obj: self._onDestroy())
        
        AnimManager.__init__(self, sx=sx, **kwargs)
        # ShadownEffect.__init__(self)
        
        if sx:
            # đảm bảo rằng border không hiển thị mà dùng border từ hàm draw của animation
            if hasattr(self, "variants") and (self.variants.get("animate", {}).get("borderWidth") or self.variants.get("animate", {}).get("borderRadius")):
                sx.update({"border-width": "0px"})

            self._setSx(sx)
            
        self._kwargs = kwargs.copy()
        
        self._setKwargs(self._kwargs)
        
        
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

    @_validate_param(file_path=FILE_PATH, param_name="key", supported_signatures=Union[str, int, type(None)])
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
        
    def _get_sx(self):
        """Assign value"""
        sx = self._sx
        
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = self._sx()
        return sx


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
            if isinstance(children_value, Callable):
                children_value = children_value()
                
            if isinstance(children_value, list):
                for content in children_value:  # Vòng for không thể tránh ở đây vì cần thêm widget vào layout
                    if content is None:
                        continue
                    
                    widget = None
                    if isinstance(content, QWidget):
                        sx = getattr(content, '_sx', None)
                        if sx and isinstance(sx, dict) and sx.get("position") == "absolute":
                            self._child_abs.append(content)
                            content._relative_to = self
                            # self.layout().addWidget(content)
                            widget = content
                        else:
                            # self.layout().addWidget(content)
                            widget = content
                    elif isinstance(content, str):
                        # self.layout().addWidget(Typography(text=content))
                        widget = Typography(text=content)
                        
                    if LOAD_WIDGET_ASYNC:
                        self._do_task_async(lambda widget=widget: self.layout().addWidget(widget))
                    else:
                        self.layout().addWidget(widget)
                    
                    # thiết lập AnimManager cho widget nếu Box có variants
                    if self.variants:
                        if hasattr(widget, "variants") and widget.variants:
                            AnimManager.setup_child(self, widget)

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
        
        useEffect(
            self._setStyleSheet,
            [self.theme.state]
        )
        self._setStyleSheet()
        
        # self.destroyed.connect(lambda obj: self._onDestroy())
        
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



        # Connect signals for State parameters
        self._connect_signals()

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            self._setupStyleSheet.cancel()
        if hasattr(self, "_schedule_children_animation_task") and self._schedule_children_animation_task and not self._schedule_children_animation_task.done():
            self._schedule_children_animation_task.cancel()
        if hasattr(self, "_schedule__animCtlPlayTask") and self._schedule__animCtlPlayTask and not self._schedule__animCtlPlayTask.done():
            self._schedule__animCtlPlayTask.cancel()
        if hasattr(self, "animCtl"):
            self.animCtl.anim_group.stop()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_setStyleSheet())

    async def _lazy_setStyleSheet(self):
        self._setStyleSheet()


    
    # def _renderStylesheet(self):
    #     sx = self._get_sx()
        
    #     shadow = sx.pop("shadown") if (sx and isinstance(sx, dict) and sx.get("shadown")) else None
        
    #     stylesheet = ""
    #     if hasattr(self, "styledDict"):
    #         root = self.styledDict.get("PyBox", {}).get("styles", {}).get("root", None)(self._kwargs)
    #         if root:
    #             stylesheet = self._getStyleSheet(styledConfig=str(root))
    #     else:
    #         stylesheet = self._getStyleSheet()
            
    #     sxQss = ""
    #     if self._get_sx():
    #         sxQss = self._getSxQss(sxStr=str(self._get_sx()), className=f"#{self.objectName()}")

    #     stylesheet = f"""
    #         {stylesheet}
    #         {sxQss}
    #     """
        
    #     self.updateStyleSheet.emit(stylesheet)
        
    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheet(cls, objectName: str, styledConfig: str="Box"):
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components
            
        PyBox_root = themeComponent["PyBox"].get("styles")["root"](cls.ownerState)
        PyBox_root_qss = get_qss_style(PyBox_root, class_name=f"#{objectName}")
        
        return PyBox_root_qss
        
    @classmethod
    def _setSx(cls, sx: dict = {}):
        if isinstance(sx, State):
            sx = sx.value
        if isinstance(sx, Callable):
            sx = sx()
        
        cls.sxDict = sx
        
    @classmethod
    def _setKwargs(cls, kwargs: dict = {}):
        cls.ownerState = kwargs

    @classmethod
    @lru_cache(maxsize=128)
    def _getSxQss(cls, sxStr: str = "", className: str = "PyWidgetBase"):
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss
        
    def _updateStylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)
    
    def _setStyleSheet(self):
        sx = self._get_sx()
        
        shadow = sx.pop("box-shadow") if (sx and isinstance(sx, dict) and sx.get("box-shadow")) else None
        
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyBox", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(objectName=self.objectName(), styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet(objectName=self.objectName())
            
        sxQss = ""
        if sx:
            sxQss = self._getSxQss(sxStr=str(sx), className=f"#{self.objectName()}")

        # stylesheet = f"""
        #     {stylesheet}
        #     {sxQss}
        #     #{self.objectName()}:hover {{
        #                         border: 1px solid green;
        #                     }}
        # """
        
        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """
        
        # print(stylesheet)
        self.setStyleSheet(stylesheet)
        
        # if shadow:
        #     self._setShadownEffect(shadow)
            

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

    
    def enterEvent(self, event):
        self.setProperty("slot", "hover")
        # self._setStyleSheet()
        return super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setProperty("slot", "leave")
        # self._setStyleSheet()
        return super().leaveEvent(event)
    
    def showEvent(self, event):

        AnimManager.showEvent(self, event)
        super().showEvent(event)
        
    # def showEvent(self, event):
    #     super().showEvent(event)
    #     # We must schedule apply_initial and play AFTER layout has assigned positions.
    #     # Use singleShot(0) to run after the event loop processes layout.
    #     if self.children_widgets and not self._children_scheduled:
    #         QTimer.singleShot(0, self._schedule_children_animation)
    #         self._children_scheduled = True