import uuid
import threading
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QMenu, QFrame, QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QFocusEvent, QHideEvent
from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from .menu_scroll_area import MenuScrollArea

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
        open: Union[State, bool],
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
        self._set_children(children)
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
        self._set_stylesheet()

        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._connect_signals()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.menu", param_name="open", supported_signatures=Union[State, bool])
    def _set_open(self, value):
        """Assign value to open."""
        self._open = value
        if isinstance(value, State):
            value.valueChanged.connect(self._on_open_changed)
        else:
            self._update_visibility()

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
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._widget_references.clear()
        self._children = value
        children = value.value if isinstance(value, State) else value

        if isinstance(children, list):
            for child in children:
                if not isinstance(child, QWidget):
                    raise TypeError(f"Each element in children must be a QWidget, got {type(child)}")
                self._widget_references.append(child)
        elif isinstance(children, QWidget):
            self._widget_references.append(children)
        elif children is not None:
            raise TypeError(f"children must be a State, List[QWidget], QWidget, or None, got {type(children)}")

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

    @_validate_param(file_path="qtmui.material.menu", param_name="lock", supported_signatures=Union[State, threading.Lock, type(None)])
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
        """Initialize the UI based on props."""
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.installEventFilter(self)

        # Set layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # Create container
        self.container = QFrame()
        self.container.setObjectName("MenuContainer")
        self.container.setLayout(QVBoxLayout())
        self.container.layout().setContentsMargins(3, 3, 3, 3)
        self.container.layout().setSpacing(3)
        self.layout().addWidget(self.container)

        # Apply width constraints
        min_width = self._get_minWidth()
        if min_width:
            self.setMinimumWidth(min_width)
        max_width = self._get_maxWidth()
        if max_width and (not min_width or max_width > min_width):
            self.setMaximumWidth(max_width)

        # Apply children
        self._update_children()

        # Update visibility
        self._update_visibility()

    def _update_children(self):
        """Update the children in the menu."""
        children = self._get_children()
        max_height = self._get_maxHeight()
        slot_props = self._get_slotProps().get("list", {})
        menu_list_props = {**self._get_MenuListProps(), **slot_props}

        # Clear existing layout
        while self.container.layout().count():
            item = self.container.layout().takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        if children:
            if max_height:
                # Use MenuScrollArea for scrollable content
                scroll_area = MenuScrollArea(children=children, **menu_list_props)
                scroll_area.setObjectName("MenuScrollArea")
                self.container.layout().addWidget(scroll_area)
                self.container.layout().setContentsMargins(0, 0, 0, 0)
                if scroll_area.sizeHint().height() < max_height:
                    self.setMinimumHeight(scroll_area.sizeHint().height())
                else:
                    self.setMinimumHeight(max_height)
                self.setMaximumHeight(max_height)
            else:
                # Add children directly
                for child in children:
                    child.setObjectName("MenuItem")
                    self.container.layout().addWidget(child)

    def _update_visibility(self):
        """Update the visibility of the menu based on open prop."""
        if self._get_open():
            anchor = self._get_anchorEl()
            pos = QPoint(0, 0)
            if isinstance(anchor, QWidget):
                pos = anchor.mapToGlobal(anchor.rect().bottomLeft())
            elif isinstance(anchor, QPoint):
                pos = anchor
            self.popup(pos)
            if self._get_autoFocus():
                self._handle_focus()
        else:
            self.hide()

    def _handle_focus(self):
        """Handle focus based on autoFocus and disableAutoFocusItem."""
        if not self._get_autoFocus():
            self.setFocus()
            return
        if self._get_disableAutoFocusItem() or self._get_variant() == "menu":
            self.setFocus()
        else:
            # Focus first focusable item
            for child in self._get_children():
                if child.isEnabled() and child.focusPolicy() != Qt.NoFocus:
                    child.setFocus()
                    break

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the Menu."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        menu_styles = component_styled.get("Menu", {}).get("styles", {})
        root_styles = menu_styles.get("root", {})
        paper_styles = menu_styles.get("paper", {})
        root_qss = get_qss_style(root_styles)
        paper_qss = get_qss_style(paper_styles)

        # Handle sx
        sx = self._get_sx()
        sx_qss = ""
        if sx:
            if isinstance(sx, (list, dict)):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, Callable):
                sx_result = sx()
                if isinstance(sx_result, (list, dict)):
                    sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
                elif isinstance(sx_result, str):
                    sx_qss = sx_result
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        # Handle classes
        classes = self._get_classes()
        classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

        # Handle PopoverClasses
        popover_classes = self._get_PopoverClasses()
        popover_classes_qss = get_qss_style(popover_classes, class_name=f"#{self.container.objectName()}") if popover_classes else ""

        # Apply MUI classes
        mui_classes = ["MuiMenu-root"]
        mui_paper_classes = ["MuiMenu-paper"]

        stylesheet = f"""
            #{self.objectName()} {{
                background-color: transparent;
                border: none;
                {root_qss}
                {classes_qss}
            }}
            #{self.container.objectName()} {{
                {paper_qss}
                {popover_classes_qss}
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def hideEvent(self, event: QHideEvent):
        """Handle the hide event."""
        self.hideSignal.emit()
        on_close = self._get_onClose()
        if on_close:
            reason = "backdropClick"  # Default reason
            if event.spontaneous():
                reason = "escapeKeyDown"  # Assume escape key for spontaneous hide
            on_close(event, reason)
        super().hideEvent(event)

    def focusInEvent(self, event: QFocusEvent):
        """Handle focus in event."""
        self._handle_focus()
        super().focusInEvent(event)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._anchorEl, State):
            self._anchorEl.valueChanged.connect(self._on_anchorEl_changed)
        if isinstance(self._autoFocus, State):
            self._autoFocus.valueChanged.connect(self._on_autoFocus_changed)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._disableAutoFocusItem, State):
            self._disableAutoFocusItem.valueChanged.connect(self._on_disableAutoFocusItem_changed)
        if isinstance(self._id, State):
            self._id.valueChanged.connect(self._on_id_changed)
        if isinstance(self._MenuListProps, State):
            self._MenuListProps.valueChanged.connect(self._on_MenuListProps_changed)
        if isinstance(self._minWidth, State):
            self._minWidth.valueChanged.connect(self._on_minWidth_changed)
        if isinstance(self._maxWidth, State):
            self._maxWidth.valueChanged.connect(self._on_maxWidth_changed)
        if isinstance(self._maxHeight, State):
            self._maxHeight.valueChanged.connect(self._on_maxHeight_changed)
        if isinstance(self._lock, State):
            self._lock.valueChanged.connect(self._on_lock_changed)
        if isinstance(self._onClose, State):
            self._onClose.valueChanged.connect(self._on_onClose_changed)
        if isinstance(self._PopoverClasses, State):
            self._PopoverClasses.valueChanged.connect(self._on_PopoverClasses_changed)
        if isinstance(self._slotProps, State):
            self._slotProps.valueChanged.connect(self._on_slotProps_changed)
        if isinstance(self._slots, State):
            self._slots.valueChanged.connect(self._on_slots_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._transitionDuration, State):
            self._transitionDuration.valueChanged.connect(self._on_transitionDuration_changed)
        if isinstance(self._TransitionProps, State):
            self._TransitionProps.valueChanged.connect(self._on_TransitionProps_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.connect(self._on_variant_changed)

    def _on_open_changed(self):
        """Handle changes to open."""
        self._update_visibility()

    def _on_anchorEl_changed(self):
        """Handle changes to anchorEl."""
        self._set_anchorEl(self._anchorEl)
        self._update_visibility()

    def _on_autoFocus_changed(self):
        """Handle changes to autoFocus."""
        self._set_autoFocus(self._autoFocus)
        self._handle_focus()

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._update_children()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_disableAutoFocusItem_changed(self):
        """Handle changes to disableAutoFocusItem."""
        self._set_disableAutoFocusItem(self._disableAutoFocusItem)
        self._handle_focus()

    def _on_id_changed(self):
        """Handle changes to id."""
        self._set_id(self._id)

    def _on_MenuListProps_changed(self):
        """Handle changes to MenuListProps."""
        self._set_MenuListProps(self._MenuListProps)
        self._update_children()

    def _on_minWidth_changed(self):
        """Handle changes to minWidth."""
        self._set_minWidth(self._minWidth)
        self._init_ui()

    def _on_maxWidth_changed(self):
        """Handle changes to maxWidth."""
        self._set_maxWidth(self._maxWidth)
        self._init_ui()

    def _on_maxHeight_changed(self):
        """Handle changes to maxHeight."""
        self._set_maxHeight(self._maxHeight)
        self._update_children()

    def _on_lock_changed(self):
        """Handle changes to lock."""
        self._set_lock(self._lock)

    def _on_onClose_changed(self):
        """Handle changes to onClose."""
        self._set_onClose(self._onClose)

    def _on_PopoverClasses_changed(self):
        """Handle changes to PopoverClasses."""
        self._set_PopoverClasses(self._PopoverClasses)
        self._set_stylesheet()

    def _on_slotProps_changed(self):
        """Handle changes to slotProps."""
        self._set_slotProps(self._slotProps)
        self._update_children()

    def _on_slots_changed(self):
        """Handle changes to slots."""
        self._set_slots(self._slots)
        self._update_children()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_transitionDuration_changed(self):
        """Handle changes to transitionDuration."""
        self._set_transitionDuration(self._transitionDuration)

    def _on_TransitionProps_changed(self):
        """Handle changes to TransitionProps."""
        self._set_TransitionProps(self._TransitionProps)
        self._update_children()

    def _on_variant_changed(self):
        """Handle changes to variant."""
        self._set_variant(self._variant)
        self._handle_focus()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._open, State):
            self._open.valueChanged.disconnect(self._on_open_changed)
        if isinstance(self._anchorEl, State):
            self._anchorEl.valueChanged.disconnect(self._on_anchorEl_changed)
        if isinstance(self._autoFocus, State):
            self._autoFocus.valueChanged.disconnect(self._on_autoFocus_changed)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._disableAutoFocusItem, State):
            self._disableAutoFocusItem.valueChanged.disconnect(self._on_disableAutoFocusItem_changed)
        if isinstance(self._id, State):
            self._id.valueChanged.disconnect(self._on_id_changed)
        if isinstance(self._MenuListProps, State):
            self._MenuListProps.valueChanged.disconnect(self._on_MenuListProps_changed)
        if isinstance(self._minWidth, State):
            self._minWidth.valueChanged.disconnect(self._on_minWidth_changed)
        if isinstance(self._maxWidth, State):
            self._maxWidth.valueChanged.disconnect(self._on_maxWidth_changed)
        if isinstance(self._maxHeight, State):
            self._maxHeight.valueChanged.disconnect(self._on_maxHeight_changed)
        if isinstance(self._lock, State):
            self._lock.valueChanged.disconnect(self._on_lock_changed)
        if isinstance(self._onClose, State):
            self._onClose.valueChanged.disconnect(self._on_onClose_changed)
        if isinstance(self._PopoverClasses, State):
            self._PopoverClasses.valueChanged.disconnect(self._on_PopoverClasses_changed)
        if isinstance(self._slotProps, State):
            self._slotProps.valueChanged.disconnect(self._on_slotProps_changed)
        if isinstance(self._slots, State):
            self._slots.valueChanged.disconnect(self._on_slots_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._transitionDuration, State):
            self._transitionDuration.valueChanged.disconnect(self._on_transitionDuration_changed)
        if isinstance(self._TransitionProps, State):
            self._TransitionProps.valueChanged.disconnect(self._on_TransitionProps_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.disconnect(self._on_variant_changed)