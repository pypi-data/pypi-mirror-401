import asyncio
import uuid
from typing import Dict, Union, Callable, Optional, Any
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton, QSizePolicy
from PySide6.QtCore import QSize, Qt, QTimer
from qtmui.hooks import State
from ..py_iconify import PyIconify
from ...qtmui_assets import QTMUI_ASSETS
from ..widget_base import PyWidgetBase
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ..utils.validate_params import _validate_param

class Chip(QFrame, PyWidgetBase):
    """
    A component that represents a compact element, such as a tag or choice, with customizable avatar, icon, label, and delete functionality.

    The `Chip` component is used to display a small piece of information, such as a tag, with optional avatar, icon, and delete button.
    It supports all props of the Material-UI `Chip` component, as well as an additional `key` prop for custom identification.
    Props of the native component are supported via `**kwargs`.

    Parameters
    ----------
    label : State or Any
        The content of the component (required). Can be a `State` object for dynamic updates.
    avatar : State, Any, or None, optional
        The avatar element to display. Default is None. Can be a `State` object for dynamic updates.
    children : State, Any, or None, optional
        Not supported; use `component` prop to change the root node structure. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    clickable : State, bool, or None, optional
        If True, the chip appears clickable and raises when pressed. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component (e.g., "default", "primary", or custom color). Default is "default".
        Can be a `State` object for dynamic updates.
    component : State, Any, or None, optional
        Component used for the root node (e.g., HTML element or custom component). Default is None.
        Can be a `State` object for dynamic updates.
    deleteIcon : State, Any, or None, optional
        Override the default delete icon element. Shown only if `onDelete` is set. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State, Any, or None, optional
        Icon element to display. Default is None. Can be a `State` object for dynamic updates.
    key : State, Any, or None, optional
        Custom key for identification. Default is None. Can be a `State` object for dynamic updates.
    onDelete : State, Callable, or None, optional
        Callback fired when the delete icon is clicked. If set, the delete icon is shown. Default is None.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the component ("small", "medium", or custom). Default is "medium".
        Can be a `State` object for dynamic updates.
    skipFocusWhenDisabled : State or bool, optional
        If True, the disabled chip escapes focus. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The variant to use ("filled", "outlined", or custom). Default is "filled".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for the `color` parameter: ["default", "primary", "secondary", "error", "info", "success", "warning"].
    VALID_SIZES : list[str]
        Valid values for the `size` parameter: ["small", "medium"].
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["filled", "outlined"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `children` prop is not supported; use the `component` prop to change the root node structure.
    - The `key` prop is specific to this implementation and not part of Material-UI `Chip`.

    Demos:
    - Chip: https://qtmui.com/material-ui/qtmui-chip/

    API Reference:
    - Chip API: https://qtmui.com/material-ui/api/chip/
    """

    VALID_COLORS = ["default", "primary", "secondary", "error", "info", "success", "warning"]
    VALID_SIZES = ["small", "medium"]
    VALID_VARIANTS = ["filled", "outlined"]

    def __init__(
        self,
        label: Optional[Union[State, str, Callable]] = None,
        avatar: Optional[Union[State, Any]] = None,
        children: Optional[Union[State, Any]] = None,
        classes: Optional[Union[State, Dict]] = None,
        clickable: Optional[Union[State, bool]] = None,
        color: Union[State, str] = "default",
        component: Optional[Union[State, Any]] = None,
        deleteIcon: Optional[Union[State, Any]] = None,
        disabled: Union[State, bool] = False,
        icon: Optional[Union[State, Any]] = None,
        key: Optional[Union[State, Any]] = None,
        onDelete: Optional[Union[State, Callable]] = None,
        size: Union[State, str] = "medium",
        skipFocusWhenDisabled: Union[State, bool] = False,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        variant: Union[State, str] = "filled",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"PyChip_{uuid.uuid4()}")

        self.theme = useTheme()

        # Set properties with validation
        self._set_label(label)
        self._set_avatar(avatar)
        self._set_children(children)
        self._set_classes(classes)
        self._set_clickable(clickable)
        self._set_color(color)
        self._set_component(component)
        self._set_deleteIcon(deleteIcon)
        self._set_disabled(disabled)
        self._set_icon(icon)
        self._set_key(key)
        self._set_onDelete(onDelete)
        self._set_size(size)
        self._set_skipFocusWhenDisabled(skipFocusWhenDisabled)
        self._set_sx(sx)
        self._set_variant(variant)

        self._btn_delete_icon = None
        self._init_ui()


    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.chip", param_name="label", supported_signatures=Union[State, Any])
    def _set_label(self, value):
        if value is None:
            raise ValueError("label is required")
        self._label = value

    def _get_label(self):
        return self._label.value if isinstance(self._label, State) else self._label

    # @_validate_param(file_path="qtmui.material.chip", param_name="avatar", supported_signatures=Union[State, Any, type(None)])
    def _set_avatar(self, value):
        self._avatar = value

    def _get_avatar(self):
        return self._avatar.value if isinstance(self._avatar, State) else self._avatar

    # @_validate_param(file_path="qtmui.material.chip", param_name="children", supported_signatures=Union[State, Any, type(None)])
    def _set_children(self, value):
        if value is not None:
            print("Warning: The `children` prop is not supported in Chip; use `component` prop instead.")
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.chip", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.chip", param_name="clickable", supported_signatures=Union[State, bool, type(None)])
    def _set_clickable(self, value):
        self._clickable = value

    def _get_clickable(self):
        return self._clickable.value if isinstance(self._clickable, State) else self._clickable

    @_validate_param(file_path="qtmui.material.chip", param_name="color", supported_signatures=Union[State, str], valid_values=VALID_COLORS + ["custom"])
    def _set_color(self, value):
        if value not in self.VALID_COLORS and not value.startswith("#"):
            raise ValueError(f"color must be one of {self.VALID_COLORS} or a hex color string")
        self._color = value

    def _get_color(self):
        return self._color.value if isinstance(self._color, State) else self._color

    # @_validate_param(file_path="qtmui.material.chip", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    # @_validate_param(file_path="qtmui.material.chip", param_name="deleteIcon", supported_signatures=Union[State, Any, type(None)])
    def _set_deleteIcon(self, value):
        self._deleteIcon = value

    def _get_deleteIcon(self):
        return self._deleteIcon.value if isinstance(self._deleteIcon, State) else self._deleteIcon

    @_validate_param(file_path="qtmui.material.chip", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        self._disabled = value

    def _get_disabled(self):
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    # @_validate_param(file_path="qtmui.material.chip", param_name="icon", supported_signatures=Union[State, Any, type(None)])
    def _set_icon(self, value):
        self._icon = value

    def _get_icon(self):
        return self._icon.value if isinstance(self._icon, State) else self._icon

    # @_validate_param(file_path="qtmui.material.chip", param_name="key", supported_signatures=Union[State, Any, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.chip", param_name="onDelete", supported_signatures=Union[State, Callable, type(None)])
    def _set_onDelete(self, value):
        self._onDelete = value

    def _get_onDelete(self):
        return self._onDelete.value if isinstance(self._onDelete, State) else self._onDelete

    @_validate_param(file_path="qtmui.material.chip", param_name="size", supported_signatures=Union[State, str], valid_values=VALID_SIZES)
    def _set_size(self, value):
        self._size = value

    def _get_size(self):
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.chip", param_name="skipFocusWhenDisabled", supported_signatures=Union[State, bool])
    def _set_skipFocusWhenDisabled(self, value):
        self._skipFocusWhenDisabled = value

    def _get_skipFocusWhenDisabled(self):
        return self._skipFocusWhenDisabled.value if isinstance(self._skipFocusWhenDisabled, State) else self._skipFocusWhenDisabled

    @_validate_param(file_path="qtmui.material.chip", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.chip", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        return self._variant.value if isinstance(self._variant, State) else self._variant

    def _init_ui(self):
        self.setObjectName("PyChip")

        if self._variant not in ["soft", "outlined", "filled"]:
            raise TypeError(f"Argument 'variant' has incorrect value (expected in ['soft', 'outlined', 'filled'], got {self._variant})")

        if self._disabled:
            self.setEnabled(False)

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        if self._avatar:
            self.layout().addWidget(self._avatar)

        elif self._icon:
            self.layout().addWidget(self._icon)


        self._lbl_content = QLabel(self._label)
        self._lbl_content.setObjectName('MuiChipTextContent')
        self.layout().addWidget(self._lbl_content)

        if self._deleteIcon:
            self._btn_delete_icon = self._deleteIcon
            self._btn_delete_icon.setCursor(Qt.PointingHandCursor)
            self.layout().addWidget(self._btn_delete_icon)
        elif self._onDelete:
            if not self._btn_delete_icon:
                self._btn_delete_icon = QToolButton()
                self._btn_delete_icon.clicked.connect(lambda checked, key=self._key: self._onDelete(key))
                self._btn_delete_icon.setCursor(Qt.PointingHandCursor)
                self.layout().addWidget(self._btn_delete_icon)

        if self._btn_delete_icon:
            self._btn_delete_icon.setObjectName("MuiChipDeleteIcon")

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        ownerState = {}

        if not component_styled:
            component_styled = self.theme.components

        PyChip_root = component_styled[f"PyChip"].get("styles")["root"][self._color]
        PyChip_root_qss = get_qss_style(PyChip_root)

        PyChip_root_prop_variant_qss = get_qss_style(PyChip_root["props"][f"{self._variant}Variant"])
        PyChip_root_prop_variant_color = PyChip_root["props"][f"{self._variant}Variant"]["color"]
        PyChip_root_prop_variant_bg_color = PyChip_root["props"][f"{self._variant}Variant"]["background-color"]
        PyChip_root_prop_variant_classes_icon_color = PyChip_root["props"][f"{self._variant}Variant"]["classes"]["icon"]["color"]
        PyChip_root_prop_size_qss = get_qss_style(PyChip_root["props"][f"{self._size}Size"])
        PyChip_root_prop_variant_slot_hover_qss = get_qss_style(PyChip_root["props"][f"{self._variant}Variant"]["slots"]["hover"])

        PyChip_root_textContent_qss = get_qss_style(PyChip_root["textContent"])

        PyChip_root_deleteIcon_qss = get_qss_style(PyChip_root["deleteIcon"])
        PyChip_root_deleteIcon_size = PyChip_root["deleteIcon"]["size"]
        PyChip_root_deleteIcon_prop_variant_qss = get_qss_style(PyChip_root["deleteIcon"]["props"][f"{self._variant}Variant"])
        PyChip_root_deleteIcon_prop_variant_hover_qss = get_qss_style(PyChip_root["deleteIcon"]["props"][f"{self._variant}Variant"]["hover"])

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

        # MuiChip
        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyChip_root_qss}
                    {PyChip_root_prop_variant_qss}
                    {PyChip_root_prop_size_qss}
                }}

                #{self.objectName()}::hover {{
                    {PyChip_root_prop_variant_slot_hover_qss}
                }}

                {sx_qss}
            """
        )
        

        # MuiChipIcon
        # print("change___________chip_icon_colooooooooooo")


        # print('PyChip_root_prop_variant_color________', PyChip_root_prop_variant_color)

        # MuiChipTextContent
        self._lbl_content.setStyleSheet(
            f"""
                #MuiChipTextContent {{
                    color: {PyChip_root_prop_variant_color};
                    {PyChip_root_textContent_qss}
                }}
            """
        )

        # MuiChipDeleteIcon
        if self._btn_delete_icon:
            if self._deleteIcon:
                self._btn_delete_icon.enterEvent = self._on_mouse_enter_btn_del
                self._btn_delete_icon.leaveEvent = self._on_mouse_leave_btn_del
            else:
                self._btn_delete_icon.setIcon(PyIconify(key=QTMUI_ASSETS.ICONS.CLOSE, color=PyChip_root_prop_variant_bg_color if self._variant == "filled" else PyChip_root_prop_variant_classes_icon_color))
                
            # if self._color == "default":
                # self._btn_delete_icon.setIcon(FluentIconBase().icon_(path=":/baseline/resource_qtmui/baseline/close.svg", color=PyChip_root_prop_variant_classes_icon_color if self._variant == "filled" else "#eeeeee"))

            self._btn_delete_icon.setStyleSheet(f"""
                #MuiChipDeleteIcon {{
                    {PyChip_root_deleteIcon_qss}
                    {PyChip_root_deleteIcon_prop_variant_qss}
                }}
                #MuiChipDeleteIcon:hover {{
                    {PyChip_root_deleteIcon_prop_variant_hover_qss}
                }}
            """)

            self._btn_delete_icon.setIconSize(QSize(int(PyChip_root_deleteIcon_size*2/3), int(PyChip_root_deleteIcon_size*2/3)))
            self._btn_delete_icon.setFixedSize(PyChip_root_deleteIcon_size, PyChip_root_deleteIcon_size)



    def _on_mouse_enter_btn_del(self, event):
        if not self._disabled:
            print('chip______delete_icon.change_color')

    def _on_mouse_leave_btn_del(self, event):
        if not self._disabled:
            print('chip______delete_icon.change_color')


