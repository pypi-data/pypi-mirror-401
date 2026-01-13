import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFocusEvent, QKeyEvent, QMouseEvent
from qtmui.hooks import State, useEffect
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
        selectedKeys: Optional[State] = None,
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
        self._set_selectedKey(selectedKeys)
        self._set_text(text)
        self._set_textAlign(textAlign)

        self.__init_ui()

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

    # @_validate_param(
    #     file_path="qtmui.material.menuitem",
    #     param_name="children",
    #     supported_signatures=Union[State, str, QWidget, List, type(None)]
    # )
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

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
        # self.setProperty("selected", str(self._get_selected()).lower())
        # self._set_stylesheet()

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
        self._selectedKeys = value

    def _get_selectedKey(self):
        """Get the selectedKey value."""
        return self._selectedKeys.value if isinstance(self._selectedKeys, State) else self._selectedKeys

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


    def __init_ui(self):
        # self.setObjectName("PyMenuItem")
        self.setObjectName(str(uuid.uuid4()))


        self.setDisabled(self._disabled)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setText(self._text)

        if self._textAlign in ["left", "center", "right"]:
            self._textAlign = f"text-align: {self._textAlign};"

        if self._minHeight:
            self.setMinimumHeight(self._minHeight)

        if self._selectedKeys:
            if isinstance(self._selectedKeys, State):
                self._selectedKeys.valueChanged.connect(self._set_selected)

        if self._children:
            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(6,6,6,6)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

            if isinstance(self._children, QWidget):
                self.layout().addWidget(self._children)
            elif isinstance(self._children, str):
                self.layout().addWidget(Typography(text=self._children))
            elif isinstance(self._children, list):
                for child in self._children:
                    if isinstance(child, str):
                        self.layout().addWidget(Typography(text=child))
                    elif isinstance(child, QWidget):
                        self.layout().addWidget(child)

        if self._onChange:
            self.selectedChange.connect(self._onChange)

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

    def retranslateUi(self):
        pass

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyMenuItem_root = component_styles[f"PyMenuItem"].get("styles")["root"]
        PyMenuItem_root_qss = get_qss_style(PyMenuItem_root)
        PyMenuItem_root_slot_hover_qss = get_qss_style(PyMenuItem_root["slots"]["hover"])
        PyMenuItem_root_slot_selected_qss = get_qss_style(PyMenuItem_root["slots"]["selected"])
        PyMenuItem_root_slot_selected_hover_qss = get_qss_style(PyMenuItem_root["slots"]["selected"]["hover"])
        PyMenuItem_root_prop_notLastOfType_qss = get_qss_style(PyMenuItem_root["props"]["notLastOfType"])

        PyMenuItem_checkbox_qss = get_qss_style(component_styles[f"PyMenuItem"].get("styles")["checkbox"])
        PyMenuItem_autocomplete_qss = get_qss_style(component_styles[f"PyMenuItem"].get("styles")["autocomplete"])
        PyMenuItem_divider_qss = get_qss_style(component_styles[f"PyMenuItem"].get("styles")["divider"])


        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyMenuItem_root_qss}
                }}
                #{self.objectName()}::hover {{
                    {PyMenuItem_root_slot_hover_qss}
                }}
                #{self.objectName()}[selected=true] {{
                    {PyMenuItem_root_slot_selected_qss}
                }}
                #{self.objectName()}[selected=true]::hover {{
                    {PyMenuItem_root_slot_selected_hover_qss}
                }}
                #{self.objectName()}[notLastOfType=true]::hover {{
                    {PyMenuItem_root_prop_notLastOfType_qss}
                }}
                #{self.objectName()} #MuiCheckbox {{
                    {PyMenuItem_checkbox_qss}
                }}
                #{self.objectName()} #MuiAutocomplete {{
                    {PyMenuItem_autocomplete_qss}
                }}
                #{self.objectName()} #PyDivider {{
                    {PyMenuItem_divider_qss}
                }}
            """
        )


    def _set_on_changed(self, onChange: Callable):
        self._onChange = onChange
        self.selectedChange.connect(self._onChange)

    def _set_selected_keys(self, selectedKeys: State):
        self._selectedKeys = selectedKeys
        self._selectedKeys.valueChanged.connect(self._set_selected)
        self._set_selected(selectedKeys.value)

    def _set_selected(self, keys):
        if isinstance(keys, list):
            if self._key in keys:
                self.setProperty("selected", "true")
            else:
                self.setProperty("selected", "false")
        else:
            if self._key == keys:
                self.setProperty("selected", "true")
            else:
                self.setProperty("selected", "false")
        self._set_stylesheet()


    def mouseReleaseEvent(self, event):
        if self._onClick:
            if self._key is not None:
                self._onClick(self._key)
            else:
                self._onClick()
        self.selectedChange.emit(self._key)
        # self.setProperty("selected", "true")
        # self._set_stylesheet()
        return super().mouseReleaseEvent(event)



    