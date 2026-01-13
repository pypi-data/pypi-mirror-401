import asyncio
from functools import lru_cache
from typing import Callable, Optional, Union, Dict
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, Signal, QSize, QTimer

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from ..system.color_manipulator import hex_string_to_qcolor
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.py_iconify import Iconify
from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from qtmui.hooks import State

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

COLORS = ['inherit', 'default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']
SIZES = ['small', 'medium']

class Radio(QPushButton):
    """
    A radio button component, styled like Material-UI Radio.

    The `Radio` component allows users to select one option from a set. It integrates with the `qtmui`
    framework, retaining existing parameters (except `text` and `hightLight`), adding new parameters,
    and aligning with MUI Radio props. Inherits from `Button` to support `ButtonBase` props.

    Parameters
    ----------
    id : State or str, optional
        The id of the input element. Default is None.
        Can be a `State` object for dynamic updates.
    checked : State or bool, optional
        If True, the component is checked. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State, QWidget, Callable, or None, optional
        The icon to display when unchecked. Default is None.
        Can be a `State` object for dynamic updates or a Callable returning a QWidget.
    checkedIcon : State, QWidget, Callable, or None, optional
        The icon to display when checked. Default is None.
        Can be a `State` object for dynamic updates or a Callable returning a QWidget.
    color : State or str, optional
        The color of the component ('default', 'primary', 'secondary', 'error', 'info', 'success', 'warning').
        Default is 'primary'.
        Can be a `State` object for dynamic updates.
    name : State or str, optional
        Name attribute of the input element. Default is None.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the state changes. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (event: Any, checked: bool) -> None
    value : State or Any, optional
        The value of the component. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If True, the ripple effect is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    inputProps : State or dict, optional
        Attributes applied to the input element. Default is None.
        Can be a `State` object for dynamic updates.
    inputRef : State or Callable, optional
        Ref to the input element. Default is None.
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the input element is required. Default is False.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the component ('small', 'medium'). Default is 'medium'.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for slots ({input, root}). Default is {}.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for slots ({input, root}). Default is {}.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `Button` class,
        supporting props of the `ButtonBase` component (e.g., disableElevation).

    Signals
    -------
    changed : Signal
        Emitted when the checked state or value changes.

    Notes
    -----
    - Existing parameters `text` and `hightLight` are removed; all other parameters are retained.
    - New parameters added to align with MUI: `classes`, `disabled`, `disableRipple`, `inputProps`,
      `inputRef`, `required`, `size`, `slotProps`, `slots`, `sx`.
    - Props of the `ButtonBase` component are supported via `**kwargs`.
    - MUI classes applied: `MuiRadio-root`, `Mui-checked`, `Mui-disabled`.
    - Integrates with `Button` for `ButtonBase` props and supports custom icons via `QWidget`.

    Demos:
    - Radio: https://qtmui.com/material-ui/qtmui-radio/

    API Reference:
    - Radio API: https://qtmui.com/material-ui/api/radio/
    """

    changed = Signal(object)

    def __init__(self,
                key: str = None,
                checked: bool = False,
                icon: str = None,
                checkedIcon: str = None,
                color: str = "default",
                disabled: Union[State, bool] = False,
                name: str = None,
                onChange: Callable = None,
                text: Optional[Union[str, State, Callable]] = None,
                value: object = None,
                size: Union[State, str] = "medium",
                sx: Optional[Union[State, Dict, Callable, str]] = None,
                *args, **kwargs
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
        self._icon = icon
        
        self._color = color
        self._checked = checked
        self._checkedIcon = checkedIcon
        self._disabled = disabled
        self._onChange = onChange
        self._name = name
        self._value = value
        self._size = size
        self._sx = sx
        
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
        self.clicked.connect(self._onClicked)
        
        self._setCheckedState()
        
        self._setStyleSheet()

    def _onClicked(self):
        if self._onChange:
            self._onChange(self.isChecked())

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
                self.setIcon(Iconify(key="akar-icons:radio-fill", color=color).qIcon())
        else:
            if isinstance(self._icon, Iconify):
                self._icon._color = self.theme.palette.grey._500
                self.setIcon(self._icon.qIcon())
            else:
                self.setIcon(Iconify(key="ion:radio-button-off", color=self.theme.palette.grey._500).qIcon())
                
        MuiRadio_style_icon_size = self.theme.components["MuiRadio"]["styles"]["icon"](self._kwargs)["size"]
        self.setIconSize(QSize(MuiRadio_style_icon_size["width"], MuiRadio_style_icon_size["height"]))
                
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

        MuiRadio_styles = theme.components[f"MuiRadio"].get("styles")
        MuiRadio_root_qss = get_qss_style(MuiRadio_styles["root"](cls.ownerState))
        MuiRadio_root_color_qss = get_qss_style(MuiRadio_styles["root"](cls.ownerState)[_color])
        MuiRadio_root_color_slot_hover_qss = get_qss_style(MuiRadio_styles["root"](cls.ownerState)[_color]["slots"]["hover"])
        
        _text_color = MuiRadio_styles["root"](cls.ownerState)[_color]["color"]
        _icon_color = MuiRadio_styles["icon"](cls.ownerState)["color"]

        _indicator_border_width = MuiRadio_styles["checkedIndicator"]["border-width"]
        _indicator_border_radius = MuiRadio_styles["checkedIndicator"]["border-radius"]
        _indicator_padding = MuiRadio_styles["checkedIndicator"]["padding"]

        stylesheet = f"""
            #{objectName} {{
                {MuiRadio_root_qss}
                {MuiRadio_root_color_qss}
            }}
            #{objectName}:hover {{
                {MuiRadio_root_color_slot_hover_qss}
            }}
        """
        
        # print('stylesheet____________________', stylesheet)

        return stylesheet

    def _setStyleSheet(self):
        
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("MuiRadio", {}).get("styles", {}).get("root", None)(self._kwargs)
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
                _styledConfig="Radio",
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
        