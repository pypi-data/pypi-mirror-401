from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QVBoxLayout, QFrame, QSizePolicy, QWidget
from PySide6.QtCore import Qt
import uuid
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..typography import Typography
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class FormControl(QFrame):
    """
    A component that provides context such as filled/focused/error/required for form inputs.

    The `FormControl` component is used to manage the state and styling of form inputs,
    supporting all props of the Material-UI `FormControl` component, as well as additional
    custom props.

    Parameters
    ----------
    component : State, str, or None, optional
        The component used for the root node (e.g., "fieldset"). Default is "fieldset".
        Can be a `State` object for dynamic updates.
    label : State, str, or None, optional
        The label text for the form control (custom feature, not part of Material-UI).
        Default is "Basic".
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically form inputs or labels. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    color : State or str, optional
        The color of the component ("primary", "secondary", "error", "info", "success",
        "warning", or custom string). Default is "primary".
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the label, input, and helper text are displayed in a disabled state.
        Default is False.
        Can be a `State` object for dynamic updates.
    error : State or bool, optional
        If True, the label is displayed in an error state. Default is False.
        Can be a `State` object for dynamic updates.
    focused : State or bool, optional
        If True, the component is displayed in a focused state. Default is False.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If True, the component takes up the full width of its container. Default is False.
        Can be a `State` object for dynamic updates.
    hiddenLabel : State or bool, optional
        If True, the label is hidden. Default is False.
        Can be a `State` object for dynamic updates.
    margin : State or str, optional
        Adjusts vertical spacing ("dense", "none", "normal"). Default is "none".
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the label indicates that the input is required. Default is False.
        Can be a `State` object for dynamic updates.
    size : State or str, optional
        The size of the component ("medium", "small", or custom string). Default is "medium".
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The variant to use ("filled", "outlined", "standard"). Default is "outlined".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_COLORS : list[str]
        Valid values for `color`: ["primary", "secondary", "error", "info", "success", "warning"].
    VALID_MARGINS : list[str]
        Valid values for `margin`: ["dense", "none", "normal"].
    VALID_SIZES : list[str]
        Valid values for `size`: ["medium", "small"].
    VALID_VARIANTS : list[str]
        Valid values for `variant`: ["filled", "outlined", "standard"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `label` parameter is a custom feature, not part of Material-UI's `FormControl`.
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - FormControl: https://qtmui.com/material-ui/qtmui-formcontrol/

    API Reference:
    - FormControl API: https://qtmui.com/material-ui/api/form-control/
    """

    VALID_COLORS = ["primary", "secondary", "error", "info", "success", "warning"]
    VALID_MARGINS = ["dense", "none", "normal"]
    VALID_SIZES = ["medium", "small"]
    VALID_VARIANTS = ["filled", "outlined", "standard"]

    def __init__(
        self,
        component: Optional[Union[State, str]] = "fieldset",
        label: Optional[Union[State, str]] = "Basic",
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        color: Union[State, str] = "primary",
        disabled: Union[State, bool] = False,
        error: Union[State, bool] = False,
        focused: Union[State, bool] = False,
        fullWidth: Union[State, bool] = False,
        hiddenLabel: Union[State, bool] = False,
        margin: Union[State, str] = "none",
        required: Union[State, bool] = False,
        size: Union[State, str] = "medium",
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        variant: Union[State, str] = "outlined",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"PyFormControl-{str(uuid.uuid4())}")

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_component(component)
        self._set_label(label)
        self._set_children(children)
        self._set_classes(classes)
        self._set_color(color)
        self._set_disabled(disabled)
        self._set_error(error)
        self._set_focused(focused)
        self._set_fullWidth(fullWidth)
        self._set_hiddenLabel(hiddenLabel)
        self._set_margin(margin)
        self._set_required(required)
        self._set_size(size)
        self._set_sx(sx)
        self._set_variant(variant)

        # Setup UI
        self._init_ui()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.formcontrol", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="label", supported_signatures=Union[State, str, type(None)])
    def _set_label(self, value):
        """Assign value to label (custom feature)."""
        self._label = value

    def _get_label(self):
        """Get the label value."""
        return self._label.value if isinstance(self._label, State) else self._label

    # @_validate_param(file_path="qtmui.material.formcontrol", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    # def _set_children(self, value):
    #     """Assign value to children and store widget references."""
    #     self._widget_references.clear()
    #     self._children = value
    #     children = self._get_children()

    #     if isinstance(children, QWidget):
    #         self._widget_references.append(children)
    #         children.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    #     elif isinstance(children, list):
    #         for child in children:
    #             if child is None:
    #                 continue
    #             if isinstance(child, QWidget):
    #                 self._widget_references.append(child)
    #                 child.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    #             else:
    #                 raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
    #     elif children is not None:
    #         raise TypeError(f"children must be a State, QWidget, or list of QWidgets, but got {type(children)}")
        
    # @_validate_param(file_path="qtmui.material.formcontrol", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children and store widget references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="color", supported_signatures=Union[State, str])
    def _set_color(self, value):
        """Assign value to color."""
        if value not in self.VALID_COLORS and not isinstance(value, str):
            raise ValueError(f"color must be one of {self.VALID_COLORS} or a custom string, got {value}")
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="error", supported_signatures=Union[State, bool])
    def _set_error(self, value):
        """Assign value to error."""
        self._error = value

    def _get_error(self):
        """Get the error value."""
        return self._error.value if isinstance(self._error, State) else self._error

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="focused", supported_signatures=Union[State, bool])
    def _set_focused(self, value):
        """Assign value to focused."""
        self._focused = value

    def _get_focused(self):
        """Get the focused value."""
        return self._focused.value if isinstance(self._focused, State) else self._focused

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="fullWidth", supported_signatures=Union[State, bool])
    def _set_fullWidth(self, value):
        """Assign value to fullWidth."""
        self._fullWidth = value

    def _get_fullWidth(self):
        """Get the fullWidth value."""
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="hiddenLabel", supported_signatures=Union[State, bool])
    def _set_hiddenLabel(self, value):
        """Assign value to hiddenLabel."""
        self._hiddenLabel = value

    def _get_hiddenLabel(self):
        """Get the hiddenLabel value."""
        return self._hiddenLabel.value if isinstance(self._hiddenLabel, State) else self._hiddenLabel

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="margin", supported_signatures=Union[State, str])
    def _set_margin(self, value):
        """Assign value to margin."""
        if value not in self.VALID_MARGINS:
            raise ValueError(f"margin must be one of {self.VALID_MARGINS}, got {value}")
        self._margin = value

    def _get_margin(self):
        """Get the margin value."""
        return self._margin.value if isinstance(self._margin, State) else self._margin

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="required", supported_signatures=Union[State, bool])
    def _set_required(self, value):
        """Assign value to required."""
        self._required = value

    def _get_required(self):
        """Get the required value."""
        return self._required.value if isinstance(self._required, State) else self._required

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="size", supported_signatures=Union[State, str])
    def _set_size(self, value):
        """Assign value to size."""
        if value not in self.VALID_SIZES and not isinstance(value, str):
            raise ValueError(f"size must be one of {self.VALID_SIZES} or a custom string, got {value}")
        self._size = value

    def _get_size(self):
        """Get the size value."""
        return self._size.value if isinstance(self._size, State) else self._size

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.formcontrol", param_name="variant", supported_signatures=Union[State, str])
    def _set_variant(self, value):
        """Assign value to variant."""
        if value not in self.VALID_VARIANTS:
            raise ValueError(f"variant must be one of {self.VALID_VARIANTS}, got {value}")
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant


    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        if self._sx != None:
            self.setObjectName(str(uuid.uuid4()))
            self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), self._sx)) # str multi line

        if isinstance(self._children, list) and len(self._children) > 0:
            for item in self._children:
                if item is not None:
                    self.layout().addWidget(item)


