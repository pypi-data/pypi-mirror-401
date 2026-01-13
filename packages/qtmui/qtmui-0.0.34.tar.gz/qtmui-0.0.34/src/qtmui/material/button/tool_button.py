from PySide6.QtCore import Qt, QSize

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor

from ..py_tool_button.py_tool_button import Iconify
from .button import Button
from ...common.icon import FluentIconBase

class IconButton(Button):
    """
    LoadingButton
    Base Button

    Args:
        loading?: True | False
        loadingPosition?: "start" | "center" | "end"
        loadingIndicator?: "Loading..." | any str

    Returns:
        new instance of LoadingButton
    """
    def __init__(self,
                icon: str,
                edge: str = "end",
                margin: int = 9,
                color: str = "inherit",
                whileTap: str = "tap",
                whileHover: str = "hover",
                *args, **kwargs
                ):
        super().__init__(color=color, startIcon=icon, *args, **kwargs)

        self._icon = icon
        self._color = color
        self._whileTap = whileTap
        self._whileHover = whileHover

        # self.layout().addWidget(icon)
        # self.layout().setContentsMargins(0,0,9,0)
        stylesheet = f"""
            QPushButton {{
                background-color: transparent;
            }}
        """
        # self.setStyleSheet(self.styleSheet() + stylesheet)
        # self.autorun_set_icon()

    def set_icon(self, theme):
        pass
        is_light_mode = theme.palette.mode == 'light'
        if self._color in ['primary', 'secondary', 'info', 'success', 'warning', 'error']:
            palette_color: PaletteColor = getattr(theme.palette, self._color)
            self._icon_color = palette_color.light if is_light_mode else palette_color.dark
        else: # inherit
            self._icon_color = theme.palette.grey._800 if is_light_mode else theme.palette.common.white
        # print("self._color________", self._icon_color)
        self.setIcon(FluentIconBase().icon_(path=self._icon, color=self._icon_color))
        self.setIconSize(QSize(18, 18))

