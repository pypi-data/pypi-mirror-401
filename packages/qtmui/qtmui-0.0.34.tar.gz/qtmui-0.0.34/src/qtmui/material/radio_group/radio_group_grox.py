# from typing import Optional, Union, Callable, List, Dict, Any
# import uuid
# from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy
# from PySide6.QtCore import Signal, Qt
# from ..radio import Radio
# from ..form_control_label import FormControlLabel
# from qtmui.hooks import State
# from ..widget_base import PyWidgetBase
# from qtmui.material.styles import useTheme
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
# from ..utils.validate_params import _validate_param

# class RadioGroup(QFrame, PyWidgetBase):
#     """
#     A radio group component, styled like Material-UI RadioGroup.

#     The `RadioGroup` component manages a set of `Radio` buttons, allowing only one to be selected at a time.
#     It integrates with the `qtmui` framework, retaining existing parameters, adding new parameters, and
#     aligning with MUI RadioGroup props. Inherits from `FormGroup` props.

#     Parameters
#     ----------
#     value : State or Any, optional
#         Value of the selected radio button. Default is None.
#         Can be a `State` object for dynamic updates.
#     orientation : State or str, optional
#         The orientation of the layout ('vertical', 'horizontal'). Default is 'vertical'.
#         Can be a `State` object for dynamic updates.
#     options : State or List[Dict], optional
#         List of options to generate `FormControlLabel` with `Radio`. Each dict should have `label` and `value`.
#         Default is None.
#         Can be a `State` object for dynamic updates.
#     onChange : State or Callable, optional
#         Callback fired when a radio button is selected. Default is None.
#         Can be a `State` object for dynamic updates.
#         Signature: (event: Any, value: Any) -> None
#     children : State or List[QWidget], optional
#         The content of the component, typically `FormControlLabel` or `Radio`. Default is None.
#         Can be a `State` object for dynamic updates.
#     defaultValue : State or Any, optional
#         The default value when the component is not controlled. Default is None.
#         Can be a `State` object for dynamic updates.
#     name : State or str, optional
#         The name used to reference the value of the control. Default is None.
#         Can be a `State` object for dynamic updates.
#     row : State or bool, optional
#         If True, the layout is horizontal (overrides orientation). Default is False.
#         Can be a `State` object for dynamic updates.
#     classes : State or dict, optional
#         Override or extend the styles applied to the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     sx : State, list, dict, Callable, str, or None, optional
#         System prop for CSS overrides and additional styles. Default is None.
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to the parent `QFrame` class,
#         supporting props of the `FormGroup` component.

#     Signals
#     -------
#     changed : Signal
#         Emitted when the selected value changes.

#     Notes
#     -----
#     - Existing parameters (`value`, `orientation`, `options`, `onChange`, `children`) are retained.
#     - New parameters added to align with MUI: `defaultValue`, `name`, `row`, `classes`, `sx`.
#     - Props of the `FormGroup` component are supported via `**kwargs`.
#     - MUI classes applied: `MuiRadioGroup-root`.
#     - Integrates with `Radio` and `FormControlLabel` for content rendering.

#     Demos:
#     - RadioGroup: https://qtmui.com/material-ui/qtmui-radio-group/

#     API Reference:
#     - RadioGroup API: https://qtmui.com/material-ui/api/radio-group/
#     """

#     changed = Signal(object)

#     VALID_ORIENTATIONS = ['vertical', 'horizontal']

#     def __init__(
#         self,
#         value: Optional[Union[State, Any]] = None,
#         orientation: Union[State, str] = 'vertical',
#         options: Optional[Union[State, List[Dict]]] = None,
#         onChange: Optional[Union[State, Callable]] = None,
#         children: Optional[Union[State, List[QWidget]]] = None,
#         defaultValue: Optional[Union[State, Any]] = None,
#         name: Optional[Union[State, str]] = None,
#         row: Union[State, bool] = False,
#         classes: Optional[Union[State, Dict]] = None,
#         sx: Optional[Union[State, List, Dict, Callable, str]] = None,
#         *args,
#         **kwargs
#     ):
#         super().__init__(*args, **kwargs)
#         self.setObjectName(f"RadioGroup-{str(uuid.uuid4())}")
#         PyWidgetBase._setUpUi(self)

#         self.theme = useTheme()
#         self._widget_references = []
#         self._selected_values = []

#         # Set properties with validation
#         self._set_value(value)
#         self._set_orientation(orientation)
#         self._set_options(options)
#         self._set_onChange(onChange)
#         self._set_children(children)
#         self._set_defaultValue(defaultValue)
#         self._set_name(name)
#         self._set_row(row)
#         self._set_classes(classes)
#         self._set_sx(sx)

