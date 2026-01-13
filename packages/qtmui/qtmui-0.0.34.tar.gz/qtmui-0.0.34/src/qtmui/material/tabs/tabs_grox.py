from functools import lru_cache
from typing import Any, Callable, Optional, Union, Dict, List
import uuid
from PyQt5.QtWidgets import QTabWidget, QTabBar, QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QCursor
from ...material.system.color_manipulator import alpha
from ...base.widget_base import PyWidgetBase
from qtmui.hooks import State
from qtmui.hooks.use_theme import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ...utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ...components.typography import Typography
from ...components.py_iconify import PyIconify
from ...components.box import Box
from .tab import Tab

class Tabs(QTabWidget, PyWidgetBase):
    """
    A tabs component, styled like Material-UI Tabs.

    The `Tabs` component manages a group of tabs with scrollable or centered layouts, aligning with
    MUI Tabs props. Inherits from native component props.

    Parameters
    ----------
    justifyContent : State, str, or None, optional
        Alignment of tabs ('flex-start', 'flex-end', qtmui-specific). Default is 'flex-start'.
        Can be a `State` object for dynamic updates.
    orientation : State, str, or None, optional
        Orientation of the tab bar ('horizontal', 'vertical'). Default is 'horizontal'.
        Can be a `State` object for dynamic updates.
    value : State, Any, or None, optional
        Value of the selected tab. Default is None.
        Can be a `State` object for dynamic updates.
    onChange : State, Callable, or None, optional
        Callback fired when the selected tab changes. Default is None.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, tabs use all available space (qtmui-specific). Default is True.
        Can be a `State` object for dynamic updates.
    fixedHeight : State, int, or None, optional
        Fixed height of the tab widget (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    minWidth : State or bool, optional
        If True, sets minimum width (qtmui-specific). Default is True.
        Can be a `State` object for dynamic updates.
    children : State, List[QWidget], QWidget, or None, optional
        Content of the tabs (typically Tab components). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    action : State, Any, or None, optional
        Callback for programmatic actions (updateIndicator, updateScrollButtons). Default is None.
        Can be a `State` object for dynamic updates.
    allowScrollButtonsMobile : State or bool, optional
        If True, scroll buttons are shown on mobile. Default is False.
        Can be a `State` object for dynamic updates.
    aria_label : State, str, or None, optional
        ARIA label for the Tabs. Default is None.
        Can be a `State` object for dynamic updates.
    aria_labelledby : State, str, or None, optional
        ARIA labelledby for the Tabs. Default is None.
        Can be a `State` object for dynamic updates.
    centered : State or bool, optional
        If True, tabs are centered. Default is False.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, str, or None, optional
        Component for the root node. Default is None.
        Can be a `State` object for dynamic updates.
    indicatorColor : State, str, or None, optional
        Color of the tab indicator ('primary', 'secondary', or custom). Default is 'primary'.
        Can be a `State` object for dynamic updates.
    scrollButtons : State, str, or bool, optional
        Behavior of scroll buttons ('auto', True, False). Default is 'auto'.
        Can be a `State` object for dynamic updates.
    selectionFollowsFocus : State or bool, optional
        If True, tab selection follows focus. Default is False.
        Can be a `State` object for dynamic updates.
    slotProps : State or Dict, optional
        Props for each slot (indicator, scrollButtons, etc.). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or Dict, optional
        Components for each slot (indicator, scrollButtons, etc.). Default is None.
        Can be a `State` object for dynamic updates.
    TabIndicatorProps : State or Dict, optional
        Props for tab indicator (deprecated, use slotProps.indicator). Default is None.
        Can be a `State` object for dynamic updates.
    TabScrollButtonProps : State or Dict, optional
        Props for scroll buttons (deprecated, use slotProps.scrollButtons). Default is None.
        Can be a `State` object for dynamic updates.
    textColor : State, str, or None, optional
        Color of tab text ('inherit', 'primary', 'secondary'). Default is 'primary'.
        Can be a `State` object for dynamic updates.
    variant : State, str, or None, optional
        Display behavior ('fullWidth', 'scrollable', 'standard'). Default is 'standard'.
        Can be a `State` object for dynamic updates.
    visibleScrollbar : State or bool, optional
        If True, scrollbar is visible. Default is False.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QTabWidget, supporting native props.

    Signals
    -------
    currentChanged : Signal(int)
        Emitted when the selected tab changes.

    Notes
    -----
    - `justifyContent`, `fixedHeight`, `minWidth` are qtmui-specific features.
    - `ScrollButtonComponent`, `TabIndicatorProps`, `TabScrollButtonProps` are deprecated; use `slotProps` and `slots`.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiTabs-root`.

    Demos:
    - Tabs: https://qtmui.com/material-ui/qtmui-tabs/

    API Reference:
    - Tabs API: https://qtmui.com/material-ui/api/tabs/
    """

    VALID_ORIENTATIONS = ['horizontal', 'vertical']
    VALID_COLORS = ['primary', 'secondary', 'inherit']
    VALID_VARIANTS = ['fullWidth', 'scrollable', 'standard']
    VALID_SCROLL_BUTTONS = ['auto', True, False]

    def __init__(
        self,
        justifyContent: Optional[Union[State, str, None]]="flex-start",
        orientation: Optional[Union[State, str, None]]="horizontal",
        value: Optional[Union[State, Any, None]]=None,
        onChange: Optional[Union[State, Callable, None]]=None,
        fullWidth: Union[State, bool]=True,
        fixedHeight: Optional[Union[State, int, None]]=None,
        minWidth: Union[State, bool]=True,
        children: Optional[Union[State, List[QWidget], QWidget, None]]=None,
        sx: Optional[Union[State, List, Dict, Callable, None]]=None,
        action: Optional[Union[State, Any, None]]=None,
        allowScrollButtonsMobile: Union[State, bool]=False,
        aria_label: Optional[Union[State, str, None]]=None,
        aria_labelledby: Optional[Union[State, str, None]]=None,
        centered: Union[State, bool]=False,
        classes: Optional[Union[State, Dict, None]]=None,
        component: Optional[Union[State, str, None]]=None,
        indicatorColor: Optional[Union[State, str, None]]="primary",
        scrollButtons: Union[State, str, bool]="auto",
        selectionFollowsFocus: Union[State, bool]=False,
        slotProps: Optional[Union[State, Dict, None]]=None,
        slots: Optional[Union[State, Dict, None]]=None,
        TabIndicatorProps: Optional[Union[State, Dict, None]]=None,
        TabScrollButtonProps: Optional[Union[State, Dict, None]]=None,
        textColor: Optional[Union[State, str, None]]="primary",
        variant: Optional[Union[State, str, None]]="standard",
        visibleScrollbar: Union[State, bool]=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(str(uuid.uuid4()))
        PyWidgetBase._setUpUi(self)
        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_justifyContent(justifyContent)
        self._set_orientation(orientation)
        self._set_value(value)
        self._set_onChange(onChange)
        self._set_fullWidth(fullWidth)
        self._set_fixedHeight(fixedHeight)
        self._set_minWidth(minWidth)
        self._set_children(children)
        self._set_sx(sx)
        self._set_action(action)
        self._set_allowScrollButtonsMobile(allowScrollButtonsMobile)
        self._set_aria_label(aria_label)
        self._set_aria_labelledby(aria_labelledby)
        self._set_centered(centered)
        self._set_classes(classes)
        self._set_component(component)
        self._set_indicatorColor(indicatorColor)
        self._set_scrollButtons(scrollButtons)
        self._set_selectionFollowsFocus(selectionFollowsFocus)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_TabIndicatorProps(TabIndicatorProps)
        self._set_TabScrollButtonProps(TabScrollButtonProps)
        self._set_textColor(textColor)
        self._set_variant(variant)
        self._set_visibleScrollbar(visibleScrollbar)

        self.keys = []
        self._init_ui()
        self._set_stylesheet()
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        i18n.langChanged.connect(self.retranslateUi)

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.tabs", param_name="justifyContent", supported_signatures=Union[State, str, type(None)])
    def _set_justifyContent(self, value):
        self._justifyContent = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_justifyContent(self):
        return self._justifyContent.value if isinstance(self._justifyContent, State) else self._justifyContent

    @_validate_param(file_path="qtmui.material.tabs", param_name="orientation", supported_signatures=Union[State, str, type(None)], valid_values=VALID_ORIENTATIONS)
    def _set_orientation(self, value):
        self._orientation = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_orientation(self):
        orientation = self._orientation.value if isinstance(self._orientation, State) else self._orientation
        return orientation if orientation in self.VALID_ORIENTATIONS else 'horizontal'

    @_validate_param(file_path="qtmui.material.tabs", param_name="value", supported_signatures=Union[State, Any, type(None)])
    def _set_value(self, value):
        self._value = value
        if isinstance(value, State):
            value.valueChanged.connect(self.set_current_tab_by_key)

    def _get_value(self):
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.tabs", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        self._onChange = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_onChange(self):
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.tabs", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        self._fullWidth = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_fullWidth(self):
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.tabs", param_name="fixedHeight", supported_signatures=Union[State, int, type(None)])
    def _set_fixedHeight(self, value):
        self._fixedHeight = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_fixedHeight(self):
        return self._fixedHeight.value if isinstance(self._fixedHeight, State) else self._fixedHeight

    @_validate_param(file_path="qtmui.material.tabs", param_name="minWidth", supported_signatures=Union[State, bool])
    def _set_minWidth(self, value):
        self._minWidth = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_minWidth(self):
        return self._minWidth.value if isinstance(self._minWidth, State) else self._minWidth

    @_validate_param(file_path="qtmui.material.tabs", param_name="children", supported_signatures=Union[State, List[QWidget], QWidget, type(None)])
    def _set_children(self, value):
        self._children = value
        if isinstance(value, QWidget):
            self._widget_references.append(value)
        elif isinstance(value, list):
            self._widget_references.extend(value)
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.tabs", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
    def _set_sx(self, value):
        self._sx = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.tabs", param_name="action", supported_signatures=Union[State, Any, type(None)])
    def _set_action(self, value):
        self._action = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_action(self):
        return self._action.value if isinstance(self._action, State) else self._action

    @_validate_param(file_path="qtmui.material.tabs", param_name="allowScrollButtonsMobile", supported_signatures=Union[State, bool])
    def _set_allowScrollButtonsMobile(self, value):
        self._allowScrollButtonsMobile = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_allowScrollButtonsMobile(self):
        return self._allowScrollButtonsMobile.value if isinstance(self._allowScrollButtonsMobile, State) else self._allowScrollButtonsMobile

    @_validate_param(file_path="qtmui.material.tabs", param_name="aria_label", supported_signatures=Union[State, str, type(None)])
    def _set_aria_label(self, value):
        self._aria_label = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_aria_label(self):
        return self._aria_label.value if isinstance(self._aria_label, State) else self._aria_label

    @_validate_param(file_path="qtmui.material.tabs", param_name="aria_labelledby", supported_signatures=Union[State, str, type(None)])
    def _set_aria_labelledby(self, value):
        self._aria_labelledby = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_aria_labelledby(self):
        return self._aria_labelledby.value if isinstance(self._aria_labelledby, State) else self._aria_labelledby

    @_validate_param(file_path="qtmui.material.tabs", param_name="centered", supported_signatures=Union[State, bool])
    def _set_centered(self, value):
        self._centered = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_centered(self):
        return self._centered.value if isinstance(self._centered, State) else self._centered

    @_validate_param(file_path="qtmui.material.tabs", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.tabs", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        self._component = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.tabs", param_name="indicatorColor", supported_signatures=Union[State, str, type(None)], valid_values=VALID_COLORS)
    def _set_indicatorColor(self, value):
        self._indicatorColor = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_indicatorColor(self):
        color = self._indicatorColor.value if isinstance(self._indicatorColor, State) else self._indicatorColor
        return color if color in self.VALID_COLORS or isinstance(color, str) else 'primary'

    @_validate_param(file_path="qtmui.material.tabs", param_name="scrollButtons", supported_signatures=Union[State, str, bool], valid_values=VALID_SCROLL_BUTTONS)
    def _set_scrollButtons(self, value):
        self._scrollButtons = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_scrollButtons(self):
        scroll = self._scrollButtons.value if isinstance(self._scrollButtons, State) else self._scrollButtons
        return scroll if scroll in self.VALID_SCROLL_BUTTONS else 'auto'

    @_validate_param(file_path="qtmui.material.tabs", param_name="selectionFollowsFocus", supported_signatures=Union[State, bool])
    def _set_selectionFollowsFocus(self, value):
        self._selectionFollowsFocus = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_selectionFollowsFocus(self):
        return self._selectionFollowsFocus.value if isinstance(self._selectionFollowsFocus, State) else self._selectionFollowsFocus

    @_validate_param(file_path="qtmui.material.tabs", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.tabs", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.tabs", param_name="TabIndicatorProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TabIndicatorProps(self, value):
        self._TabIndicatorProps = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_TabIndicatorProps(self):
        return self._TabIndicatorProps.value if isinstance(self._TabIndicatorProps, State) else self._TabIndicatorProps

    @_validate_param(file_path="qtmui.material.tabs", param_name="TabScrollButtonProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TabScrollButtonProps(self, value):
        self._TabScrollButtonProps = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_TabScrollButtonProps(self):
        return self._TabScrollButtonProps.value if isinstance(self._TabScrollButtonProps, State) else self._TabScrollButtonProps

    @_validate_param(file_path="qtmui.material.tabs", param_name="textColor", supported_signatures=Union[State, str, type(None)], valid_values=VALID_COLORS)
    def _set_textColor(self, value):
        self._textColor = value
        if isinstance(value, State):
            value.valueChanged.connect(self._set_stylesheet)

    def _get_textColor(self):
        color = self._textColor.value if isinstance(self._textColor, State) else self._textColor
        return color if color in self.VALID_COLORS else 'primary'

    @_validate_param(file_path="qtmui.material.tabs", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_variant(self):
        variant = self._variant.value if isinstance(self._variant, State) else self._variant
        return variant if variant in self.VALID_VARIANTS else 'standard'

    @_validate_param(file_path="qtmui.material.tabs", param_name="visibleScrollbar", supported_signatures=Union[State, bool])
    def _set_visibleScrollbar(self, value):
        self._visibleScrollbar = value
        if isinstance(value, State):
            value.valueChanged.connect(self.update_ui)

    def _get_visibleScrollbar(self):
        return self._visibleScrollbar.value if isinstance(self._visibleScrollbar, State) else self._visibleScrollbar

    def _init_ui(self):
        # Clear existing tabs
        while self.count():
            widget = self.widget(0)
            self.removeTab(0)
            if widget:
                widget.deleteLater()

        # Apply layout settings
        if self._get_fixedHeight():
            self.setFixedHeight(self._get_fixedHeight())
        if self._get_minWidth():
            self.setMinimumWidth(200)  # Arbitrary default minWidth
        if self._get_orientation() == "vertical":
            self.setTabPosition(QTabWidget.West)
        else:
            self.setTabPosition(QTabWidget.North)

        # Apply ARIA attributes
        if self._get_aria_label():
            self.setProperty("aria-label", self._get_aria_label())
        if self._get_aria_labelledby():
            self.setProperty("aria-labelledby", self._get_aria_labelledby())

        # Apply centered or justifyContent
        if self._get_centered():
            self.tabBar().setProperty("centered", "true")
        elif self._get_justifyContent() == "flex-end":
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)

        # Apply variant
        if self._get_variant() == "fullWidth" or self._get_fullWidth():
            self.tabBar().setExpanding(True)
        else:
            self.tabBar().setExpanding(False)

        # Initialize scroll buttons
        scroll_buttons = self._get_scrollButtons()
        show_scroll = scroll_buttons == True or (scroll_buttons == "auto" and self._get_allowScrollButtonsMobile())
        self.setUsesScrollButtons(show_scroll)
        self.setDocumentMode(self._get_variant() == "scrollable")

        # Initialize children
        children = self._get_children()
        if isinstance(children, list):
            for index, tab in enumerate(children):
                if isinstance(tab, Tab):
                    self.addTab(tab, "")
                    self.set_tab_with_icon_at_position(index, tab._get_label(), tab._get_icon(), tab._get_iconPosition())
                    if tab._get_key():
                        self.keys.append(tab._get_key())

        # Set cursor
        self.tabBar().setCursor(QCursor(Qt.PointingHandCursor))

        # Connect signals
        self.currentChanged.connect(self.on_tab_changed)
        if self._get_onChange():
            self.currentChanged.connect(lambda index: self._get_onChange()(self.currentWidget()._get_key()))

        # Apply selectionFollowsFocus
        if self._get_selectionFollowsFocus():
            self.tabBar().focusInEvent = lambda event: self.setCurrentIndex(self.tabBar().currentIndex())

        # Set current tab
        if self._get_value():
            self.set_current_tab_by_key(self._get_value())

        # Apply action
        if self._get_action():
            QTimer.singleShot(0, lambda: self._get_action()(self))

    def set_tab_with_icon_at_position(self, index, title, icon, iconPosition="top"):
        custom_widget = QWidget(self)
        layout = QVBoxLayout(custom_widget) if iconPosition in ["top", "bottom"] else QHBoxLayout(custom_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.theme.spacing(1))

        # Create label
        label_text = Typography(variant="body1", text=title, color=self._get_textColor()) if title else None
        if label_text:
            label_text.setParent(custom_widget)
            self._widget_references.append(label_text)

        # Create icon
        label_icon = None
        if isinstance(icon, str):
            label_icon = PyIconify(key=icon, size=20, color=self.theme.palette[self._get_textColor()].main)
            label_icon.setParent(custom_widget)
            self._widget_references.append(label_icon)
        elif isinstance(icon, QWidget):
            label_icon = icon
            label_icon.setParent(custom_widget)

        # Arrange icon and text
        if iconPosition == "top":
            if label_icon:
                layout.addWidget(label_icon)
            if label_text:
                layout.addWidget(label_text)
        elif iconPosition == "bottom":
            if label_text:
                layout.addWidget(label_text)
            if label_icon:
                layout.addWidget(label_icon)
        elif iconPosition == "start":
            if label_icon:
                layout.addWidget(label_icon)
            if label_text:
                layout.addWidget(label_text)
        elif iconPosition == "end":
            if label_text:
                layout.addWidget(label_text)
            if label_icon:
                layout.addWidget(label_icon)

        layout.setAlignment(Qt.AlignCenter)
        custom_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabBar().setTabButton(index, QTabBar.RightSide, custom_widget)

    @classmethod
    @lru_cache(maxsize=128)
    def _get_stylesheet(cls, _theme_mode: str) -> str:
        theme = useTheme()
        tabs_styles = theme.components.get("Tabs", {}).get("styles", {})
        tab_bar_styles = theme.components.get("TabBar", {}).get("styles", {})
        
        tabs_root_qss = get_qss_style(tabs_styles.get("root", {}))
        tabs_pane_qss = get_qss_style(tabs_styles.get("pane", {}))
        tab_bar_root_qss = get_qss_style(tab_bar_styles.get("root", {}))
        tab_bar_tab_qss = get_qss_style(tab_bar_styles.get("tab", {}))
        tab_bar_tab_selected_qss = get_qss_style(tab_bar_styles.get("tab", {}).get("slots", {}).get("selected", {}))
        tab_bar_tab_not_selected_qss = get_qss_style(tab_bar_styles.get("tab", {}).get("slots", {}).get("notSelected", {}))

        stylesheet = f"""
            QTabWidget {{
                {tabs_root_qss}
            }}
            QTabWidget::pane {{
                {tabs_pane_qss}
            }}
            QTabBar {{
                {tab_bar_root_qss}
            }}
            QTabBar::tab {{
                {tab_bar_tab_qss}
                color: {theme.palette[self._get_textColor()].main};
            }}
            QTabBar::tab:selected {{
                {tab_bar_tab_selected_qss}
                border-bottom: 2px solid {theme.palette[self._get_indicatorColor()].main};
            }}
            QTabBar::tab:!selected {{
                {tab_bar_tab_not_selected_qss}
            }}
            QTabBar[centered=true] {{
                alignment: center;
            }}
        """
        return stylesheet

    def _set_stylesheet(self):
        _theme_mode = self.theme.palette.mode
        stylesheet = self._get_stylesheet(_theme_mode)
        
        # Handle classes
        classes = self._get_classes() or {}
        classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}")

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

        # Apply variant and scrollbar
        variant_qss = ""
        if self._get_variant() == "scrollable" or self._get_visibleScrollbar():
            variant_qss = "QTabBar { overflow-x: auto; }"

        self.setStyleSheet(f"""
            {stylesheet}
            #{self.objectName()} {{
                {classes_qss}
                {variant_qss}
            }}
            {sx_qss}
        """)

    def set_current_tab_by_key(self, key):
        for i in range(self.count()):
            tab = self.widget(i)
            if getattr(tab, '_get_key', lambda: None)() == key:
                self.setCurrentIndex(i)
                return True
        return False

    def retranslateUi(self):
        for i in range(self.count()):
            tab = self.widget(i)
            if isinstance(tab, Tab):
                current_text = tab._get_label() or f"Tab {i + 1}"
                self.setTabText(i, translate(current_text))

    def on_tab_changed(self, index):
        current_tab = self.widget(index)
        if current_tab:
            current_tab._init_ui()

    def update_ui(self):
        self._init_ui()
        self._set_stylesheet()

    def _on_destroyed(self):
        self._widget_references.clear()

    def disable_pointer_events(self):
        self.setCursor(Qt.BlankCursor)

    def paintEvent(self, event):
        PyWidgetBase.paintEvent(self, event)
        return super().paintEvent(event)

    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)