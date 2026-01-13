import asyncio
from functools import lru_cache
from typing import Callable, Optional, Union, Dict, Any
from PySide6.QtGui import QPainter, QPen, QIcon
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QEvent
from PySide6.QtWidgets import QPushButton

from ..system.color_manipulator import hex_string_to_qcolor
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.py_iconify import Iconify
from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ..utils.functions import _get_fn_args
from ...qtmui_assets import QTMUI_ASSETS
from ..utils.validate_params import _validate_param

COLORS = ['inherit', 'default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']
SIZES = ['small', 'medium']

class Checkbox(QPushButton):
    """
    A component that allows the user to select an option, with support for checked, indeterminate, and disabled states.

    The `Checkbox` component is used to toggle a boolean value, with customizable icons, colors, and sizes.
    It supports all props of the Material-UI `Checkbox` component and `ButtonBase` component, as well as
    additional props for state and gutters. Props of `ButtonBase` are supported via `**kwargs`.

    Parameters
    ----------
    checked : State, bool, or None, optional
        If True, the component is checked. Default is False.
        Can be a `State` object for dynamic updates.
    checkedIcon : State, str, Iconify, or None, optional
        The icon to display when the component is checked. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component (e.g., "primary", "secondary", or custom color).
        Default is "primary". Can be a `State` object for dynamic updates.
    defaultChecked : State, bool, or None, optional
        The default checked state for uncontrolled components. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If True, removes padding around the checkbox. Default is False.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If True, the ripple effect is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State, str, Iconify, or None, optional
        The icon to display when the component is unchecked. Default is None.
        Can be a `State` object for dynamic updates.
    id : State, str, or None, optional
        The id of the input element. Default is None.
        Can be a `State` object for dynamic updates.
    indeterminate : State or bool, optional
        If True, the component appears indeterminate. Default is False.
        Can be a `State` object for dynamic updates.
    indeterminateIcon : State, str, Iconify, or None, optional
        The icon to display when the component is indeterminate. Default is None.
        Can be a `State` object for dynamic updates.
    inputProps : State or dict, optional
        Attributes applied to the input element. Deprecated; use slotProps.input instead.
        Default is None. Can be a `State` object for dynamic updates.
    onChange : State, Callable, or None, optional
        Callback fired when the state changes. Default is None.
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the input element is required. Default is False.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the component ("small", "medium", or custom). Default is "medium".
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (input, root). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (input, root). Default is None.
        Can be a `State` object for dynamic updates.
    state : State, bool, or None, optional
        Custom state for the component. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    value : State, Any, or None, optional
        The value of the component. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `Button` class, supporting
        props of the `ButtonBase` component (e.g., disableElevation, href).

    Attributes
    ----------
    valueChanged : Signal
        Signal emitted when the checkbox state changes, carrying the new value.
    VALID_COLORS : list[str]
        Valid values for the `color` parameter: ["default", "primary", "secondary", "error", "info "success", "warning"].
    VALID_SIZES : list[str]
        Valid values for the `size` parameter: ["small", "medium"].

    Notes
    -----
    - Props of the `ButtonBase` component are supported via `**kwargs` (e.g., `disableElevation`, `href`).
    - The `state` and `disableGutters` props are specific to this implementation and not part of Material-UI `Checkbox`.
    - The `inputProps` prop is deprecated; use `slotProps.input` instead.

    Demos:
    - Checkbox: https://qtmui.com/material-ui/qtmui-checkbox/

    API Reference:
    - Checkbox API: https://qtmui.com/material-ui/api/checkbox/
    - ButtonBase API: https://qtmui.com/material-ui/api/button-base/
    """

    valueChanged = Signal(object)

    VALID_COLORS = ["default", "primary", "secondary", "error", "info", "success", "warning"]
    VALID_SIZES = ["small", "medium"]

    def __init__(
        self,
        key: str = None,
        checked: Optional[Union[State, bool]] = False,
        checkedIcon: Optional[Union[State, str, Iconify]] = None,
        color: Union[State, str] = "primary",
        defaultChecked: Optional[Union[State, bool]] = None,
        disabled: Union[State, bool] = False,
        disableGutters: Union[State, bool] = False,
        disableRipple: Union[State, bool] = False,
        icon: Optional[Union[State, str, Iconify]] = None,
        indeterminate: Union[State, bool] = False,
        indeterminateIcon: Optional[Union[State, str, Iconify]] = None,
        inputProps: Optional[Union[State, Dict]] = None,
        onChange: Optional[Union[State, Callable]] = None,
        required: Union[State, bool] = False,
        size: Union[State, str] = "medium",
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        state: Optional[Union[State, bool]] = False,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        value: Optional[Union[State, Any]] = None,
        *args,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(id(self)))
        
        if sx:
            self._setSx(sx)
            
        self._kwargs = {
            **kwargs,
            "size": size,
            "color": color,
        }
            
        self._setKwargs(self._kwargs)
        
        self._key = key
        self._checked = checked
        self._checkedIcon = checkedIcon
        self._color = color
        self._defaultChecked = defaultChecked
        self._disabled = disabled
        self._disableGutters = disableGutters
        self._disableRipple = disableRipple
        self._disableRipple = disableRipple
        self._icon = icon
        self._indeterminate = indeterminate
        self._indeterminateIcon = indeterminateIcon
        self._inputProps = inputProps
        self._onChange = onChange
        self._required = required
        self._size = size
        self._slotProps = slotProps
        self._slots = slots
        self._state = state
        self._sx = sx
        self._value = value
        
        self._init_ui()
        
    
    def _get_checked(self):
        return self._checked.value if isinstance(self._checked, State) else self._checked
    
    def _init_ui(self):
        if self._disabled:
            self.setEnabled(False)
        else:
            self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.clicked.connect(self._updateIcon)
        # QTimer.singleShot(0, self._updateIcon)
        
        self._setCheckedState()
        
        self._connectStates()
        
        self._setStyleSheet()
        
        
    
    def onClicked(self):
        print(self.isChecked())
    
    def _connectStates(self):
        if isinstance(self._checked, State):
            useEffect(
                self._setCheckedState,
                [self._checked]
            )
    
    def _setCheckedState(self, state=None):
        if state is None:
            state = self._get_checked()
        self.setChecked(state)
        self._updateIcon()
        
    
    def _updateIcon(self):
        self.theme = useTheme()
        
        if self.isChecked():
            if self._color == "inherit":
                color = self.theme.palette.text.primary
            elif self._color == "default":
                color = self.theme.palette.text.secondary
            elif self._color in COLORS:
                color = getattr(self.theme.palette, self._color).main
            else:
                color = self.theme.palette.text.secondary
                
            if isinstance(self._checkedIcon, Iconify):
                self._checkedIcon._color = color
                self.setIcon(self._checkedIcon.qIcon())
                print(self._checkedIcon._key)
            else:
                self.setIcon(Iconify(key="mdi:checkbox-marked", color=color).qIcon())
        else:
            if isinstance(self._icon, Iconify):
                self._icon._color = self.theme.palette.grey._500
                self.setIcon(self._icon.qIcon())
            else:
                self.setIcon(Iconify(key="system-uicons:checkbox-empty", color=self.theme.palette.grey._500).qIcon())
                
        MuiCheckbox_style_icon_size = self.theme.components["MuiCheckbox"]["styles"]["icon"](self._kwargs)["size"]
        self.setIconSize(QSize(MuiCheckbox_style_icon_size["width"], MuiCheckbox_style_icon_size["height"]))
                
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

    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheet(cls, objectName, _styledConfig: str, _size: str, _color: str, _theme_mode: str):
        theme = useTheme()

        MuiCheckbox_styles = theme.components[f"MuiCheckbox"].get("styles")
        MuiCheckbox_root_qss = get_qss_style(MuiCheckbox_styles["root"](cls.ownerState))
        MuiCheckbox_root_color_qss = get_qss_style(MuiCheckbox_styles["root"](cls.ownerState)[_color])
        MuiCheckbox_root_color_slot_hover_qss = get_qss_style(MuiCheckbox_styles["root"](cls.ownerState)[_color]["slots"]["hover"])
        
        _text_color = MuiCheckbox_styles["root"](cls.ownerState)[_color]["color"]
        _icon_color = MuiCheckbox_styles["icon"](cls.ownerState)["color"]

        _indicator_border_width = MuiCheckbox_styles["checkedIndicator"]["border-width"]
        _indicator_border_radius = MuiCheckbox_styles["checkedIndicator"]["border-radius"]
        _indicator_padding = MuiCheckbox_styles["checkedIndicator"]["padding"]

        stylesheet = f"""
            #{objectName} {{
                {MuiCheckbox_root_qss}
                {MuiCheckbox_root_color_qss}
            }}
            #{objectName}:hover {{
                {MuiCheckbox_root_color_slot_hover_qss}
            }}
        """
        
        # print('stylesheet____________________', stylesheet)

        return stylesheet

    def _setStyleSheet(self):
        
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("MuiCheckbox", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(
                    self.objectName(),
                    _styledConfig=str(root),
                    _size=self._size,
                    _color=self._color,
                    _theme_mode=useTheme().palette.mode,
                )
        else:
            stylesheet = self._getStyleSheet(
                self.objectName(),
                _styledConfig="Checkbox",
                _size=self._size,
                _color=self._color,
                _theme_mode=useTheme().palette.mode,
            )
            
        sxQss = ""
        if self._sx:
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            
        if self._color == "inherit":
            self._color = "default"

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """
        
        self.setStyleSheet(stylesheet)
        

