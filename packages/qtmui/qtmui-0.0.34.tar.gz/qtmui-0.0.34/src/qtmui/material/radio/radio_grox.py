# import asyncio
# from typing import Optional, Union, Callable, Dict, List, Any
# import uuid
# from PySide6.QtGui import QPainter, QPen, QColor
# from PySide6.QtCore import Qt, Signal, QSize, QTimer
# from PySide6.QtWidgets import QWidget, QVBoxLayout
# from qtmui.material.styles.create_theme.theme_reducer import ThemeState
# from qtmui.material.styles.create_theme.create_palette import PaletteColor
# from ..system.color_manipulator import hex_string_to_qcolor
# from ..button.button import Button
# from qtmui.hooks import State
# from qtmui.material.styles import useTheme
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
# from ..utils.validate_params import _validate_param

# class Radio(Button):
#     """
#     A radio button component, styled like Material-UI Radio.

#     The `Radio` component allows users to select one option from a set. It integrates with the `qtmui`
#     framework, retaining existing parameters (except `text` and `hightLight`), adding new parameters,
#     and aligning with MUI Radio props. Inherits from `Button` to support `ButtonBase` props.

#     Parameters
#     ----------
#     id : State or str, optional
#         The id of the input element. Default is None.
#         Can be a `State` object for dynamic updates.
#     checked : State or bool, optional
#         If True, the component is checked. Default is False.
#         Can be a `State` object for dynamic updates.
#     icon : State, QWidget, Callable, or None, optional
#         The icon to display when unchecked. Default is None.
#         Can be a `State` object for dynamic updates or a Callable returning a QWidget.
#     checkedIcon : State, QWidget, Callable, or None, optional
#         The icon to display when checked. Default is None.
#         Can be a `State` object for dynamic updates or a Callable returning a QWidget.
#     color : State or str, optional
#         The color of the component ('default', 'primary', 'secondary', 'error', 'info', 'success', 'warning').
#         Default is 'primary'.
#         Can be a `State` object for dynamic updates.
#     name : State or str, optional
#         Name attribute of the input element. Default is None.
#         Can be a `State` object for dynamic updates.
#     onChange : State or Callable, optional
#         Callback fired when the state changes. Default is None.
#         Can be a `State` object for dynamic updates.
#         Signature: (event: Any, checked: bool) -> None
#     value : State or Any, optional
#         The value of the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     classes : State or dict, optional
#         Override or extend the styles applied to the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     disabled : State or bool, optional
#         If True, the component is disabled. Default is False.
#         Can be a `State` object for dynamic updates.
#     disableRipple : State or bool, optional
#         If True, the ripple effect is disabled. Default is False.
#         Can be a `State` object for dynamic updates.
#     inputProps : State or dict, optional
#         Attributes applied to the input element. Default is None.
#         Can be a `State` object for dynamic updates.
#     inputRef : State or Callable, optional
#         Ref to the input element. Default is None.
#         Can be a `State` object for dynamic updates.
#     required : State or bool, optional
#         If True, the input element is required. Default is False.
#         Can be a `State` object for dynamic updates.
#     size : State or str, optional
#         The size of the component ('small', 'medium'). Default is 'medium'.
#         Can be a `State` object for dynamic updates.
#     slotProps : State or dict, optional
#         Props for slots ({input, root}). Default is {}.
#         Can be a `State` object for dynamic updates.
#     slots : State or dict, optional
#         Components for slots ({input, root}). Default is {}.
#         Can be a `State` object for dynamic updates.
#     sx : State, list, dict, Callable, str, or None, optional
#         System prop for CSS overrides and additional styles. Default is None.
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to the parent `Button` class,
#         supporting props of the `ButtonBase` component (e.g., disableElevation).

#     Signals
#     -------
#     changed : Signal
#         Emitted when the checked state or value changes.

#     Notes
#     -----
#     - Existing parameters `text` and `hightLight` are removed; all other parameters are retained.
#     - New parameters added to align with MUI: `classes`, `disabled`, `disableRipple`, `inputProps`,
#       `inputRef`, `required`, `size`, `slotProps`, `slots`, `sx`.
#     - Props of the `ButtonBase` component are supported via `**kwargs`.
#     - MUI classes applied: `MuiRadio-root`, `Mui-checked`, `Mui-disabled`.
#     - Integrates with `Button` for `ButtonBase` props and supports custom icons via `QWidget`.

