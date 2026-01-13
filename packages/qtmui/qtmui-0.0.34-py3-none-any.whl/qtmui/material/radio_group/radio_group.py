import asyncio
from typing import Optional, Union, Callable, List, Dict, Any
import uuid
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QWidget, QApplication
from PySide6.QtCore import Signal, Qt, QTimer
from ..radio import Radio
from ..form_control_label import FormControlLabel
from qtmui.hooks import State, useEffect
from ..widget_base import PyWidgetBase
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class RadioGroup(QFrame, PyWidgetBase):
    """
    A radio group component, styled like Material-UI RadioGroup.

    The `RadioGroup` component manages a set of `Radio` buttons, allowing only one to be selected at a time.
    It integrates with the `qtmui` framework, retaining existing parameters, adding new parameters, and
    aligning with MUI RadioGroup props. Inherits from `FormGroup` props.

    Parameters
    ----------
    value : State or Any, optional
        Value of the selected radio button. Default is None.
        Can be a `State` object for dynamic updates.
    orientation : State or str, optional
        The orientation of the layout ('vertical', 'horizontal'). Default is 'vertical'.
        Can be a `State` object for dynamic updates.
    options : State or List[Dict], optional
        List of options to generate `FormControlLabel` with `Radio`. Each dict should have `label` and `value`.
        Default is None.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when a radio button is selected. Default is None.
        Can be a `State` object for dynamic updates.
        Signature: (event: Any, value: Any) -> None
    children : State or List[QWidget], optional
        The content of the component, typically `FormControlLabel` or `Radio`. Default is None.
        Can be a `State` object for dynamic updates.
    defaultValue : State or Any, optional
        The default value when the component is not controlled. Default is None.
        Can be a `State` object for dynamic updates.
    name : State or str, optional
        The name used to reference the value of the control. Default is None.
        Can be a `State` object for dynamic updates.
    row : State or bool, optional
        If True, the layout is horizontal (overrides orientation). Default is False.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the `FormGroup` component.

    Signals
    -------
    changed : Signal
        Emitted when the selected value changes.

    Notes
    -----
    - Existing parameters (`value`, `orientation`, `options`, `onChange`, `children`) are retained.
    - New parameters added to align with MUI: `defaultValue`, `name`, `row`, `classes`, `sx`.
    - Props of the `FormGroup` component are supported via `**kwargs`.
    - MUI classes applied: `MuiRadioGroup-root`.
    - Integrates with `Radio` and `FormControlLabel` for content rendering.

    Demos:
    - RadioGroup: https://qtmui.com/material-ui/qtmui-radio-group/

    API Reference:
    - RadioGroup API: https://qtmui.com/material-ui/api/radio-group/
    """

    valueChanged = Signal(object)

    VALID_ORIENTATIONS = ['vertical', 'horizontal']

    def __init__(
        self,
        value: Optional[Union[State, Any]] = None,
        orientation: Union[State, str] = 'vertical',
        options: Optional[Union[State, List[Dict]]] = None,
        onChange: Optional[Union[State, Callable]] = None,
        children: Optional[Union[State, List[QWidget]]] = None,
        defaultValue: Optional[Union[State, Any]] = None,
        name: Optional[Union[State, str]] = None,
        row: Union[State, bool] = False,
        classes: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName(f"RadioGroup-{str(uuid.uuid4())}")
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()
        self._widget_references = []
        self._selected_values = []

        # Set properties with validation
        self._set_value(value)
        self._set_orientation(orientation)
        self._set_options(options)
        self._set_onChange(onChange)
        self._set_children(children)
        self._set_defaultValue(defaultValue)
        self._set_name(name)
        self._set_row(row)
        self._set_classes(classes)
        self._set_sx(sx)

        self._init_ui()

    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.radio_group", param_name="value", supported_signatures=Union[State, Any, type(None)])
    def _set_value(self, value):
        """Assign value to value."""
        self._value = value

    def _get_value(self):
        """Get the value value."""
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.radio_group", param_name="orientation", supported_signatures=Union[State, str], valid_values=VALID_ORIENTATIONS)
    def _set_orientation(self, value):
        """Assign value to orientation."""
        self._orientation = value

    def _get_orientation(self):
        """Get the orientation value."""
        return self._orientation.value if isinstance(self._orientation, State) else self._orientation

    # @_validate_param(file_path="qtmui.material.radio_group", param_name="options", supported_signatures=Union[State, List[Dict], type(None)], validator=lambda x: all(isinstance(opt, dict) and 'label' in opt and 'value' in opt for opt in x) if isinstance(x, list) else True)
    def _set_options(self, value):
        """Assign value to options."""
        self._options = value

    def _get_options(self):
        """Get the options value."""
        return self._options.value if isinstance(self._options, State) else self._options

    @_validate_param(file_path="qtmui.material.radio_group", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        """Assign value to onChange."""
        self._onChange = value

    def _get_onChange(self):
        """Get the onChange value."""
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.radio_group", param_name="children", supported_signatures=Union[State, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        children = self._children.value if isinstance(self._children, State) else self._children
        return children if isinstance(children, list) else []

    # @_validate_param(file_path="qtmui.material.radio_group", param_name="defaultValue", supported_signatures=Union[State, Any, type(None)])
    def _set_defaultValue(self, value):
        """Assign value to defaultValue."""
        self._defaultValue = value

    def _get_defaultValue(self):
        """Get the defaultValue value."""
        return self._defaultValue.value if isinstance(self._defaultValue, State) else self._defaultValue

    @_validate_param(file_path="qtmui.material.radio_group", param_name="name", supported_signatures=Union[State, str, type(None)])
    def _set_name(self, value):
        """Assign value to name."""
        self._name = value

    def _get_name(self):
        """Get the name value."""
        return self._name.value if isinstance(self._name, State) else self._name

    @_validate_param(file_path="qtmui.material.radio_group", param_name="row", supported_signatures=Union[State, bool])
    def _set_row(self, value):
        """Assign value to row."""
        self._row = value

    def _get_row(self):
        """Get the row value."""
        return self._row.value if isinstance(self._row, State) else self._row

    @_validate_param(file_path="qtmui.material.radio_group", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.radio_group", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    
    def _init_ui(self):
        self.setEnabled(False)
        if self._orientation == "vertical":
            self.setLayout(QVBoxLayout())
            self.layout().setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        else:
            self.setLayout(QHBoxLayout())
            self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        if self._options:
            for option in self._options:
                self.layout().addWidget(
                        FormControlLabel(
                            label=option.get("label"), 
                            value=option.get("value"),
                            control=Radio(
                                checked=option.get("value") == self._get_value(), 
                                # onChange=lambda checked, value=option.get("value"): self._on_change(value),
                            )
                        ),
                )
        elif self._children:
            if not isinstance(self._children, list):
                raise TypeError(f"Argument 'children' has incorrect type (expected list, got {type(self._children)})")
            for widget in self._children:
                self.layout().addWidget(widget)


            # all_wgs = QApplication.dumpObjectTree(self)
            # print(all_wgs)

        self._set_stylesheet()
        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self.destroyed.connect(self._on_destroyed)
        self._set_stylesheet()
        
        # Phải thực hiện điều này để quá trình async add widget thì có thể FormControlLabel chưa có trong danh sách 
        # children dẫn tới hàm _on_change của Radio không được kết nối
        QTimer.singleShot(0, self._scheduleConnectRadioState)

    def _onDestroy(self, obj=None):
        # Cancel task nếu đang chạy
        if hasattr(self, "_connectRadioStateTask") and self._connectRadioStateTask and not self._connectRadioStateTask.done():
            self._connectRadioStateTask.cancel()

    def _scheduleConnectRadioState(self):
        self._connectRadioStateTask = asyncio.ensure_future(self._lazy_connectRadioState())

    async def _lazy_connectRadioState(self):
        while not self.findChildren(Radio):
            await asyncio.sleep(1)
        self._connectRadioState()

    def _connectRadioState(self):
        for widget in self.findChildren(FormControlLabel):
            if widget._control:
                widget._control._onChange = lambda checked, value=widget._value: self._on_change(value)
                if widget._value == self._get_value():
                    widget._control.setChecked(True)
                    widget._control._updateIcon()
        self.setEnabled(True)


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components


    def _on_change(self, value):
        # self._value = value
        # if isinstance(self._value, State):
        #     self._value.set_value(value)
            
        self.valueChanged.emit(value)
        
        if self._onChange:
            self._onChange(value)

        for widget in self.findChildren(FormControlLabel):
            widget._control.setChecked(False)
            if widget._value == self._get_value():
                widget._control.setChecked(True)
            widget._control._updateIcon()