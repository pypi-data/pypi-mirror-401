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
from ..._____assets import ASSETS
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
        color: Union[State, str] = "standard",
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
        self._set_stylesheet()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._connect_signals()

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
        """Initialize the UI based on props."""
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.theme.spacing(1))
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Clear existing buttons
        self._button_references.clear()

        # First button
        if self._get_showFirstButton():
            first_button = IconButton(
                icon=Iconify(key=ASSETS.ICONS.DOUBLE_ARROW_LEFT),
                size=self._get_size(),
                variant="text",
                color=self._get_color(),
                disabled=self._get_disabled()
            )
            first_button.clicked.connect(lambda: self.go_to_page(1))
            self.layout().addWidget(first_button)
            self._button_references.append(first_button)
            self._set_aria_label(first_button, "first")

        # Previous button
        if not self._get_hidePrevButton():
            prev_button = IconButton(
                icon=Iconify(key=ASSETS.ICONS.ARROW_LEFT),
                size=self._get_size(),
                variant="text",
                color=self._get_color(),
                disabled=self._get_disabled()
            ) if self._get_shape() == "circular" else Button(
                startIcon=PyIconify(key=ASSETS.ICONS.ARROW_LEFT),
                size=self._get_size(),
                variant="text",
                color=self._get_color(),
                disabled=self._get_disabled()
            )
            prev_button.clicked.connect(self.prev_page)
            self.layout().addWidget(prev_button)
            self._button_references.append(prev_button)
            self._set_aria_label(prev_button, "previous")
            self.prev_button = prev_button

        # Page buttons
        self.page_buttons = []
        self.create_page_buttons()

        # Next button
        if not self._get_hideNextButton():
            next_button = IconButton(
                icon=Iconify(key=ASSETS.ICONS.ARROW_RIGHT),
                size=self._get_size(),
                variant="text",
                color=self._get_color(),
                disabled=self._get_disabled()
            ) if self._get_shape() == "circular" else Button(
                startIcon=PyIconify(key=ASSETS.ICONS.ARROW_RIGHT),
                size=self._get_size(),
                variant="text",
                color=self._get_color(),
                disabled=self._get_disabled()
            )
            next_button.clicked.connect(self.next_page)
            self.layout().addWidget(next_button)
            self._button_references.append(next_button)
            self._set_aria_label(next_button, "next")
            self.next_button = next_button

        # Last button
        if self._get_showLastButton():
            last_button = IconButton(
                icon=Iconify(key=ASSETS.ICONS.DOUBLE_ARROW_RIGHT),
                size=self._get_size(),
                variant="text",
                color=self._get_color(),
                disabled=self._get_disabled()
            )
            last_button.clicked.connect(lambda: self.go_to_page(self._get_count()))
            self.layout().addWidget(last_button)
            self._button_references.append(last_button)
            self._set_aria_label(last_button, "last")

        self.update_buttons()

    def _set_aria_label(self, button, item_type):
        """Set accessible name for a button using getItemAriaLabel."""
        get_aria_label = self._get_getItemAriaLabel()
        if get_aria_label:
            page = {
                "first": 1,
                "last": self._get_count(),
                "next": min(self._current_page + 1, self._get_count()),
                "previous": max(self._current_page - 1, 1),
            }.get(item_type, self._current_page)
            selected = (page == self._current_page) if item_type == "page" else False
            button.setAccessibleName(get_aria_label(item_type, page, selected))

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the Pagination."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        pagination_styles = component_styled.get("Pagination", {}).get("styles", {})
        root_styles = pagination_styles.get("root", {})
        root_qss = get_qss_style(root_styles)

        # Handle sx
        sx = self._get_sx()
        sx_qss = ""
        if sx:
            if isinstance(sx, (list, dict)):
                sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
            elif isinstance(sx, Callable):
                sx_result = sx()
                if isinstance(sx_result, (list, dict)):
                    sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
                elif isinstance(sx_result, str):
                    sx_qss = sx_result
            elif isinstance(sx, str) and sx != "":
                sx_qss = sx

        # Handle classes
        classes = self._get_classes()
        classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

        # Apply MUI classes
        mui_classes = ["MuiPagination-root"]
        if self._get_variant() == "outlined":
            mui_classes.append("MuiPagination-outlined")
        else:
            mui_classes.append("MuiPagination-text")

        # Apply variant
        variant_qss = "border: 1px solid rgba(0, 0, 0, 0.23);" if self._get_variant() == "outlined" else ""

        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                {classes_qss}
                {variant_qss}
            }}
            #{self.objectName()}:disabled {{
                opacity: 0.5;
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def create_page_buttons(self):
        """Create page buttons based on boundaryCount and siblingCount."""
        for btn in self.page_buttons:
            self.layout().removeWidget(btn)
            btn.deleteLater()
        self.page_buttons.clear()

        count = self._get_count()
        boundary_count = self._get_boundaryCount()
        sibling_count = self._get_siblingCount()
        current_page = self._current_page

        # Calculate pages to display
        pages = []
        start_pages = list(range(1, min(boundary_count + 1, count + 1)))
        end_pages = list(range(max(count - boundary_count + 1, 1), count + 1))
        sibling_start = max(boundary_count + 1, current_page - sibling_count)
        sibling_end = min(current_page + sibling_count, count - boundary_count)

        # Add start pages
        pages.extend(start_pages)

        # Add ellipsis after start pages
        if sibling_start > boundary_count + 2:
            pages.append("...")

        # Add sibling pages
        pages.extend(range(sibling_start, sibling_end + 1))

        # Add ellipsis before end pages
        if sibling_end < count - boundary_count - 1:
            pages.append("...")

        # Add end pages
        pages.extend(end_pages[max(0, len(end_pages) - boundary_count):])

        # Remove duplicates while preserving order
        seen = set()
        pages = [p for p in pages if not (p in seen or seen.add(p))]

        render_item = self._get_renderItem()
        for page in pages:
            if page == "...":
                btn = QLabel("...")
                btn.setAlignment(Qt.AlignCenter)
            else:
                params = {
                    "text": str(page),
                    "size": self._get_size(),
                    "variant": self._get_variant(),
                    "color": self._get_color(),
                    "sx": {
                        "border-radius": "15px" if self._get_size() == "small" else "18px" if self._get_size() == "medium" else "24px"
                    },
                    "disabled": self._get_disabled(),
                    "selected": page == current_page
                }
                btn = render_item(params) if render_item else Button(**params)
                btn.setMinimumWidth(30 if self._get_size() == "small" else 36)
                btn.clicked.connect(lambda p=page: self.go_to_page(p))
                self._set_aria_label(btn, "page")
            self.layout().addWidget(btn)
            self.page_buttons.append(btn)

    def update_buttons(self):
        """Update the state of pagination buttons."""
        for btn in self.page_buttons:
            if isinstance(btn, Button) and btn.text().isdigit():
                btn.set_selected(int(btn.text()) == self._current_page)
        if hasattr(self, "prev_button"):
            self.prev_button.setEnabled(not self._get_disabled() and self._current_page > 1)
        if hasattr(self, "next_button"):
            self.next_button.setEnabled(not self._get_disabled() and self._current_page < self._get_count())

    def go_to_page(self, page):
        """Navigate to a specific page."""
        if not self._get_disabled() and 1 <= page <= self._get_count():
            self._current_page = page
            self.update_buttons()
            if self._get_onChange():
                self._get_onChange()(None, page)
            self.pageChanged.emit(page)

    def prev_page(self):
        """Navigate to the previous page."""
        if not self._get_disabled() and self._current_page > 1:
            self._current_page -= 1
            self.update_buttons()
            if self._get_onChange():
                self._get_onChange()(None, self._current_page)
            self.pageChanged.emit(self._current_page)

    def next_page(self):
        """Navigate to the next page."""
        if not self._get_disabled() and self._current_page < self._get_count():
            self._current_page += 1
            self.update_buttons()
            if self._get_onChange():
                self._get_onChange()(None, self._current_page)
            self.pageChanged.emit(self._current_page)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._boundaryCount, State):
            self._boundaryCount.valueChanged.connect(self._on_boundaryCount_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.connect(self._on_color_changed)
        if isinstance(self._count, State):
            self._count.valueChanged.connect(self._on_count_changed)
        if isinstance(self._defaultPage, State):
            self._defaultPage.valueChanged.connect(self._on_defaultPage_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.connect(self._on_disabled_changed)
        if isinstance(self._getItemAriaLabel, State):
            self._getItemAriaLabel.valueChanged.connect(self._on_getItemAriaLabel_changed)
        if isinstance(self._hideNextButton, State):
            self._hideNextButton.valueChanged.connect(self._on_hideNextButton_changed)
        if isinstance(self._hidePrevButton, State):
            self._hidePrevButton.valueChanged.connect(self._on_hidePrevButton_changed)
        if isinstance(self._onChange, State):
            self._onChange.valueChanged.connect(self._on_onChange_changed)
        if isinstance(self._page, State):
            self._page.valueChanged.connect(self._on_page_changed)
        if isinstance(self._renderItem, State):
            self._renderItem.valueChanged.connect(self._on_renderItem_changed)
        if isinstance(self._shape, State):
            self._shape.valueChanged.connect(self._on_shape_changed)
        if isinstance(self._showFirstButton, State):
            self._showFirstButton.valueChanged.connect(self._on_showFirstButton_changed)
        if isinstance(self._showLastButton, State):
            self._showLastButton.valueChanged.connect(self._on_showLastButton_changed)
        if isinstance(self._siblingCount, State):
            self._siblingCount.valueChanged.connect(self._on_siblingCount_changed)
        if isinstance(self._size, State):
            self._size.valueChanged.connect(self._on_size_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.connect(self._on_variant_changed)

    def _on_boundaryCount_changed(self):
        """Handle changes to boundaryCount."""
        self._set_boundaryCount(self._boundaryCount)
        self.create_page_buttons()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_color_changed(self):
        """Handle changes to color."""
        self._set_color(self._color)
        self._init_ui()

    def _on_count_changed(self):
        """Handle changes to count."""
        self._set_count(self._count)
        self.create_page_buttons()

    def _on_defaultPage_changed(self):
        """Handle changes to defaultPage."""
        self._set_defaultPage(self._defaultPage)
        if not self._get_page():
            self._current_page = self._get_defaultPage()
            self.update_buttons()

    def _on_disabled_changed(self):
        """Handle changes to disabled."""
        self._set_disabled(self._disabled)
        self._init_ui()

    def _on_getItemAriaLabel_changed(self):
        """Handle changes to getItemAriaLabel."""
        self._set_getItemAriaLabel(self._getItemAriaLabel)
        self._init_ui()

    def _on_hideNextButton_changed(self):
        """Handle changes to hideNextButton."""
        self._set_hideNextButton(self._hideNextButton)
        self._init_ui()

    def _on_hidePrevButton_changed(self):
        """Handle changes to hidePrevButton."""
        self._set_hidePrevButton(self._hidePrevButton)
        self._init_ui()

    def _on_onChange_changed(self):
        """Handle changes to onChange."""
        self._set_onChange(self._onChange)

    def _on_page_changed(self):
        """Handle changes to page."""
        self._set_page(self._page)
        self._current_page = self._get_page() or self._get_defaultPage()
        self.update_buttons()

    def _on_renderItem_changed(self):
        """Handle changes to renderItem."""
        self._set_renderItem(self._renderItem)
        self.create_page_buttons()

    def _on_shape_changed(self):
        """Handle changes to shape."""
        self._set_shape(self._shape)
        self._init_ui()

    def _on_showFirstButton_changed(self):
        """Handle changes to showFirstButton."""
        self._set_showFirstButton(self._showFirstButton)
        self._init_ui()

    def _on_showLastButton_changed(self):
        """Handle changes to showLastButton."""
        self._set_showLastButton(self._showLastButton)
        self._init_ui()

    def _on_siblingCount_changed(self):
        """Handle changes to siblingCount."""
        self._set_siblingCount(self._siblingCount)
        self.create_page_buttons()

    def _on_size_changed(self):
        """Handle changes to size."""
        self._set_size(self._size)
        self._init_ui()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_variant_changed(self):
        """Handle changes to variant."""
        self._set_variant(self._variant)
        self._set_stylesheet()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._boundaryCount, State):
            self._boundaryCount.valueChanged.disconnect(self._on_boundaryCount_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.disconnect(self._on_color_changed)
        if isinstance(self._count, State):
            self._count.valueChanged.disconnect(self._on_count_changed)
        if isinstance(self._defaultPage, State):
            self._defaultPage.valueChanged.disconnect(self._on_defaultPage_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.disconnect(self._on_disabled_changed)
        if isinstance(self._getItemAriaLabel, State):
            self._getItemAriaLabel.valueChanged.disconnect(self._on_getItemAriaLabel_changed)
        if isinstance(self._hideNextButton, State):
            self._hideNextButton.valueChanged.disconnect(self._on_hideNextButton_changed)
        if isinstance(self._hidePrevButton, State):
            self._hidePrevButton.valueChanged.disconnect(self._on_hidePrevButton_changed)
        if isinstance(self._onChange, State):
            self._onChange.valueChanged.disconnect(self._on_onChange_changed)
        if isinstance(self._page, State):
            self._page.valueChanged.disconnect(self._on_page_changed)
        if isinstance(self._renderItem, State):
            self._renderItem.valueChanged.disconnect(self._on_renderItem_changed)
        if isinstance(self._shape, State):
            self._shape.valueChanged.disconnect(self._on_shape_changed)
        if isinstance(self._showFirstButton, State):
            self._showFirstButton.valueChanged.disconnect(self._on_showFirstButton_changed)
        if isinstance(self._showLastButton, State):
            self._showLastButton.valueChanged.disconnect(self._on_showLastButton_changed)
        if isinstance(self._siblingCount, State):
            self._siblingCount.valueChanged.disconnect(self._on_siblingCount_changed)
        if isinstance(self._size, State):
            self._size.valueChanged.disconnect(self._on_size_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.disconnect(self._on_variant_changed)