#         self._init_ui()
#         self._set_stylesheet()

#         self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
#         self.destroyed.connect(self._on_destroyed)
#         self._connect_signals()

#     # Setter and Getter methods
#     @_validate_param(
#         file_path="qtmui.material.radio_group",
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
#         file_path="qtmui.material.radio_group",
#         param_name="orientation",
#         supported_signatures=Union[State, str],
#         valid_values=VALID_ORIENTATIONS
#     )
#     def _set_orientation(self, value):
#         """Assign value to orientation."""
#         self._orientation = value

#     def _get_orientation(self):
#         """Get the orientation value."""
#         return self._orientation.value if isinstance(self._orientation, State) else self._orientation

#     @_validate_param(
#         file_path="qtmui.material.radio_group",
#         param_name="options",
#         supported_signatures=Union[State, List[Dict], type(None)],
#         validator=lambda x: all(isinstance(opt, dict) and 'label' in opt and 'value' in opt for opt in x) if isinstance(x, list) else True
#     )
#     def _set_options(self, value):
#         """Assign value to options."""
#         self._options = value

#     def _get_options(self):
#         """Get the options value."""
#         return self._options.value if isinstance(self._options, State) else self._options

#     @_validate_param(
#         file_path="qtmui.material.radio_group",
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
#         file_path="qtmui.material.radio_group",
#         param_name="children",
#         supported_signatures=Union[State, List, type(None)]
#     )
#     def _set_children(self, value):
#         """Assign value to children and store references."""
#         self._widget_references.clear()
#         self._children = value
#         children = value.value if isinstance(value, State) else value

#         if isinstance(children, list):
#             for child in children:
#                 if not isinstance(child, QWidget):
#                     raise TypeError(f"Each element in children must be a QWidget, got {type(child)}")
#                 self._widget_references.append(child)
#         elif children is not None:
#             raise TypeError(f"children must be a State, List[QWidget], or None, got {type(children)}")

#     def _get_children(self):
#         """Get the children value."""
#         children = self._children.value if isinstance(self._children, State) else self._children
#         return children if isinstance(children, list) else []

#     @_validate_param(
#         file_path="qtmui.material.radio_group",
#         param_name="defaultValue",
#         supported_signatures=Union[State, Any, type(None)]
#     )
#     def _set_defaultValue(self, value):
#         """Assign value to defaultValue."""
#         self._defaultValue = value

#     def _get_defaultValue(self):
#         """Get the defaultValue value."""
#         return self._defaultValue.value if isinstance(self._defaultValue, State) else self._defaultValue

#     @_validate_param(
#         file_path="qtmui.material.radio_group",
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
#         file_path="qtmui.material.radio_group",
#         param_name="row",
#         supported_signatures=Union[State, bool]
#     )
#     def _set_row(self, value):
#         """Assign value to row."""
#         self._row = value

#     def _get_row(self):
#         """Get the row value."""
#         return self._row.value if isinstance(self._row, State) else self._row

#     @_validate_param(
#         file_path="qtmui.material.radio_group",
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
#         file_path="qtmui.material.radio_group",
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
#         # Clear previous widgets
#         self._widget_references.clear()
#         if hasattr(self, 'layout') and self.layout():
#             while self.layout().count():
#                 item = self.layout().takeAt(0)
#                 if item.widget():
#                     item.widget().setParent(None)

#         # Set layout based on row or orientation
#         is_horizontal = self._get_row() or self._get_orientation() == 'horizontal'
#         self.setLayout(QHBoxLayout() if is_horizontal else QVBoxLayout())
#         self.layout().setContentsMargins(0, 0, 0, 0)
#         self.layout().setSpacing(self.theme.spacing(1))
#         self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

#         # Determine initial value
#         initial_value = self._get_value() if self._get_value() is not None else self._get_defaultValue()

#         # Add options
#         options = self._get_options()
#         if options:
#             for option in options:
#                 radio = Radio(
#                     value=option.get('value'),
#                     checked=option.get('value') == initial_value,
#                     onChange=self._on_radio_change,
#                     name=self._get_name()
#                 )
#                 form_control = FormControlLabel(
#                     label=option.get('label'),
#                     control=radio
#                 )
#                 self.layout().addWidget(form_control)
#                 self._widget_references.append(form_control)

#         # Add children
#         children = self._get_children()
#         for widget in children:
#             if isinstance(widget, Radio):
#                 widget._set_name(self._get_name())
#                 widget._set_checked(widget._get_value() == initial_value)
#                 widget.changed.connect(self._on_radio_change)
#             self.layout().addWidget(widget)
#             self._widget_references.append(widget)

