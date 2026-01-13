# qtmui/material/stack.py
import asyncio
from functools import lru_cache

import threading
from typing import Callable, Optional, Union, Dict, List, Any
from PySide6.QtWidgets import QFrame, QSpacerItem, QSizePolicy, QWidget, QGraphicsDropShadowEffect, QBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer, Signal, QRunnable, QThreadPool
from PySide6.QtGui import QColor, QPainter
import uuid
import re
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.widget_base import PyWidgetBase
from qtmui.utils.data import deep_merge
from qtmui.configs import LOAD_WIDGET_ASYNC

# from ..flow_layout import FlowLayout
from ..layouts.flow_layout import FlowLayout

from qtmui.material.utils.sx_helper import padding_to_qmargins_args, get_sx_dict, get_padding_tuple

from qtmui.material.utils.style_decorator import StyleDecorator

from ..utils.validate_params import _validate_param

class Stack(QFrame, PyWidgetBase):
    """
    A stack component, styled like Material-UI Stack.

    The `Stack` component manages layout of immediate children in a flexbox-like manner,
    supporting direction, spacing, alignment, and dividers, aligning with MUI Stack props.
    Inherits from native component props.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget. Default is None.
    direction : State, str, List[str], or Dict, optional
        Defines the flex-direction ('row', 'row-reverse', 'column', 'column-reverse').
        Supports arrays or objects for responsive design. Default is 'column'.
        Can be a `State` object for dynamic updates.
    spacing : State, int, float, List, or Dict, optional
        Defines the space between immediate children. Default is 0.
        Can be a `State` object for dynamic updates.
    divider : State, QWidget, or None, optional
        Adds an element between each child. Default is None.
        Can be a `State` object for dynamic updates.
    hightLight : State or bool, optional
        If True, applies a highlight effect (qtmui-specific). Default is False.
        Can be a `State` object for dynamic updates.
    key : State or Any, optional
        Unique key identifier. Default is None.
        Can be a `State` object for dynamic updates.
    alignItems : State or str, optional
        Defines the align-items style ('flex-start', 'center', 'flex-end', 'stretch', 'baseline').
        Default is 'stretch'.
        Can be a `State` object for dynamic updates.
    justifyContent : State or str, optional
        Defines the justify-content style ('flex-start', 'flex-end', 'center', 'space-between',
        'space-around', 'space-evenly'). Default is 'flex-start'.
        Can be a `State` object for dynamic updates.
    flexWrap : State or str, optional
        Defines the flex-wrap style ('nowrap', 'wrap'). Default is 'nowrap'.
        Can be a `State` object for dynamic updates.
    flexGrow : State, int, or None, optional
        Defines the flex-grow factor. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, List[QWidget], QWidget, or None, optional
        List of child elements. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State, str, or None, optional
        Variant style (qtmui-specific, e.g., 'outlined'). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, str, type, or None, optional
        Component used for the root node. Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    useFlexGap : State or bool, optional
        If True, uses CSS flexbox gap instead of margin. Default is False.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting native component props.

    Notes
    -----
    - Existing parameters (13) are retained; 2 new parameters added to align with MUI Stack.
    - `hightLight` and `variant` are qtmui-specific and not part of MUI Stack.
    - Supports responsive direction and spacing via arrays or objects.
    - MUI classes applied: `MuiStack-root`.

    Demos:
    - Stack: https://qtmui.com/material-ui/qtmui-stack/

    API Reference:
    - Stack API: https://qtmui.com/material-ui/api/stack/
    """

    updateStyleSheet = Signal(object)


    VALID_DIRECTIONS = ["row", "row-reverse", "column", "column-reverse"]  # Chuyển thành list để khớp với _validate_param
    VALID_ALIGN_ITEMS = ["flex-start", "center", "flex-end", "stretch", "baseline"]
    VALID_JUSTIFY_CONTENT = ["flex-start", "flex-end", "center", "space-between", "space-around", "space-evenly"]
    VALID_FLEX_WRAP = ["nowrap", "wrap"]
    VALID_VARIANTS = [None, "outlined"]

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        direction: Optional[Union[State, str, dict]] = "column",  # Direction for arranging child elements
        spacing: Optional[Union[State, int, float, dict]] = 0,  # Spacing between child elements
        divider: Optional[Union[State, Callable, QWidget, bool]] = None,  # Divider between child elements
        hightLight: Optional[Union[State, bool]] = False,  # Highlight effect
        key: Optional[Union[State, str]] = None,  # Key identifier
        alignItems: Optional[Union[State, str]] = "stretch",  # Alignment of child elements
        justifyContent: Optional[Union[State, str]] = "flex-start",  # Justification of child elements
        flexWrap: Optional[Union[State, str]] = "nowrap",  # Flex wrap behavior
        flexGrow: Optional[Union[State, int]] = None,  # Flex grow factor
        children: Optional[Union[State, List[QWidget]]] = None,  # List of child elements
        variant: Optional[Union[State, str]] = None,  # Variant style
        sx: Optional[Union[State, Callable, str, Dict]] = None,  # Custom styles
        asynRenderQss: Optional[Union[State, bool]] = False,
        **kwargs
    ):
        super().__init__(parent)
        self.setObjectName(str(uuid.uuid4()))  # Gán objectName trước khi gọi set_sx
        
        self._flowLayoutPadding = None
        self._repaint_scheduled = False
        
        # self._sx: Dict[str, Any] = sx or {"border": "1px solid rgba(0,0,0,100)"}
        # self._decor = StyleDecorator(self, self._sx)
        
        
        if sx:
            # Nếu flexWrap thì dùng FlowLayout, lúc này border và padding sẽ bị bóc ra khỏi sx để paint border, 
            # padding truyền cho FlowLayout
            strFlexWrap = "nowrap"
            if isinstance(flexWrap, State):
                strFlexWrap = flexWrap.value
            elif isinstance(flexWrap, str):
                strFlexWrap = flexWrap
            
            if strFlexWrap == "wrap":
                sx_dict = get_sx_dict(sx)
                self._flowLayoutPadding = get_padding_tuple(sx_dict)
                self._decor = StyleDecorator(self, sx_dict)
                
                sx.update({"padding": "0px"})
                sx.update({"border-width": "0px"})
            
            self._setSx(sx)
        self._setKwargs(kwargs)
        
        self._kwargs = kwargs.copy()
        
        
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()

        # List of child components with position: absolute
        self._child_abs = []
        self.breakpoint = None
        

        # Gán giá trị ban đầu cho các thuộc tính bằng các hàm _set_*
        self._set_direction(direction)
        self._set_spacing(spacing)
        self._set_divider(divider)
        self._set_hightLight(hightLight)
        self._set_key(key)
        self._set_alignItems(alignItems)
        self._set_justifyContent(justifyContent)
        self._set_flexWrap(flexWrap)
        self._set_flexGrow(flexGrow)
        self._set_children(children or [])
        self._set_variant(variant)
        self._set_sx(sx)

        # from PyWidgetBase
        self._setup_sx_position(sx)  # Gán sx và khởi tạo các thuộc tính định vị

        self._asynRenderQss = asynRenderQss

        self._init_ui()


    # @_validate_param(file_path="qtmui.material.stack", param_name="direction", supported_signatures=Union[State, dict, str], valid_values=VALID_DIRECTIONS)
    def _set_direction(self, value):
        """Assign value to direction."""
        self._direction = value

    def _get_direction(self):
        """Get the direction value."""
        return self._direction.value if isinstance(self._direction, State) else self._direction

    # @_validate_param(file_path="qtmui.material.stack", param_name="spacing", supported_signatures=Union[State, int, float], validator=lambda x: x >= 0)
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value

    def _get_spacing(self):
        """Get the spacing value."""
        spacing_value = self._spacing.value if isinstance(self._spacing, State) else self._spacing
        if (isinstance(spacing_value, int) or isinstance(spacing_value, float)):
            spacing_value = spacing_value * self.theme.spacing.default_spacing
        
        return spacing_value
    
    def _get_list_padding(self):
        """Get the spacing value."""
        padding_value = self._get_sx_value("padding")
        padding_left_value = self._get_sx_value("padding-left")
        if isinstance(padding_value, str) and padding_value.endswith("px"):
            padding_value = int(padding_value.replace("px", "").strip())
        spacing_value = self._spacing.value if isinstance(self._spacing, State) else self._spacing
        if (isinstance(spacing_value, int) or isinstance(spacing_value, float)):
            spacing_value = spacing_value * self.theme.spacing.default_spacing
        
        return spacing_value

    @_validate_param(file_path="qtmui.material.stack", param_name="divider", supported_signatures=Union[State, Callable, QWidget, bool, type(None)])
    def _set_divider(self, value):
        """Assign value to divider."""
        self._divider = value

    def _get_divider(self):
        """Get the divider value."""
        return self._divider.value if isinstance(self._divider, State) else self._divider

    @_validate_param(file_path="qtmui.material.stack", param_name="hightLight", supported_signatures=Union[State, bool])
    def _set_hightLight(self, value):
        """Assign value to hightLight."""
        self._hightLight = value

    def _get_hightLight(self):
        """Get the hightLight value."""
        return self._hightLight.value if isinstance(self._hightLight, State) else self._hightLight

    # @_validate_param(file_path="qtmui.material.stack", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.stack", param_name="alignItems", supported_signatures=Union[State, str], valid_values=VALID_ALIGN_ITEMS)
    def _set_alignItems(self, value):
        """Assign value to alignItems."""
        self._alignItems = value

    def _get_alignItems(self):
        """Get the alignItems value."""
        return self._alignItems.value if isinstance(self._alignItems, State) else self._alignItems

    @_validate_param(file_path="qtmui.material.stack", param_name="justifyContent", supported_signatures=Union[State, str], valid_values=VALID_JUSTIFY_CONTENT)
    def _set_justifyContent(self, value):
        """Assign value to justifyContent."""
        self._justifyContent = value

    def _get_justifyContent(self):
        """Get the justifyContent value."""
        return self._justifyContent.value if isinstance(self._justifyContent, State) else self._justifyContent

    @_validate_param(file_path="qtmui.material.stack", param_name="flexWrap", supported_signatures=Union[State, str], valid_values=VALID_FLEX_WRAP)
    def _set_flexWrap(self, value):
        """Assign value to flexWrap."""
        self._flexWrap = value

    def _get_flexWrap(self):
        """Get the flexWrap value."""
        return self._flexWrap.value if isinstance(self._flexWrap, State) else self._flexWrap

    @_validate_param(file_path="qtmui.material.stack", param_name="flexGrow", supported_signatures=Union[State, int, type(None)], validator=lambda x: x >= 0 if x is not None else True)
    def _set_flexGrow(self, value):
        """Assign value to flexGrow."""
        self._flexGrow = value

    def _get_flexGrow(self):
        """Get the flexGrow value."""
        return self._flexGrow.value if isinstance(self._flexGrow, State) else self._flexGrow

    @_validate_param(file_path="qtmui.material.stack", param_name="children", supported_signatures=Union[State, list])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the list of children."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.stack", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.stack", param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value"""
        self._sx = value

    def _init_ui(self):
        """Initialize the Stack UI."""
        self.theme = useTheme()

        # Connect signals for State parameters
        self._connect_signals()

        self._update_layout()

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)

        # Update positions of child components with position: absolute
        PyWidgetBase.update_absolute_children(self)

        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        if self._asynRenderQss:
            self.updateStyleSheet.connect(self._updateStylesheet)
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
    def _getStyleSheet(cls, objectName: str, styledConfig: str="Stack"):
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components
            
        PyStack_root = themeComponent["PyStack"].get("styles")["root"](cls.ownerState)
        PyStack_root_qss = get_qss_style(PyStack_root, class_name=f"Stack")
        PyStack_root_prop_outlinedVariant_qss = get_qss_style(PyStack_root["props"]["outlinedVariant"])
        # print('PyStack_root_prop_outlinedVariant_qss_____________________', PyStack_root_prop_outlinedVariant_qss)

        stylesheet = f"""
            {PyStack_root_qss}
            #{objectName}[variant=outlined] {{
                {PyStack_root_prop_outlinedVariant_qss}
            }}
        """

        return stylesheet
    
    def _renderStylesheet(self):
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyStack", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(objectName=self.objectName(), styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet(objectName=self.objectName())
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
        stylesheet = f"""
            {stylesheet}
            {sxQss}
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
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss
        
    def _updateStylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)
    
    def _setStyleSheet(self):
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyStack", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(objectName=self.objectName(), styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet(objectName=self.objectName())
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """

        self.setStyleSheet(stylesheet)


    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._direction, State):
            self._direction.valueChanged.connect(self._change_direction)
        if isinstance(self._spacing, State):
            self._spacing.valueChanged.connect(self._update_spacing)
        if isinstance(self._divider, State):
            self._divider.valueChanged.connect(self._setup_layout)
        if isinstance(self._hightLight, State):
            self._hightLight.valueChanged.connect(self._update_highlight)
        if isinstance(self._key, State):
            self._key.valueChanged.connect(self._set_key)
        if isinstance(self._alignItems, State):
            self._alignItems.valueChanged.connect(self._setup_layout)
        if isinstance(self._justifyContent, State):
            self._justifyContent.valueChanged.connect(self._setup_layout)
        if isinstance(self._flexWrap, State):
            self._flexWrap.valueChanged.connect(self._update_flex_wrap)
        if isinstance(self._flexGrow, State):
            self._flexGrow.valueChanged.connect(self._setup_layout)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._update_children)
        if isinstance(self._variant, State):
            self._variant.valueChanged.connect(self._update_variant)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._setStyleSheet)



    def _update_layout(self):
        """Update the layout based on current properties."""
        _flexWrap = self._get_flexWrap()
        if _flexWrap == "wrap":
            clean_list = list(filter(lambda x: x is not None, self._get_children()))
            self.setLayout(FlowLayout(parent=self, spacing=self._get_spacing(), margin=self._flowLayoutPadding, children=clean_list, alignItems="center", justifyContent=self._get_justifyContent(), sx=self._sx))
            return

        self._layout = QBoxLayout(self._get_direction_enum(self._direction))
        self.setLayout(self._layout)
        self._update_spacing()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self._setup_layout()

    def _update_spacing(self):
        """Update the spacing of the layout."""
        spacing_value = self._get_spacing()
        self._layout.setSpacing(self._resolve_breakpoint_value(spacing_value, self._get_breakpoint()))
        self.update()

    def _update_highlight(self):
        """Update highlight effect."""
        hightLight_value = self._get_hightLight()
        if hightLight_value:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(5)
            shadow.setColor(QColor(0, 0, 0, 50))
            shadow.setOffset(2, 2)
            self.setGraphicsEffect(shadow)
        else:
            self.setGraphicsEffect(None)
        self.update()

    def _update_flex_wrap(self):
        """Update the flex wrap behavior."""
        self._update_layout()

    def _update_children(self):
        """Update the children of the Stack."""
        self._clear_widgets()
        self._setup_layout()

    def _update_variant(self):
        """Update the variant style."""
        variant_value = self._get_variant()
        if variant_value == "outlined":
            self.setProperty("variant", "outlined")
        self._setStyleSheet()


    def _change_direction(self):
        """Handle direction change."""
        self._layout.setDirection(self._get_direction_enum(self._direction))
        self.update()
        self._setup_layout()


    def _setup_layout(self):
        """Asynchronously set up the layout."""
        try:
            self._clear_layout()
            _direction = self._get_direction()
            self._layout.setDirection(self._get_direction_enum(_direction))

            children = self._get_children()
            if children:
                for index, widget in enumerate(children, 1):
                    if widget is None:
                        continue  # Skip if widget is None
                    # Check if the widget has position: absolute
                    sx = getattr(widget, '_sx', None)
                    if sx and isinstance(sx, dict) and sx.get("position") == "absolute":
                        self._child_abs.append(widget)
                        widget._relative_to = self

                    if LOAD_WIDGET_ASYNC:
                        self._do_task_async(lambda index=index, widget=widget: self._add_widget(index, widget))
                    else:
                        self._add_widget(index, widget)

            self.update()
            self.update_absolute_children()
        except Exception as e:
            pass
            # raise  # Ném lỗi trực tiếp mà không cần logging

    def _clear_layout(self):
        """Clear all widgets from the layout."""
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                # If widget has position: absolute, remove from managed list
                if widget in self._child_abs:
                    self._child_abs.remove(widget)
                    widget._relative_to = None
            elif isinstance(item, QSpacerItem):
                self._layout.removeItem(item)

    def _clear_widgets(self):
        """Clear old widgets and disconnect their signals if any."""
        children = self._get_children()
        for child in children:
            if child and hasattr(child, 'destroyed'):
                try:
                    child.destroyed.disconnect()
                except TypeError:
                    pass  # Ignore if signal is already disconnected or not connected
            if child:
                child.setParent(None)
                if child in self._child_abs:
                    self._child_abs.remove(child)
                    child._relative_to = None


    def _on_destroyed(self):
        """Disconnect signals when the object is destroyed."""
        try:
            self.theme.state.valueChanged.disconnect(self._update_stylesheet)
        except TypeError:
            pass
        self._layout = None
        self._children = None




    def _add_widget(self, index, widget: QWidget):
        """Add a widget to the layout with proper alignment and spacing."""
        _justifyContent = self._get_justifyContent()
        _direction = self._get_direction()

        if index == 1:
            for i in reversed(range(self._layout.count())):
                item = self._layout.itemAt(i)
                if isinstance(item, QSpacerItem):
                    self._layout.removeItem(item)

        if _justifyContent == "space-around":
            if index == 1:
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
            if index == len(self._get_children()):
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            else:
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
                if self._divider:
                    divider = self._create_divider()
                    if divider:
                        self._layout.addWidget(divider)
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        elif _justifyContent == "space-between":
            self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
            if index < len(self._get_children()):
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
                if self._divider:
                    divider = self._create_divider()
                    if divider:
                        self._layout.addWidget(divider)

        elif _justifyContent == "space-evenly":
            if index == 1:
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
            if index == len(self._get_children()):
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            else:
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
                if self._divider:
                    divider = self._create_divider()
                    if divider:
                        self._layout.addWidget(divider)

        elif _justifyContent == "flex-start":
            if _direction == "row-reverse":
                self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
                if self._divider and index < len(self._get_children()):
                    divider = self._create_divider()
                    if divider:
                        self._layout.addWidget(divider)
                if index == len(self._get_children()):
                    self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
            else:
                if index == 1 and _direction in ["row", "column", "column-reverse"]:
                    pass
                self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
                if self._divider and index < len(self._get_children()):
                    divider = self._create_divider()
                    if divider:
                        self._layout.addWidget(divider)
                if index == len(self._get_children()) and _direction == "row":
                    self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
                elif index == len(self._get_children()) and _direction not in ["row", "row-reverse"]:
                    self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        elif _justifyContent == "flex-end":
            if index == 1:
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
            if self._divider and index < len(self._get_children()):
                divider = self._create_divider()
                if divider:
                    self._layout.addWidget(divider)

        elif _justifyContent == "center":
            if index == 1:
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self._add_widget_with_alignment_and_flex_shrink(self._layout, widget)
            if self._divider and index < len(self._get_children()):
                divider = self._create_divider()
                if divider:
                    self._layout.addWidget(divider)
            if index == len(self._get_children()):
                self._layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum) if _direction in ["row", "row-reverse"] else QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def _add_widget_with_alignment_and_flex_shrink(self, layout: QBoxLayout, widget: QWidget):
        """Add a widget to the layout with alignment and flex shrink considerations."""
        _direction = self._get_direction()
        _alignItems = self._get_alignItems()

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        align_type = None

        align_self = self._get_align_self(widget)
        flex_grow = self._get_flex_grow(widget)
        flex_shrink = self._get_flex_shrink(widget)

        if _direction in ["row", "row-reverse"]:
            if align_self == "stretch" or (_alignItems == "stretch" and align_self is None):
                size_policy.setVerticalPolicy(QSizePolicy.Expanding)
            elif align_self == "baseline" or (_alignItems == "baseline" and align_self is None):
                align_type = Qt.AlignTop
            else:
                align_type = self._get_align_mapped(align_self) if align_self else {
                    "flex-start": Qt.AlignTop,
                    "center": Qt.AlignVCenter,
                    "flex-end": Qt.AlignBottom
                }.get(_alignItems, Qt.AlignVCenter)
        else:  # column or column-reverse
            if align_self == "stretch" or (_alignItems == "stretch" and align_self is None):
                size_policy.setHorizontalPolicy(QSizePolicy.Expanding)
            elif align_self == "baseline" or (_alignItems == "baseline" and align_self is None):
                align_type = Qt.AlignLeft
            else:
                align_type = self._get_align_mapped(align_self) if align_self else {
                    "flex-start": Qt.AlignLeft,
                    "center": Qt.AlignHCenter,
                    "flex-end": Qt.AlignRight
                }.get(_alignItems, Qt.AlignHCenter)

        try:
            widget.setSizePolicy(size_policy)
        except Exception as e:
            pass  # Bỏ logging, chỉ bỏ qua lỗi

        stretch = int(flex_grow or 0)
        if align_type is not None:
            if stretch > 0:
                layout.addWidget(widget, stretch=stretch, alignment=align_type)
            else:
                layout.addWidget(widget, alignment=align_type)
        else:
            if stretch > 0:
                layout.addWidget(widget, stretch=stretch)
            else:
                layout.addWidget(widget)

    def _get_align_self(self, widget: QWidget):
        """Get the alignSelf property from the widget's sx."""
        if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
            return widget._sx.get("alignSelf")
        return None

    def _get_flex_grow(self, widget: QWidget):
        """Get the flexGrow property from the widget's sx or Stack's flexGrow."""
        flexGrow = self._get_flexGrow()
        if flexGrow:
            return flexGrow
        if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
            return widget._sx.get("flexGrow", 0)
        return 0

    def _get_flex_shrink(self, widget: QWidget):
        """Get the flexShrink property from the widget's sx."""
        if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
            return widget._sx.get("flexShrink", 0)
        return 0

    def _get_flex_basis(self, widget: QWidget):
        """Get the flexBasis property from the widget's sx."""
        if hasattr(widget, '_sx') and widget._sx and isinstance(widget._sx, dict):
            return widget._sx.get("flexBasis")
        return None

    def _get_direction_enum(self, direction):
        """Map direction to QBoxLayout direction."""
        direction = direction.value if isinstance(direction, State) else direction
        direction_map = {
            "row": QBoxLayout.LeftToRight,
            "row-reverse": QBoxLayout.RightToLeft,
            "column": QBoxLayout.TopToBottom,
            "column-reverse": QBoxLayout.BottomToTop
        }
        return direction_map.get(self._resolve_breakpoint_value(direction, self._get_breakpoint()), QBoxLayout.TopToBottom)

    def _change_direction(self):
        """Handle direction change."""
        self._layout.setDirection(self._get_direction_enum(self._resolve_breakpoint_value(self._direction, self._get_breakpoint())))
        self.update()
        self._setup_layout()

    def _create_divider(self):
        """Create a divider widget based on the divider property."""
        _divider = self._get_divider()
        if isinstance(_divider, Callable):
            divider = _divider()
            if isinstance(divider, QWidget):
                return divider
            raise TypeError(f"The return result of the divider has incorrect type (expected QWidget, got {type(divider)})")
        elif isinstance(_divider, QWidget):
            return _divider
        elif _divider is True:
            line = QFrame()
            _direction = self._get_direction()
            line.setFrameShape(QFrame.HLine if _direction in ["column", "column-reverse"] else QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)
            return line
        return None

    def _parse_alignment(self, alignItems):
        """Parse alignment to Qt alignment based on direction."""
        _direction = self._get_direction()
        _alignItems = self._get_alignItems()
        align_map = {
            "flex-start": Qt.AlignLeft if _direction in ["row", "row-reverse"] else Qt.AlignTop,
            "center": Qt.AlignCenter,
            "flex-end": Qt.AlignRight if _direction in ["row", "row-reverse"] else Qt.AlignBottom,
            "stretch": Qt.AlignJustify,
            "baseline": Qt.AlignTop if _direction in ["row", "row-reverse"] else Qt.AlignLeft
        }
        return align_map.get(_alignItems, Qt.AlignCenter)



    def _resolve_breakpoint_value(self, config_dict, current_bp):
        if not isinstance(config_dict, dict):
            return config_dict

        breakpoints = ["xs", "sm", "md", "lg", "xl"]
        if current_bp not in breakpoints:
            current_bp = "xs"

        bp_index = breakpoints.index(current_bp)
        if current_bp in config_dict:
            return config_dict[current_bp]

        for i in range(bp_index - 1, -1, -1):
            bp = breakpoints[i]
            if bp in config_dict:
                return config_dict[bp]

        return None

    def _get_breakpoint(self):
        width = QApplication.instance().mainWindow.width()
        if width >= 1536:
            return "xl"
        elif width >= 1200:
            return "lg"
        elif width >= 900:
            return "md"
        elif width >= 600:
            return "sm"
        else:
            return "xs"


    def _schedule_repaint(self):
        """
        phải được gọi mỗi khi có thay đổi sx
        """
        if self._repaint_scheduled:
            return
        self._repaint_scheduled = True

        def _go():
            self._repaint_scheduled = False
            self.update()

        QTimer.singleShot(0, _go)
    
    def showEvent(self, event):
        if self._asynRenderQss:
            threading.Thread(target=self._renderStylesheet, args=(), daemon=True).start()
        return super().showEvent(event)
    
    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        # return super().resizeEvent(event)
        super().resizeEvent(event)
        
        if hasattr(self, "_decor"):
            self._decor.invalidate_cache()
            self._schedule_repaint()

        
    def paintEvent(self, arg__1):
        """Handle paint events."""
        PyWidgetBase.paintEvent(self, arg__1)
        # return super().paintEvent(arg__1)
        super().paintEvent(arg__1)
        
        if hasattr(self, "_decor"):
            p = QPainter(self)
            self._decor.paint(p, self.size(), self.devicePixelRatioF())
            p.end()