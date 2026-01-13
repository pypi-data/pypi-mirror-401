import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QFrame
from PySide6.QtCore import Qt, Signal
from qtmui.hooks import State
from ..button.icon_button import IconButton
from ..button.button import Button
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase
from ..py_iconify import PyIconify, Iconify
from ...qtmui_assets import QTMUI_ASSETS
from ..utils.validate_params import _validate_param

class Pagination(QFrame, PyWidgetBase):
    """
    A component that renders a pagination control, styled like Material-UI Pagination.

    The `Pagination` component allows users to navigate through pages, with support for boundary and sibling pages,
    custom rendering, and accessibility features. It integrates with `Button` and `IconButton` components in the `qtmui`
    framework, retaining all existing parameters and aligning with MUI props.

    Parameters
    ----------
    boundaryCount : State or int, optional
        Number of always visible pages at the beginning and end. Default is 1.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The active color ("primary", "secondary", "standard", or custom). Default is "standard".
        Can be a `State` object for dynamic updates.
    count : State or int, optional
        The total number of pages. Default is 1.
        Can be a `State` object for dynamic updates.
    defaultPage : State or int, optional
        The page selected by default when uncontrolled. Default is 1.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    getItemAriaLabel : State or Callable, optional
        Function returning a user-friendly name for the current page. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (type: str, page: int | None, selected: bool) -> str
    hideNextButton : State or bool, optional
        If True, hide the next-page button. Default is False.
        Can be a `State` object for dynamic updates.
    hidePrevButton : State or bool, optional
        If True, hide the previous-page button. Default is False.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the page changes. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (event: Any, page: int) -> None
    page : State or int, optional
        The current page (starts from 1). Default is None (uses defaultPage).
        Can be a `State` object for dynamic updates.
    renderItem : State or Callable, optional
        Function to render pagination items. Default is None (uses Button/IconButton).
        Can be a `State` object for dynamic updates.
        Signature: (params: Dict) -> QWidget
    shape : State or str, optional
        Shape of pagination items ("circular" or "rounded"). Default is "circular".
        Can be a `State` object for dynamic updates.
    showFirstButton : State or bool, optional
        If True, show the first-page button. Default is False.
        Can be a `State` object for dynamic updates.
    showLastButton : State or bool, optional
        If True, show the last-page button. Default is False.
        Can be a `State` object for dynamic updates.
    siblingCount : State or int, optional
        Number of always visible pages before and after the current page. Default is 1.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        Size of the component ("small", "medium", "large"). Default is "medium".
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Variant of the component ("outlined" or "text"). Default is "text".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., id, className).

    Signals
    -------
    pageChanged : Signal
        Emitted when the page changes, carrying the new page number.

    Notes
    -----
    - All existing parameters from the previous implementation are retained, with `enabled` replaced by `disabled`.
    - Props of the native component are supported via `**kwargs`.
    - The `page` prop starts numbering from 1, consistent with MUI Pagination.
    - MUI classes applied: `MuiPagination-root`, `MuiPagination-outlined`, `MuiPagination-text`.
    - Integrates with `Button`, `IconButton`, and `PyIconify` for consistent styling.

    Demos:
    - Pagination: https://qtmui.com/material-ui/qtmui-pagination/

    API Reference:
    - Pagination API: https://qtmui.com/material-ui/api/pagination/
    """

    pageChanged = Signal(int)

    VALID_COLORS = ["primary", "secondary", "standard"]
    VALID_SHAPES = ["circular", "rounded"]
    VALID_SIZES = ["small", "medium", "large"]
    VALID_VARIANTS = ["outlined", "text"]

    def __init__(
        self,
        boundaryCount: Union[State, int] = 1,
        classes: Optional[Union[State, Dict]] = None,
        color: Union[State, str] = "default",
        count: Union[State, int] = 1,
        defaultPage: Union[State, int] = 1,
        disabled: Union[State, bool] = False,
        getItemAriaLabel: Optional[Union[State, Callable]] = None,
        hideNextButton: Union[State, bool] = False,
        hidePrevButton: Union[State, bool] = False,
        onChange: Optional[Union[State, Callable]] = None,
        page: Optional[Union[State, int]] = None,
        renderItem: Optional[Union[State, Callable]] = None,
        shape: Union[State, str] = "circular",
        showFirstButton: Union[State, bool] = False,
        showLastButton: Union[State, bool] = False,
        siblingCount: Union[State, int] = 1,
        size: Union[State, str] = "medium",
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        variant: Union[State, str] = "text",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"Pagination-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._button_references = []

        # Set properties with validation
        self._set_boundaryCount(boundaryCount)
        self._set_classes(classes)
        self._set_color(color)
        self._set_count(count)
        self._set_defaultPage(defaultPage)
        self._set_disabled(disabled)
        self._set_getItemAriaLabel(getItemAriaLabel)
        self._set_hideNextButton(hideNextButton)
        self._set_hidePrevButton(hidePrevButton)
        self._set_onChange(onChange)
        self._set_page(page)
        self._set_renderItem(renderItem)
        self._set_shape(shape)
        self._set_showFirstButton(showFirstButton)
        self._set_showLastButton(showLastButton)
        self._set_siblingCount(siblingCount)
        self._set_size(size)
        self._set_sx(sx)
        self._set_variant(variant)

        self._current_page = self._get_page() or self._get_defaultPage()

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="boundaryCount",
        supported_signatures=Union[State, int],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_boundaryCount(self, value):
        """Assign value to boundaryCount."""
        self._boundaryCount = value

    def _get_boundaryCount(self):
        """Get the boundaryCount value."""
        return self._boundaryCount.value if isinstance(self._boundaryCount, State) else self._boundaryCount

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="classes",
        supported_signatures=Union[State, Dict, type(None)]
    )
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="color",
        supported_signatures=Union[State, str]
    )
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="count",
        supported_signatures=Union[State, int],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_count(self, value):
        """Assign value to count."""
        self._count = value

    def _get_count(self):
        """Get the count value."""
        return self._count.value if isinstance(self._count, State) else self._count

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="defaultPage",
        supported_signatures=Union[State, int],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_defaultPage(self, value):
        """Assign value to defaultPage."""
        self._defaultPage = value

    def _get_defaultPage(self):
        """Get the defaultPage value."""
        return self._defaultPage.value if isinstance(self._defaultPage, State) else self._defaultPage

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="disabled",
        supported_signatures=Union[State, bool]
    )
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="getItemAriaLabel",
        supported_signatures=Union[State, Callable, type(None)]
    )
    def _set_getItemAriaLabel(self, value):
        """Assign value to getItemAriaLabel."""
        self._getItemAriaLabel = value

    def _get_getItemAriaLabel(self):
        """Get the getItemAriaLabel value."""
        return self._getItemAriaLabel.value if isinstance(self._getItemAriaLabel, State) else self._getItemAriaLabel

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="hideNextButton",
        supported_signatures=Union[State, bool]
    )
    def _set_hideNextButton(self, value):
        """Assign value to hideNextButton."""
        self._hideNextButton = value

    def _get_hideNextButton(self):
        """Get the hideNextButton value."""
        return self._hideNextButton.value if isinstance(self._hideNextButton, State) else self._hideNextButton

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="hidePrevButton",
        supported_signatures=Union[State, bool]
    )
    def _set_hidePrevButton(self, value):
        """Assign value to hidePrevButton."""
        self._hidePrevButton = value

    def _get_hidePrevButton(self):
        """Get the hidePrevButton value."""
        return self._hidePrevButton.value if isinstance(self._hidePrevButton, State) else self._hidePrevButton

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="onChange",
        supported_signatures=Union[State, Callable, type(None)]
    )
    def _set_onChange(self, value):
        """Assign value to onChange."""
        self._onChange = value

    def _get_onChange(self):
        """Get the onChange value."""
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="page",
        supported_signatures=Union[State, int, type(None)],
        validator=lambda x: x > 0 if isinstance(x, int) else True
    )
    def _set_page(self, value):
        """Assign value to page."""
        self._page = value

    def _get_page(self):
        """Get the page value."""
        return self._page.value if isinstance(self._page, State) else self._page

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="renderItem",
        supported_signatures=Union[State, Callable, type(None)]
    )
    def _set_renderItem(self, value):
        """Assign value to renderItem."""
        self._renderItem = value

    def _get_renderItem(self):
        """Get the renderItem value."""
        return self._renderItem.value if isinstance(self._renderItem, State) else self._renderItem

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="shape",
        supported_signatures=Union[State, str],
        valid_values=VALID_SHAPES
    )
    def _set_shape(self, value):
        """Assign value to shape."""
        self._shape = value

    def _get_shape(self):
        """Get the shape value."""
        return self._shape.value if isinstance(self._shape, State) else self._shape

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="showFirstButton",
        supported_signatures=Union[State, bool]
    )
    def _set_showFirstButton(self, value):
        """Assign value to showFirstButton."""
        self._showFirstButton = value

    def _get_showFirstButton(self):
        """Get the showFirstButton value."""
        return self._showFirstButton.value if isinstance(self._showFirstButton, State) else self._showFirstButton

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="showLastButton",
        supported_signatures=Union[State, bool]
    )
    def _set_showLastButton(self, value):
        """Assign value to showLastButton."""
        self._showLastButton = value

    def _get_showLastButton(self):
        """Get the showLastButton value."""
        return self._showLastButton.value if isinstance(self._showLastButton, State) else self._showLastButton

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="siblingCount",
        supported_signatures=Union[State, int],
        validator=lambda x: x >= 0 if isinstance(x, int) else True
    )
    def _set_siblingCount(self, value):
        """Assign value to siblingCount."""
        self._siblingCount = value

    def _get_siblingCount(self):
        """Get the siblingCount value."""
        return self._siblingCount.value if isinstance(self._siblingCount, State) else self._siblingCount

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="size",
        supported_signatures=Union[State, str],
        valid_values=VALID_SIZES
    )
    def _set_size(self, value):
        """Assign value to size."""
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="sx",
        supported_signatures=Union[State, List, Dict, Callable, str, type(None)]
    )
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(
        file_path="qtmui.material.pagination",
        param_name="variant",
        supported_signatures=Union[State, str],
        valid_values=VALID_VARIANTS
    )
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant


    def _init_ui(self):
        self.setObjectName("PyPagination")

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Previous button
        if self._shape == "circular":
            # self.prev_button = IconButton(icon=PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_LEFT), size=self._size, variant="text", color=self._color)
            self.prev_button = IconButton(icon=Iconify(key="ri:arrow-left-s-line"), size=self._size, variant="text", color=self._color)
        else:
            self.prev_button = Button(startIcon=Iconify(key="ri:arrow-left-s-line"), size=self._size, variant="text", color=self._color)

        self.prev_button.clicked.connect(self.prev_page)
        self.layout().addWidget(self.prev_button)

        # Next button
        if self._shape == "circular":
            # self.next_button = IconButton(icon=PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_RIGHT), size=self._size, variant="text", color=self._color)
            self.next_button = IconButton(icon=Iconify(key="ri:arrow-right-s-line"), size=self._size, variant="text", color=self._color)
        else:
            # self.next_button = Button(startIcon=PyIconify(key=QTMUI_ASSETS.ICONS.ARROW_RIGHT), size=self._size, variant="text", color=self._color)
            self.next_button = Button(startIcon=Iconify(key="ri:arrow-right-s-line"), size=self._size, variant="text", color=self._color)

        self.next_button.clicked.connect(self.next_page)

        # Page buttons
        self.page_buttons = []
        self.create_page_buttons()

        self.update_buttons()

        # self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyPagination_styles_root_qss = get_qss_style(component_styles["PyPagination"].get("styles")["root"][self._color])
        # print('PyPagination_styles_root_qss___________', PyPagination_styles_root_qss)

        for button in self.page_buttons:
            if isinstance(button, Button):
                if (button.text().isdigit() and int(button.text()) == self._current_page) :
                    button.set_selected(True)
                else:
                    button.set_selected(False)


    def create_page_buttons(self):
        # Clear existing buttons
        for btn in self.page_buttons:
            self.layout().removeWidget(btn)
            btn.deleteLater()
        self.page_buttons.clear()

        # Create page buttons
        if self._count <= 7:
            pages = range(1, self._count + 1)
        else:
            if self._current_page <= 4:
                pages = list(range(1, 6)) + ["..."] + [self._count]
            elif self._current_page > self._count - 4:
                pages = [1] + ["..."] + list(range(self._count - 4, self._count + 1))
            else:
                pages = [1] + ["..."] + list(range(self._current_page - 1, self._current_page + 2)) + ["..."] + [self._count]

        for page in pages:
            if page == "...":
                btn = QLabel(page)
                btn.setAlignment(Qt.AlignCenter)
            else:
                btn = Button(
                    text=str(page), 
                    size=self._size, 
                    variant=self._variant, 
                    color=self._color, 
                    sx=f"""
                        Button {{
                            border-radius: {"15px" if self._size == "small" else "18px" if self._size == "medium" else "24px"};
                        }}
                    """
                )
                btn.setMinimumWidth(30 if self._size == "small" else 36)
                btn.clicked.connect(lambda p=page: self.go_to_page(p))
            self.layout().addWidget(btn)
            self.page_buttons.append(btn)
        self.layout().insertWidget(-1, self.next_button)

        self._set_stylesheet()


    def update_buttons(self):
        self.create_page_buttons()
        # for btn in self.page_buttons:
        #     try:
        #         if isinstance(btn, Button) and (btn.label.text().isdigit() and int(btn.label.text()) == self._current_page) :
        #             # btn.setStyleSheet("background-color: #1c1c1c; color: white; border-radius: 50%;")
        #             print('zoooooooooooo_____select')
        #             btn.set_selected(True)
        #         elif isinstance(btn, Button) :
        #             # btn.setStyleSheet("")
        #             btn.set_selected(False)
        #     except Exception as e:
        #         print('______666____', btn.text())


        self.prev_button.setEnabled(self._current_page > 1)
        self.next_button.setEnabled(self._current_page < self._count)

    def go_to_page(self, page):
        self._current_page = page
        self.update_buttons()

    def prev_page(self):
        if self._current_page > 1:
            self._current_page -= 1
            self.update_buttons()

    def next_page(self):
        if self._current_page < self._count:
            self._current_page += 1
            self.update_buttons()


