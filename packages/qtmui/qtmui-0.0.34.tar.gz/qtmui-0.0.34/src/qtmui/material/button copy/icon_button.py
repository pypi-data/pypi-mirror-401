import asyncio
from typing import Callable, Dict, List, Optional, Union

from qtmui.hooks import State
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from .button import Button
from ..py_iconify import Iconify

class IconButton(Button):
    """
    A button component that displays an icon, supporting Material-UI IconButton props.

    The `IconButton` component is used to render a button with an icon as its primary content,
    supporting loading states, ripple effects, and edge alignment.

    Parameters
    ----------
    children : State, str, PyIconify, QWidget, or None, optional
        The icon or content to display. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component ("inherit", "default", "primary", "secondary", "error", "info",
        "success", "warning", or custom). Default is "default".
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the button is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableFocusRipple : State or bool, optional
        If True, the keyboard focus ripple is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If True, the ripple effect is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    edge : State, str, or bool, optional
        Aligns the button with negative margin ("start", "end", False). Default is False.
        Can be a `State` object for dynamic updates.
    loading : State or bool, optional
        If True, shows the loading indicator and disables the button. Default is None.
        Can be a `State` object for dynamic updates.
    loadingIndicator : State, str, QWidget, or None, optional
        Element shown during loading (default: CircularProgress). Default is None.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the button ("small", "medium", "large"). Default is "medium".
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    margin : State or int, optional
        Custom margin for the button. Default is 9.
        Can be a `State` object for dynamic updates.
    whileTap : State or str, optional
        Effect applied while the button is tapped. Default is "tap".
        Can be a `State` object for dynamic updates.
    whileHover : State or str, optional
        Effect applied while the button is hovered. Default is "hover".
        Can be a `State` object for dynamic updates.
    *args
        Additional positional arguments passed to the parent `Button` class.
    **kwargs
        Additional keyword arguments passed to the parent `Button` class,
        supporting props of the ButtonBase component (e.g., parent, onClick).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for `color`: ["inherit", "default", "primary", "secondary", "error", "info", "success", "warning"].
    VALID_EDGES : list[str | bool]
        Valid values for `edge`: ["start", "end", False].
    VALID_SIZES : list[str]
        Valid values for `size`: ["small", "medium", "large"].

    Notes
    -----
    - Props of the ButtonBase component are supported via `*args` and `**kwargs`.
    - The `loadingIndicator` should contain an element with role="progressbar" for accessibility.
    - Custom properties `margin`, `whileTap`, and `whileHover` are specific to PyMUI.

    Demos:
    - IconButton: https://qtmui.com/material-ui/qtmui-iconbutton/

    API Reference:
    - IconButton API: https://qtmui.com/material-ui/api/icon-button/
    """
    def __init__(
                self,
                # children: Optional[Union[State, str, PyIconify, QWidget]] = None,
                # classes: Optional[Union[State, Dict]] = None,
                color: Union[State, str] = "default",
                # disabled: Union[State, bool] = False,
                # disableFocusRipple: Union[State, bool] = False,
                # disableRipple: Union[State, bool] = False,
                # edge: Union[State, str, bool] = False,
                # loading: Optional[Union[State, bool]] = None,
                # loadingIndicator: Optional[Union[State, str, QWidget]] = None,
                # size: Union[State, str] = "medium",
                # sx: Optional[Union[State, List, Dict, Callable, str]] = None,
                margin: Union[State, int] = 9,
                whileTap: Union[State, str] = "tap",
                whileHover: Union[State, str] = "hover",
                icon: Optional[Union[str, Iconify]] = None,
                *args, **kwargs
                ):
        super().__init__(startIcon=icon, *args, **kwargs) # isFab=True, 

        self._icon = icon
        self._color = color
        self._whileTap = whileTap
        self._whileHover = whileHover
        
        self.___set_stylesheet()
        

    def ___set_stylesheet(self, component_styled=None):
        super()._set_stylesheet()
        
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        stylesheet = f"""
            #{self.objectName()} {{
                border-radius: {"15px" if self._size == "small" else "18px" if self._size == "medium" else "24px"};
            }}

            {sx_qss}
        """
        self.setStyleSheet(self.styleSheet() + stylesheet)