#     def _on_radio_change(self, value, checked):
#         """Handle radio selection change."""
#         if not checked:
#             return
#         for radio in self.findChildren(Radio):
#             radio._set_checked(radio._get_value() == value)
#         self._value = value
#         self.changed.emit(value)
#         if self._get_onChange():
#             self._get_onChange()(None, value)

#     def _set_stylesheet(self, component_styled=None):
#         """Set the stylesheet for the RadioGroup."""
#         self.theme = useTheme()
#         component_styled = component_styled or self.theme.components
#         radio_group_styles = component_styled.get("RadioGroup", {}).get("styles", {})
#         root_styles = radio_group_styles.get("root", {})
#         root_qss = get_qss_style(root_styles)

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

#         # Apply MUI classes
#         mui_classes = ["MuiRadioGroup-root"]

#         stylesheet = f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#                 background: {self.theme.palette.background.default};
#             }}
#             {sx_qss}
#         """
#         self.setStyleSheet(stylesheet)

#     def _connect_signals(self):
#         """Connect valueChanged signals of State parameters to their slots."""
#         if isinstance(self._value, State):
#             self._value.valueChanged.connect(self._on_value_changed)
#         if isinstance(self._orientation, State):
#             self._orientation.valueChanged.connect(self._on_orientation_changed)
#         if isinstance(self._options, State):
#             self._options.valueChanged.connect(self._on_options_changed)
#         if isinstance(self._onChange, State):
#             self._onChange.valueChanged.connect(self._on_onChange_changed)
#         if isinstance(self._children, State):
#             self._children.valueChanged.connect(self._on_children_changed)
#         if isinstance(self._defaultValue, State):
#             self._defaultValue.valueChanged.connect(self._on_defaultValue_changed)
#         if isinstance(self._name, State):
#             self._name.valueChanged.connect(self._on_name_changed)
#         if isinstance(self._row, State):
#             self._row.valueChanged.connect(self._on_row_changed)
#         if isinstance(self._classes, State):
#             self._classes.valueChanged.connect(self._on_classes_changed)
#         if isinstance(self._sx, State):
#             self._sx.valueChanged.connect(self._on_sx_changed)

#     def _on_value_changed(self):
#         """Handle changes to value."""
#         self._set_value(self._value)
#         self._init_ui()

#     def _on_orientation_changed(self):
#         """Handle changes to orientation."""
#         self._set_orientation(self._orientation)
#         self._init_ui()

#     def _on_options_changed(self):
#         """Handle changes to options."""
#         self._set_options(self._options)
#         self._init_ui()

#     def _on_onChange_changed(self):
#         """Handle changes to onChange."""
#         self._set_onChange(self._onChange)

#     def _on_children_changed(self):
#         """Handle changes to children."""
#         self._set_children(self._children)
#         self._init_ui()

#     def _on_defaultValue_changed(self):
#         """Handle changes to defaultValue."""
#         self._set_defaultValue(self._defaultValue)
#         self._init_ui()

#     def _on_name_changed(self):
#         """Handle changes to name."""
#         self._set_name(self._name)
#         self._init_ui()

#     def _on_row_changed(self):
#         """Handle changes to row."""
#         self._set_row(self._row)
#         self._init_ui()

#     def _on_classes_changed(self):
#         """Handle changes to classes."""
#         self._set_classes(self._classes)
#         self._set_stylesheet()

#     def _on_sx_changed(self):
#         """Handle changes to sx."""
#         self._set_sx(self._sx)
#         self._set_stylesheet()

#     def _on_destroyed(self):
#         """Clean up connections when the widget is destroyed."""
#         if hasattr(self, "theme"):
#             self.theme.state.valueChanged.disconnect(self._set_stylesheet)
#         if isinstance(self._value, State):
#             self._value.valueChanged.disconnect(self._on_value_changed)
#         if isinstance(self._orientation, State):
#             self._orientation.valueChanged.disconnect(self._on_orientation_changed)
#         if isinstance(self._options, State):
#             self._options.valueChanged.disconnect(self._on_options_changed)
#         if isinstance(self._onChange, State):
#             self._onChange.valueChanged.disconnect(self._on_onChange_changed)
#         if isinstance(self._children, State):
#             self._children.valueChanged.disconnect(self._on_children_changed)
#         if isinstance(self._defaultValue, State):
#             self._defaultValue.valueChanged.disconnect(self._on_defaultValue_changed)
#         if isinstance(self._name, State):
#             self._name.valueChanged.disconnect(self._on_name_changed)
#         if isinstance(self._row, State):
#             self._row.valueChanged.disconnect(self._on_row_changed)
#         if isinstance(self._classes, State):
#             self._classes.valueChanged.disconnect(self._on_classes_changed)
#         if isinstance(self._sx, State):
#             self._sx.valueChanged.disconnect(self._on_sx_changed)