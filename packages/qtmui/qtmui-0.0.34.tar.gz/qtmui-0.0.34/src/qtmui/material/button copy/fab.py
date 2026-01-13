import asyncio
from typing import Callable, Dict, List, Optional, Union

from qtmui.hooks import State
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer

from qtmui.material.styles import useTheme

from .button import Button
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class Fab(Button):
    """
    A Floating Action Button (FAB) component based on Material-UI's Fab.

    The `Fab` component extends the `Button` component to provide a floating action button
    with circular or extended styling, supporting all props of the Material-UI `Fab` component,
    as well as additional custom props.

    Parameters
    ----------
    icon : State, str, or None, optional
        The icon to display (custom feature, not part of Material-UI). Maps to `startIcon`.
        Default is None.
        Can be a `State` object for dynamic updates.
    animate : State or bool, optional
        If True, applies a rotation animation (custom feature, not part of Material-UI).
        Default is False.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically an icon or text. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component ("default", "error", "info", "inherit", "primary",
        "secondary", "success", "warning", or custom string). Default is "default".
        Can be a `State` object for dynamic updates.
    component : State, str, or None, optional
        The component used for the root node (e.g., "QPushButton"). Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableFocusRipple : State or bool, optional
        If True, the keyboard focus ripple is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If True, the ripple effect is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    href : State, str, or None, optional
        The URL to link to when the button is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the component ("small", "medium", "large", or custom string).
        Default is "large".
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The variant to use ("circular", "extended", or custom string). Default is "circular".
        Can be a `State` object for dynamic updates.
    *args
        Additional positional arguments passed to the parent `Button` class.
    **kwargs
        Additional keyword arguments passed to the parent `Button` class, supporting
        props of the `ButtonBase` component (e.g., onClick, style).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for `color`: ["default", "error", "info", "inherit", "primary",
        "secondary", "success", "warning"].
    VALID_SIZES : list[str]
        Valid values for `size`: ["small", "medium", "large"].
    VALID_VARIANTS : list[str]
        Valid values for `variant`: ["circular", "extended"].

    Notes
    -----
    - Props of the `ButtonBase` component are supported via `**kwargs` (e.g., `onClick`, `style`).
    - The `icon` and `animate` parameters are custom features, not part of Material-UI's `Fab`.
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - Fab: https://qtmui.com/material-ui/qtmui-fab/

    API Reference:
    - Fab API: https://qtmui.com/material-ui/api/fab/
    """

    def __init__(
                self,
                icon: Optional[Union[State, str]] = None,
                animate: Union[State, bool] = False,
                # children: Optional[Union[State, QWidget, List[QWidget]]] = None,
                # classes: Optional[Union[State, Dict]] = None,
                # color: Union[State, str] = "default",
                # component: Optional[Union[State, str]] = None,
                # disabled: Union[State, bool] = False,
                # disableFocusRipple: Union[State, bool] = False,
                # disableRipple: Union[State, bool] = False,
                # href: Optional[Union[State, str]] = None,
                # size: Union[State, str] = "large",
                sx: Optional[Union[State, Dict, Callable, str]] = None,
                # variant: Union[State, str] = "circular",
                *args,
                **kwargs
                ):
        super().__init__(startIcon=icon, *args, **kwargs)

        self._sx = sx
        self._kwargs = kwargs
        self._animate = animate

    def _set_stylesheet(self, component_styled=None):
        super()._set_stylesheet()

        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        MuiButtonSize_styles_root_qss = get_qss_style(component_styled["PyFab"].get("styles")["root"]["props"][f"{self._size}Size"])

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
                {MuiButtonSize_styles_root_qss}
            }}

            {sx_qss}
        """

        self.setStyleSheet(self.styleSheet() + stylesheet)
