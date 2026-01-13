from typing import Optional, Callable,Union

from qtmui.material.py_iconify import Iconify
from qtmui.hooks import State

from .button import Button

class ToggleButton(Button):
    def __init__(
        self,
        icon: Optional[Iconify] = ":/round/resource_qtmui/round/access_time.svg",
        text: Optional[Union[str, State, Callable]] = None,
        value: Optional[object] = None,
        selected: bool = False,
        *args, **kwargs
    ):
        super().__init__(text=text, startIcon=icon, value=value, *args, **kwargs)

        self._selected = selected

        self._setup_toggle_button()

    def _setup_toggle_button(self):
        self.setCheckable(True)  # Toggle button cần có trạng thái check/uncheck

        """Thiết lập trạng thái được chọn của ToggleButton."""
        if self._selected:
            super().set_selected(True)


