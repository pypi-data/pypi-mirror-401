from functools import lru_cache
from typing import Any, Callable, List, Optional, Union, Dict
import uuid
from PySide6.QtWidgets import (
    QVBoxLayout, 
    QTabBar, 
    QWidget, 
    QHBoxLayout, 
    QLabel, 
    QSizePolicy, 
    QTabWidget,
    QWidget, 
    QSizePolicy, 
    QPushButton
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QCursor

from ...material.system.color_manipulator import alpha

from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from .tab import Tab
from qtmui.hooks import State
from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

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

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.tabs", param_name="justifyContent", supported_signatures=Union[State, str, type(None)])
    def _set_justifyContent(self, value):
        self._justifyContent = value

    def _get_justifyContent(self):
        return self._justifyContent.value if isinstance(self._justifyContent, State) else self._justifyContent

    @_validate_param(file_path="qtmui.material.tabs", param_name="orientation", supported_signatures=Union[State, str, type(None)], valid_values=VALID_ORIENTATIONS)
    def _set_orientation(self, value):
        self._orientation = value

    def _get_orientation(self):
        orientation = self._orientation.value if isinstance(self._orientation, State) else self._orientation
        return orientation if orientation in self.VALID_ORIENTATIONS else 'horizontal'

    # @_validate_param(file_path="qtmui.material.tabs", param_name="value", supported_signatures=Union[State, Any, type(None)])
    def _set_value(self, value):
        self._value = value

    def _get_value(self):
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.tabs", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        self._onChange = value

    def _get_onChange(self):
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.tabs", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        self._fullWidth = value

    def _get_fullWidth(self):
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.tabs", param_name="fixedHeight", supported_signatures=Union[State, int, type(None)])
    def _set_fixedHeight(self, value):
        self._fixedHeight = value

    def _get_fixedHeight(self):
        return self._fixedHeight.value if isinstance(self._fixedHeight, State) else self._fixedHeight

    @_validate_param(file_path="qtmui.material.tabs", param_name="minWidth", supported_signatures=Union[State, bool])
    def _set_minWidth(self, value):
        self._minWidth = value

    def _get_minWidth(self):
        return self._minWidth.value if isinstance(self._minWidth, State) else self._minWidth

    # @_validate_param(file_path="qtmui.material.tabs", param_name="children", supported_signatures=Union[State, List[QWidget], QWidget, type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.tabs", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.tabs", param_name="action", supported_signatures=Union[State, Any, type(None)])
    def _set_action(self, value):
        self._action = value

    def _get_action(self):
        return self._action.value if isinstance(self._action, State) else self._action

    @_validate_param(file_path="qtmui.material.tabs", param_name="allowScrollButtonsMobile", supported_signatures=Union[State, bool])
    def _set_allowScrollButtonsMobile(self, value):
        self._allowScrollButtonsMobile = value

    def _get_allowScrollButtonsMobile(self):
        return self._allowScrollButtonsMobile.value if isinstance(self._allowScrollButtonsMobile, State) else self._allowScrollButtonsMobile

    @_validate_param(file_path="qtmui.material.tabs", param_name="aria_label", supported_signatures=Union[State, str, type(None)])
    def _set_aria_label(self, value):
        self._aria_label = value

    def _get_aria_label(self):
        return self._aria_label.value if isinstance(self._aria_label, State) else self._aria_label

    @_validate_param(file_path="qtmui.material.tabs", param_name="aria_labelledby", supported_signatures=Union[State, str, type(None)])
    def _set_aria_labelledby(self, value):
        self._aria_labelledby = value

    def _get_aria_labelledby(self):
        return self._aria_labelledby.value if isinstance(self._aria_labelledby, State) else self._aria_labelledby

    @_validate_param(file_path="qtmui.material.tabs", param_name="centered", supported_signatures=Union[State, bool])
    def _set_centered(self, value):
        self._centered = value

    def _get_centered(self):
        return self._centered.value if isinstance(self._centered, State) else self._centered

    @_validate_param(file_path="qtmui.material.tabs", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.tabs", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.tabs", param_name="indicatorColor", supported_signatures=Union[State, str, type(None)], valid_values=VALID_COLORS)
    def _set_indicatorColor(self, value):
        self._indicatorColor = value

    def _get_indicatorColor(self):
        color = self._indicatorColor.value if isinstance(self._indicatorColor, State) else self._indicatorColor
        return color if color in self.VALID_COLORS or isinstance(color, str) else 'primary'

    @_validate_param(file_path="qtmui.material.tabs", param_name="scrollButtons", supported_signatures=Union[State, str, bool], valid_values=VALID_SCROLL_BUTTONS)
    def _set_scrollButtons(self, value):
        self._scrollButtons = value

    def _get_scrollButtons(self):
        scroll = self._scrollButtons.value if isinstance(self._scrollButtons, State) else self._scrollButtons
        return scroll if scroll in self.VALID_SCROLL_BUTTONS else 'auto'

    @_validate_param(file_path="qtmui.material.tabs", param_name="selectionFollowsFocus", supported_signatures=Union[State, bool])
    def _set_selectionFollowsFocus(self, value):
        self._selectionFollowsFocus = value

    def _get_selectionFollowsFocus(self):
        return self._selectionFollowsFocus.value if isinstance(self._selectionFollowsFocus, State) else self._selectionFollowsFocus

    @_validate_param(file_path="qtmui.material.tabs", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.tabs", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.tabs", param_name="TabIndicatorProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TabIndicatorProps(self, value):
        self._TabIndicatorProps = value

    def _get_TabIndicatorProps(self):
        return self._TabIndicatorProps.value if isinstance(self._TabIndicatorProps, State) else self._TabIndicatorProps

    @_validate_param(file_path="qtmui.material.tabs", param_name="TabScrollButtonProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TabScrollButtonProps(self, value):
        self._TabScrollButtonProps = value

    def _get_TabScrollButtonProps(self):
        return self._TabScrollButtonProps.value if isinstance(self._TabScrollButtonProps, State) else self._TabScrollButtonProps

    @_validate_param(file_path="qtmui.material.tabs", param_name="textColor", supported_signatures=Union[State, str, type(None)], valid_values=VALID_COLORS)
    def _set_textColor(self, value):
        self._textColor = value

    def _get_textColor(self):
        color = self._textColor.value if isinstance(self._textColor, State) else self._textColor
        return color if color in self.VALID_COLORS else 'primary'

    @_validate_param(file_path="qtmui.material.tabs", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        variant = self._variant.value if isinstance(self._variant, State) else self._variant
        return variant if variant in self.VALID_VARIANTS else 'standard'

    @_validate_param(file_path="qtmui.material.tabs", param_name="visibleScrollbar", supported_signatures=Union[State, bool])
    def _set_visibleScrollbar(self, value):
        self._visibleScrollbar = value

    def _get_visibleScrollbar(self):
        return self._visibleScrollbar.value if isinstance(self._visibleScrollbar, State) else self._visibleScrollbar


    def _init_ui(self):

        theme = useTheme()
        
        self.custom_widgets = {}
        
        self.hasIcon = False

        if self._fixedHeight:
            self.setFixedHeight(self._fixedHeight)

        # self.initUI()

        # self.setTabBar(TabBar())

        if self._minWidth:
            self.setMinimumWidth(self._minWidth)

        if self._orientation == "vertical":
            self.setTabPosition(QTabWidget.West)

        if self._justifyContent == "flex-end":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self._children.reverse()


        # Đặt tab bar vào một layout tùy chỉnh

        self._padding_for_only_icon = ""
        self._margin_left_for_icon = ""

        if isinstance(self._children, list) and len(self._children) > 0:
            for index, tab in enumerate(self._children, 0):
                if isinstance(tab, Tab):
                    if tab._icon and tab._label:
                        self.hasIcon = True
                        if tab._iconPosition in ["end", "bottom", "top"]:
                            self._padding_for_only_icon = "padding-left: -20px;"
                            self.tabBar().setProperty("hasIconAndLabel", "true")
                            # self._margin_left_for_icon = "margin-left: 24px;"
                            # self.addTab(tab, tab._icon, tab._label, Qt.AlignmentFlag.AlignRight)
                            self.addTab(tab, self._getTranslatedText(tab._label))
                            # self.tabBar().set_tab_with_icon_at_end(index, tab._label, FluentIconBase().icon_(path=tab._icon, color=theme.palette.text.secondary))
                            self.set_tab_with_icon_at_position(
                                index, 
                                tab._label, 
                                tab._icon() if isinstance(tab._icon, Callable) else tab._icon, 
                                tab._iconPosition
                            )

                        else:
                            self.addTab(tab, tab._icon() if isinstance(tab._icon, Callable) else tab._icon, tab._label)
                    elif tab._label:
                        self.addTab(tab, self._getTranslatedText(tab._label))
                    elif tab._icon:
                        self._padding_for_only_icon = "padding-left: 24px;"
                        self.tabBar().setProperty("hasIcon", "true")
                        # self.addTab(tab, tab._icon, "", Qt.AlignmentFlag.AlignCenter)
                        self.addTab(tab, tab._icon, "")
                        # self.addTab(tab, FluentIconBase().icon_(path=tab._icon, color=theme.palette.text.secondary))

        # self.set_cursor_pointer_to_tabs()
        self.tabBar().setCursor(QCursor(Qt.PointingHandCursor))

        self.currentChanged.connect(self.on_tab_changed)

        if self._onChange:
            self.currentChanged.connect(lambda index: self._onChange(self.currentWidget()._key))

        if self.currentWidget():
            self.currentWidget()._init_ui()

        # self.setTabShape(QTabWidget.Rounded)

        if self._value:
            if isinstance(self._value, State):
                self._value.valueChanged.connect(self.set_current_tab_by_key)
                self.set_current_tab_by_key(self._value.value)
            if isinstance(self._value, str):
                self.set_current_tab_by_key(self._value)

        self._update_stylesheet()
        self.theme.state.valueChanged.connect(self._update_stylesheet)
        # self.destroyed.connect(lambda ojb: self._on_destroyed())
        self.destroyed.connect(self._on_destroyed)

        i18n.langChanged.connect(self.retranslateUi)



    def _update_stylesheet(self):
        """Slot to set the stylesheet."""
        self._set_stylesheet()

    async def _async_update_stylesheet(self):
        """Slot to set the stylesheet."""
        self._set_stylesheet()

    @classmethod
    @lru_cache(maxsize=128)
    def _get_stylesheet(cls, _theme_mode: str):
        
        theme = useTheme()
        # self._text_color_disabled = theme.palette.text.disabled # opacity
        # self._text_color_disabled = alpha(theme.palette.primary.main, theme.palette.action.disabledOpacity) # opacity
        # self._text_color_primary = theme.palette.text.primary # opacity
        # self._text_color_secondary = theme.palette.text.secondary # opacity
        
        PyTabWidget = theme.components[f"PyTabWidget"].get("styles")
        PyTabWidget_root_qss = get_qss_style(PyTabWidget["root"])
        PyTabWidget_pane_qss = get_qss_style(PyTabWidget["pane"])
        PyTabWidget_label_qss = get_qss_style(PyTabWidget["label"])
        PyTabWidget_label_slot_hover_qss = get_qss_style(PyTabWidget["label"]["slots"]["hover"])

        PyTabBar = theme.components[f"PyTabBar"].get("styles")
        PyTabBar_root = PyTabBar["root"]
        PyTabBar_tab = PyTabBar["tab"]
        PyTabBar_root_qss = get_qss_style(PyTabBar_root)
        PyTabBar_tab_qss = get_qss_style(PyTabBar_tab)
        PyTabBar_tab_slot_selected_qss = get_qss_style(PyTabBar_tab["slots"]["selected"])
        PyTabBar_tab_slot_notSelected_qss = get_qss_style(PyTabBar_tab["slots"]["notSelected"])
        PyTabBar_tab_prop_hasIcon_qss = get_qss_style(PyTabBar_tab["props"]["hasIcon"])
        PyTabBar_tab_prop_hasIconAndLabel_qss = get_qss_style(PyTabBar_tab["props"]["hasIconAndLabel"])

        # print('vadddddddddddddddd_________')

        # Apply the final styles
        stylesheet = f"""
            QTabWidget{{
                {PyTabWidget_root_qss}
            }}
            QTabWidget::pane{{
                {PyTabWidget_pane_qss}
            }}

            QTabBar {{
                {PyTabBar_root_qss}

            }}
            QTabBar::tab {{
                {PyTabBar_tab_qss}
            }}

            QTabBar::tab:selected {{
                {PyTabBar_tab_slot_selected_qss}
            }}

            QTabBar::tab:!selected {{
                {PyTabBar_tab_slot_notSelected_qss}
            }}

            QTabBar::tab[hasIcon=true] {{
                {PyTabBar_tab_prop_hasIcon_qss}
            }}
            QTabBar::tab[hasIconAndLabel=true] {{
                {PyTabBar_tab_prop_hasIconAndLabel_qss}
            }}

            QLabel {{
                {PyTabWidget_label_qss}
            }}

            QLabel::hover {{
                {PyTabWidget_label_slot_hover_qss}
            }}
            
        """

        return stylesheet

    def _set_stylesheet(self, component_styled=None):
        _theme_mode = useTheme().palette.mode
        stylesheet = self._get_stylesheet(_theme_mode)
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

        self.setStyleSheet(stylesheet + sx_qss)


    def set_current_tab_by_key(self, key):
        for i in range(self.count()):
            tab = self.widget(i)
            if getattr(tab, '_key', None) == key:
                self.setCurrentIndex(i)
                return True  # Đã tìm thấy và thiết lập tab
        return False  # Không tìm thấy tab có _key khớ

    def retranslateUi(self):
       # Dùng phương thức count() để lấy số lượng tab và cập nhật tên của tất cả các tab
        for i in range(self.count()):
            # current_text = self.tabText(i)  # Lấy ra tabText hiện tại
            tabBar = self.widget(i)  # Lấy ra tabText hiện tại
            # print(f"Current text of Tab {i + 1}: {current_text}")  # In ra tabText hiện tại
            print('aaaaaaaaaaaaaaaaaaa', self._getTranslatedText(tabBar._label))
            if self.hasIcon:
                self.setTabText(i, "")  # Cập nhật tên tab mới với tabText cũ
            else:
                self.setTabText(i, self._getTranslatedText(tabBar._label))  # Cập nhật tên tab mới với tabText cũ
                
            # Lấy custom widget theo index
            try:
                label = self.custom_widgets[i].findChild(QLabel, f"label_text_{i}")
                if label:
                    label.setText(self._getTranslatedText(tabBar._label))
            except Exception as e:
                pass
                

    def set_tab_with_icon_at_position(self, index, title, icon, iconPosition="top"):
        # Tạo widget chứa text và icon
        custom_widget = QWidget(self)
        
        # Xử lý vị trí icon
        if iconPosition in ["top", "bottom"]:
            layout = QVBoxLayout(custom_widget)
        else:
            layout = QHBoxLayout(custom_widget)

        # QLabel cho text
        label_text = QLabel(self._getTranslatedText(title))
        label_text.setObjectName(f'label_text_{index}')

        # QLabel cho icon
        if isinstance(icon, QIcon):
            label_icon = QLabel()
            label_icon.setAlignment((Qt.AlignVCenter | Qt.AlignHCenter))
            label_icon.setPixmap(icon.pixmap(20, 20))  # Điều chỉnh kích thước icon
        else:
            label_icon = icon

        # Thêm icon và text vào layout theo vị trí icon
        if iconPosition == "top":
            layout.addWidget(label_icon)
            layout.addWidget(label_text)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        elif iconPosition == "bottom":
            layout.addWidget(label_text)
            layout.addWidget(label_icon)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        elif iconPosition == "start":  # Đổi 'left' thành 'start'
            layout.addWidget(label_icon)
            layout.addWidget(label_text)
            layout.setAlignment(Qt.AlignCenter)
        elif iconPosition == "end":  # Đổi 'right' thành 'end'
            layout.addWidget(label_text)
            layout.addWidget(label_icon)
            layout.setAlignment(Qt.AlignCenter)

        # Căn chỉnh nội dung
        
        layout.setContentsMargins(0, 0, 0, 0)

        # Điều chỉnh kích thước cho custom_widget
        custom_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Điều chỉnh kích thước tối thiểu cho custom_widget để phù hợp với nội dung
        custom_widget.setMinimumSize(custom_widget.sizeHint().width() + 24, custom_widget.sizeHint().height())

        # Đặt widget vào tab
        self.setTabText(index, "")
        self.setTabIcon(index, QIcon())  # Xóa icon gốc nếu có
        self.setTabEnabled(index, True)

        self.custom_widgets[index] = custom_widget
        # Thêm widget tùy chỉnh vào tab
        self.tabBar().setTabButton(index, QTabBar.RightSide, custom_widget)


    def set_cursor_pointer_to_tabs(self):
        tab_bar = self.tabBar()  # Lấy QTabBar của QTabWidget
        for i in range(tab_bar.count()):
            tab_bar.setCursor(i, QCursor(Qt.PointingHandCursor))  # Đặt cursor pointer cho từng tab


    def on_tab_changed(self, index):
        current_tab = self.widget(index)
        current_tab._init_ui()

    def disable_pointer_events(self):
        self.setCursor(Qt.BlankCursor)

    def paintEvent(self, arg__1):
        PyWidgetBase.paintEvent(self, arg__1)
        return super().paintEvent(arg__1)

    def resizeEvent(self, event):
        PyWidgetBase.resizeEvent(self, event)
        return super().resizeEvent(event)

