import asyncio
from functools import lru_cache
import os
import threading
import time
import uuid
from typing import Optional, Callable, Union, Dict, List

from PySide6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QPoint, Signal, QTimer, QEvent, QSize
from PySide6.QtGui import QPalette

from qtmui.hooks import State
from qtmui.material.py_iconify import Iconify, PyIconify
from qtmui.material.menu import Menu
from .button_base import ButtonBase

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

# Biến global để xác định nguồn lỗi
FILE_PATH = "qtmui.material.button"

from ..utils.validate_params import _validate_param

COLORS = ['inherit', 'default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']
SIZES = ['small', 'medium', 'large']
VARIANTS = ['text', 'contained', 'outlined', 'soft']

class Button(ButtonBase):
    """
    A clickable button widget with customizable appearance and behavior.

    The `Button` widget provides a versatile component for triggering actions
    or events in a user interface. It supports various styles, sizes, and states,
    with dynamic state management for properties like color, size, and visibility.
    It inherits properties from `ButtonBase` and extends them with additional
    customization options such as icons, menu integration, and loading states.

    Parameters
    ----------
    autoFocus : State or bool, optional
        If true, the button automatically receives focus on render. Default is False.
        Can be a `State` object for dynamic updates.
    id : State or str, optional
        A unique identifier for the button, used for DOM or accessibility purposes.
        Default is None. Can be a `State` object for dynamic updates.
    text : State, str, or Callable, optional
        The text content of the button. Can be a callable returning a string for
        dynamic text. Default is None. Can be a `State` object for dynamic updates.
    value : State or Any, optional
        The value associated with the button, used for form submission or state
        management. Default is None. Can be a `State` object for dynamic updates.
    active : State or bool, optional
        Whether the button is in an active state (e.g., toggled). Default is None.
        Can be a `State` object for dynamic updates.
    isLoadingButton : State or bool, optional
        If true, displays a loading indicator and disables the button. Default is False.
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        A unique identifier for the widget, used for referencing or state management.
        Default is None. Can be a `State` object for dynamic updates.
    children : State, list, or str, optional
        The content of the button, typically a string for the button label or a list
        of widgets. Can be a `State` object for dynamic content management.
        Default is None.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color theme of the button. Valid values include "inherit", "default",
        "primary", "secondary", "info", "success", "warning", "error". Default is "default".
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node, either a string (HTML element) or a custom component.
        Default is None. Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If true, the button is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableElevation : State or bool, optional
        If true, no elevation (shadow) is applied to the button. Default is False.
        Can be a `State` object for dynamic updates.
    disableFocusRipple : State or bool, optional
        If true, the keyboard focus ripple effect is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If true, the ripple effect is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disablePointerEvents : State or bool, optional
        If true, pointer events (e.g., clicks) are disabled. Default is False.
        Can be a `State` object for dynamic updates.
    menu : State or Menu, optional
        A menu component to display when the button is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    endIcon : State or PyIconify, optional
        An icon displayed after the button content. Default is None.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If true, the button takes up the full width of its container. Default is False.
        Can be a `State` object for dynamic updates.
    href : State or str, optional
        The URL to link to when the button is clicked. If defined, the button acts as a link.
        Default is None. Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the button. Valid values include "small", "medium", "large".
        Default is "medium". Can be a `State` object for dynamic updates.
    startIcon : State or PyIconify, optional
        An icon displayed before the button content. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, Callable, str, or dict, optional
        Custom styles for the button. Can be a CSS-like string, a dictionary of style
        properties, a callable returning styles, or a `State` object for dynamic styling.
        Default is None.
    type : State or str, optional
        The type of the button, either "button" or "submit". Default is "button".
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The visual style of the button. Valid values include "text", "contained", "outlined", "soft".
        Default is "text". Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `ButtonBase` class.

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for the `color` parameter: ["inherit", "default", "primary",
        "secondary", "info", "success", "warning", "error"].
    VALID_SIZES : list[str]
        Valid values for the `size` parameter: ["small", "medium", "large"].
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["text", "contained", "outlined", "soft"].
    VALID_TYPES : list[str]
        Valid values for the `type` parameter: ["button", "submit"].

    Demos:
    - Button: https://qtmui.com/material-ui/qtmui-button/

    API Reference:
    - Button API: https://qtmui.com/material-ui/api/button/
    """

    themeChanged = Signal(object)
    updateStyleSheet = Signal(object)
    

    VALID_COLORS = ['inherit', 'default', 'primary', 'secondary', 'info', 'success', 'warning', 'error']
    VALID_SIZES = ['small', 'medium', 'large']
    VALID_VARIANTS = ['text', 'contained', 'outlined', 'soft', 'extended', 'softExtended', 'outlined', 'outlinedExtended']
    VALID_TYPES = ['button', 'submit']

    def __init__(
        self,
        autoFocus: Optional[Union[State, bool]] = False,
        id: Optional[Union[State, str]] = None,
        text: Optional[Union[State, str, Callable]] = None,
        # value: Optional[Union[State, Any]] = None,
        value = None,
        active: Optional[Union[State, bool]] = None,
        isLoadingButton: Optional[Union[State, bool]] = False,
        key: Optional[Union[State, str]] = None,
        checked: Optional[Union[State, bool]] = False, # Checkbox mode
        checkboxIcon: Optional[Union[State, str, Iconify]] = None, # Checkbox mode
        checkedIcon: Optional[Union[State, str, Iconify]] = None, # Checkbox mode
        children: Optional[Union[State, List, str]] = None,
        classes: Optional[Union[State, Dict]] = None,
        color: Optional[Union[State, str]] = "default",
        component: Optional[Union[State, str]] = None,
        componentType: Optional[Union[State, str]] = "Button", # "IconButton", "Fab", "LoaddingButton", "Button"
        disabled: Optional[Union[State, bool]] = False,
        disableElevation: Optional[Union[State, bool]] = False,
        disableFocusRipple: Optional[Union[State, bool]] = False,
        disableRipple: Optional[Union[State, bool]] = False,
        disablePointerEvents: Optional[Union[State, bool]] = False,
        menu: Optional[Union[State, Menu]] = None,
        endIcon: Optional[Union[State, Iconify]] = None,
        fullWidth: Optional[Union[State, bool]] = False,
        href: Optional[Union[State, str]] = None,
        size: Optional[Union[State, str]] = "medium",
        startIcon: Optional[Union[State, Iconify]] = None,
        sx: Optional[Union[State, Callable, str, Dict]] = None,
        type: Optional[Union[State, str]] = "button",
        variant: Optional[Union[State, str]] = "text",
        asynRenderQss: Optional[Union[State, bool]] = False,
        *args, **kwargs
    ):
        super().__init__(
            children=children,
            classes=classes,
            component=component,
            disabled=disabled,
            disableRipple=disableRipple,
            sx=sx,
            *args, **kwargs
        )
        self.setObjectName(str(uuid.uuid4()))
        
        if sx:
            self._setSx(sx)
            
        self._kwargs = {
            **kwargs,
            "variant": variant,
            "size": size,
            "color": color,
        }
            
        self._setKwargs(self._kwargs)
        
        start_time = time.time()
        
        self._componentType = componentType
        
        self._checked = checked
        self._checkboxIcon = checkboxIcon
        self._checkedIcon = checkedIcon
        
        self._set_autoFocus(autoFocus)
        self._set_id(id)
        self._set_text(text)
        self._set_value(value)
        self._set_active(active)
        self._set_isLoadingButton(isLoadingButton)
        self._set_key(key)
        self._set_children(children)
        self._set_classes(classes)
        self._set_color(color)
        self._set_component(component)
        self._set_disabled(disabled)
        self._set_disableElevation(disableElevation)
        self._set_disableFocusRipple(disableFocusRipple)
        self._set_disableRipple(disableRipple)
        self._set_disablePointerEvents(disablePointerEvents)
        self._set_menu(menu)
        self._set_endIcon(endIcon)
        self._set_fullWidth(fullWidth)
        self._set_href(href)
        self._set_size(size)
        self._set_startIcon(startIcon)
        self._set_sx(sx)
        self._set_type(type)
        self._set_variant(variant)
        
        # print('timmmmmmmmmmmmmmmmm66666666666', self._startIcon, isinstance(self._startIcon, Iconify))

        self._selected = False
        self._text_color = None
        self._background_color = None
        self._hover_background_color = None
        self._border_color = None

        self._init_task = None
        # Kích hoạt init UI sau khi sự kiện hiện đang chờ xử lý
        # QTimer.singleShot(0, self._schedule_init)
        
        
        self._asynRenderQss = asynRenderQss
        
        self.init_ui()
        
        end_time = time.time()
        # print("time_loading_textfield___________________________", end_time - start_time)
        # print("time_loading_button___________________________", (end_time - start_time)/0.0005490779876708984)
        
    def connect_signal_slot(self):
        if isinstance(self._text, State):
            self._text.valueChanged.connect(self.retranslateUi)

    def init_ui(self):
        self.theme = useTheme()
        
        self.connect_signal_slot()

        if not self._fullWidth:
            self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        if self._disablePointerEvents:
            self.setCursor(Qt.BlankCursor)
        else:
            self.setCursor(Qt.PointingHandCursor)

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()
        
        self.theme.state.valueChanged.connect(self._onThemeChanged)
        # QTimer.singleShot(0, self._scheduleSetStyleSheet)
        if self._asynRenderQss:
            self.updateStyleSheet.connect(self._updateStylesheet)
        else:
            self._setStyleSheet()
        
        self._setIcon()

        self.destroyed.connect(lambda obj: self._onDestroy())

    def _onDestroy(self, obj=None):
        # print(f"Button {self._key}: _onDestroy")
        if hasattr(self, "_setupStyleSheet") and self._setupStyleSheet and not self._setupStyleSheet.done():
            # print(f"Button {self._key}: _onDestroy: Cancelling setupStyleSheet task")
            self._setupStyleSheet.cancel()

    def _onThemeChanged(self):
        if not self.isVisible():
            return
        QTimer.singleShot(0, self._scheduleSetStyleSheet)

    def _schedule_init(self):
        # Tạo task và lưu reference
        self._setupStyleSheet = asyncio.ensure_future(self.init_ui())

    def retranslateUi(self):

        self.setText(self._getTranslatedText(self._text))
            
        if isinstance(self._children, Callable):
            self.setText(translate(self._children))
        elif isinstance(self._children, str):
            self.setText(self._children)
        else:
            if isinstance(self._children, list):
                self.setLayout(QHBoxLayout())
                self.layout().setContentsMargins(0,0,0,0)
                for widget in self._children:
                    if isinstance(widget, QWidget):
                        self.layout().addWidget(widget)

    def _scheduleSetStyleSheet(self):
        self._setupStyleSheet = asyncio.ensure_future(self._lazy_setStyleSheet())

    async def _lazy_setStyleSheet(self):
        self._setStyleSheet()

    def _setupCheckbox(self):
        
        if bool(self._checked):
            theme = useTheme()
            if self._color == "inherit":
                color = theme.palette.text.primary
            elif self._color == "default":
                color = theme.palette.text.secondary
            elif self._color in COLORS:
                color = getattr(theme.palette, self._color).main
            else:
                color = theme.palette.text.secondary
                
            if isinstance(self._checkedIcon, Iconify):
                self._checkedIcon._color = color
                self.setIcon(self._checkedIcon.qIcon())
            else:
                self.setIcon(Iconify(key="mdi:checkbox-marked", color=color).qIcon())
        else:
            if isinstance(self._checkboxIcon, Iconify):
                self._checkboxIcon._color = self.theme.palette.grey._500
                self.setIcon(self._checkboxIcon.qIcon())
            else:
                # if hasattr(self, "_destroyed") and self._destroyed:
                #     return
                self.setIcon(Iconify(key="system-uicons:checkbox-empty", color=self.theme.palette.grey._500).qIcon())
                
        self.setIconSize(QSize(20, 20) if self._size == "small" else QSize(26, 26))
        self.setFixedSize(QSize(30, 30) if self._size == "small" else QSize(36, 36))

    @classmethod
    def _setSx(cls, sx: dict = {}):
        cls.sxDict = sx
        
    @classmethod
    def _setKwargs(cls, kwargs: dict = {}):
        cls.ownerState = kwargs

    @classmethod
    @lru_cache(maxsize=128)
    def _getSxQss(cls, sxStr: str = "", className: str = "PyWidgetBase"):
        sx_qss = get_qss_style(cls.sxDict, class_name=className)
        return sx_qss

    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheet(cls, _styledConfig: str, _variant: str, _size: str, _color: str, _theme_mode: str, _componentType: str = "Button", _qssProps: str = ""):
        theme = useTheme()
        MuiButton_root = theme.components["MuiButton"].get("styles")["root"]({})
        MuiButton_root_size_qss = get_qss_style(MuiButton_root["size"][_size])
        MuiButton_root_size_textVariant_qss = get_qss_style(MuiButton_root["size"][_size]["textVariant"])
        MuiButton_root_colorStyle_prop_variant_qss = get_qss_style(
            MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]
        )
        MuiButton_root_colorStyle_prop_variant_slot_hover_qss = get_qss_style(
            MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]["slots"]["hover"]
        )
        MuiButton_root_colorStyle_prop_variant_slot_checked_qss = get_qss_style(
            MuiButton_root["colorStyle"][_color]["props"][f"{_variant}Variant"]["slots"]["checked"]
        )
        
        IconButton_qss = ""
        Fab_qss = ""
        Checkbox_qss = ""
        Radio_qss = ""
        
        if _componentType == "IconButton":
            # icon_button_qss = get_qss_style(MuiButton_root["iconButton"])
            # icon_button_qss = icon_button_qss.replace("_________object_name_______", f"Button")
            # icon_button_qss = icon_button_qss.replace("MuiButton_root_colorStyle_prop_variant_slot_hover_qss", MuiButton_root_colorStyle_prop_variant_slot_hover_qss)
            # icon_button_qss = icon_button_qss.replace("MuiButton_root_colorStyle_prop_variant_slot_checked_qss", MuiButton_root_colorStyle_prop_variant_slot_checked_qss)
            # icon_button_qss = icon_button_qss.replace("MuiButton_root_size_textVariant_qss", MuiButton_root_size_textVariant_qss)
            # icon_button_qss = f'border-radius: {"15px" if self._size == "small" else "18px" if self._size == "medium" else "24px"};'

            if _color == "inherit":
                color = theme.palette.text.primary
            elif _color == "default":
                color = theme.palette.text.secondary
            elif _color in COLORS:
                color = getattr(theme.palette, _color).main
            else:
                color = theme.palette.text.secondary

            # thiết lập cho IconButton
            IconButton_qss = f"""
                Button{_qssProps} {{
                    border-radius: {"15px" if _size == "small" else "18px" if _size == "medium" else "24px"};
                    color: {color};
                }}
            """
        elif _componentType == "Fab":
            PyFab_styles_root_size_qss = get_qss_style(theme.components["PyFab"].get("styles")["root"]["props"][f"{_size}Size"])
            Fab_qss = f"""
                Button{_qssProps} {{
                    {PyFab_styles_root_size_qss}
                }}
            """
        elif _componentType == "Checkbox":
            ownerState = {
                "size": _size
            }

            # component_styles[f"MuiCheckbox"].get("styleOverrides") or 
            MuiCheckbox = theme.components[f"MuiCheckbox"].get("styles")
            MuiCheckbox_root_qss = get_qss_style(theme.components[f"MuiCheckbox"].get("styles")["root"](ownerState)[_color])
            _text_color = MuiCheckbox["root"](ownerState)[_color]["color"]
            _icon_color = MuiCheckbox["icon"]["color"]

            _indicator_border_width = MuiCheckbox["checkedIndicator"]["border-width"]
            _indicator_border_radius = MuiCheckbox["checkedIndicator"]["border-radius"]
            _indicator_padding = MuiCheckbox["checkedIndicator"]["padding"]

            MuiCheckbox_root_override_qss = ""
            _icon_color_override = None
            _text_color_override = None
            if theme.components[f"MuiCheckbox"].get("styleOverrides"):
                MuiCheckbox_override = theme.components[f"MuiCheckbox"].get("styleOverrides")
                MuiCheckbox_root_override_qss = get_qss_style(MuiCheckbox_override["root"](ownerState)[_color])
                _text_color = MuiCheckbox_override["root"](ownerState)[_color].get("color") or _text_color

                if MuiCheckbox_override.get("icon"):
                    _icon_color = MuiCheckbox_override["icon"].get("color") or _icon_color

                if MuiCheckbox_override.get("checkedIndicator"):
                    _indicator_border_width = MuiCheckbox["checkedIndicator"].get("border-width") or _indicator_border_width
                    _indicator_border_radius = MuiCheckbox["checkedIndicator"].get("border-radius") or _indicator_border_radius
                    _indicator_padding = MuiCheckbox["checkedIndicator"].get("padding") or _indicator_padding


            Checkbox_qss = f"""
                Button{_qssProps} {{
                    {MuiCheckbox_root_qss}
                    {MuiCheckbox_root_override_qss}
                    color: {_text_color};
                }}
            """

        elif _componentType == "RadioButton":
            PyRadio_root = theme.components[f"PyRadio"].get("styles")["root"](cls.ownerState)
            PyRadio_root_qss = get_qss_style(PyRadio_root)
            # PyRadio_root_color_qss = PyRadio_root[_color]["color"]

            Radio_qss = f"""
                Button{_qssProps} {{
                    {PyRadio_root_qss}
                }}
            """

        stylesheet = f"""
            Button{_qssProps}{{
                {MuiButton_root_size_qss}
                {MuiButton_root_size_textVariant_qss}
                {MuiButton_root_colorStyle_prop_variant_qss}
            }}
            Button{_qssProps}:hover {{
                {MuiButton_root_colorStyle_prop_variant_slot_hover_qss}
            }}
            Button{_qssProps}[selected=true] {{
                {MuiButton_root_colorStyle_prop_variant_slot_checked_qss}
            }}
            {IconButton_qss}
            {Fab_qss}
            {Checkbox_qss}
            {Radio_qss}
        """

        return stylesheet

    @classmethod
    @lru_cache(maxsize=128)
    def _getStyleSheetFromFile(cls, file):
        print(f"Loading stylesheet from file: {file}")
        with open(file, "r", encoding="utf-8") as f:
            stylesheet = f.read()
        return stylesheet

    def _setStyleSheet(self):
        self._variant = self._variant.replace("Extended", "").replace("extended", "contained")
        
        qssProps = f"[type={self._componentType.lower()}][variant={self._variant.lower()}][color={self._color.lower()}]"
        qssFile = f"{qssProps}[mode={useTheme().palette.mode.lower()}].qss" # Lưu trữ theo chế độ sáng/tối
        
        self.setProperty("type", self._componentType.lower())
        self.setProperty("variant", self._variant.lower())
        self.setProperty("color", self._color.lower())
        # self.setProperty("mode", useTheme().palette.mode.lower())
        
        # print("property", self.property("type"), self.property("variant"), self.property("color"), self.property("mode"))
        
        
        # self.update()
        return

        if os.path.exists(qssFile):
            stylesheet = self._getStyleSheetFromFile(qssFile)
            self.setStyleSheet(stylesheet)
            return
        
        print(f"Generating stylesheet and saving to {qssFile}...")
        
        stylesheet = ""
        if hasattr(self, "styledDict"):
            root = self.styledDict.get("MuiButton", {}).get("styles", {}).get("root", None)(self._kwargs)
            if root:
                stylesheet = self._getStyleSheet(
                    _styledConfig=str(root),
                    _variant=self._variant,
                    _size=self._size,
                    _color=self._color,
                    _theme_mode=useTheme().palette.mode,
                    _componentType=self._componentType,
                    _qssProps=qssProps
                )
        else:
            stylesheet = self._getStyleSheet(
                _styledConfig="Button",
                _variant=self._variant,
                _size=self._size,
                _color=self._color,
                _theme_mode=useTheme().palette.mode,
                _componentType=self._componentType,
                _qssProps=qssProps
            )
            
        sxQss = ""
        if self._sx:
            # sxQss = self._getSxQss(sxStr=str(self._sx), className=f"#{self.objectName()}")
            sxQss = self._getSxQss(sxStr=str(self._sx), className=f"Button")
            
        self.setProperty("variant", self._variant)
        if self._color == "inherit":
            self._color = "default"

        stylesheet = f"""
            {stylesheet}
            {sxQss}
        """
        
        with open(qssFile, "w", encoding="utf-8") as f:
            f.write(stylesheet)
            
        self.setStyleSheet(stylesheet)
            
        
        # print(stylesheet)
        # with open("button_stylesheet.qss", "w", encoding="utf-8") as f:
        #     f.write(stylesheet)
        # self.setStyleSheet(stylesheet)
        
        if self._componentType == "Checkbox":
            self._setupCheckbox()

    def _renderStylesheet(self):
        _theme_mode = useTheme().palette.mode
        
        # time.sleep(1)
        self.setProperty("variant", self._variant)
        if self._color == "inherit":
            self._color = "default"

        self._variant = self._variant.replace("Extended", "").replace("extended", "contained")

        stylesheet = self._getStyleSheet(self._variant, self._size, self._color, _theme_mode, self._componentType)
        # stylesheet = stylesheet.replace("_________object_name_______", self.objectName())
        
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


        self.updateStyleSheet.emit(stylesheet + sx_qss)
        
    def _updateStylesheet(self, stylesheet):
        self.setStyleSheet(stylesheet)

    def _setIcon(self):
        if self._startIcon and isinstance(self._startIcon, Callable):
            self._startIcon = self._startIcon()

        if isinstance(self._startIcon, Iconify):
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            self._startIcon._color = color.name()
            self.setIcon(self._startIcon.qIcon())#"#919eab"
        elif isinstance(self._endIcon, Iconify):
            color = self.palette().color(QPalette.ColorRole.ButtonText)
            self._endIcon._color = color.name()
            self.setIcon(self._endIcon.qIcon())
            self.setLayoutDirection(Qt.RightToLeft)

    def _show_menu(self, state=None):
        if state or not self._menu.isVisible():
            self._menu.show()
        else:
            self._menu.hide()

    def _hide_popup(self):
        if self._popup:
            self._popup.hide()

    def _show_popup(self, state=None):
        if not self._popup:
            self._popup = QWidget(self, Qt.Window | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
            self._popup.setParent(self)
            self._popup.setObjectName(str(uuid.uuid4()))
            self._popup.setStyleSheet(f"#{self._popup.objectName()} {{background-color: white;border: 0px solid transparent; border-radius: 8px;}}")
            self._popup.setLayout(QVBoxLayout())
            self._popup.layout().setContentsMargins(0,0,0,0)
            self._popup.layout().addWidget(self._menu)
            self._popup.setAttribute(Qt.WA_TranslucentBackground)

        if state or not self._popup.isVisible() or not self._menu.isVisible():
            if not self.visibleRegion().isEmpty():
                self._popup.show()
                self._menu.show()
        else:
            self._popup.hide()
            self._menu.hide()
            return

        popup_position = self.mapToGlobal(QPoint(0, self.height()))
        self._popup.setGeometry(popup_position.x(), popup_position.y(), self._menu._minWidth or self.width(), self._popup.sizeHint().height())
        self._menu.setFixedWidth(self._menu._minWidth or self.width())

    def mouseReleaseEvent(self, event):
        if isinstance(self._href, Callable):
            self._href()
        return super().mouseReleaseEvent(event)

    def set_visible(self, state):
        if state == True:
            if not self.isVisible():
                self.parent().layout().insertWidget(0, self)
        else:
            if self.isVisible():
                self.parent().layout().insertWidget(-1, self)

    def set_collapse_icon(self, icon):
        self.setIcon(icon)

    def get_selected(self):
        return self._selected

    def set_selected(self, selected):
        if self._selected != selected:
            self._selected = selected
        self.setProperty("selected", selected)
        self._setStyleSheet()

    def changeEvent(self, event: QEvent):
        if event.type() == event.Type.StyleChange:
            try:
                if self._startIcon or self._endIcon:
                    self._setIcon()
            except Exception as e:
                import traceback
                traceback.print_exc()
        super().changeEvent(event)
        
    def showEvent(self, event):
        if self._asynRenderQss:
            threading.Thread(target=self._renderStylesheet, args=(), daemon=True).start()
        return super().showEvent(event)
        
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
        
        
        
        
        
        
        
        
        
        
        
    @_validate_param(file_path=FILE_PATH, param_name="autoFocus", supported_signatures=Union[State, bool, type(None)])
    def _set_autoFocus(self, value):
        """Assign value to autoFocus."""
        self._autoFocus = value

    def _get_autoFocus(self):
        """Get the autoFocus value."""
        return self._autoFocus.value if isinstance(self._autoFocus, State) else self._autoFocus

    @_validate_param(file_path=FILE_PATH, param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        """Assign value to id."""
        self._id = value

    def _get_id(self):
        """Get the id value."""
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path=FILE_PATH, param_name="text", supported_signatures=Union[State, str, Callable, type(None)])
    def _set_text(self, value):
        """Assign value to text."""
        self._text = value

    def _get_text(self):
        """Get the text value."""
        return self._text.value if isinstance(self._text, State) else self._text

    # @_validate_param(file_path=FILE_PATH, param_name="value", supported_signatures=Union[State, str, type(None)])
    def _set_value(self, value):
        """Assign value to value."""
        self._value = value

    def _get_value(self):
        """Get the value value."""
        return self._value.value if hasattr(self._value, 'value') else self._value

    @_validate_param(file_path=FILE_PATH, param_name="active", supported_signatures=Union[State, bool, type(None)])
    def _set_active(self, value):
        """Assign value to active."""
        self._active = value

    def _get_active(self):
        """Get the active value."""
        return self._active.value if isinstance(self._active, State) else self._active

    @_validate_param(file_path=FILE_PATH, param_name="isLoadingButton", supported_signatures=Union[State, bool, type(None)])
    def _set_isLoadingButton(self, value):
        """Assign value to isLoadingButton."""
        self._isLoadingButton = value

    def _get_isLoadingButton(self):
        """Get the isLoadingButton value."""
        return self._isLoadingButton.value if isinstance(self._isLoadingButton, State) else self._isLoadingButton

    @_validate_param(file_path=FILE_PATH, param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    # @_validate_param(file_path=FILE_PATH, param_name="children", supported_signatures=Union[State, List, str, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path=FILE_PATH, param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path=FILE_PATH, param_name="color", supported_signatures=Union[State, str, type(None)], valid_values=VALID_COLORS)
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path=FILE_PATH, param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path=FILE_PATH, param_name="disabled", supported_signatures=Union[State, bool, type(None)])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path=FILE_PATH, param_name="disableElevation", supported_signatures=Union[State, bool, type(None)])
    def _set_disableElevation(self, value):
        """Assign value to disableElevation."""
        self._disableElevation = value

    def _get_disableElevation(self):
        """Get the disableElevation value."""
        return self._disableElevation.value if isinstance(self._disableElevation, State) else self._disableElevation

    @_validate_param(file_path=FILE_PATH, param_name="disableFocusRipple", supported_signatures=Union[State, bool, type(None)])
    def _set_disableFocusRipple(self, value):
        """Assign value to disableFocusRipple."""
        self._disableFocusRipple = value

    def _get_disableFocusRipple(self):
        """Get the disableFocusRipple value."""
        return self._disableFocusRipple.value if isinstance(self._disableFocusRipple, State) else self._disableFocusRipple

    @_validate_param(file_path=FILE_PATH, param_name="disableRipple", supported_signatures=Union[State, bool, type(None)])
    def _set_disableRipple(self, value):
        """Assign value to disableRipple."""
        self._disableRipple = value

    def _get_disableRipple(self):
        """Get the disableRipple value."""
        return self._disableRipple.value if isinstance(self._disableRipple, State) else self._disableRipple

    @_validate_param(file_path=FILE_PATH, param_name="disablePointerEvents", supported_signatures=Union[State, bool, type(None)])
    def _set_disablePointerEvents(self, value):
        """Assign value to disablePointerEvents."""
        self._disablePointerEvents = value

    def _get_disablePointerEvents(self):
        """Get the disablePointerEvents value."""
        return self._disablePointerEvents.value if isinstance(self._disablePointerEvents, State) else self._disablePointerEvents

    @_validate_param(file_path=FILE_PATH, param_name="menu", supported_signatures=Union[State, Menu, type(None)])
    def _set_menu(self, value):
        """Assign value to menu."""
        self._menu = value

    def _get_menu(self):
        """Get the menu value."""
        return self._menu.value if isinstance(self._menu, State) else self._menu

    # @_validate_param(file_path=FILE_PATH, param_name="endIcon", supported_signatures=Union[State, PyIconify, type(None)])
    def _set_endIcon(self, value):
        """Assign value to endIcon."""
        self._endIcon = value

    def _get_endIcon(self):
        """Get the endIcon value."""
        return self._endIcon.value if isinstance(self._endIcon, State) else self._endIcon

    @_validate_param(file_path=FILE_PATH, param_name="fullWidth", supported_signatures=Union[State, bool, type(None)])
    def _set_fullWidth(self, value):
        """Assign value to fullWidth."""
        self._fullWidth = value

    def _get_fullWidth(self):
        """Get the fullWidth value."""
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    # @_validate_param(file_path=FILE_PATH, param_name="href", supported_signatures=Union[State, str, type(None)])
    def _set_href(self, value):
        """Assign value to href."""
        self._href = value

    def _get_href(self):
        """Get the href value."""
        return self._href.value if isinstance(self._href, State) else self._href

    @_validate_param(file_path=FILE_PATH, param_name="size", supported_signatures=Union[State, str, type(None)], valid_values=VALID_SIZES)
    def _set_size(self, value):
        """Assign value to size."""
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size

    # @_validate_param(file_path=FILE_PATH, param_name="startIcon", supported_signatures=Union[State, PyIconify, type(None)])
    def _set_startIcon(self, value):
        """Assign value to startIcon."""
        self._startIcon = value

    def _get_startIcon(self):
        """Get the startIcon value."""
        return self._startIcon.value if isinstance(self._startIcon, State) else self._startIcon

    @_validate_param(file_path=FILE_PATH, param_name="sx", supported_signatures=Union[State, Callable, str, Dict, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path=FILE_PATH, param_name="type", supported_signatures=Union[State, str, type(None)], valid_values=VALID_TYPES)
    def _set_type(self, value):
        """Assign value to type."""
        self._type = value

    def _get_type(self):
        """Get the type value."""
        return self._type.value if isinstance(self._type, State) else self._type

    @_validate_param(file_path=FILE_PATH, param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant