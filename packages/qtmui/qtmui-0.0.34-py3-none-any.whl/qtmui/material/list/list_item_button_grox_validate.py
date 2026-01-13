import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QWidget, QPushButton
from PySide6.QtCore import Qt, Signal
from qtmui.hooks import State
from ..button.button_base import ButtonBase
from ..typography import Typography
from qtmui.material.styles import useTheme
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles.create_theme.components.list import list as list_fn

from .list_item_checkbox import ListItemCheckbox

class ListItemButton(QPushButton):
    """
    A component that renders a clickable button within a ListItem, styled like Material-UI ListItemButton.

    The `ListItemButton` component extends ButtonBase and is used to create interactive list items with
    support for selection, dense layouts, dividers, and customizable alignment and padding.

    Parameters
    ----------
    alignItems : State or str, optional
        Defines the align-items style property ("center", "flex-start"). Default is "center".
        Can be a `State` object for dynamic updates.
    autoFocus : State or bool, optional
        If True, the list item is focused during the first mount. Default is False.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the list item (widgets, text, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "QFrame"). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    dense : State or bool, optional
        If True, uses compact vertical padding. Default is False (inherits from parent List).
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If True, removes left and right padding. Default is False.
        Can be a `State` object for dynamic updates.
    divider : State or bool, optional
        If True, adds a 1px light border to the bottom. Default is False.
        Can be a `State` object for dynamic updates.
    focusVisibleClassName : State or str, optional
        Class name applied when the element gains focus via keyboard. Default is None.
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        The key for the list item, used for identification in lists. Default is None.
        Can be a `State` object for dynamic updates.
    minHeight : State or int, optional
        The minimum height of the list item. Default is None.
        Can be a `State` object for dynamic updates.
    onClick : State or Callable, optional
        Callback function triggered when the list item is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    selected : State or bool, optional
        If True, applies selected styling. Default is False.
        Can be a `State` object for dynamic updates.
    selectedKey : State or str, optional
        The key of the currently selected item, used to determine selection state. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the list item ("small", "medium", "large"). Default is "medium".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `ButtonBase` class,
        supporting props of ButtonBase and native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_ALIGN_ITEMS : list[str]
        Valid values for `alignItems`: ["center", "flex-start"].
    VALID_SIZES : list[str]
        Valid values for `size`: ["small", "medium", "large"].

    Signals
    -------
    themeChanged : Signal
        Emitted when the theme changes.

    Notes
    -----
    - Props of the ButtonBase component are supported via `**kwargs` (e.g., `onClick`, `disabled`, `focusVisible`).
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop supports widgets, text (rendered as Typography), or lists of widgets/text.
    - The `dense` prop defaults to the value inherited from the parent List component.

    Demos:
    - ListItemButton: https://qtmui.com/material-ui/qtmui-listitembutton/

    API Reference:
    - ListItemButton API: https://qtmui.com/material-ui/api/list-item-button/
    """

    VALID_ALIGN_ITEMS = ["center", "flex-start"]
    VALID_SIZES = ["small", "medium", "large"]

    themeChanged = Signal()

    def __init__(
        self,
        alignItems: Union[State, str] = "center",
        autoFocus: Union[State, bool] = False,
        children: Optional[Union[State, QWidget, List[Union[QWidget, str]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, str]] = None,
        dense: Union[State, bool] = False,
        disabled: Union[State, bool] = False,
        disableGutters: Union[State, bool] = False,
        divider: Union[State, bool] = False,
        focusVisibleClassName: Optional[Union[State, str]] = None,
        key: Optional[Union[State, str]] = None,
        minHeight: Optional[Union[State, int]] = None,
        onClick: Optional[Union[State, Callable]] = None,
        selected: Union[State, bool] = False,
        selectedKey: Optional[Union[State, str]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        size: Union[State, str] = "medium",
        **kwargs
    ):
        super().__init__()
        self.setObjectName(f"ListItemButton-{str(uuid.uuid4())}")

        self.kwargs =  kwargs

        self.theme = useTheme()
        self._widget_references = []

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
        self._set_onClick(onClick)
        self._validate_selected(selected)
        self._set_selectedKey(selectedKey)
        self._set_sx(sx)
        self._set_size(size)

        self._init_ui()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.list_item_button", param_name="alignItems", supported_signatures=Union[State, str], valid_values=VALID_ALIGN_ITEMS)
    def _set_alignItems(self, value):
        """Assign value to alignItems."""
        self._alignItems = value

    def _get_alignItems(self):
        """Get the alignItems value."""
        return self._alignItems.value if isinstance(self._alignItems, State) else self._alignItems

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="autoFocus", supported_signatures=Union[State, bool])
    def _set_autoFocus(self, value):
        """Assign value to autoFocus."""
        self._autoFocus = value

    def _get_autoFocus(self):
        """Get the autoFocus value."""
        return self._autoFocus.value if isinstance(self._autoFocus, State) else self._autoFocus

    # @_validate_param(file_path="qtmui.material.list_item_button", param_name="children", supported_signatures=Union[State, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="dense", supported_signatures=Union[State, bool])
    def _set_dense(self, value):
        """Assign value to dense."""
        self._dense = value

    def _get_dense(self):
        """Get the dense value."""
        return self._dense.value if isinstance(self._dense, State) else self._dense

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value
        self.setDisabled(self._get_disabled())

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="disableGutters", supported_signatures=Union[State, bool])
    def _set_disableGutters(self, value):
        """Assign value to disableGutters."""
        self._disableGutters = value

    def _get_disableGutters(self):
        """Get the disableGutters value."""
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="divider", supported_signatures=Union[State, bool])
    def _set_divider(self, value):
        """Assign value to divider."""
        self._divider = value

    def _get_divider(self):
        """Get the divider value."""
        return self._divider.value if isinstance(self._divider, State) else self._divider

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="focusVisibleClassName", supported_signatures=Union[State, str, type(None)])
    def _set_focusVisibleClassName(self, value):
        """Assign value to focusVisibleClassName."""
        self._focusVisibleClassName = value

    def _get_focusVisibleClassName(self):
        """Get the focusVisibleClassName value."""
        return self._focusVisibleClassName.value if isinstance(self._focusVisibleClassName, State) else self._focusVisibleClassName

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="minHeight", supported_signatures=Union[State, int, type(None)])
    def _set_minHeight(self, value):
        """Assign value to minHeight."""
        self._minHeight = value

    def _get_minHeight(self):
        """Get the minHeight value."""
        return self._minHeight.value if isinstance(self._minHeight, State) else self._minHeight

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="onClick", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClick(self, value):
        """Assign value to onClick."""
        self._onClick = value

    def _get_onClick(self):
        """Get the onClick value."""
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="selected", supported_signatures=Union[State, bool])
    def _validate_selected(self, value=None):
        """Assign value to selected based on selected or selectedKey."""
        self._selected = value

    def _get_selected(self):
        """Get the selected value."""
        return self._selected

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="selectedKey", supported_signatures=Union[State, str, type(None)])
    def _set_selectedKey(self, value):
        """Assign value to selectedKey."""
        self._selectedKey = value

    def _get_selectedKey(self):
        """Get the selectedKey value."""
        return self._selectedKey.value if isinstance(self._selectedKey, State) else self._selectedKey

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.list_item_button", param_name="size", supported_signatures=Union[State, str], valid_values=VALID_SIZES)
    def _set_size(self, value):
        """Assign value to size."""
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size


    def _init_ui(self):
        
        # self.set_styleFn(list_fn)

        self.setDisabled(self._disabled)

        self.setLayout(QHBoxLayout())
        # self.layout().setContentsMargins(6,6,6,6)
        self.layout().setContentsMargins(0,0,0,0)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.setCursor(Qt.CursorShape.PointingHandCursor)


        if self._minHeight:
            self.setMinimumHeight(self._minHeight)

        if self._selectedKey:
            if isinstance(self._selectedKey, State):
                self._selectedKey.valueChanged.connect(self._set_selected)

        self._set_selected()

        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")
            
            for child in self._children:
                if hasattr(child, '_secondary'):
                    if getattr(child, '_secondary'):
                        self.setFixedHeight(48)

                if isinstance(child, QWidget):
                    self.layout().addWidget(child)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _set_selected(self, value=None):
        if len(self.findChildren(ListItemCheckbox)):
            item_checkbox: ListItemCheckbox = self.findChildren(ListItemCheckbox)[0]
            item_checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)

            if self._key == 0:
                pass
            if isinstance(self._selectedKey, State):
                if self._key in self._selectedKey.value:
                    item_checkbox._checkbox.set_checked(True)
                else:
                    item_checkbox._checkbox.set_checked(False)
        else:
            if isinstance(self._selectedKey, State):
                if self._selectedKey.value == self._key:
                    self._selected = True
                else:
                    self._selected = False
            elif self._selectedKey:
                if self._selectedKey == self._key:
                    self._selected = True
                else:
                    self._selected = False
            self._set_stylesheet()


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()
        ownerState = {}
        if not component_styled:
            component_styled = self.theme.components

        # Thêm viền nếu divider=True
        if self._selected:
            self.setProperty("selected", "true")
        if self._divider:
            self.setProperty("divider", "true")
        if self._disableGutters:
            self.setProperty("disableGutters", "true")

        ownerState = {
            "size": self._size,
            **self.kwargs
        }

        # print('________00000000000', self.styleFn(self.theme))

        PyListItemButton_root = component_styled[f"PyListItemButton"].get("styles")["root"](ownerState)
        PyListItemButton_root_qss = get_qss_style(PyListItemButton_root)
        PyListItemButton_root_slot_hover_qss = get_qss_style(PyListItemButton_root["slots"]["hover"])
        PyListItemButton_root_slot_selected_qss = get_qss_style(PyListItemButton_root["slots"]["selected"])
        PyListItemButton_root_slot_selected_hover_qss = get_qss_style(PyListItemButton_root["slots"]["selected"]["hover"])
        PyListItemButton_root_props_divider_qss = get_qss_style(PyListItemButton_root["props"]["divider"])
        PyListItemButton_root_props_disableGutters_qss = get_qss_style(PyListItemButton_root["props"]["disableGutters"])

        PyListItemButton_root_props_active_qss = ""
        PyListItemButton_root_props_active_slot_hover_qss = ""
        if PyListItemButton_root["props"].get("active"):
            self.setProperty("active", True)
            PyListItemButton_root_props_active_qss = get_qss_style(PyListItemButton_root["props"]["active"])
            PyListItemButton_root_props_active_slot_hover_qss = get_qss_style(PyListItemButton_root["props"]["active"]["slots"]["hover"])


        # self.setStyleSheet(
        #     f"""
        #         #PyListItemButton {{
        #             {PyListItemButton_root_qss}
        #         }}
        #         #PyListItemButton:hover {{
        #             {PyListItemButton_root_slot_hover_qss}
        #         }}
        #         #PyListItemButton[active=true] {{
        #             {PyListItemButton_root_props_active_qss}
        #         }}
        #         #PyListItemButton[active=true]:hover {{
        #             {PyListItemButton_root_props_active_slot_hover_qss}
        #         }}
        #         #PyListItemButton[selected=true] {{
        #             {PyListItemButton_root_slot_selected_qss}
        #         }}
        #         #PyListItemButton[selected=true]:hover {{
        #             {PyListItemButton_root_slot_selected_hover_qss}
        #         }}
        #         #PyListItemButton[divider=true] {{
        #             {PyListItemButton_root_props_divider_qss}
        #         }}
        #         #PyListItemButton[disableGutters=true] {{
        #             {PyListItemButton_root_props_disableGutters_qss}
        #         }}
        #     """
        # )

        self.setStyleSheet(
            f"""
                #PyListItemButton {{
                    {PyListItemButton_root_qss}
                }}
                #PyListItemButton:hover {{
                    {PyListItemButton_root_slot_hover_qss}
                }}

                #PyListItemButton[selected=true] {{
                    {PyListItemButton_root_slot_selected_qss}
                }}
                #PyListItemButton[selected=true]:hover {{
                    {PyListItemButton_root_slot_selected_hover_qss}
                }}
                #PyListItemButton[divider=true] {{
                    {PyListItemButton_root_props_divider_qss}
                }}
                #PyListItemButton[disableGutters=true] {{
                    {PyListItemButton_root_props_disableGutters_qss}
                }}
            """
        )


    def _get_align_items_style(self, alignItems):
        """Thiết lập style cho align-items"""
        if alignItems == 'center':
            return "text-align: center;"
        elif alignItems == 'flex-start':
            return "text-align: left;"
        return ""

    def focusInEvent(self, event):
        """Quản lý lớp khi element được focus"""
        super().focusInEvent(event)
        if self._focusVisibleClassName:
            self.setStyleSheet(self.styleSheet() + f" {self._focusVisibleClassName} {{ outline: 1px solid #000; }}")

    def mouseReleaseEvent(self, event):
        if self._onClick:
            self._onClick(self._key)
        # print(self.findChildren(ListItemCheckbox)[0])
        # if self.findChildren(ListItemCheckbox):
        #     print(self.findChildren(ListItemCheckbox)[0])
        #     self.findChildren(ListItemCheckbox)[0].onClick()
            
        return super().mouseReleaseEvent(event)


    