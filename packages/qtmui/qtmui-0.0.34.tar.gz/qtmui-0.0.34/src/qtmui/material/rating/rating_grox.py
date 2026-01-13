from typing import Optional, Union, Callable, Dict, List, Any
import uuid
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor
from ..system.color_manipulator import lighten, rgbToHex
from ..py_tool_button import PyToolButton
from ..py_iconify.py_iconify import PyIconify
from ..widget_base import PyWidgetBase
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..._____assets import ASSETS
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
        icon: Optional[Union[State, QWidget, Callable]] = None,
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
        self._set_stylesheet()

        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._connect_signals()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.rating", param_name="max", supported_signatures=Union[State, int], validator=lambda x: x > 0)
    def _set_max(self, value):
        """Assign value to max."""
        self._max = value

    def _get_max(self):
        """Get the max value."""
        return self._max.value if isinstance(self._max, State) else self._max

    @_validate_param(file_path="qtmui.material.rating", param_name="value", supported_signatures=Union[State, float, type(None)])
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

    @_validate_param(file_path="qtmui.material.rating", param_name="icon", supported_signatures=Union[State, QWidget, Callable, type(None)])
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

    @_validate_param(file_path="qtmui.material.rating", param_name="precision", supported_signatures=Union[State, float], validator=lambda x: x > 0)
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

    def _init_ui(self):
        """Initialize the UI based on props."""
        self.theme = useTheme()
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Clear previous widgets
        self._widget_references.clear()
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Determine initial value
        initial_value = self._get_value() if self._get_value() is not None else self._get_defaultValue()
        self._currentValue = initial_value

        # Get icon sizes from theme
        icon_styles = self.theme.components.get("Rating", {}).get("styles", {}).get("root", {}).get("props", {})
        size_key = f"size{self._get_size().capitalize()}"
        icon_width = icon_styles.get(size_key, {}).get("svgIcon", {}).get("width", 24)
        icon_height = icon_styles.get(size_key, {}).get("svgIcon", {}).get("height", 24)
        self._iconSize = QSize(icon_width, icon_height)

        # Colors
        self._selected_color = self.theme.palette.primary.main
        self._unselected_color = self.theme.palette.text.secondary

        # Create rating buttons
        self._icons = []
        max_rating = self._get_max()
        for i in range(max_rating):
            icon_widget = self._get_icon() or PyIconify(key=ASSETS.ICONS.STAR, color=self._unselected_color, size=self._iconSize)
            empty_icon_widget = self._get_emptyIcon() or PyIconify(key=ASSETS.ICONS.STAR_OUTLINE, color=self._unselected_color, size=self._iconSize)
            container = self._get_IconContainerComponent() or PyToolButton
            rating_button = container(
                icon=icon_widget if i < (self._currentValue or 0) else empty_icon_widget,
                size=self._iconSize,
                tooltip=self._get_label_text(i + 1)
            )
            rating_button.setCursor(QCursor(Qt.PointingHandCursor) if not (self._get_disabled() or self._get_readOnly()) else QCursor(Qt.ArrowCursor))
            rating_button.setIconSize(self._iconSize)

            # Set initial color
            if i < (self._currentValue or 0):
                rating_button._set_text_color(self._selected_color)
            else:
                rating_button._set_text_color(self._unselected_color)

            # Connect events
            rating_button.enterEvent = lambda event, idx=i: self._on_hover_enter(idx)
            rating_button.leaveEvent = lambda event, idx=i: self._on_hover_leave(idx)
            rating_button.clicked.connect(lambda checked, idx=i: self._on_icon_clicked(idx))

            self._layout.addWidget(rating_button)
            self._icons.append(rating_button)
            self._widget_references.append(rating_button)

        self.setFixedWidth(self.sizeHint().width() + 10)
        self.setMinimumHeight(self.sizeHint().height() + 5)

    def _get_label_text(self, value):
        """Get the label text for a given value."""
        get_label_text = self._get_getLabelText()
        if get_label_text:
            return get_label_text(value)
        return f"{value or '0'} Star{'s' if value != 1 else ''}" if value else self._get_emptyLabelText() or 'Empty'

    def _on_hover_enter(self, index):
        """Handle hover enter event."""
        if self._get_disabled() or self._get_readOnly():
            return
        highlight_only = self._get_highlightSelectedOnly()
        for i in range(self._get_max()):
            if highlight_only and i != index:
                self._icons[i]._set_text_color(self._unselected_color)
                self._icons[i].setIconSize(self._iconSize)
                self._icons[i].setFixedSize(self._iconSize.width(), self._iconSize.height())
            elif i <= index:
                self._icons[i]._set_text_color(self._selected_color)
                self._icons[i].setIconSize(QSize(self._iconSize.width() + 5, self._iconSize.height() + 5))
                self._icons[i].setFixedSize(self._iconSize.width() + 5, self._iconSize.height() + 5)
            else:
                self._icons[i]._set_text_color(self._unselected_color)
                self._icons[i].setIconSize(self._iconSize)
                self._icons[i].setFixedSize(self._iconSize.width(), self._iconSize.height())
        if self._get_onChangeActive():
            self._get_onChangeActive()(None, index + 1)
            self.activeChanged.emit(None, index + 1)

    def _on_hover_leave(self, index):
        """Handle hover leave event."""
        if self._get_disabled() or self._get_readOnly():
            return
        for i in range(self._get_max()):
            if i < (self._currentValue or 0):
                self._icons[i]._set_text_color(self._selected_color)
            else:
                self._icons[i]._set_text_color(self._unselected_color)
            self._icons[i].setIconSize(self._iconSize)
            self._icons[i].setFixedSize(self._iconSize.width(), self._iconSize.height())

    def _on_icon_clicked(self, index):
        """Handle icon click event."""
        if self._get_disabled() or self._get_readOnly():
            return
        new_value = index + 1
        precision = self._get_precision()
        new_value = round(new_value / precision) * precision
        self._currentValue = new_value
        self._set_value(new_value)
        self._on_hover_enter(index)
        self.changed.emit(None, new_value)
        if self._get_onChange():
            self._get_onChange()(None, new_value)

    def _set_stylesheet(self, component_styled=None):
        """Set the stylesheet for the Rating."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        rating_styles = component_styled.get("Rating", {}).get("styles", {})
        root_styles = rating_styles.get("root", {})
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

        # Handle slotProps.root
        root_props = self._get_slotProps().get('root', {})
        root_props_qss = get_qss_style(root_props.get('sx', {}), class_name=f"#{self.objectName()}")

        # Apply MUI classes
        mui_classes = ["MuiRating-root"]
        if self._get_disabled():
            mui_classes.append("Mui-disabled")

        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                {classes_qss}
                {root_props_qss}
                background: transparent;
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._max, State):
            self._max.valueChanged.connect(self._on_max_changed)
        if isinstance(self._value, State):
            self._value.valueChanged.connect(self._on_value_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.connect(self._on_disabled_changed)
        if isinstance(self._icon, State):
            self._icon.valueChanged.connect(self._on_icon_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.connect(self._on_color_changed)
        if isinstance(self._name, State):
            self._name.valueChanged.connect(self._on_name_changed)
        if isinstance(self._readOnly, State):
            self._readOnly.valueChanged.connect(self._on_readOnly_changed)
        if isinstance(self._precision, State):
            self._precision.valueChanged.connect(self._on_precision_changed)
        if isinstance(self._onChange, State):
            self._onChange.valueChanged.connect(self._on_onChange_changed)
        if isinstance(self._onChangeActive, State):
            self._onChangeActive.valueChanged.connect(self._on_onChangeActive_changed)
        if isinstance(self._size, State):
            self._size.valueChanged.connect(self._on_size_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.connect(self._on_component_changed)
        if isinstance(self._defaultValue, State):
            self._defaultValue.valueChanged.connect(self._on_defaultValue_changed)
        if isinstance(self._emptyIcon, State):
            self._emptyIcon.valueChanged.connect(self._on_emptyIcon_changed)
        if isinstance(self._emptyLabelText, State):
            self._emptyLabelText.valueChanged.connect(self._on_emptyLabelText_changed)
        if isinstance(self._getLabelText, State):
            self._getLabelText.valueChanged.connect(self._on_getLabelText_changed)
        if isinstance(self._highlightSelectedOnly, State):
            self._highlightSelectedOnly.valueChanged.connect(self._on_highlightSelectedOnly_changed)
        if isinstance(self._IconContainerComponent, State):
            self._IconContainerComponent.valueChanged.connect(self._on_IconContainerComponent_changed)
        if isinstance(self._slotProps, State):
            self._slotProps.valueChanged.connect(self._on_slotProps_changed)
        if isinstance(self._slots, State):
            self._slots.valueChanged.connect(self._on_slots_changed)

    def _on_max_changed(self):
        """Handle changes to max."""
        self._set_max(self._max)
        self._init_ui()

    def _on_value_changed(self):
        """Handle changes to value."""
        self._set_value(self._value)
        self._init_ui()

    def _on_disabled_changed(self):
        """Handle changes to disabled."""
        self._set_disabled(self._disabled)
        self._set_stylesheet()

    def _on_icon_changed(self):
        """Handle changes to icon."""
        self._set_icon(self._icon)
        self._init_ui()

    def _on_color_changed(self):
        """Handle changes to color."""
        self._set_color(self._color)
        self._set_stylesheet()

    def _on_name_changed(self):
        """Handle changes to name."""
        self._set_name(self._name)

    def _on_readOnly_changed(self):
        """Handle changes to readOnly."""
        self._set_readOnly(self._readOnly)
        self._init_ui()

    def _on_precision_changed(self):
        """Handle changes to precision."""
        self._set_precision(self._precision)
        self._init_ui()

    def _on_onChange_changed(self):
        """Handle changes to onChange."""
        self._set_onChange(self._onChange)

    def _on_onChangeActive_changed(self):
        """Handle changes to onChangeActive."""
        self._set_onChangeActive(self._onChangeActive)

    def _on_size_changed(self):
        """Handle changes to size."""
        self._set_size(self._size)
        self._init_ui()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_component_changed(self):
        """Handle changes to component."""
        self._set_component(self._component)
        self._init_ui()

    def _on_defaultValue_changed(self):
        """Handle changes to defaultValue."""
        self._set_defaultValue(self._defaultValue)
        self._init_ui()

    def _on_emptyIcon_changed(self):
        """Handle changes to emptyIcon."""
        self._set_emptyIcon(self._emptyIcon)
        self._init_ui()

    def _on_emptyLabelText_changed(self):
        """Handle changes to emptyLabelText."""
        self._set_emptyLabelText(self._emptyLabelText)
        self._init_ui()

    def _on_getLabelText_changed(self):
        """Handle changes to getLabelText."""
        self._set_getLabelText(self._getLabelText)
        self._init_ui()

    def _on_highlightSelectedOnly_changed(self):
        """Handle changes to highlightSelectedOnly."""
        self._set_highlightSelectedOnly(self._highlightSelectedOnly)
        self._init_ui()

    def _on_IconContainerComponent_changed(self):
        """Handle changes to IconContainerComponent."""
        self._set_IconContainerComponent(self._IconContainerComponent)
        self._init_ui()

    def _on_slotProps_changed(self):
        """Handle changes to slotProps."""
        self._set_slotProps(self._slotProps)
        self._set_stylesheet()

    def _on_slots_changed(self):
        """Handle changes to slots."""
        self._set_slots(self._slots)
        self._init_ui()

    def _on_destroyed(self):
        """Clean up connections when the widget is destroyed."""
        if hasattr(self, "theme"):
            self.theme.state.valueChanged.disconnect(self._set_stylesheet)
        if isinstance(self._max, State):
            self._max.valueChanged.disconnect(self._on_max_changed)
        if isinstance(self._value, State):
            self._value.valueChanged.disconnect(self._on_value_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.disconnect(self._on_disabled_changed)
        if isinstance(self._icon, State):
            self._icon.valueChanged.disconnect(self._on_icon_changed)
        if isinstance(self._color, State):
            self._color.valueChanged.disconnect(self._on_color_changed)
        if isinstance(self._name, State):
            self._name.valueChanged.disconnect(self._on_name_changed)
        if isinstance(self._readOnly, State):
            self._readOnly.valueChanged.disconnect(self._on_readOnly_changed)
        if isinstance(self._precision, State):
            self._precision.valueChanged.disconnect(self._on_precision_changed)
        if isinstance(self._onChange, State):
            self._onChange.valueChanged.disconnect(self._on_onChange_changed)
        if isinstance(self._onChangeActive, State):
            self._onChangeActive.valueChanged.disconnect(self._on_onChangeActive_changed)
        if isinstance(self._size, State):
            self._size.valueChanged.disconnect(self._on_size_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.disconnect(self._on_sx_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.disconnect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.disconnect(self._on_component_changed)
        if isinstance(self._defaultValue, State):
            self._defaultValue.valueChanged.disconnect(self._on_defaultValue_changed)
        if isinstance(self._emptyIcon, State):
            self._emptyIcon.valueChanged.disconnect(self._on_emptyIcon_changed)
        if isinstance(self._emptyLabelText, State):
            self._emptyLabelText.valueChanged.disconnect(self._on_emptyLabelText_changed)
        if isinstance(self._getLabelText, State):
            self._getLabelText.valueChanged.disconnect(self._on_getLabelText_changed)
        if isinstance(self._highlightSelectedOnly, State):
            self._highlightSelectedOnly.valueChanged.disconnect(self._on_highlightSelectedOnly_changed)
        if isinstance(self._IconContainerComponent, State):
            self._IconContainerComponent.valueChanged.disconnect(self._on_IconContainerComponent_changed)
        if isinstance(self._slotProps, State):
            self._slotProps.valueChanged.disconnect(self._on_slotProps_changed)
        if isinstance(self._slots, State):
            self._slots.valueChanged.disconnect(self._on_slots_changed)