#     Demos:
#     - Radio: https://qtmui.com/material-ui/qtmui-radio/

#     API Reference:
#     - Radio API: https://qtmui.com/material-ui/api/radio/
#     """

#     changed = Signal(object, bool)

#     VALID_COLORS = ['default', 'primary', 'secondary', 'error', 'info', 'success', 'warning']
#     VALID_SIZES = ['small', 'medium']

#     def __init__(
#         self,
#         id: Optional[Union[State, str]] = None,
#         checked: Union[State, bool] = False,
#         icon: Optional[Union[State, QWidget, Callable]] = None,
#         checkedIcon: Optional[Union[State, QWidget, Callable]] = None,
#         color: Union[State, str] = 'primary',
#         name: Optional[Union[State, str]] = None,
#         onChange: Optional[Union[State, Callable]] = None,
#         value: Optional[Union[State, Any]] = None,
#         classes: Optional[Union[State, Dict]] = None,
#         disabled: Union[State, bool] = False,
#         disableRipple: Union[State, bool] = False,
#         inputProps: Optional[Union[State, Dict]] = None,
#         inputRef: Optional[Union[State, Callable]] = None,
#         required: Union[State, bool] = False,
#         size: Union[State, str] = 'medium',
#         slotProps: Union[State, Dict] = {},
#         slots: Union[State, Dict] = {},
#         sx: Optional[Union[State, List, Dict, Callable, str]] = None,
#         *args,
#         **kwargs
#     ):
#         super().__init__(variant="text", *args, **kwargs)
#         self.setObjectName(f"Radio-{str(uuid.uuid4())}")

#         self.theme = useTheme()
#         self._widget_references = []
#         self._indicator_color_checked = None

#         # Set properties with validation
#         self._set_id(id)
#         self._set_checked(checked)
#         self._set_icon(icon)
#         self._set_checkedIcon(checkedIcon)
#         self._set_color(color)
#         self._set_name(name)
#         self._set_onChange(onChange)
#         self._set_value(value)
#         self._set_classes(classes)
#         self._set_disabled(disabled)
#         self._set_disableRipple(disableRipple)
#         self._set_inputProps(inputProps)
#         self._set_inputRef(inputRef)
#         self._set_required(required)
#         self._set_size(size)
#         self._set_slotProps(slotProps)
#         self._set_slots(slots)
#         self._set_sx(sx)

#         self._init_ui()
#         self._set_stylesheet()

#         self.useEffect(
        #     self._set_stylesheet,
        #     [theme.state]
        # )
#         self.destroyed.connect(self._on_destroyed)
#         self._connect_signals()

#     # Setter and Getter methods
#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="id",
#         supported_signatures=Union[State, str, type(None)]
#     )
#     def _set_id(self, value):
#         """Assign value to id."""
#         self._id = value
#         if value and not isinstance(value, State):
#             self.setObjectName(value)

#     def _get_id(self):
#         """Get the id value."""
#         return self._id.value if isinstance(self._id, State) else self._id

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="checked",
#         supported_signatures=Union[State, bool]
#     )
#     def _set_checked(self, value):
#         """Assign value to checked."""
#         self._checked = value
#         self._checkedValue = value.value if isinstance(value, State) else value

#     def _get_checked(self):
#         """Get the checked value."""
#         return self._checked.value if isinstance(self._checked, State) else self._checked

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="icon",
#         supported_signatures=Union[State, QWidget, Callable, type(None)]
#     )
#     def _set_icon(self, value):
#         """Assign value to icon."""
#         self._icon = value

#     def _get_icon(self):
#         """Get the icon value."""
#         icon = self._icon
#         if isinstance(icon, State):
#             icon = icon.value
#         if callable(icon):
#             icon = icon()
#         return icon if isinstance(icon, QWidget) else None

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="checkedIcon",
#         supported_signatures=Union[State, QWidget, Callable, type(None)]
#     )
#     def _set_checkedIcon(self, value):
#         """Assign value to checkedIcon."""
#         self._checkedIcon = value

