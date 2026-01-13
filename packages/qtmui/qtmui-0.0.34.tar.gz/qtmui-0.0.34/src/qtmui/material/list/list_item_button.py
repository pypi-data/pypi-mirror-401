import asyncio
from functools import lru_cache
import threading
from typing import Callable, Dict, List, Optional, Union

from PySide6.QtWidgets import QHBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal, QTimer

from qtmui.hooks import State
from qtmui.utils.data import deep_merge

from ..system.color_manipulator import alpha

from ..button.button_base import ButtonBase
from .list_item_checkbox import ListItemCheckbox
from ..utils.validate_params import _validate_param

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style


class ListItemButton(ButtonBase):
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
    themeChanged = Signal()
    
    updateStyleSheet = Signal(object)

    VALID_ALIGN_ITEMS = ["center", "flex-start"]
    VALID_SIZES = ["small", "medium", "large"]

    def __init__(self, 
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
                asynRenderQss: Optional[Union[State, bool]] = False,
                
                 **kwargs):
        super().__init__()
        self.setObjectName(str(id(self)))
        if sx:
            self._setSx(sx)
            
        self._kwargs = {
            **kwargs,
            "size": size,
        }
            
        self._setKwargs(self._kwargs)
        
        self._setUpUi()

        # Gán các props thành thuộc tính của class
        self.kwargs = kwargs

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

        self._asynRenderQss = asynRenderQss

        self.__init_ui()

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

    # @_validate_param(file_path="qtmui.material.list_item_button", param_name="key", supported_signatures=Union[State, str, type(None)])
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
        return self._selected.value if isinstance(self._selected, State) else self._selected

    # @_validate_param(file_path="qtmui.material.list_item_button", param_name="selectedKey", supported_signatures=Union[State, str, type(None)])
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

    def __init_ui(self):
        
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
                
        if isinstance(self._selected, State):
            self._selected.valueChanged.connect(self._set_selected)

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
                    
        self.theme = useTheme()

        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        if self._asynRenderQss:
            self.updateStyleSheet.connect(self._updateStylesheet)
        else:
            self._setStyleSheet()
        
        self.destroyed.connect(lambda obj: self._onDestroy())


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
    def _getStyleSheet(cls, objectName: str, styledConfig: str="ListItemButton"):
        theme = useTheme()
        if hasattr(cls, "styledDict"):
            themeComponent = deep_merge(theme.components, cls.styledDict)
        else:
            themeComponent = theme.components
            
        PyListItemButton_root = themeComponent["PyListItemButton"].get("styles")["root"](cls.ownerState)
        PyListItemButton_root_qss = get_qss_style(PyListItemButton_root)
        
        PyListItemButton_root_slot_hover_qss = get_qss_style(PyListItemButton_root["slots"]["hover"])
        PyListItemButton_root_slot_selected_qss = get_qss_style(PyListItemButton_root["slots"]["selected"])
        PyListItemButton_root_slot_selected_hover_qss = get_qss_style(PyListItemButton_root["slots"]["selected"]["hover"])
        PyListItemButton_root_props_divider_qss = get_qss_style(PyListItemButton_root["props"]["divider"])
        PyListItemButton_root_props_disableGutters_qss = get_qss_style(PyListItemButton_root["props"]["disableGutters"])

        PyListItemButton_root_props_active_qss = ""
        PyListItemButton_root_props_active_slot_hover_qss = ""
        if PyListItemButton_root["props"].get("active"):
            cls.setProperty("active", True)
            PyListItemButton_root_props_active_qss = get_qss_style(PyListItemButton_root["props"]["active"])
            PyListItemButton_root_props_active_slot_hover_qss = get_qss_style(PyListItemButton_root["props"]["active"]["slots"]["hover"])

        stylesheet = f"""
                #{objectName} {{
                    {PyListItemButton_root_qss}
                }}
                #{objectName}:hover {{
                    {PyListItemButton_root_slot_hover_qss}
                }}

                #{objectName}[selected=true] {{
                    {PyListItemButton_root_slot_selected_qss}
                }}
                #{objectName}[selected=true]:hover {{
                    {PyListItemButton_root_slot_selected_hover_qss}
                }}
                #{objectName}[divider=true] {{
                    {PyListItemButton_root_props_divider_qss}
                }}
                #{objectName}[disableGutters=true] {{
                    {PyListItemButton_root_props_disableGutters_qss}
                }}
                #{objectName}[active=true] {{
                    {PyListItemButton_root_props_active_qss}
                }}
                #{objectName}[active=true]:hover {{
                    {PyListItemButton_root_props_active_slot_hover_qss}
                }}
                
                """
        
        return stylesheet
    
    def _renderStylesheet(self):
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyListItemButton", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(objectName=self.objectName(), styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet(objectName=self.objectName())
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"ListItemButton")

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
        
        # Thêm viền nếu divider=True
        if self._get_selected():
            self.setProperty("selected", "true")
        else:
            self.setProperty("selected", "false")
            
        if self._divider:
            self.setProperty("divider", "true")
        if self._disableGutters:
            self.setProperty("disableGutters", "true")
        
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("PyListItemButton", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(objectName=self.objectName(), styledConfig=str(root))
        else:
            stylesheet = self._getStyleSheet(objectName=self.objectName())
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"ListItemButton")

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """
        
        self.setStyleSheet(stylesheet)


    def _set_selected_key(self, value=None):
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
            self._setStyleSheet()

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

        self._setStyleSheet()


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
            try:
                self._onClick(self._key)
            except Exception as e:
                self._onClick()
        return super().mouseReleaseEvent(event)

    def showEvent(self, event):
        if self._asynRenderQss:
            threading.Thread(target=self._renderStylesheet, args=(), daemon=True).start()
        return super().showEvent(event)