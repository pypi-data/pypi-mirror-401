from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout
from ..box import Box
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State
from ..utils.validate_params import _validate_param

class AccordionDetails(Box):
    """
    A component that displays the details content of an Accordion.

    The `AccordionDetails` component is used to render the content that is shown or hidden
    when an `Accordion` is expanded or collapsed. It inherits from the `Box` component and
    supports all native props of `Box` via `**kwargs`. It provides customizable styling
    through `classes` and `sx` props, consistent with Material-UI's `AccordionDetails`.

    Parameters
    ----------
    children : State, list, QWidget, or None, optional
        The content of the component, such as text, widgets, or a list of widgets.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        The system prop that allows defining system overrides as well as additional CSS
        styles. Can be a CSS-like string, a dictionary of style properties, a callable
        returning styles, or a `State` object for dynamic styling. Default is None.
    **kwargs
        Additional keyword arguments passed to the parent `Box` class, supporting all
        native props of the `Box` component (e.g., `component`, `display`, `flexDirection`).

    Notes
    -----
    - Props of the native `Box` component are available via `**kwargs`.
    - The component uses the theme's `PyAccordionDetails` styles for default appearance.

    Demos:
    - AccordionDetails: https://qtmui.com/material-ui/qtmui-accordion-details/

    API Reference:
    - AccordionDetails API: https://qtmui.com/material-ui/api/accordion-details/
    """

    def __init__(
        self,
        children: Optional[Union[State, List, QWidget]] = None,
        classes: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(children=children, **kwargs)
        self.setObjectName("AccordionDetails")

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_children(children)
        self._set_classes(classes)
        self._set_sx(sx)

        self.render()

    @_validate_param(file_path="qtmui.material.accordion_details", param_name="children", supported_signatures=Union[State, List, QWidget, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.accordion_details", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.accordion_details", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def render(self):
        self.setLayout(QHBoxLayout())

        """
        Phương thức để render AccordionDetails theo các thuộc tính đã thiết lập.
        """
        # Render nội dung accordion details
        # print(f"Rendering AccordionDetails with children: {self._children}")

        # # Áp dụng các class nếu có
        # if self._classes:
        #     print(f"Applying classes: {self._classes}")

        # # Áp dụng các style thông qua sx
        # if self._sx:
        #     print(f"Applying sx: {self._sx}")

        if self._children:
            if isinstance(self._children, list):
                for widget in self._children:
                    self.layout().addWidget(widget)
            else:
                self.layout().addWidget(self._children)