#     def _get_checkedIcon(self):
#         """Get the checkedIcon value."""
#         icon = self._checkedIcon
#         if isinstance(icon, State):
#             icon = icon.value
#         if callable(icon):
#             icon = icon()
#         return icon if isinstance(icon, QWidget) else None

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="color",
#         supported_signatures=Union[State, str],
#         valid_values=VALID_COLORS
#     )
#     def _set_color(self, value):
#         """Assign value to color."""
#         self._color = value

#     def _get_color(self):
#         """Get the color value."""
#         return self._color.value if isinstance(self._color, State) else self._color

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="name",
#         supported_signatures=Union[State, str, type(None)]
#     )
#     def _set_name(self, value):
#         """Assign value to name."""
#         self._name = value

#     def _get_name(self):
#         """Get the name value."""
#         return self._name.value if isinstance(self._name, State) else self._name

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="onChange",
#         supported_signatures=Union[State, Callable, type(None)]
#     )
#     def _set_onChange(self, value):
#         """Assign value to onChange."""
#         self._onChange = value

#     def _get_onChange(self):
#         """Get the onChange value."""
#         return self._onChange.value if isinstance(self._onChange, State) else self._onChange

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="value",
#         supported_signatures=Union[State, Any, type(None)]
#     )
#     def _set_value(self, value):
#         """Assign value to value."""
#         self._value = value

#     def _get_value(self):
#         """Get the value value."""
#         return self._value.value if isinstance(self._value, State) else self._value

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="classes",
#         supported_signatures=Union[State, Dict, type(None)]
#     )
#     def _set_classes(self, value):
#         """Assign value to classes."""
#         self._classes = value

#     def _get_classes(self):
#         """Get the classes value."""
#         return self._classes.value if isinstance(self._classes, State) else self._classes

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="disabled",
#         supported_signatures=Union[State, bool]
#     )
#     def _set_disabled(self, value):
#         """Assign value to disabled."""
#         self._disabled = value
#         self.setEnabled(not (value.value if isinstance(value, State) else value))

#     def _get_disabled(self):
#         """Get the disabled value."""
#         return self._disabled.value if isinstance(self._disabled, State) else self._disabled

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="disableRipple",
#         supported_signatures=Union[State, bool]
#     )
#     def _set_disableRipple(self, value):
#         """Assign value to disableRipple."""
#         self._disableRipple = value

#     def _get_disableRipple(self):
#         """Get the disableRipple value."""
#         return self._disableRipple.value if isinstance(self._disableRipple, State) else self._disableRipple

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="inputProps",
#         supported_signatures=Union[State, Dict, type(None)]
#     )
#     def _set_inputProps(self, value):
#         """Assign value to inputProps."""
#         self._inputProps = value

#     def _get_inputProps(self):
#         """Get the inputProps value."""
#         return self._inputProps.value if isinstance(self._inputProps, State) else self._inputProps

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="inputRef",
#         supported_signatures=Union[State, Callable, type(None)]
#     )
#     def _set_inputRef(self, value):
#         """Assign value to inputRef."""
#         self._inputRef = value

#     def _get_inputRef(self):
#         """Get the inputRef value."""
#         return self._inputRef.value if isinstance(self._inputRef, State) else self._inputRef

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="required",
#         supported_signatures=Union[State, bool]
#     )
#     def _set_required(self, value):
#         """Assign value to required."""
#         self._required = value

#     def _get_required(self):
#         """Get the required value."""
#         return self._required.value if isinstance(self._required, State) else self._required

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="size",
#         supported_signatures=Union[State, str],
#         valid_values=VALID_SIZES
#     )
#     def _set_size(self, value):
#         """Assign value to size."""
#         self._size = value

#     def _get_size(self):
#         """Get the size value."""
#         return self._size.value if isinstance(self._size, State) else self._size

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="slotProps",
#         supported_signatures=Union[State, Dict]
#     )
#     def _set_slotProps(self, value):
#         """Assign value to slotProps."""
#         self._slotProps = value

