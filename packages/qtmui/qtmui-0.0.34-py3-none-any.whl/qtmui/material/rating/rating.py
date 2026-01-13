from typing import Optional, Union, Callable, Dict, List, Any
import uuid
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QWidget
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QCursor
from ..system.color_manipulator import lighten, rgbToHex
from ..py_tool_button import PyToolButton
from ..py_iconify import PyIconify, Iconify
from ..widget_base import PyWidgetBase
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ...qtmui_assets import QTMUI_ASSETS
from qtmui.hooks import State
from ..utils.validate_params import _validate_param

class Rating(QFrame, PyWidgetBase):
    """
    A rating component, styled like Material-UI Rating.

    The `Rating` component allows users to select a rating value using icons. It integrates with the `qtmui`
    framework, retaining existing parameters, adding new parameters, and aligning with MUI Rating props.
    Inherits from native component props.

    Parameters
    ----------
    max : State or int, optional
        Maximum rating. Default is 5.
        Can be a `State` object for dynamic updates.
    value : State, float, or None, optional
        The rating value. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State, QWidget, Callable, or None, optional
        The icon to display for selected ratings. Default is None.
        Can be a `State` object for dynamic updates or a Callable returning a QWidget.
    color : State or str, optional
        The color of the component. Default is None.
        Can be a `State` object for dynamic updates.
    name : State or str, optional
        The name attribute of the radio input elements. Default is None.
        Can be a `State` object for dynamic updates.
    readOnly : State or bool, optional
        If True, removes all hover effects and pointer events. Default is False.
        Can be a `State` object for dynamic updates.
    precision : State or float, optional
        The minimum increment value change allowed. Default is 1.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the value changes. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (event: Any, value: float | None) -> None
    onChangeActive : State or Callable, optional
        Callback fired when the hover state changes. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (event: Any, value: float) -> None
    size : State or str, optional
        The size of the component ('small', 'medium', 'large'). Default is 'medium'.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or type, optional
        The component used for the root node. Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    defaultValue : State, float, or None, optional
        The default value when not controlled. Default is None.
        Can be a `State` object for dynamic updates.
    emptyIcon : State, QWidget, Callable, or None, optional
        The icon to display when empty. Default is None.
        Can be a `State` object for dynamic updates or a Callable returning a QWidget.
    emptyLabelText : State or str, optional
        The label read when the rating input is empty. Default is None.
        Can be a `State` object for dynamic updates.
    getLabelText : State or Callable, optional
        Function to provide a user-friendly name for the current value. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (value: float) -> str
    highlightSelectedOnly : State or bool, optional
        If True, only the selected icon is highlighted. Default is False.
        Can be a `State` object for dynamic updates.
    IconContainerComponent : State or type, optional
        The component containing the icon (deprecated, use slotProps.icon). Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for slots ({decimal, icon, label, root}). Default is {}.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for slots ({decimal, icon, label, root}). Default is {}.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent component,
        supporting props of the native component.

    Signals
    -------
    changed : Signal
        Emitted when the rating value changes.
    activeChanged : Signal
        Emitted when the hover state changes.

    Notes
    -----
    - Existing parameters are retained; new parameters added to align with MUI.
    - Props of the native component are supported via `**kwargs`.
    - MUI classes applied: `MuiRating-root`, `Mui-disabled`.
    - Integrates with `PyToolButton` and `PyIconify` for icon rendering.

    Demos:
    - Rating: https://qtmui.com/material-ui/qtmui-rating/

    API Reference:
    - Rating API: https://qtmui.com/material-ui/api/rating/
    """

    changed = Signal(object, float)
    activeChanged = Signal(object, float)

    VALID_SIZES = ['small', 'medium', 'large']

    def __init__(
        self,
        max: Union[State, int] = 5,
        value: Optional[Union[State, float]] = None,
        disabled: Union[State, bool] = False,
        icon: Optional[Union[State, Iconify]] = None,
        color: Optional[Union[State, str]] = None,
        name: Optional[Union[State, str]] = None,
        readOnly: Union[State, bool] = False,
        precision: Union[State, float] = 1,
        onChange: Optional[Union[State, Callable]] = None,
        onChangeActive: Optional[Union[State, Callable]] = None,
        size: Union[State, str] = 'medium',
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, type]] = None,
        defaultValue: Optional[Union[State, float]] = None,
        emptyIcon: Optional[Union[State, QWidget, Callable]] = None,
        emptyLabelText: Optional[Union[State, str]] = None,
        getLabelText: Optional[Union[State, Callable]] = None,
        highlightSelectedOnly: Union[State, bool] = False,
        IconContainerComponent: Optional[Union[State, type]] = None,
        slotProps: Union[State, Dict] = {},
        slots: Union[State, Dict] = {},
        *args,
        **kwargs
    ):
        root_component = component if component else QFrame
        super().__init__(*args, **kwargs, __class__=root_component)
        self.setObjectName(f"Rating-{str(uuid.uuid4())}")
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()
        self._widget_references = []
        self._currentValue = None

        # Set properties with validation
        self._set_max(max)
        self._set_value(value)
        self._set_disabled(disabled)
        self._set_icon(icon)
        self._set_color(color)
        self._set_name(name)
        self._set_readOnly(readOnly)
        self._set_precision(precision)
        self._set_onChange(onChange)
        self._set_onChangeActive(onChangeActive)
        self._set_size(size)
        self._set_sx(sx)
        self._set_classes(classes)
        self._set_component(component)
        self._set_defaultValue(defaultValue)
        self._set_emptyIcon(emptyIcon)
        self._set_emptyLabelText(emptyLabelText)
        self._set_getLabelText(getLabelText)
        self._set_highlightSelectedOnly(highlightSelectedOnly)
        self._set_IconContainerComponent(IconContainerComponent)
        self._set_slotProps(slotProps)
        self._set_slots(slots)

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.rating", param_name="max", supported_signatures=Union[State, int], validator=lambda x: x > 0)
    def _set_max(self, value):
        """Assign value to max."""
        self._max = value

    def _get_max(self):
        """Get the max value."""
        return self._max.value if isinstance(self._max, State) else self._max

    # @_validate_param(file_path="qtmui.material.rating", param_name="value", supported_signatures=Union[State, float, type(None)])
    def _set_value(self, value):
        """Assign value to value."""
        self._value = value
        self._currentValue = value.value if isinstance(value, State) else value

    def _get_value(self):
        """Get the value value."""
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.rating", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value
        self.setEnabled(not (value.value if isinstance(value, State) else value))

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    # @_validate_param(file_path="qtmui.material.rating", param_name="icon", supported_signatures=Union[State, QWidget, Callable, type(None)])
    def _set_icon(self, value):
        """Assign value to icon."""
        self._icon = value

    def _get_icon(self):
        """Get the icon value."""
        icon = self._icon
        if isinstance(icon, State):
            icon = icon.value
        if callable(icon):
            icon = icon()
        return icon if isinstance(icon, QWidget) else None

    @_validate_param(file_path="qtmui.material.rating", param_name="color", supported_signatures=Union[State, str, type(None)])
    def _set_color(self, value):
        """Assign value to color."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.rating", param_name="name", supported_signatures=Union[State, str, type(None)])
    def _set_name(self, value):
        """Assign value to name."""
        self._name = value

    def _get_name(self):
        """Get the name value."""
        return self._name.value if isinstance(self._name, State) else self._name

    @_validate_param(file_path="qtmui.material.rating", param_name="readOnly", supported_signatures=Union[State, bool])
    def _set_readOnly(self, value):
        """Assign value to readOnly."""
        self._readOnly = value

    def _get_readOnly(self):
        """Get the readOnly value."""
        return self._readOnly.value if isinstance(self._readOnly, State) else self._readOnly

    # @_validate_param(file_path="qtmui.material.rating", param_name="precision", supported_signatures=Union[State, float], validator=lambda x: x > 0)
    def _set_precision(self, value):
        """Assign value to precision."""
        self._precision = value

    def _get_precision(self):
        """Get the precision value."""
        return self._precision.value if isinstance(self._precision, State) else self._precision

    @_validate_param(file_path="qtmui.material.rating", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        """Assign value to onChange."""
        self._onChange = value

    def _get_onChange(self):
        """Get the onChange value."""
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.rating", param_name="onChangeActive", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChangeActive(self, value):
        """Assign value to onChangeActive."""
        self._onChangeActive = value

    def _get_onChangeActive(self):
        """Get the onChangeActive value."""
        return self._onChangeActive.value if isinstance(self._onChangeActive, State) else self._onChangeActive

    @_validate_param(file_path="qtmui.material.rating", param_name="size", supported_signatures=Union[State, str], valid_values=VALID_SIZES)
    def _set_size(self, value):
        """Assign value to size."""
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.rating", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.rating", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.rating", param_name="component", supported_signatures=Union[State, type, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.rating", param_name="defaultValue", supported_signatures=Union[State, float, type(None)])
    def _set_defaultValue(self, value):
        """Assign value to defaultValue."""
        self._defaultValue = value

    def _get_defaultValue(self):
        """Get the defaultValue value."""
        return self._defaultValue.value if isinstance(self._defaultValue, State) else self._defaultValue

    @_validate_param(file_path="qtmui.material.rating", param_name="emptyIcon", supported_signatures=Union[State, QWidget, Callable, type(None)])
    def _set_emptyIcon(self, value):
        """Assign value to emptyIcon."""
        self._emptyIcon = value

    def _get_emptyIcon(self):
        """Get the emptyIcon value."""
        icon = self._emptyIcon
        if isinstance(icon, State):
            icon = icon.value
        if callable(icon):
            icon = icon()
        return icon if isinstance(icon, QWidget) else None

    @_validate_param(file_path="qtmui.material.rating", param_name="emptyLabelText", supported_signatures=Union[State, str, type(None)])
    def _set_emptyLabelText(self, value):
        """Assign value to emptyLabelText."""
        self._emptyLabelText = value

    def _get_emptyLabelText(self):
        """Get the emptyLabelText value."""
        return self._emptyLabelText.value if isinstance(self._emptyLabelText, State) else self._emptyLabelText

    @_validate_param(file_path="qtmui.material.rating", param_name="getLabelText", supported_signatures=Union[State, Callable, type(None)])
    def _set_getLabelText(self, value):
        """Assign value to getLabelText."""
        self._getLabelText = value

    def _get_getLabelText(self):
        """Get the getLabelText value."""
        return self._getLabelText.value if isinstance(self._getLabelText, State) else self._getLabelText

    @_validate_param(file_path="qtmui.material.rating", param_name="highlightSelectedOnly", supported_signatures=Union[State, bool])
    def _set_highlightSelectedOnly(self, value):
        """Assign value to highlightSelectedOnly."""
        self._highlightSelectedOnly = value

    def _get_highlightSelectedOnly(self):
        """Get the highlightSelectedOnly value."""
        return self._highlightSelectedOnly.value if isinstance(self._highlightSelectedOnly, State) else self._highlightSelectedOnly

    @_validate_param(file_path="qtmui.material.rating", param_name="IconContainerComponent", supported_signatures=Union[State, type, type(None)])
    def _set_IconContainerComponent(self, value):
        """Assign value to IconContainerComponent."""
        self._IconContainerComponent = value

    def _get_IconContainerComponent(self):
        """Get the IconContainerComponent value."""
        return self._IconContainerComponent.value if isinstance(self._IconContainerComponent, State) else self._IconContainerComponent

    @_validate_param(file_path="qtmui.material.rating", param_name="slotProps", supported_signatures=Union[State, Dict])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.rating", param_name="slots", supported_signatures=Union[State, Dict])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots


    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _init_ui(self):
        self.theme = useTheme()

        icon_width = self.theme.components["PyRating"].get("styles")["root"]["props"][f"size{self._size.capitalize()}"]["svgIcon"]["width"]
        icon_height = self.theme.components["PyRating"].get("styles")["root"]["props"][f"size{self._size.capitalize()}"]["svgIcon"]["height"]
        self._iconSize = QSize(icon_width, icon_height)

        self._selected_color = self.theme.components["PyRating"].get("styles")["icon"]["root"]["slots"]["selected"]["color"]
        self._unselect_color = self.theme.components["PyRating"].get("styles")["icon"]["root"]["color"]

        if self._disabled:
            self.setEnabled(False)
            self._selected_color = self.theme.components["PyRating"].get("styles")["icon"]["root"]["slots"]["selected"]["color"]
            self._unselect_color = self.theme.components["PyRating"].get("styles")["icon"]["root"]["color"]

        # Thiết lập layout cho các biểu tượng rating
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Danh sách các biểu tượng (PyToolButton)
        self._icons = []

        # Tạo các biểu tượng và thêm chúng vào layout
        for i in range(self._max):
            
            if not isinstance(self._icon, Iconify):
                self._icon = Iconify(key="material-symbols:star-rounded")
                # self._icon = Iconify(key="material-symbols:heart-broken")
            self.ratingButton = PyToolButton(icon=self._icon, iconSize=self._iconSize, tooltip=f"{i + 1} Star")
            # self.ratingButton = PyToolButton(icon=Iconify(key=self._icon or QTMUI_ASSETS.ICONS.STAR, color="#555555", size=self._iconSize), size=self._iconSize, tooltip=f"{i + 1} Star")
            self.ratingButton.setCursor(QCursor(Qt.PointingHandCursor))
            
            self.ratingButton.setIconSize(self._iconSize)

            # Đặt màu mặc định cho các icon dựa trên giá trị value
            if i < self._value:
                # self.ratingButton._set_text_color(self._selected_color)  # Màu được chọn
                self.ratingButton._set_text_color("#FFAB00")  # Màu được chọn
            else:
                self.ratingButton._set_text_color(self._unselect_color)  # Màu chưa được chọn

            # Thêm sự kiện hover cho từng icon
            self.ratingButton.enterEvent = lambda event, idx=i: self._on_hover_enter(idx)
            self.ratingButton.leaveEvent = lambda event, idx=i: self._on_hover_leave(idx)
            self.ratingButton.clicked.connect(lambda checked, idx=i: self._on_icon_clicked(idx))
            
            # Thêm icon vào layout và danh sách icon
            self._layout.addWidget(self.ratingButton)
            self._icons.append(self.ratingButton)

        self.setFixedWidth(self.sizeHint().width() + 10)
        self.setMinimumHeight(self.sizeHint().height() + 5)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        if self._disabled:
            self.setProperty("disabled", "true")
        if self._size == "small":

            
            self.setProperty("size", "small")
        elif self._size == "medium":
            self.setProperty("size", "medium")
        else: # large
            self.setProperty("size", "large")

        PyRating_root = component_styled[f"PyRating"].get("styles")["root"]
        PyRating_root_slot_disabled_qss = get_qss_style(PyRating_root["slots"]["disabled"])
        PyRating_root_slot_smallSize_width = component_styled["PyRating"].get("styles")["root"]["props"][f"size{self._size.capitalize()}"]["svgIcon"]["width"]

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

        # self.setStyleSheet(
        #     f"""
        #         #PyRating {{
        #         }}
        #         #PyRating[disabled=true] {{
        #             {PyRating_root_slot_disabled_qss}
        #         }}
        #         #PyRating[size=small] {{
        #         }}
        #         #PyRating[size=medium] {{
        #         }}
        #         #PyRating[size=large] {{
        #         }}
        #     """
        # )
        


    def _on_hover_enter(self, index):
        """
        Xử lý khi hover vào một icon, thay đổi kích thước và tô màu từ vị trí hiện tại về trước.
        """
        if not self._disabled and not self._readOnly:
            for i in range(self._max):
                self._icons[i].setIconSize(self._iconSize)
                self._icons[i].setFixedSize(self._iconSize.width(), self._iconSize.height())  # Tăng kích thước icon

                if i <= index:
                    self._icons[i]._set_text_color(self._selected_color)  # Highlight icon
                    if i == index:
                        self._icons[i].setIconSize(QSize(self._iconSize.width() + 5, self._iconSize.height() + 5))  # Tăng kích thước icon
                        self._icons[i].setFixedSize(self._iconSize.width() + 5, self._iconSize.height() + 5)  # Tăng kích thước icon
                    # self._icons[i].update()
                else:
                    self._icons[i]._set_text_color(self._unselect_color)  # Reset icon color
                    # self._icons[i].setIconSize(self._iconSize)
                    # self._icons[i].setIconSize(QSize(40, 40))



                # self._icons[i].setIconSize(QSize(self._iconSize.width()+2, self._iconSize.height()+2))
                # self._icons[i].setIconSize(QSize(40, 40))

            # Gọi callback onChangeActive nếu có
            if self._onChangeActive:
                self._onChangeActive("event", index + 1)

    def _on_hover_leave(self, index=None):
        """
        Xử lý khi rời chuột khỏi một icon, quay về kích thước và màu ban đầu theo giá trị hiện tại.
        """
        if not self._disabled and not self._readOnly:
            for i in range(self._max):
                if i < self._currentValue:
                    self._icons[i]._set_text_color(self._selected_color)
                else:
                    self._icons[i]._set_text_color(self._unselect_color)

                self._icons[i].setIconSize(self._iconSize)
                self._icons[i].setFixedSize(self._iconSize.width(), self._iconSize.height())  # Tăng kích thước icon


    def _on_icon_clicked(self, index):
        """
        Xử lý khi một icon được nhấp chuột, đặt giá trị rating và tô màu tương ứng.
        """
        if not self._disabled and not self._readOnly:
            self._currentValue = index + 1  # Cập nhật giá trị hiện tại
            self._on_hover_enter(index)  # Tô màu icon
            # Gọi callback onChange nếu có
            if self._onChange:
                self._onChange(self._currentValue)
