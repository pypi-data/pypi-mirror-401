import asyncio
from typing import Callable, Union, Dict, Optional, List
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer, QEvent
import uuid
from qtmui.hooks import State
from ..spacer import HSpacer
from ..widget_base import PyWidgetBase
from ...material.styles import useTheme
from ..typography import Typography
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class FormControlLabel(QFrame, PyWidgetBase):
    """
    A component that provides a label for a control element like Radio, Switch, or Checkbox.

    The `FormControlLabel` component is used to associate a label with a form control,
    supporting all props of the Material-UI `FormControlLabel` component, as well as
    additional custom props.

    Parameters
    ----------
    control : State or QWidget, required
        A control element (e.g., Radio, Switch, Checkbox).
        Can be a `State` object for dynamic updates.
    checked : State or bool, optional
        If True, the component appears selected. Default is False.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    componentsProps : State or dict, optional
        Props used for each slot inside (deprecated, use `slotProps` instead). Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the control is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableTypography : State or bool, optional
        If True, the label is rendered without a typography node. Default is False.
        Can be a `State` object for dynamic updates.
    inputRef : State or object, optional
        Reference to the input element. Default is None.
        Can be a `State` object for dynamic updates.
    label : State, str, QWidget, List[QWidget], or None, optional
        Text or element used as the label. Default is None.
        Can be a `State` object for dynamic updates.
    labelPlacement : State or str, optional
        Position of the label ("bottom", "end", "start", "top"). Default is "end".
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        Identifier for the component (custom feature, not part of Material-UI). Default is None.
        Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the state changes. Default is None.
        Signature: function(event: dict) => void
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the label indicates that the input is required. Default is False.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props used for each slot inside. Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components used for each slot inside (e.g., typography). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    value : State or any, optional
        Value of the component. Default is None.
        Can be a `State` object for dynamic updates.
    highlight : State or bool, optional
        If True, applies a highlight border (custom feature, not part of Material-UI). Default is False.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the component takes up the full width (custom feature, not part of Material-UI). Default is False.
        Can be a `State` object for dynamic updates.
    spacing : State or int, optional
        Spacing between elements in the layout (custom feature, not part of Material-UI). Default is 6.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_LABEL_PLACEMENTS : list[str]
        Valid values for `labelPlacement`: ["bottom", "end", "start", "top"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `key`, `highlight`, `fullWidth`, and `spacing` parameters are custom features, not part of Material-UI's `FormControlLabel`.
    - The `componentsProps` prop is deprecated; use `slotProps` instead.
    - The `control` prop is required and must be a `QWidget` (e.g., Radio, Switch, Checkbox).

    Demos:
    - FormControlLabel: https://qtmui.com/material-ui/qtmui-formcontrollabel/

    API Reference:
    - FormControlLabel API: https://qtmui.com/material-ui/api/form-control-label/
    """

    VALID_LABEL_PLACEMENTS = ["bottom", "end", "start", "top"]

    def __init__(
        self,
        control: Union[State, QWidget],
        checked: Union[State, bool] = False,
        classes: Optional[Union[State, Dict]] = None,
        componentsProps: Optional[Union[State, Dict]] = None,
        disabled: Union[State, bool] = False,
        disableTypography: Union[State, bool] = False,
        inputRef: Optional[Union[State, object]] = None,
        label: Optional[Union[State, str, QWidget, List[QWidget], Callable]] = None,
        labelPlacement: Union[State, str] = "end",
        key: Optional[Union[State, str]] = None,
        onChange: Optional[Union[State, Callable]] = None,
        required: Union[State, bool] = False,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        value: Optional[Union[State, any]] = None,
        highlight: Union[State, bool] = False,
        fullWidth: Union[State, bool] = False,
        spacing: Union[State, int] = 6,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(f"MuiFormControlLabel-{str(uuid.uuid4())}")

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_control(control)
        self._set_checked(checked)
        self._set_classes(classes)
        self._set_componentsProps(componentsProps)
        self._set_disabled(disabled)
        self._set_disableTypography(disableTypography)
        self._set_inputRef(inputRef)
        self._set_label(label)
        self._set_labelPlacement(labelPlacement)
        self._set_key(key)
        self._set_onChange(onChange)
        self._set_required(required)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)
        self._set_value(value)
        self._set_highlight(highlight)
        self._set_fullWidth(fullWidth)
        self._set_spacing(spacing)

        # Setup UI
        self._init_ui()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="control", supported_signatures=Union[State, QWidget])
    def _set_control(self, value):
        """Assign value to control."""
        if not isinstance(value, (State, QWidget)):
            raise TypeError(f"control must be a State or QWidget, got {type(value)}")
        self._control = value
        # control = self._get_control()
        # if isinstance(control, QWidget):
        #     if hasattr(control, "setChecked"):
        #         control.setChecked(self._get_checked())
        #     if hasattr(control, "setEnabled"):
        #         control.setEnabled(not self._get_disabled())
        #     if hasattr(control, "setProperty"):
        #         control.setProperty("required", self._get_required())
        #         control.style().unpolish(control)
        #         control.style().polish(control)
        #     if self._get_onChange() and hasattr(control, "stateChanged"):
        #         control.stateChanged.connect(lambda: self.handle_change({"target": {"checked": control.isChecked()}}))
        #     elif self._get_onChange() and hasattr(control, "toggled"):
        #         control.toggled.connect(lambda checked: self.handle_change({"target": {"checked": checked}}))

    def _get_control(self):
        """Get the control value."""
        return self._control.value if isinstance(self._control, State) else self._control

    # @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="checked", supported_signatures=Union[State, bool])
    def _set_checked(self, value):
        """Assign value to checked."""
        self._checked = value

    def _get_checked(self):
        """Get the checked value."""
        return self._checked.value if isinstance(self._checked, State) else self._checked

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_componentsProps(self, value):
        """Assign value to componentsProps."""
        self._componentsProps = value

    def _get_componentsProps(self):
        """Get the componentsProps value."""
        return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value
        control = self._get_control()
        if isinstance(control, QWidget) and hasattr(control, "setEnabled"):
            control.setEnabled(not self._get_disabled())

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="disableTypography", supported_signatures=Union[State, bool])
    def _set_disableTypography(self, value):
        """Assign value to disableTypography."""
        self._disableTypography = value

    def _get_disableTypography(self):
        """Get the disableTypography value."""
        return self._disableTypography.value if isinstance(self._disableTypography, State) else self._disableTypography

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="inputRef", supported_signatures=Union[State, object, type(None)])
    def _set_inputRef(self, value):
        """Assign value to inputRef."""
        self._inputRef = value

    def _get_inputRef(self):
        """Get the inputRef value."""
        return self._inputRef.value if isinstance(self._inputRef, State) else self._inputRef

    # @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="label", supported_signatures=Union[State, str, QWidget, List[QWidget], type(None)])
    def _set_label(self, value):
        """Assign value to label."""
        self._label = value

    def _get_label(self):
        """Get the label value."""
        return self._label.value if isinstance(self._label, State) else self._label

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="labelPlacement", supported_signatures=Union[State, str])
    def _set_labelPlacement(self, value):
        """Assign value to labelPlacement."""
        if value not in self.VALID_LABEL_PLACEMENTS:
            raise ValueError(f"labelPlacement must be one of {self.VALID_LABEL_PLACEMENTS}, got {value}")
        self._labelPlacement = value

    def _get_labelPlacement(self):
        """Get the labelPlacement value."""
        return self._labelPlacement.value if isinstance(self._labelPlacement, State) else self._labelPlacement

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        """Assign value to key (custom feature)."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        """Assign value to onChange."""
        self._onChange = value

    def _get_onChange(self):
        """Get the onChange value."""
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="required", supported_signatures=Union[State, bool])
    def _set_required(self, value):
        """Assign value to required."""
        self._required = value
        # control = self._get_control()
        # if isinstance(control, QWidget) and hasattr(control, "setProperty"):
        #     control.setProperty("required", self._get_required())
        #     control.style().unpolish(control)
        #     control.style().polish(control)

    def _get_required(self):
        """Get the required value."""
        return self._required.value if isinstance(self._required, State) else self._required

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="value", supported_signatures=Union[State, any, type(None)])
    def _set_value(self, value):
        """Assign value to value."""
        self._value = value

    def _get_value(self):
        """Get the value value."""
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="highlight", supported_signatures=Union[State, bool])
    def _set_highlight(self, value):
        """Assign value to highlight (custom feature)."""
        self._highlight = value

    def _get_highlight(self):
        """Get the highlight value."""
        return self._highlight.value if isinstance(self._highlight, State) else self._highlight

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        """Assign value to fullWidth (custom feature)."""
        self._fullWidth = value

    def _get_fullWidth(self):
        """Get the fullWidth value."""
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.formcontrollabel", param_name="spacing", supported_signatures=Union[State, int])
    def _set_spacing(self, value):
        """Assign value to spacing (custom feature)."""
        self._spacing = value

    def _get_spacing(self):
        """Get the spacing value."""
        return self._spacing.value if isinstance(self._spacing, State) else self._spacing


    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        # if self._fullWidth:
        #     self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        # else:
        #     self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        if self._labelPlacement == "start":
            self.setLayout(QHBoxLayout())
            # if self._label is not None:
            #     self.layout().addWidget(QLabel(self._label))
            # if self._control is not None:
            #     self.layout().addWidget(self._control)
        elif self._labelPlacement == "end":
            self.setLayout(QHBoxLayout())
            # self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
            # if self._control is not None:
            #     self.layout().addWidget(self._control)
            # if self._label is not None:
            #     self.layout().addWidget(QLabel(self._label))
        elif self._labelPlacement == "top":
            self.setLayout(QVBoxLayout())
            # if self._label is not None:
            #     lb = QLabel(self._label)
            #     lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            #     self.layout().addWidget(lb)
            # if self._control is not None:
            #     self.layout().addWidget(self._control)
        elif self._labelPlacement == "bottom":
            self.setLayout(QVBoxLayout())
            # if self._control is not None:
            #     self.layout().addWidget(self._control)
            # if self._label is not None:
            #     lb = QLabel(self._label)
            #     lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            #     self.layout().addWidget(lb)

        # if isinstance(self._label, list) and all(isinstance(item, str) for item in self._label):

        if isinstance(self._label, list):
            frm_label = QFrame()
            frm_label.setLayout(QVBoxLayout())
            label_layout = frm_label.layout()
            self.add_children(layout=label_layout, children=self._label)
            self.layout().addWidget(frm_label)
        elif isinstance(self._label, str):
            self.add_children(self.layout(), Typography(text=self._label))
        elif isinstance(self._label, QWidget):
            self.add_children(self.layout(), self._label)

        if self._fullWidth: # self._sx and isinstance(self._sx, dict) and self._sx.get("width").find("%") != -1
            if self._control is not None:
                if self._labelPlacement == "start" or self._labelPlacement == "top":
                    self.layout().addWidget(HSpacer())
                    self.layout().addWidget(self._control)
                else:
                    self.layout().insertWidget(0, HSpacer())
                    self.layout().insertWidget(0, self._control)
        else:
            if self._control is not None:
                if self._labelPlacement == "start" or self._labelPlacement == "top":
                    self.layout().addWidget(self._control)
                else:
                    self.layout().insertWidget(0, self._control)
        
        if not self._control._key:
            self._control._key = self._key
        if not self._control._value:
            self._control._value = self._value

        # layout = self.layout()
        # if self._label is not None:
        #     self.add_children(layout=layout, children=self._label)

        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(self._spacing)

        for widget in self.findChildren(QWidget):
            widget.installEventFilter(self)  # Bắt sự kiện từ con

        if self._tooltip:
            PyWidgetBase._installTooltipFilter(self)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def add_children(self, layout, children):
        if isinstance(children, str):
            layout.addWidget(QLabel(children), 0, 
                             Qt.AlignmentFlag.AlignLeft if self._labelPlacement == "start" else 
                             Qt.AlignmentFlag.AlignRight if self._labelPlacement == "end" else  
                             Qt.AlignmentFlag.AlignCenter)
        elif isinstance(children, QWidget):
            layout.addWidget(children, 0, Qt.AlignmentFlag.AlignLeft if self._labelPlacement == "start" 
                             else Qt.AlignmentFlag.AlignRight if self._labelPlacement == "end" 
                             else  Qt.AlignmentFlag.AlignCenter)
        elif isinstance(children, list):
            for widget in children:
                if isinstance(widget, QWidget):
                    layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignLeft if self._labelPlacement == "start" 
                                     else Qt.AlignmentFlag.AlignRight if self._labelPlacement == "end" 
                                     else  Qt.AlignmentFlag.AlignCenter)
                    


    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.MouseButtonPress:
    #         print('prrrrrrrrrr', obj)
    #         return False

    def handle_change(self, event: dict):
        """
        Xử lý sự kiện thay đổi trạng thái của component.

        Args:
            event (dict): Sự kiện thay đổi, lấy trạng thái mới từ event.target.checked.
        """
        if self._onChange:
            self._onChange(event)

    def render(self):
        """
        Hàm render component.
        """
        # Sử dụng control và các thuộc tính đã

    def _set_stylesheet(self):
        theme = useTheme()
        
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
                
        stylesheet = f"""
            #{self.objectName()} {{
                color: {theme.palette.text.secondary};
            }}

            {sx_qss}

        """
        self.setStyleSheet(stylesheet)