#     def _get_slotProps(self):
#         """Get the slotProps value."""
#         return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="slots",
#         supported_signatures=Union[State, Dict]
#     )
#     def _set_slots(self, value):
#         """Assign value to slots."""
#         self._slots = value

#     def _get_slots(self):
#         """Get the slots value."""
#         return self._slots.value if isinstance(self._slots, State) else self._slots

#     @_validate_param(
#         file_path="qtmui.material.radio",
#         param_name="sx",
#         supported_signatures=Union[State, List, Dict, Callable, str, type(None)]
#     )
#     def _set_sx(self, value):
#         """Assign value to sx."""
#         self._sx = value

#     def _get_sx(self):
#         """Get the sx value."""
#         return self._sx.value if isinstance(self._sx, State) else self._sx

#     def _init_ui(self):
#         """Initialize the UI based on props."""
#         self.setMouseTracking(True)
#         self.setLayout(QVBoxLayout())
#         self.layout().setContentsMargins(0, 0, 0, 0)
#         self.layout().setSpacing(0)

#         # Clear previous widgets
#         self._widget_references.clear()
#         while self.layout().count():
#             item = self.layout().takeAt(0)
#             if item.widget():
#                 item.widget().setParent(None)

#         # Set size
#         size = self._get_size()
#         self.setFixedSize(QSize(30, 30) if size == "small" else QSize(36, 36))

#         # Add icon
#         icon = self._get_checkedIcon() if self._get_checked() else self._get_icon()
#         if icon:
#             self.layout().addWidget(icon)
#             self._widget_references.append(icon)
#         else:
#             # Default radio rendering will be handled in paintEvent
#             pass

#         # Connect click event
#         self.clicked.connect(self._on_click)

#         # Apply disabled state
#         self.setEnabled(not self._get_disabled())

#         # Apply inputRef
#         input_ref = self._get_inputRef()
#         if input_ref:
#             input_ref(self)

#     def _on_click(self):
#         """Handle click event."""
#         if self._get_disabled():
#             return
#         self._checkedValue = not self._checkedValue
#         self._set_checked(self._checkedValue)
#         self.changed.emit(self._get_value(), self._checkedValue)
#         if self._get_onChange():
#             self._get_onChange()(None, self._checkedValue)
#         self._init_ui()  # Update icon
#         self.update()

#     def _set_stylesheet(self, component_styled=None):
#         """Set the stylesheet for the Radio."""
#         super()._set_stylesheet(component_styled)
#         self.theme = useTheme()
#         component_styled = component_styled or self.theme.components
#         radio_styles = component_styled.get("Radio", {}).get("styles", {})
#         root_styles = radio_styles.get("root", {})
#         root_qss = get_qss_style(root_styles)

#         # Determine color
#         color = self._get_color()
#         palette_color = self.theme.palette.get(color, self.theme.palette.primary)
#         self._indicator_color_checked = hex_string_to_qcolor(palette_color.main)

#         # Handle sx
#         sx = self._get_sx()
#         sx_qss = ""
#         if sx:
#             if isinstance(sx, (list, dict)):
#                 sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
#             elif isinstance(sx, Callable):
#                 sx_result = sx()
#                 if isinstance(sx_result, (list, dict)):
#                     sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
#                 elif isinstance(sx_result, str):
#                     sx_qss = sx_result
#             elif isinstance(sx, str) and sx != "":
#                 sx_qss = sx

#         # Handle classes
#         classes = self._get_classes()
#         classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

#         # Handle slotProps.root
#         root_props = self._get_slotProps().get('root', {})
#         root_props_qss = get_qss_style(root_props.get('sx', {}), class_name=f"#{self.objectName()}")

#         # Apply MUI classes
#         mui_classes = ["MuiRadio-root"]
#         if self._get_checked():
#             mui_classes.append("Mui-checked")
#         if self._get_disabled():
#             mui_classes.append("Mui-disabled")

#         stylesheet = f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#                 {root_props_qss}
#                 background: transparent;
#                 border-radius: {"15px" if self._get_size() == "small" else "18px"};
#             }}
#             {sx_qss}
#         """
#         self.setStyleSheet(stylesheet)

