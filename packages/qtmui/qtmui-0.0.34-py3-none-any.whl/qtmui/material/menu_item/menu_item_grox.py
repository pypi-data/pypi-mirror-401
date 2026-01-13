import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFocusEvent, QKeyEvent, QMouseEvent
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..typography import Typography
from .menu_item_base import MenuItemBase
from qtmui.i18n.use_translation import translate, i18n

class MenuItem(MenuItemBase):
    """
    A component that renders a menu item, styled like Material-UI MenuItem.

    The `MenuItem` component is used within a `Menu` to represent an actionable item, with support for
    selection, dense layout, dividers, and focus management. It integrates with `Menu`, `ListSubheader`,
    and `Masonry` components in the `qtmui` framework, retaining all existing parameters and adding
    support for additional MUI props.

    Parameters
    ----------
    alignItems : State or str, optional
        Alignment of items in the layout ("flex-start", "center", "flex-end"). Default is "center".
        Can be a `State` object for dynamic updates.
    autoFocus : State or bool, optional
        If True, the item is focused during the first mount or when changed to True. Default is False.
        Can be a `State` object for dynamic updates.
    children : State, str, QWidget, or List[QWidget], optional
        The content of the component. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, type, str, or None, optional
        The component used for the root node (e.g., QFrame). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    dense : State or bool, optional
        If True, uses compact padding. Default is False, inherited from parent Menu.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the item is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If True, removes left and right padding. Default is False.
        Can be a `State` object for dynamic updates.
    divider : State or bool, optional
        If True, adds a 1px border at the bottom. Default is False.
        Can be a `State` object for dynamic updates.
    focusVisibleClassName : State or str, optional
        Class name applied when the item gains focus via keyboard. Default is None.
        Can be a `State` object for dynamic updates.
    key : State, str, int, or None, optional
        Identifier for the item. Default is None.
        Can be a `State` object for dynamic updates.
    minHeight : State or int, optional
        Minimum height of the item in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the selection state changes. Default is None.
        Can be a `State` object for dynamic updates.
    onClick : State or Callable, optional
        Callback fired when the item is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    onFocus : State or Callable, optional
        Callback fired when the item gains focus. Default is None.
        Can be a `State` object for dynamic updates.
    onKeyDown : State or Callable, optional
        Callback fired when a key is pressed. Default is None.
        Can be a `State` object for dynamic updates.
    selected : State or bool, optional
        If True, the item is selected. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        Size of the item ("small", "medium", "large"). Default is "medium".
        Can be a `State` object for dynamic updates.
    parent : QWidget or None, optional
        Parent widget. Default is None.
    selectedKey : State or None, optional
        State containing the selected key(s). Default is None.
        Can be a `State` object for dynamic updates.
    text : State or str, optional
        Text content of the item, used if children is None. Default is ''.
        Can be a `State` object for dynamic updates.
    textAlign : State or str, optional
        Text alignment ("left", "center", "right"). Default is "left".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `MenuItemBase` class,
        supporting props of the ButtonBase component (e.g., style, className).

    Signals
    -------
    selectedChange : Signal
        Emitted when the selection state changes.
    clicked : Signal
        Emitted when the item is clicked.
    focusReceived : Signal
        Emitted when the item gains focus.
    keyPressed : Signal
        Emitted when a key is pressed.

    Notes
    -----
    - All existing parameters from the previous implementation are retained.
    - Props of the ButtonBase component are supported via `**kwargs` and explicit parameters (`disabled`, `onClick`, `onFocus`, `onKeyDown`).
    - The `dense` prop is inherited from the parent `Menu` if not explicitly set.
    - The `focusVisibleClassName` prop applies a class when focused via keyboard, emulating CSS `:focus-visible`.
    - MUI classes applied: `MuiMenuItem-root`, `MuiMenuItem-selected`, `MuiMenuItem-dense`, 
      `MuiMenuItem-divider`, `MuiMenuItem-guttersDisabled`.
    - Integrates with `Menu`, `ListSubheader`, and `Masonry` components for consistent styling and layout.

    Demos:
    - MenuItem: https://qtmui.com/material-ui/qtmui-menuitem/

    API Reference:
    - MenuItem API: https://qtmui.com/material-ui/api/menu-item/
    """

    selectedChange = Signal(object)
    clicked = Signal()
    focusReceived = Signal()
    keyPressed = Signal()

    VALID_ALIGN_ITEMS = ["flex-start", "center", "flex-end"]
    VALID_SIZES = ["small", "medium", "large"]
    VALID_TEXT_ALIGNS = ["left", "center", "right"]

    def __init__(
        self,
        alignItems: Union[State, str] = "center",
        autoFocus: Union[State, bool] = False,
        children: Optional[Union[State, str, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, type, str]] = None,
        dense: Union[State, bool] = False,
        disabled: Union[State, bool] = False,
        disableGutters: Union[State, bool] = False,
        divider: Union[State, bool] = False,
        focusVisibleClassName: Optional[Union[State, str]] = None,
        key: Optional[Union[State, str, int]] = None,
        minHeight: Optional[Union[State, int]] = None,
        onChange: Optional[Union[State, Callable]] = None,
        onClick: Optional[Union[State, Callable]] = None,
        onFocus: Optional[Union[State, Callable]] = None,
        onKeyDown: Optional[Union[State, Callable]] = None,
        selected: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        size: Union[State, str] = "medium",
        parent: Optional[QWidget] = None,
        selectedKey: Optional[State] = None,
        text: Union[State, str] = "",
        textAlign: Union[State, str] = "left",
        **kwargs
    ):
        super().__init__(parent=parent, **kwargs)
        self.setObjectName(f"MenuItem-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []
        self._keyboard_focus = False

        # Set properties with validation
        self._set_alignItems(alignItems)
        self._set_autoFocus(autoFocus)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_dense(dense)
        self._set_disabled(disabled)
        self._set_disableGutters(disableGutters)
        self._set_divider(divider)
        self._set_focusVisibleClassName(focusVisibleClassName)
        self._set_key(key)
        self._set_minHeight(minHeight)
        self._set_onChange(onChange)
        self._set_onClick(onClick)
        self._set_onFocus(onFocus)
        self._set_onKeyDown(onKeyDown)
        self._set_selected(selected)
        self._set_sx(sx)
        self._set_size(size)
        self._set_selectedKey(selectedKey)
        self._set_text(text)
        self._set_textAlign(textAlign)

        self._init_ui()
        self._set_stylesheet()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._connect_signals()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

    # Setter and Getter methods
    @_validate_param(
        file_path="qtmui.material.menuitem",
        param_name="alignItems",
        supported_signatures=Union[State, str],
        valid_values=VALID_ALIGN_ITEMS
    )
    def _set_alignItems(self, value):
        """Assign value to alignItems."""
        self._alignItems = value

    def _get_alignItems(self):
        """Get the alignItems value."""
        return self._alignItems.value if isinstance(self._alignItems, State) else self._alignItems

    @_validate_param(file_path="qtmui.material.menuitem", param_name="autoFocus", supported_signatures=Union[State, bool])
    def _set_autoFocus(self, value):
        """Assign value to autoFocus."""
        self._autoFocus = value
        if self._get_autoFocus():
            self.setFocus()

    def _get_autoFocus(self):
        """Get the autoFocus value."""
        return self._autoFocus.value if isinstance(self._autoFocus, State) else self._autoFocus

    @_validate_param(
        file_path="qtmui.material.menuitem",
        param_name="children",
        supported_signatures=Union[State, str, QWidget, List, type(None)]
    )
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
        elif isinstance(children, (QWidget, str)):
            if isinstance(children, str):
                typography = Typography(text=children, variant="body1")
                self._widget_references.append(typography)
            else:
                self._widget_references.append(children)
        elif children is not None:
            raise TypeError(f"children must be a State, str, QWidget, List[QWidget], or None, got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        children = self._children.value if isinstance(self._children, State) else self._children
        if isinstance(children, str):
            return [Typography(text=children, variant="body1")]
        return children if isinstance(children, list) else [children] if isinstance(children, QWidget) else []

    @_validate_param(file_path="qtmui.material.menuitem", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.menuitem", param_name="component", supported_signatures=Union[State, type, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component or QFrame

    @_validate_param(file_path="qtmui.material.menuitem", param_name="dense", supported_signatures=Union[State, bool])
    def _set_dense(self, value):
        """Assign value to dense."""
        self._dense = value

    def _get_dense(self):
        """Get the dense value."""
        dense = self._dense.value if isinstance(self._dense, State) else self._dense
        # Inherit from parent Menu if available
        parent = self.parent()
        if hasattr(parent, "_get_dense") and not dense:
            return parent._get_dense()
        return dense

    @_validate_param(file_path="qtmui.material.menuitem", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value
        self.setDisabled(self._get_disabled())

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.menuitem", param_name="disableGutters", supported_signatures=Union[State, bool])
    def _set_disableGutters(self, value):
        """Assign value to disableGutters."""
        self._disableGutters = value

    def _get_disableGutters(self):
        """Get the disableGutters value."""
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    @_validate_param(file_path="qtmui.material.menuitem", param_name="divider", supported_signatures=Union[State, bool])
    def _set_divider(self, value):
        """Assign value to divider."""
        self._divider = value

    def _get_divider(self):
        """Get the divider value."""
        return self._divider.value if isinstance(self._divider, State) else self._divider

    @_validate_param(
        file_path="qtmui.material.menuitem",
        param_name="focusVisibleClassName",
        supported_signatures=Union[State, str, type(None)],
        validator=lambda x: isinstance(x, str) and x.strip() != "" if x else True
    )
    def _set_focusVisibleClassName(self, value):
        """Assign value to focusVisibleClassName."""
        self._focusVisibleClassName = value

    def _get_focusVisibleClassName(self):
        """Get the focusVisibleClassName value."""
        return self._focusVisibleClassName.value if isinstance(self._focusVisibleClassName, State) else self._focusVisibleClassName

    @_validate_param(file_path="qtmui.material.menuitem", param_name="key", supported_signatures=Union[State, str, int, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(
        file_path="qtmui.material.menuitem",
        param_name="minHeight",
        supported_signatures=Union[State, int, type(None)],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_minHeight(self, value):
        """Assign value to minHeight."""
        self._minHeight = value

    def _get_minHeight(self):
        """Get the minHeight value."""
        return self._minHeight.value if isinstance(self._minHeight, State) else self._minHeight

    @_validate_param(file_path="qtmui.material.menuitem", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        """Assign value to onChange."""
        self._onChange = value
        if value:
            self.selectedChange.connect(self._get_onChange)

    def _get_onChange(self):
        """Get the onChange value."""
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.menuitem", param_name="onClick", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClick(self, value):
        """Assign value to onClick."""
        self._onClick = value

    def _get_onClick(self):
        """Get the onClick value."""
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    @_validate_param(file_path="qtmui.material.menuitem", param_name="onFocus", supported_signatures=Union[State, Callable, type(None)])
    def _set_onFocus(self, value):
        """Assign value to onFocus."""
        self._onFocus = value

    def _get_onFocus(self):
        """Get the onFocus value."""
        return self._onFocus.value if isinstance(self._onFocus, State) else self._onFocus

    @_validate_param(file_path="qtmui.material.menuitem", param_name="onKeyDown", supported_signatures=Union[State, Callable, type(None)])
    def _set_onKeyDown(self, value):
        """Assign value to onKeyDown."""
        self._onKeyDown = value

    def _get_onKeyDown(self):
        """Get the onKeyDown value."""
        return self._onKeyDown.value if isinstance(self._onKeyDown, State) else self._onKeyDown

    @_validate_param(file_path="qtmui.material.menuitem", param_name="selected", supported_signatures=Union[State, bool])
    def _set_selected(self, value):
        """Assign value to selected."""
        self._selected = value
        self.setProperty("selected", str(self._get_selected()).lower())
        self._set_stylesheet()

    def _get_selected(self):
        """Get the selected value."""
        selected = self._selected.value if isinstance(self._selected, State) else self._selected
        if self._get_selectedKey() is not None:
            keys = self._get_selectedKey()
            key = self._get_key()
            if key is not None:
                return key in (keys if isinstance(keys, list) else [keys])
        return selected

    @_validate_param(file_path="qtmui.material.menuitem", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(
        file_path="qtmui.material.menuitem",
        param_name="size",
        supported_signatures=Union[State, str],
        valid_values=VALID_SIZES
    )
    def _set_size(self, value):
        """Assign value to size."""
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.menuitem", param_name="selectedKey", supported_signatures=Union[State, type(None)])
    def _set_selectedKey(self, value):
        """Assign value to selectedKey."""
        self._selectedKey = value
        if value:
            value.valueChanged.connect(self._on_selectedKey_changed)

    def _get_selectedKey(self):
        """Get the selectedKey value."""
        return self._selectedKey.value if isinstance(self._selectedKey, State) else self._selectedKey

    @_validate_param(file_path="qtmui.material.menuitem", param_name="text", supported_signatures=Union[State, str])
    def _set_text(self, value):
        """Assign value to text."""
        self._text = value

    def _get_text(self):
        """Get the text value."""
        return self._text.value if isinstance(self._text, State) else self._text

    @_validate_param(
        file_path="qtmui.material.menuitem",
        param_name="textAlign",
        supported_signatures=Union[State, str],
        valid_values=VALID_TEXT_ALIGNS
    )
    def _set_textAlign(self, value):
        """Assign value to textAlign."""
        self._textAlign = value

    def _get_textAlign(self):
        """Get the textAlign value."""
        return self._textAlign.value if isinstance(self._textAlign, State) else self._textAlign

    def _init_ui(self):
        """Initialize the UI based on props."""
        component = self._get_component()
        if not isinstance(self, component):
            # Re-instantiate with the correct component class
            self.__class__ = type("DynamicMenuItem", (component, MenuItemBase), {})
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        # Apply minHeight
        min_height = self._get_minHeight()
        if min_height:
            self.setMinimumHeight(min_height)

        # Set layout
        self.setLayout(QHBoxLayout())
        padding = self.theme.spacing(1) if self._get_dense() else self.theme.spacing(2)
        self.layout().setContentsMargins(0 if self._get_disableGutters() else padding, padding, 0 if self._get_disableGutters() else padding, padding)
        self.layout().setSpacing(self.theme.spacing(1))

        # Apply alignItems
        align = self._get_alignItems()
        alignment = {
            "flex-start": Qt.AlignTop,
            "center": Qt.AlignVCenter,
            "flex-end": Qt.AlignBottom
        }.get(align, Qt.AlignVCenter)
        self.layout().setAlignment(alignment)

        # Clear previous widgets
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Apply children or text
        children = self._get_children()
        if children:
            for child in children:
                if isinstance(child, Typography):
                    child.setProperty("text-align", self._get_textAlign())
                self.layout().addWidget(child)
        elif self._get_text():
            typography = Typography(text=self._get_text(), variant="body1")
            typography.setProperty("text-align", self._get_textAlign())
            self._widget_references.append(typography)
            self.layout().addWidget(typography)

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the MenuItem."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        menuitem_styles = component_styled.get("MenuItem", {}).get("styles", {})
        root_styles = menuitem_styles.get("root", {})
        selected_styles = menuitem_styles.get("slots", {}).get("selected", {})
        hover_styles = menuitem_styles.get("slots", {}).get("hover", {})
        root_qss = get_qss_style(root_styles)
        selected_qss = get_qss_style(selected_styles)
        hover_qss = get_qss_style(hover_styles)

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

        # Handle focusVisibleClassName
        focus_visible_qss = ""
        focus_visible_class = self._get_focusVisibleClassName()
        if focus_visible_class and self._keyboard_focus:
            focus_visible_qss = f".{focus_visible_class} {{ border: 2px solid {self.theme.palette.primary.main}; }}"

        # Apply MUI classes
        mui_classes = ["MuiMenuItem-root"]
        if self._get_selected():
            mui_classes.append("MuiMenuItem-selected")
        if self._get_dense():
            mui_classes.append("MuiMenuItem-dense")
        if self._get_divider():
            mui_classes.append("MuiMenuItem-divider")
        if self._get_disableGutters():
            mui_classes.append("MuiMenuItem-guttersDisabled")

        # Apply divider
        divider_qss = f"border-bottom: 1px solid {self.theme.palette.divider};" if self._get_divider() else ""

        # Apply size
        size = self._get_size()
        font_size = {"small": 12, "medium": 14, "large": 16}.get(size, 14)
        padding = self.theme.spacing(1) if self._get_dense() else self.theme.spacing(2)

        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                {classes_qss}
                {divider_qss}
                font-size: {font_size}px;
                padding: {padding}px {0 if self._get_disableGutters() else padding}px;
            }}
            #{self.objectName()}:hover {{
                {hover_qss}
                background-color: {self.theme.palette.action.hover};
            }}
            #{self.objectName()}[selected=true] {{
                {selected_qss}
                background-color: {self.theme.palette.action.selected};
            }}
            #{self.objectName()}:disabled {{
                color: {self.theme.palette.text.disabled};
                opacity: 0.5;
            }}
            {sx_qss}
            {focus_visible_qss}
        """
        self.setStyleSheet(stylesheet)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release event."""
        if event.button() == Qt.LeftButton and not self._get_disabled():
            if self._get_onClick():
                key = self._get_key()
                if key is not None:
                    self._get_onClick()(key)
                else:
                    self._get_onClick()()
            self.clicked.emit()
            self.selectedChange.emit(self._get_key())
        super().mouseReleaseEvent(event)

    def focusInEvent(self, event: QFocusEvent):
        """Handle focus in event."""
        self._keyboard_focus = event.reason() in (Qt.TabFocusReason, Qt.BacktabFocusReason)
        if self._get_onFocus():
            self._get_onFocus()(event)
        self.focusReceived.emit()
        self._set_stylesheet()
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        """Handle focus out event."""
        self._keyboard_focus = False
        self._set_stylesheet()
        super().focusOutEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key press event."""
        if not self._get_disabled():
            if self._get_onKeyDown():
                self._get_onKeyDown()(event)
            self.keyPressed.emit()
            if event.key() in (Qt.Key_Return, Qt.Key_Space) and self._get_onClick():
                key = self._get_key()
                if key is not None:
                    self._get_onClick()(key)
                else:
                    self._get_onClick()()
                self.clicked.emit()
                self.selectedChange.emit(self._get_key())
        super().keyPressEvent(event)

    def retranslateUi(self):
        """Update UI for language changes."""
        if self._get_text() and not self._get_children():
            self._init_ui()

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._alignItems, State):
            self._alignItems.valueChanged.connect(self._on_alignItems_changed)
        if isinstance(self._autoFocus, State):
            self._autoFocus.valueChanged.connect(self._on_autoFocus_changed)
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.connect(self._on_component_changed)
        if isinstance(self._dense, State):
            self._dense.valueChanged.connect(self._on_dense_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.connect(self._on_disabled_changed)
        if isinstance(self._disableGutters, State):
            self._disableGutters.valueChanged.connect(self._on_disableGutters_changed)
        if isinstance(self._divider, State):
            self._divider.valueChanged.connect(self._on_divider_changed)
        if isinstance(self._focusVisibleClassName, State):
            self._focusVisibleClassName.valueChanged.connect(self._on_focusVisibleClassName_changed)
        if isinstance(self._key, State):
            self._key.valueChanged.connect(self._on_key_changed)
        if isinstance(self._minHeight, State):
            self._minHeight.valueChanged.connect(self._on_minHeight_changed)
        if isinstance(self._onChange, State):
            self._onChange.valueChanged.connect(self._on_onChange_changed)
        if isinstance(self._onClick, State):
            self._onClick.valueChanged.connect(self._on_onClick_changed)
        if isinstance(self._onFocus, State):
            self._onFocus.valueChanged.connect(self._on_onFocus_changed)
        if isinstance(self._onKeyDown, State):
            self._onKeyDown.valueChanged.connect(self._on_onKeyDown_changed)
        if isinstance(self._selected, State):
            self._selected.valueChanged.connect(self._on_selected_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._size, State):
            self._size.valueChanged.connect(self._on_size_changed)
        if isinstance(self._text, State):
            self._text.valueChanged.connect(self._on_text_changed)
        if isinstance(self._textAlign, State):
            self._textAlign.valueChanged.connect(self._on_textAlign_changed)

    def _on_alignItems_changed(self):
        """Handle changes to alignItems."""
        self._set_alignItems(self._alignItems)
        self._init_ui()

    def _on_autoFocus_changed(self):
        """Handle changes to autoFocus."""
        self._set_autoFocus(self._autoFocus)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._init_ui()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_component_changed(self):
        """Handle changes to component."""
        self._set_component(self._component)
        self._init_ui()

    def _on_dense_changed(self):
        """Handle changes to dense."""
        self._set_dense(self._dense)
        self._init_ui()
        self._set_stylesheet()

    def _on_disabled_changed(self):
        """Handle changes to disabled."""
        self._set_disabled(self._disabled)
        self._set_stylesheet()

    def _on_disableGutters_changed(self):
        """Handle changes to disableGutters."""
        self._set_disableGutters(self._disableGutters)
        self._init_ui()
        self._set_stylesheet()

    def _on_divider_changed(self):
        """Handle changes to divider."""
        self._set_divider(self._divider)
        self._set_stylesheet()

    def _on_focusVisibleClassName_changed(self):
        """Handle changes to focusVisibleClassName."""
        self._set_focusVisibleClassName(self._focusVisibleClassName)
        self._set_stylesheet()

    def _on_key_changed(self):
        """Handle changes to key."""
        self._set_key(self._key)
        self._set_selected(self._get_selected())

    def _on_minHeight_changed(self):
        """Handle changes to minHeight."""
        self._set_minHeight(self._minHeight)
        self._init_ui()

    def _on_onChange_changed(self):
        """Handle changes to onChange."""
        self._set_onChange(self._onChange)

    def _on_onClick_changed(self):
        """Handle changes to onClick."""
        self._set_onClick(self._onClick)

    def _on_onFocus_changed(self):
        """Handle changes to onFocus."""
        self._set_onFocus(self._onFocus)

    def _on_onKeyDown_changed(self):
        """Handle changes to onKeyDown."""
        self._set_onKeyDown(self._onKeyDown)

    def _on_selected_changed(self):
        """Handle changes to selected."""
        self._set_selected(self._selected)

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_size_changed(self):
        """Handle changes to size."""
        self._set_size(self._size)
        self._set_stylesheet()

    def _on_selectedKey_changed(self):
        """Handle changes to selectedKey."""
        self._set_selected(self._get_selected())

    def _on_text_changed(self):
        """Handle changes to text."""
        self._set_text(self._text)
        self._init_ui()

    def _on_textAlign_changed(self):
        """Handle changes to textAlign."""
        self._set_textAlign(self._textAlign)
        self._init_ui()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._alignItems, State):
            self._alignItems.valueChanged.disconnect(self._on_alignItems_changed)
        if isinstance(self._autoFocus, State):
            self._autoFocus.valueChanged.disconnect(self._on_autoFocus_changed)
        if isinstance(self._children, State):
            self._children.valueChanged.disconnect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.disconnect(self._on_component_changed)
        if isinstance(self._dense, State):
            self._dense.valueChanged.disconnect(self._on_dense_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.disconnect(self._on_disabled_changed)
        if isinstance(self._disableGutters, State):
            self._disableGutters.valueChanged.disconnect(self._on_disableGutters_changed)
        if isinstance(self._divider, State):
            self._divider.valueChanged.disconnect(self._on_divider_changed)
        if isinstance(self._focusVisibleClassName, State):
            self._focusVisibleClassName.valueChanged.disconnect(self._on_focusVisibleClassName_changed)
        if isinstance(self._key, State):
            self._key.valueChanged.disconnect(self._on_key_changed)
        if isinstance(self._minHeight, State):
            self._minHeight.valueChanged.disconnect(self._on_minHeight_changed)
        if isinstance(self._onChange, State):
            self._onChange.valueChanged.disconnect(self._on_onChange_changed)
        if isinstance(self._onClick, State):
            self._onClick.valueChanged.disconnect(self._on_onClick_changed)
        if isinstance(self._onFocus, State):
            self._onFocus.valueChanged.disconnect(self._on_onFocus_changed)
        if isinstance(self._onKeyDown, State):
            self._onKeyDown.valueChanged.disconnect(self._on_onKeyDown_changed)
        if isinstance(self._selected, State):
            self._selected.valueChanged.disconnect(self._on_selected_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._size, State):
            self._size.valueChanged.disconnect(self._on_size_changed)
        if isinstance(self._selectedKey, State):
            self._selectedKey.valueChanged.disconnect(self._on_selectedKey_changed)
        if isinstance(self._text, State):
            self._text.valueChanged.disconnect(self._on_text_changed)
        if isinstance(self._textAlign, State):
            self._textAlign.valueChanged.disconnect(self._on_textAlign_changed)