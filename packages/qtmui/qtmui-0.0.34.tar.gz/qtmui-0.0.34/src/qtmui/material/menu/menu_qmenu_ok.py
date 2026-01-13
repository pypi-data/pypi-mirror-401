import uuid
import threading
from typing import Optional, Union, Dict, List, Callable

from qtmui.common.ui_functions import clear_layout
from PySide6.QtWidgets import QMenu, QFrame, QVBoxLayout, QWidget, QScrollArea, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QFocusEvent, QColor
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from .menu_scroll_area import MenuScrollArea

# class Menu(QMenu):
class Menu(QMenu):
    """
    A component that renders a menu, styled like Material-UI Menu, with support for positioning and transitions.

    The `Menu` component displays a list of menu items, typically `MenuItem` components, with support for
    positioning relative to an anchor element, focus management, and styling overrides.

    Parameters
    ----------
    open : State or bool
        If True, the menu is shown (required).
        Can be a `State` object for dynamic updates.
    anchorEl : State, QWidget, Callable, or None, optional
        An element or function that returns one, used to set the position of the menu. Default is None.
        Can be a `State` object for dynamic updates.
    autoFocus : State or bool, optional
        If True, focuses the menu or first item on open. Default is True.
        Can be a `State` object for dynamic updates.
    children : State, List[QWidget], QWidget, or None, optional
        Menu contents, normally MenuItems. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    disableAutoFocusItem : State or bool, optional
        If True, prevents focusing the active item on open. Default is False.
        Can be a `State` object for dynamic updates.
    id : State or str, optional
        The identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    MenuListProps : State or dict, optional
        Props applied to the MenuList element. Default is None.
        Deprecated: Use `slotProps.list` instead.
        Can be a `State` object for dynamic updates.
    minWidth : State or int, optional
        The minimum width of the menu in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    maxWidth : State or int, optional
        The maximum width of the menu in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    maxHeight : State or int, optional
        The maximum height of the menu in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    lock : State or threading.Lock, optional
        A threading lock for thread-safe operations. Default is None.
        Can be a `State` object for dynamic updates.
    onClose : State or Callable, optional
        Callback fired when the menu requests to be closed. Default is None.
        Signature: function(event: object, reason: string) => void
        Can be a `State` object for dynamic updates.
    PopoverClasses : State or dict, optional
        Classes applied to the Popover element. Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (`backdrop`, `list`, `paper`, `root`, `transition`). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components used for each slot (`backdrop`, `list`, `paper`, `root`, `transition`). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    transitionDuration : State, str, int, dict, or None, optional
        The length of the transition in ms, or 'auto'. Default is 'auto'.
        Can be a `State` object for dynamic updates.
    TransitionProps : State or dict, optional
        Props applied to the transition element. Default is None.
        Deprecated: Use `slotProps.transition` instead.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The variant to use ("menu" or "selectedMenu"). Default is "selectedMenu".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QMenu` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for `variant`: ["menu", "selectedMenu"].
    hideSignal : Signal
        Signal emitted when the menu is hidden.

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `open` prop is required to control the visibility of the menu.
    - The `MenuListProps` and `TransitionProps` are deprecated; use `slotProps.list` and `slotProps.transition` instead.
    - The `variant` prop affects focus behavior: "menu" prevents item focus, "selectedMenu" focuses the first item.

    Demos:
    - Menu: https://qtmui.com/material-ui/qtmui-menu/

    API Reference:
    - Menu API: https://qtmui.com/material-ui/api/menu/
    """

    VALID_VARIANTS = ["menu", "selectedMenu"]
    hideSignal = Signal()

    def __init__(
        self,
        open: Union[State, bool] = None,
        anchorEl: Optional[Union[State, QWidget, Callable]] = None,
        autoFocus: Union[State, bool] = True,
        children: Optional[Union[State, List[QWidget], QWidget]] = None,
        classes: Optional[Union[State, Dict]] = None,
        disableAutoFocusItem: Union[State, bool] = False,
        id: Optional[Union[State, str]] = None,
        MenuListProps: Optional[Union[State, Dict]] = None,
        minWidth: Optional[Union[State, int]] = None,
        maxWidth: Optional[Union[State, int]] = None,
        maxHeight: Optional[Union[State, int]] = None,
        lock: Optional[Union[State, threading.Lock]] = None,
        onClose: Optional[Union[State, Callable]] = None,
        PopoverClasses: Optional[Union[State, Dict]] = None,
        slotProps: Optional[Union[State, Dict[str, Union[Dict, Callable]]]] = None,
        slots: Optional[Union[State, Dict[str, str]]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        transitionDuration: Optional[Union[State, str, int, Dict[str, int]]] = "auto",
        TransitionProps: Optional[Union[State, Dict]] = None,
        variant: Union[State, str] = "selectedMenu",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"Menu-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_open(open)
        self._set_anchorEl(anchorEl)
        self._set_autoFocus(autoFocus)
        self._validate_children(children)
        self._set_classes(classes)
        self._set_disableAutoFocusItem(disableAutoFocusItem)
        self._set_id(id)
        self._set_MenuListProps(MenuListProps)
        self._set_minWidth(minWidth)
        self._set_maxWidth(maxWidth)
        self._set_maxHeight(maxHeight)
        self._set_lock(lock)
        self._set_onClose(onClose)
        self._set_PopoverClasses(PopoverClasses)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_transitionDuration(transitionDuration)
        self._set_TransitionProps(TransitionProps)
        self._set_variant(variant)

        self._init_ui()

    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.menu", param_name="open", supported_signatures=Union[State, bool])
    def _set_open(self, value):
        """Assign value to open."""
        self._open = value

    def _get_open(self):
        """Get the open value."""
        return self._open.value if isinstance(self._open, State) else self._open

    @_validate_param(file_path="qtmui.material.menu", param_name="anchorEl", supported_signatures=Union[State, QWidget, Callable, type(None)])
    def _set_anchorEl(self, value):
        """Assign value to anchorEl."""
        self._anchorEl = value

    def _get_anchorEl(self):
        """Get the anchorEl value."""
        anchor = self._anchorEl.value if isinstance(self._anchorEl, State) else self._anchorEl
        if callable(anchor):
            anchor = anchor()
        return anchor

    @_validate_param(file_path="qtmui.material.menu", param_name="autoFocus", supported_signatures=Union[State, bool])
    def _set_autoFocus(self, value):
        """Assign value to autoFocus."""
        self._autoFocus = value

    def _get_autoFocus(self):
        """Get the autoFocus value."""
        return self._autoFocus.value if isinstance(self._autoFocus, State) else self._autoFocus

    @_validate_param(file_path="qtmui.material.menu", param_name="children", supported_signatures=Union[State, List, QWidget, type(None)])
    def _validate_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        children = self._children.value if isinstance(self._children, State) else self._children
        return children if isinstance(children, list) else [children] if isinstance(children, QWidget) else []

    @_validate_param(file_path="qtmui.material.menu", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.menu", param_name="disableAutoFocusItem", supported_signatures=Union[State, bool])
    def _set_disableAutoFocusItem(self, value):
        """Assign value to disableAutoFocusItem."""
        self._disableAutoFocusItem = value

    def _get_disableAutoFocusItem(self):
        """Get the disableAutoFocusItem value."""
        return self._disableAutoFocusItem.value if isinstance(self._disableAutoFocusItem, State) else self._disableAutoFocusItem

    @_validate_param(file_path="qtmui.material.menu", param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        """Assign value to id."""
        self._id = value

    def _get_id(self):
        """Get the id value."""
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path="qtmui.material.menu", param_name="MenuListProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_MenuListProps(self, value):
        """Assign value to MenuListProps."""
        self._MenuListProps = value or {}

    def _get_MenuListProps(self):
        """Get the MenuListProps value."""
        return self._MenuListProps.value if isinstance(self._MenuListProps, State) else self._MenuListProps

    @_validate_param(file_path="qtmui.material.menu", param_name="minWidth", supported_signatures=Union[State, int, type(None)], validator=lambda x: x > 0 if isinstance(x, int) else True)
    def _set_minWidth(self, value):
        """Assign value to minWidth."""
        self._minWidth = value

    def _get_minWidth(self):
        """Get the minWidth value."""
        return self._minWidth.value if isinstance(self._minWidth, State) else self._minWidth

    @_validate_param(file_path="qtmui.material.menu", param_name="maxWidth", supported_signatures=Union[State, int, type(None)], validator=lambda x: x > 0 if isinstance(x, int) else True)
    def _set_maxWidth(self, value):
        """Assign value to maxWidth."""
        self._maxWidth = value

    def _get_maxWidth(self):
        """Get the maxWidth value."""
        return self._maxWidth.value if isinstance(self._maxWidth, State) else self._maxWidth

    @_validate_param(file_path="qtmui.material.menu", param_name="maxHeight", supported_signatures=Union[State, int, type(None)], validator=lambda x: x > 0 if isinstance(x, int) else True)
    def _set_maxHeight(self, value):
        """Assign value to maxHeight."""
        self._maxHeight = value

    def _get_maxHeight(self):
        """Get the maxHeight value."""
        return self._maxHeight.value if isinstance(self._maxHeight, State) else self._maxHeight

    # @_validate_param(file_path="qtmui.material.menu", param_name="lock", supported_signatures=Union[State, threading.Lock, type(None)])
    def _set_lock(self, value):
        """Assign value to lock."""
        self._lock = value

    def _get_lock(self):
        """Get the lock value."""
        return self._lock.value if isinstance(self._lock, State) else self._lock

    @_validate_param(file_path="qtmui.material.menu", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClose(self, value):
        """Assign value to onClose."""
        self._onClose = value

    def _get_onClose(self):
        """Get the onClose value."""
        return self._onClose.value if isinstance(self._onClose, State) else self._onClose

    @_validate_param(file_path="qtmui.material.menu", param_name="PopoverClasses", supported_signatures=Union[State, Dict, type(None)])
    def _set_PopoverClasses(self, value):
        """Assign value to PopoverClasses."""
        self._PopoverClasses = value

    def _get_PopoverClasses(self):
        """Get the PopoverClasses value."""
        return self._PopoverClasses.value if isinstance(self._PopoverClasses, State) else self._PopoverClasses

    @_validate_param(file_path="qtmui.material.menu", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value or {}

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.menu", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value or {}

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.menu", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.menu", param_name="transitionDuration", supported_signatures=Union[State, str, int, Dict, type(None)])
    def _set_transitionDuration(self, value):
        """Assign value to transitionDuration."""
        self._transitionDuration = value

    def _get_transitionDuration(self):
        """Get the transitionDuration value."""
        return self._transitionDuration.value if isinstance(self._transitionDuration, State) else self._transitionDuration

    @_validate_param(file_path="qtmui.material.menu", param_name="TransitionProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TransitionProps(self, value):
        """Assign value to TransitionProps."""
        self._TransitionProps = value or {}

    def _get_TransitionProps(self):
        """Get the TransitionProps value."""
        return self._TransitionProps.value if isinstance(self._TransitionProps, State) else self._TransitionProps

    @_validate_param(file_path="qtmui.material.menu", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant


    def _init_ui(self):

        # self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # self.installEventFilter(self)

        # if self._open:
        #     if isinstance(self._open, State):
        #         self._open.valueChanged.connect(self.show)
        #         if self._open.value:
        #             self.show()
        #             QTimer.singleShot(200, self.show)

        if self._minWidth:
            self.setMinimumWidth(self._minWidth)

        if self._maxWidth and self._minWidth and self._maxWidth > self._minWidth:
            self.setMaximumWidth(self._maxWidth)


        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        # self.setStyleSheet("border: 1px solid transparent; border-radius: 8px;")
        # self.setStyleSheet(
        #     f"""
        #         QMenu {{
        #             background-color: transparent;
        #             border: none;
        #         }}
        #     """
        # )# background-color: transparent; 

        self.container = QFrame()
        self.layout().addWidget(self.container)
        self.container.setLayout(QVBoxLayout())
        self.container.layout().setContentsMargins(3,3,3,3)
        self.container.layout().setSpacing(3)
        self.container.setObjectName("PyMenuContainer")
        
        # self.container.setAttribute(Qt.WA_TranslucentBackground)
        # self.container.setAutoFillBackground(False)
        

        if self._maxHeight:
            if isinstance(self._children, State):
                self._children.valueChanged.connect(self._set_scroll_children)
                self._set_scroll_children(self._children.value)
            else:
                if not isinstance(self._children, list):
                    raise TypeError("children must be type (list)")
                self._set_scroll_children(self._children)
        else:
            if isinstance(self._children, State):
                self._children.valueChanged.connect(self._set_children)
                self._set_children(self._children.value)
            else:
                if self._children:
                    if not isinstance(self._children, list):
                        raise TypeError("children must be type (list)")
                    for child in self._children:
                        # self.add_widget_action(child)
                        self.container.layout().addWidget(child)

        # if not self._lock:
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint |
                            Qt.NoDropShadowWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setAutoFillBackground(False)
        # self.setShadowEffect() # cái này mà đi kèm với menu background có color không phải transparent thì tạo ra góc => disable trộn màu

        # self.watch_global_var_changed()
        self.installEventFilter(self)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        # self.destroyed.connect(self._on_destroyed)

    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 20)):
        """ add shadow to dialog """
        shadowEffect = QGraphicsDropShadowEffect(self.container)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        self.container.setGraphicsEffect(None)
        self.container.setGraphicsEffect(shadowEffect)


    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def retranslateUi(self):
        pass

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyMenu = component_styles[f"PyMenu"].get("styles")
        PyMenu_root_qss = get_qss_style(PyMenu["root"])
        PyMenu_container_qss = get_qss_style(PyMenu["container"])

        PyMenuItem = component_styles[f"PyMenuItem"].get("styles")
        PyMenuItem_root_qss = get_qss_style(PyMenuItem["root"])


        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyMenu_root_qss}
                }}
                Li {{
                    {PyMenuItem_root_qss}
                }}
            """
        )

        self.container.setStyleSheet(
            f"""
                #PyMenuContainer {{
                    {PyMenu_container_qss}
                    
                }}
                Li {{
                    {PyMenuItem_root_qss}
                }}
            """
        )

    def _set_children(self, children):
        clear_layout(self.container.layout())
        if children:
            for child in children:
                if isinstance(child, QWidget):
                    child.setObjectName("PyMenuItem")
                    self.container.layout().addWidget(child)

    def _set_scroll_children(self, children):
        clear_layout(self.container.layout())

        # print("_set_scroll_children___________________", children)
        
        self.menu_scroll_area = MenuScrollArea(
            children=children
        )
        
        self.container.layout().addWidget(self.menu_scroll_area)
        self.container.layout().setContentsMargins(0,0,0,0)

        if self.menu_scroll_area.sizeHint().height() < self._maxHeight:
            self.setMinimumHeight(self.menu_scroll_area.sizeHint().height())
        else:
            self.setMinimumHeight(self._maxHeight)
        self.setMaximumHeight(self._maxHeight)