#     def paintEvent(self, event):
#         """Custom paint event for default radio rendering."""
#         super().paintEvent(event)
#         if self._get_icon() or self._get_checkedIcon():
#             return  # Skip default rendering if custom icons are provided

#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         size = self._get_size()
#         padding = 6 if size == "small" else 8
#         border = 2 if self._get_checked() else 1

#         rect = self.rect().adjusted(padding, padding, -padding, -padding)
#         height = rect.height()
#         center_point = rect.x()
#         circle_diameter = height

#         if self._get_checked():
#             painter.setBrush(Qt.NoBrush)
#             painter.setPen(QPen(self._indicator_color_checked, border))
#             painter.drawEllipse(center_point - 1, center_point, circle_diameter, circle_diameter)

#             inner_padding = padding + 4
#             inner_rect = self.rect().adjusted(inner_padding, inner_padding, -inner_padding, -inner_padding)
#             inner_height = inner_rect.height()
#             inner_center = inner_rect.x()
#             inner_diameter = inner_height
#             painter.setPen(Qt.NoPen)
#             painter.setBrush(self._indicator_color_checked)
#             painter.drawEllipse(inner_center - 1, inner_center, inner_diameter, inner_diameter)
#         else:
#             painter.setBrush(Qt.NoBrush)
#             painter.setPen(QPen(hex_string_to_qcolor(self.theme.palette.text.secondary), border))
#             painter.drawEllipse(center_point - 1, center_point, circle_diameter, circle_diameter)

#         painter.end()

#     def _connect_signals(self):
#         """Connect valueChanged signals of State parameters to their slots."""
#         if isinstance(self._id, State):
#             self._id.valueChanged.connect(self._on_id_changed)
#         if isinstance(self._checked, State):
#             self._checked.valueChanged.connect(self._on_checked_changed)
#         if isinstance(self._icon, State):
#             self._icon.valueChanged.connect(self._on_icon_changed)
#         if isinstance(self._checkedIcon, State):
#             self._checkedIcon.valueChanged.connect(self._on_checkedIcon_changed)
#         if isinstance(self._color, State):
#             self._color.valueChanged.connect(self._on_color_changed)
#         if isinstance(self._name, State):
#             self._name.valueChanged.connect(self._on_name_changed)
#         if isinstance(self._onChange, State):
#             self._onChange.valueChanged.connect(self._on_onChange_changed)
#         if isinstance(self._value, State):
#             self._value.valueChanged.connect(self._on_value_changed)
#         if isinstance(self._classes, State):
#             self._classes.valueChanged.connect(self._on_classes_changed)
#         if isinstance(self._disabled, State):
#             self._disabled.valueChanged.connect(self._on_disabled_changed)
#         if isinstance(self._disableRipple, State):
#             self._disableRipple.valueChanged.connect(self._on_disableRipple_changed)
#         if isinstance(self._inputProps, State):
#             self._inputProps.valueChanged.connect(self._on_inputProps_changed)
#         if isinstance(self._inputRef, State):
#             self._inputRef.valueChanged.connect(self._on_inputRef_changed)
#         if isinstance(self._required, State):
#             self._required.valueChanged.connect(self._on_required_changed)
#         if isinstance(self._size, State):
#             self._size.valueChanged.connect(self._on_size_changed)
#         if isinstance(self._slotProps, State):
#             self._slotProps.valueChanged.connect(self._on_slotProps_changed)
#         if isinstance(self._slots, State):
#             self._slots.valueChanged.connect(self._on_slots_changed)
#         if isinstance(self._sx, State):
#             self._sx.valueChanged.connect(self._on_sx_changed)

#     def _on_id_changed(self):
#         """Handle changes to id."""
#         self._set_id(self._id)

#     def _on_checked_changed(self):
#         """Handle changes to checked."""
#         self._set_checked(self._checked)
#         self._init_ui()
#         self.update()

#     def _on_icon_changed(self):
#         """Handle changes to icon."""
#         self._set_icon(self._icon)
#         self._init_ui()

#     def _on_checkedIcon_changed(self):
#         """Handle changes to checkedIcon."""
#         self._set_checkedIcon(self._checkedIcon)
#         self._init_ui()

