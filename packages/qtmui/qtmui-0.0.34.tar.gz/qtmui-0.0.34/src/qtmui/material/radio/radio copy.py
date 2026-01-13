import asyncio
from typing import Callable, Optional, Union
from PySide6.QtWidgets import QCheckBox, QRadioButton
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, Signal, QSize, QTimer

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from ..system.color_manipulator import hex_string_to_qcolor

from ..button.button import Button
from qtmui.hooks import State

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class Radio(Button):
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
                id: str = None,
                checked: bool = False,
                icon: str = None,
                checkedIcon: str = None,
                color: str = "default",
                name: str = None,
                onChange: Callable = None,
                text: Optional[Union[str, State, Callable]] = None,
                value: object = None,
                hightLight: bool = False,
                *args, **kwargs
                ):
        super().__init__(color=color, startIcon="", text="", variant="text", componentType="RadioButton", *args, **kwargs)

        self._id = id
        self._icon = icon
        
        self._color = color
        self._checked = checked
        self._checkedIcon = checkedIcon
        self._onChange = onChange
        self._name = name
        self._value = value
        self._indicator_color_checked = None

        self.__init_ui()

    def __init_ui(self):
        if self._id:
            self.setObjectName(self._id)

        self.clicked.connect(self.onClick)

        if isinstance(self._checked, State):
            self._checked.valueChanged.connect(self._setChecked)
            self._checkedValue = self._checked.value
        else:
            self._checkedValue = self._checked
        
        self._setChecked(self._checkedValue)
        
        self.setFixedSize(QSize(30, 30) if self._size == "small" else QSize(36, 36))
        
    
    def onClick(self):
        self.changed.emit(self)
        self._checkedValue = True
        if self._onChange:
            self._onChange(self)
        self.update()

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value: bool):
        # if self._checked != value:
        self._checked = value
        self._setStyleSheet()
        self.update()  # Gọi lại để cập nhật giao diện

    def _setChecked(self, value: bool):
        # if self._checked != value:
        self._checkedValue = value
        # self.set_radio_theme()
        self.update()  # Gọi lại để cập nhật giao diện

    def paintEvent(self, event):
        super().paintEvent(event)
        if not hasattr(self, "theme"):
            self.theme = useTheme()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self._indicator_color_checked:
            self._indicator_color_checked = self.theme.components[f"PyRadio"].get("styles")["root"](self._kwargs)[self._color]["color"]

        if self._checkedValue:
            # if theme.components.get('MuiCheckbox'):
            #     padding = theme.components[f"MuiCheckbox"]["styleOverrides"]["root"]

            self.border = 2
            self.padding = 6 if self._size == "small" else 8

            rect = self.rect().adjusted(self.padding, self.padding, -self.padding, -self.padding)
            height = rect.height()
            center_point = rect.x() 
            circle_diameter = height
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor(self._indicator_color_checked), self.border))
            painter.drawEllipse(center_point - 1, center_point, circle_diameter, circle_diameter)

            self.padding = self.padding + 4
            rect = self.rect().adjusted(self.padding, self.padding, -self.padding, -self.padding)
            height = rect.height()
            center_point = rect.x()
            circle_diameter = height
            painter.setPen(Qt.NoPen)
            # painter.setBrush(QBrush(hex_string_to_qcolor(self._indicator_color_checked)))
            painter.setBrush(QColor(self._indicator_color_checked))
            painter.drawEllipse(center_point - 1, center_point, circle_diameter, circle_diameter)
        else:
            # if theme.components.get('MuiCheckbox'):
            #     padding = theme.components[f"MuiCheckbox"]["styleOverrides"]["root"]

            self.border = 1
            self.padding = 6 if self._size == "small" else 8

            rect = self.rect().adjusted(self.padding, self.padding, -self.padding, -self.padding)
            height = rect.height()
            center_point = rect.x()
            circle_diameter = height
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(hex_string_to_qcolor(self.theme.palette.text.secondary), self.border))
            painter.drawEllipse(center_point -1, center_point, circle_diameter, circle_diameter)

        painter.end()