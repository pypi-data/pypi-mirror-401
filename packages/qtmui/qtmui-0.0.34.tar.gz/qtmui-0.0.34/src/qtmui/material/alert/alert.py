import asyncio
from typing import Any, Optional, Callable, Union, List, Dict
import uuid
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QToolButton, QWidget, QSizePolicy, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.theme_reducer import ThemeState
from qtmui.material.styles.create_theme.create_palette import PaletteColor
from qtmui.utils.translator import getTranslatedText
from ..system.color_manipulator import alpha, lighten_hex
from ...common.icon import FluentIconBase
from ..widget_base import PyWidgetBase
from ..py_tool_button.py_tool_button import PyToolButton
from qtmui.i18n.use_translation import translate, i18n
from qtmui.hooks import State
from ..utils.validate_params import _validate_param
from ...qtmui_assets import QTMUI_ASSETS

class Alert(QFrame, PyWidgetBase):
    """
    A component that displays an alert message with customizable severity, color, and actions.

    The `Alert` component is used to convey important information to the user, such as success,
    warning, error, or info messages. It supports various customization options including
    severity-based styling, icons, actions, and close buttons. It inherits properties from
    `QFrame` and `Paper` components, including `elevation`. Props of the Material-UI `Paper`
    component are also supported.

    Parameters
    ----------
    action : State, QWidget, list[QWidget], or None, optional
        The action to display at the end of the alert. Default is None.
        Can be a `State` object for dynamic updates.
    alertTitle : State or str, optional
        The title of the alert, displayed above the main message. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, list[QWidget], or None, optional
        The content of the component, typically text or widgets. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    closeText : State or str, optional
        The label for the close button. Default is "Close".
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component. If not provided, it is derived from the `severity` prop.
        Supports "error", "info", "success", "warning", or custom theme colors.
        Default is None. Can be a `State` object for dynamic updates.
    components : State or dict, optional
        The components used for each slot inside (e.g., CloseButton, CloseIcon).
        Default is {}. Deprecated: Use `slots` instead.
        Can be a `State` object for dynamic updates.
    componentsProps : State or dict, optional
        Extra props for the slot components. Default is {}.
        Deprecated: Use `slotProps` instead.
        Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        The elevation level of the component, affecting the shadow depth (0-24).
        Default is 1. Can be a `State` object for dynamic updates.
    icon : State, PyToolButton, bool, or None, optional
        Override the icon displayed before the children. If False, no icon is displayed.
        Default is None. Can be a `State` object for dynamic updates.
    iconMapping : State or dict, optional
        Custom mapping of severity to icons. Default is None.
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        A unique identifier for the alert. Default is None.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the alert takes up the full width of its container. Default is True.
        Can be a `State` object for dynamic updates.
    onClose : State or Callable, optional
        Callback fired when the component requests to be closed.
        Signature: function(event: Any) => None.
        Default is None. Can be a `State` object for dynamic updates.
    role : State or str, optional
        The ARIA role attribute of the element. Default is "alert".
        Can be a `State` object for dynamic updates.
    severity : State or str, optional
        The severity of the alert, defining its color and icon.
        Valid values: "error", "info", "success", "warning".
        Default is "success". Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the alert (e.g., "small", "medium", "large"). Default is "medium".
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props used for each slot inside (e.g., action, closeButton, closeIcon, icon,
        message, root). Default is {}. Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components used for each slot inside (e.g., action, closeButton, closeIcon, icon,
        message, root). Default is {}. Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        The system prop for defining CSS overrides and additional styles.
        Default is None. Can be a `State` object for dynamic updates.
    text : State or str, optional
        The main message text of the alert.
        Default is "This is an info alert — check it out!".
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The visual style of the alert. Valid values: "filled", "outlined", "standard".
        Default is "standard". Can be a `State` object for dynamic updates.

    Attributes
    ----------
    VALID_SEVERITIES : list[str]
        Valid values for the `severity` parameter: ["error", "info", "success", "warning"].
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["filled", "outlined", "standard"].

    Demos:
    - Alert: https://qtmui.com/material-ui/qtmui-alert/

    API Reference:
    - Alert API: https://qtmui.com/material-ui/api/alert/
    """

    VALID_SEVERITIES = ["error", "info", "success", "warning"]
    VALID_VARIANTS = ["filled", "outlined", "standard"]

    def __init__(
        self,
        action: Optional[Union[State, QWidget, List[QWidget]]] = None,
        alertTitle: Optional[Union[State, str]] = None,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        closeText: Union[State, str] = "Close",
        color: Optional[Union[State, str]] = None,
        components: Optional[Union[State, Dict]] = None,
        componentsProps: Optional[Union[State, Dict]] = None,
        elevation: Optional[Union[State, int]] = 1,
        icon: Optional[Union[State, PyToolButton, bool]] = None,
        iconMapping: Optional[Union[State, Dict]] = None,
        key: Optional[Union[State, str]] = None,
        fullWidth: Union[State, bool] = True,
        onClose: Optional[Union[State, Callable[[Any], None]]] = None,
        role: Union[State, str] = "alert",
        severity: Union[State, str] = "success",
        size: Union[State, str] = "medium",
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        text: Optional[Union[str, State, Callable]] = "This is an info alert — check it out!",
        variant: Union[State, str] = "standard",
    ):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_action(action)
        self._set_alertTitle(alertTitle)
        self._set_children(children)
        self._set_classes(classes)
        self._set_closeText(closeText)
        self._set_color(color)
        self._set_components(components)
        self._set_componentsProps(componentsProps)
        self._set_elevation(elevation)
        self._set_icon(icon)
        self._set_iconMapping(iconMapping)
        self._set_key(key)
        self._set_fullWidth(fullWidth)
        self._set_onClose(onClose)
        self._set_role(role)
        self._set_severity(severity)
        self._set_size(size)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_text(text)
        self._set_variant(variant)

        if not self._get_color():
            self._set_color(self._get_severity())

        self._btn_close = None
        self._lbl_alert_title = None
        self._lbl_alert_text = None
        self._frm_left = None
        self._frm_right = None
        self._frm_right_action = None
        self._init_ui()

    # @_validate_param(file_path="qtmui.material.alert", param_name="action", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_action(self, value):
        self._action = value

    def _get_action(self):
        return self._action.value if isinstance(self._action, State) else self._action

    @_validate_param(file_path="qtmui.material.alert", param_name="alertTitle", supported_signatures=Union[State, str, type(None)])
    def _set_alertTitle(self, value):
        self._alertTitle = value

    def _get_alertTitle(self):
        return self._alertTitle.value if isinstance(self._alertTitle, State) else self._alertTitle

    # @_validate_param(file_path="qtmui.material.alert", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.alert", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.alert", param_name="closeText", supported_signatures=Union[State, str])
    def _set_closeText(self, value):
        self._closeText = value

    def _get_closeText(self):
        return self._closeText.value if isinstance(self._closeText, State) else self._closeText

    @_validate_param(file_path="qtmui.material.alert", param_name="color", supported_signatures=Union[State, str, type(None)])
    def _set_color(self, value):
        self._color = value

    def _get_color(self):
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.alert", param_name="components", supported_signatures=Union[State, Dict, type(None)])
    def _set_components(self, value):
        self._components = value or {}

    def _get_components(self):
        return self._components.value if isinstance(self._components, State) else self._components

    @_validate_param(file_path="qtmui.material.alert", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_componentsProps(self, value):
        self._componentsProps = value or {}

    def _get_componentsProps(self):
        return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

    # @_validate_param(file_path="qtmui.material.alert", param_name="elevation", supported_signatures=Union[State, int, type(None)], valid_values=range(0, 25))
    def _set_elevation(self, value):
        self._elevation = value

    def _get_elevation(self):
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(file_path="qtmui.material.alert", param_name="icon", supported_signatures=Union[State, PyToolButton, bool, type(None)])
    def _set_icon(self, value):
        self._icon = value

    def _get_icon(self):
        return self._icon.value if isinstance(self._icon, State) else self._icon

    @_validate_param(file_path="qtmui.material.alert", param_name="iconMapping", supported_signatures=Union[State, Dict, type(None)])
    def _set_iconMapping(self, value):
        self._iconMapping = value

    def _get_iconMapping(self):
        return self._iconMapping.value if isinstance(self._iconMapping, State) else self._iconMapping

    @_validate_param(file_path="qtmui.material.alert", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.alert", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        self._fullWidth = value

    def _get_fullWidth(self):
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.alert", param_name="onClose", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClose(self, value):
        self._onClose = value

    def _get_onClose(self):
        return self._onClose.value if isinstance(self._onClose, State) else self._onClose

    @_validate_param(file_path="qtmui.material.alert", param_name="role", supported_signatures=Union[State, str])
    def _set_role(self, value):
        self._role = value

    def _get_role(self):
        return self._role.value if isinstance(self._role, State) else self._role

    @_validate_param(file_path="qtmui.material.alert", param_name="severity", supported_signatures=Union[State, str], valid_values=VALID_SEVERITIES)
    def _set_severity(self, value):
        self._severity = value

    def _get_severity(self):
        return self._severity.value if isinstance(self._severity, State) else self._severity

    @_validate_param(file_path="qtmui.material.alert", param_name="size", supported_signatures=Union[State, str])
    def _set_size(self, value):
        self._size = value

    def _get_size(self):
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.alert", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value or {}

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.alert", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value or {}

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.alert", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.alert", param_name="text", supported_signatures=Union[State, str, Callable])
    def _set_text(self, value):
        self._text = value

    def _get_text(self):
        return self._text.value if isinstance(self._text, State) else self._text

    @_validate_param(file_path="qtmui.material.alert", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        return self._variant.value if isinstance(self._variant, State) else self._variant

    def __setupStates(self):
        if isinstance(self._text, State):
            self._text.valueChanged.connect(self.retranslateUi)

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        # self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter)

        self._icon = self._get_icon_by_severity()

        self._frm_left = QWidget()
        self._frm_left.setStyleSheet('background: transparent; border: none;')
        self._frm_left.setLayout(QVBoxLayout())
        self._frm_left.layout().setContentsMargins(0,0,0,0)
        self._frm_left.layout().addWidget(self._icon)
        self._frm_left.layout().setAlignment(Qt.AlignmentFlag.AlignTop if not self._action else Qt.AlignmentFlag.AlignCenter)
        self._frm_left.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        self.layout().addWidget(self._frm_left)

        self.frm_content = QWidget()
        self.frm_content.setStyleSheet('background: transparent; border: none;')
        self.vlo_frm_content = QVBoxLayout(self.frm_content)
        self.frm_content.setLayout(self.vlo_frm_content)
        self.vlo_frm_content.setContentsMargins(0,0,0,0)
        if self._alertTitle:
            self._lbl_alert_title = QLabel(self)
            self._lbl_alert_title.setObjectName("PyAlertTitle")
            self.vlo_frm_content.addWidget(self._lbl_alert_title)

        self._lbl_alert_text = QLabel(self)
        self._lbl_alert_text.setObjectName("PyAlertContent")
        self.vlo_frm_content.addWidget(self._lbl_alert_text)

        self.layout().addWidget(self.frm_content)

        self._frm_right = QWidget()
        self._frm_right.setStyleSheet('background: transparent; border: none;')
        self._frm_right.setLayout(QVBoxLayout())
        self._frm_right.layout().setContentsMargins(0,0,0,0)
        self._frm_right.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self._frm_right.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.layout().addWidget(self._frm_right)

        if self._action:
            self._frm_right_action = QWidget()
            self._frm_right_action.setStyleSheet('background: transparent; border: none;')
            self._frm_right_action.setLayout(QHBoxLayout())
            self._frm_right_action.layout().setContentsMargins(0,0,0,0)
            self._frm_right_action.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
            self._frm_right.layout().addWidget(self._frm_right_action)
            if isinstance(self._action, list):
                for widget in self._action:
                    self._frm_right_action.layout().addWidget(widget)
            else:
                self._frm_right_action.layout().addWidget(self._action)

        if self._onClose:
            self._btn_close = QToolButton()
            self._btn_close.setCursor(Qt.PointingHandCursor)
            self._btn_close.clicked.connect(self._onClose)

            self._frm_right.layout().addWidget(self._btn_close)


        # init theme & language
        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)
        
        self.__setupStates()

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def retranslateUi(self):
        if self._lbl_alert_title:
            self._lbl_alert_title.setText(getTranslatedText(self._alertTitle))
        if self._lbl_alert_text:
            self._lbl_alert_text.setText(getTranslatedText(self._text))
        # if isinstance(self._alertTitle, Callable):
        #     self._lbl_alert_title.setText(translate(self._alertTitle).capitalize())
        # else:
        #     if self._lbl_alert_title:
        #         self._lbl_alert_title.setText(self._alertTitle.capitalize())

        # if isinstance(self._text, Callable):
        #     self._lbl_alert_text.setText(translate(self._text))
        # else:
        #     self._lbl_alert_text.setText(self._text)

    def _set_stylesheet(self, _theme=None):
        theme = useTheme()
        component_styles = theme.components

        self._component_name = f"PyAlert{self._variant.capitalize()}"

        # styles
        PyAlert_root = component_styles[self._component_name].get("styles")["root"][self._color]
        PyAlert_root_color = PyAlert_root['color']
        PyAlert_root_qss = get_qss_style(PyAlert_root)

        PyAlertTitle_root = component_styles["PyAlertTitle"].get("styles")["root"]
        PyAlertTitle_root_qss = get_qss_style(PyAlertTitle_root[self._color])

        # override
        PyAlert_root_qss_override = ""
        PyAlert_root_color_override = None
        if component_styles[self._component_name].get("styleOverrides"):
            PyAlert_root_override = component_styles[self._component_name].get("styleOverrides")["root"][self._color]
            PyAlert_root_color_override = PyAlert_root_override['color']
            PyAlert_root_qss_override = get_qss_style(PyAlert_root_override)

        PyAlertTitle_root_qss_override = ""
        if component_styles[self._component_name].get("styleOverrides"):
            PyAlertTitle_root_override = component_styles["PyAlertTitle"].get("styleOverrides")["root"]
            PyAlertTitle_root_qss_override = get_qss_style(PyAlertTitle_root_override[self._color])

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


        # if self._lbl_alert_title:
        #     stylesheet = f"""
        #         #PyAlertTitle {{
        #             {PyAlertTitle_root_qss}
        #             {PyAlertTitle_root_qss_override}
        #             {sx_qss}
        #         }}
        #     """
        #     print('stylesheet_________', stylesheet)
        #     self._lbl_alert_title.setStyleSheet(stylesheet)

        # self._lbl_alert_text.setStyleSheet(f"""
        #     #PyAlertContent {{
        #         color: {PyAlert_root_color_override or PyAlert_root_color};
        #     }}
        # """)

        self.setStyleSheet(f"""
            #{self.objectName()} {{
                {PyAlert_root_qss}
                {PyAlert_root_qss_override}
            }}

            #PyAlertTitle {{
                {PyAlertTitle_root_qss}
                {PyAlertTitle_root_qss_override}
            }}

            #PyAlertContent {{
                color: {PyAlert_root_color_override or PyAlert_root_color};
            }}

            {sx_qss}

        """)


        # icon && tool button
        if self._btn_close:
            self._btn_close.setIcon(FluentIconBase().icon_(path=QTMUI_ASSETS.ICONS.CLOSE, color=PyAlert_root_color))
            self._btn_close.setStyleSheet(self._btn_close.styleSheet() + f"""
                QToolButton {{
                    background-color: transparent;
                    border: none;
                    padding: 2px;
                    border-radius: 8px;
                }}
                QToolButton:hover {{
                    background-color: {alpha(PyAlert_root_color_override or PyAlert_root_color, 0.36)};
                }}
            """)

            self._btn_close.setFixedSize(18, 18)

        # print('alert__icon.change__colo__')


    def _map_severity_to_color(self, severity: str) -> str:
        """Map mức độ severity sang màu mặc định."""
        color_mapping = {
            'error': 'red',
            'info': 'blue',
            'success': 'green',
            'warning': 'orange'
        }
        return color_mapping.get(severity, 'success')

    def _get_icon_by_severity(self) -> PyToolButton:
        """Lấy icon mặc định dựa vào mức độ severity."""
        default_icons = {
            'error': QTMUI_ASSETS.ICONS.ALERT.ERROR,
            'info': QTMUI_ASSETS.ICONS.ALERT.INFO,
            'success': QTMUI_ASSETS.ICONS.ALERT.SUCCESS,
            'warning': QTMUI_ASSETS.ICONS.ALERT.WARNING
        }
        return PyToolButton(icon=default_icons.get(self._severity, QTMUI_ASSETS.ICONS.ALERT.INFO))

    def _default_icon_mapping(self) -> dict:
        """Trả về mapping mặc định giữa severity và icon."""
        return {
            'error': 'ErrorOutlinedIcon',
            'info': 'InfoOutlinedIcon',
            'success': 'SuccessOutlinedIcon',
            'warning': 'WarningOutlinedIcon',
        }

    def close(self, event: Any) -> None:
        """Gọi callback onClose nếu được cung cấp."""
        if self._onClose:
            self._onClose(event)

    def render(self) -> dict:
        """Render component Alert thành một đối tượng có thể sử dụng."""
        return {
            'action': self._action,
            'children': self._children,
            'classes': self._classes,
            'closeText': self._closeText,
            'color': self._color,
            'components': self._components,
            'componentsProps': self._componentsProps,
            'icon': self._icon,
            'iconMapping': self._iconMapping,
            'onClose': self._onClose,
            'role': self._role,
            'severity': self._severity,
            'slotProps': self._slotProps,
            'slots': self._slots,
            'sx': self._sx,
            'variant': self._variant,
        }