#     def _on_color_changed(self):
#         """Handle changes to color."""
#         self._set_color(self._color)
#         self._set_stylesheet()

#     def _on_name_changed(self):
#         """Handle changes to name."""
#         self._set_name(self._name)

#     def _on_onChange_changed(self):
#         """Handle changes to onChange."""
#         self._set_onChange(self._onChange)

#     def _on_value_changed(self):
#         """Handle changes to value."""
#         self._set_value(self._value)

#     def _on_classes_changed(self):
#         """Handle changes to classes."""
#         self._set_classes(self._classes)
#         self._set_stylesheet()

#     def _on_disabled_changed(self):
#         """Handle changes to disabled."""
#         self._set_disabled(self._disabled)
#         self._set_stylesheet()

#     def _on_disableRipple_changed(self):
#         """Handle changes to disableRipple."""
#         self._set_disableRipple(self._disableRipple)

#     def _on_inputProps_changed(self):
#         """Handle changes to inputProps."""
#         self._set_inputProps(self._inputProps)

#     def _on_inputRef_changed(self):
#         """Handle changes to inputRef."""
#         self._set_inputRef(self._inputRef)

#     def _on_required_changed(self):
#         """Handle changes to required."""
#         self._set_required(self._required)

#     def _on_size_changed(self):
#         """Handle changes to size."""
#         self._set_size(self._size)
#         self._init_ui()

#     def _on_slotProps_changed(self):
#         """Handle changes to slotProps."""
#         self._set_slotProps(self._slotProps)
#         self._set_stylesheet()

#     def _on_slots_changed(self):
#         """Handle changes to slots."""
#         self._set_slots(self._slots)
#         self._init_ui()

#     def _on_sx_changed(self):
#         """Handle changes to sx."""
#         self._set_sx(self._sx)
#         self._set_stylesheet()

#     def _on_destroyed(self):
#         """Clean up connections when the widget is destroyed."""
#         if hasattr(self, "theme"):
#             self.theme.state.valueChanged.disconnect(self._set_stylesheet)
#         if isinstance(self._id, State):
#             self._id.valueChanged.disconnect(self._on_id_changed)
#         if isinstance(self._checked, State):
#             self._checked.valueChanged.disconnect(self._on_checked_changed)
#         if isinstance(self._icon, State):
#             self._icon.valueChanged.disconnect(self._on_icon_changed)
#         if isinstance(self._checkedIcon, State):
#             self._checkedIcon.valueChanged.disconnect(self._on_checkedIcon_changed)
#         if isinstance(self._color, State):
#             self._color.valueChanged.disconnect(self._on_color_changed)
#         if isinstance(self._name, State):
#             self._name.valueChanged.disconnect(self._on_name_changed)
#         if isinstance(self._onChange, State):
#             self._onChange.valueChanged.disconnect(self._on_onChange_changed)
#         if isinstance(self._value, State):
#             self._value.valueChanged.disconnect(self._on_value_changed)
#         if isinstance(self._classes, State):
#             self._classes.valueChanged.disconnect(self._on_classes_changed)
#         if isinstance(self._disabled, State):
#             self._disabled.valueChanged.disconnect(self._on_disabled_changed)
#         if isinstance(self._disableRipple, State):
#             self._disableRipple.valueChanged.disconnect(self._on_disableRipple_changed)
#         if isinstance(self._inputProps, State):
#             self._inputProps.valueChanged.disconnect(self._on_inputProps_changed)
#         if isinstance(self._inputRef, State):
#             self._inputRef.valueChanged.disconnect(self._on_inputRef_changed)
#         if isinstance(self._required, State):
#             self._required.valueChanged.disconnect(self._on_required_changed)
#         if isinstance(self._size, State):
#             self._size.valueChanged.disconnect(self._on_size_changed)
#         if isinstance(self._slotProps, State):
#             self._slotProps.valueChanged.disconnect(self._on_slotProps_changed)
#         if isinstance(self._slots, State):
#             self._slots.valueChanged.disconnect(self._on_slots_changed)
#         if isinstance(self._sx, State):
#             self._sx.valueChanged.disconnect(self._on_sx_changed)