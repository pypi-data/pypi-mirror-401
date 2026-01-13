from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
import uuid
from qtmui.hooks import State, useEffect
from ...material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param
from qtmui.utils.translator import getTranslatedText

class FormHelperText(QLabel):
    """
    A component that provides helper text for form controls.

    The `FormHelperText` component is used to display helper or error messages below
    form controls, supporting all props of the Material-UI `FormHelperText` component.

    Parameters
    ----------
    children : State, str, QWidget, Callable, or None, optional
        The content of the component. If ' ', reserves one line height for a future message.
        Can be a string, a QWidget, a translation function, or a `State` object for dynamic updates.
        Default is None.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "p"). Default is None (uses QLabel or QFrame).
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the helper text is displayed in a disabled state. Default is False.
        Can be a `State` object for dynamic updates.
    error : State or bool, optional
        If True, the helper text is displayed in an error state. Default is False.
        Can be a `State` object for dynamic updates.
    filled : State or bool, optional
        If True, the helper text uses filled classes key. Default is False.
        Can be a `State` object for dynamic updates.
    focused : State or bool, optional
        If True, the helper text uses focused classes key. Default is False.
        Can be a `State` object for dynamic updates.
    margin : State or str, optional
        If "dense", adjusts vertical spacing (normally from FormControl). Default is "dense".
        Can be a `State` object for dynamic updates.
    required : State or bool, optional
        If True, the helper text uses required classes key. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The variant to use ("filled", "outlined", "standard", or custom string). Default is "standard".
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QLabel` or `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_MARGINS : list[str]
        Valid values for `margin`: ["dense"].
    VALID_VARIANTS : list[str]
        Valid values for `variant`: ["filled", "outlined", "standard"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - If `children` is a `QWidget`, the component uses a `QFrame` with a `QHBoxLayout` to contain it.
    - If `children` is ' ', the component reserves one line height for a future message.

    Demos:
    - FormHelperText: https://qtmui.com/material-ui/qtmui-formhelpertext/

    API Reference:
    - FormHelperText API: https://qtmui.com/material-ui/api/form-helper-text/
    """

    VALID_MARGINS = ["dense"]
    VALID_VARIANTS = ["filled", "outlined", "standard"]

    def __init__(
        self,
        children: Optional[Union[State, str, QWidget, Callable]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, str]] = None,
        disabled: Union[State, bool] = False,
        error: Union[State, bool] = False,
        filled: Union[State, bool] = False,
        focused: Union[State, bool] = False,
        margin: Union[State, str] = "dense",
        required: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        variant: Union[State, str] = "standard",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"MuiFormHelperText-{str(uuid.uuid4())}")

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_disabled(disabled)
        self._set_error(error)
        self._set_filled(filled)
        self._set_focused(focused)
        self._set_margin(margin)
        self._set_required(required)
        self._set_sx(sx)
        self._set_variant(variant)

        # Setup UI
        self._init_ui()

        # Apply styles
        self._set_stylesheet()

        # Connect signals
        self._connect_signals()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="children", supported_signatures=Union[State, str, QWidget, Callable, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value
        self.setEnabled(not self._get_disabled())

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="error", supported_signatures=Union[State, bool])
    def _set_error(self, value):
        """Assign value to error."""
        self._error = value

    def _get_error(self):
        """Get the error value."""
        return self._error.value if isinstance(self._error, State) else self._error

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="filled", supported_signatures=Union[State, bool])
    def _set_filled(self, value):
        """Assign value to filled."""
        self._filled = value

    def _get_filled(self):
        """Get the filled value."""
        return self._filled.value if isinstance(self._filled, State) else self._filled

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="focused", supported_signatures=Union[State, bool])
    def _set_focused(self, value):
        """Assign value to focused."""
        self._focused = value

    def _get_focused(self):
        """Get the focused value."""
        return self._focused.value if isinstance(self._focused, State) else self._focused

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="margin", supported_signatures=Union[State, str])
    def _set_margin(self, value):
        """Assign value to margin."""
        if value not in self.VALID_MARGINS:
            raise ValueError(f"margin must be one of {self.VALID_MARGINS}, got {value}")
        self._margin = value

    def _get_margin(self):
        """Get the margin value."""
        return self._margin.value if isinstance(self._margin, State) else self._margin

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="required", supported_signatures=Union[State, bool])
    def _set_required(self, value):
        """Assign value to required."""
        self._required = value

    def _get_required(self):
        """Get the required value."""
        return self._required.value if isinstance(self._required, State) else self._required

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.formhelpertext", param_name="variant", supported_signatures=Union[State, str])
    def _set_variant(self, value):
        """Assign value to variant."""
        if value not in self.VALID_VARIANTS and not isinstance(value, str):
            raise ValueError(f"variant must be one of {self.VALID_VARIANTS} or a custom string, got {value}")
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    def _init_ui(self):
        """Initialize the UI based on props."""
        children = self._get_children()

        # If children is a QWidget, use QFrame with QHBoxLayout
        if isinstance(children, QWidget):
            self.__class__ = QFrame  # Change base class to QFrame
            self.setLayout(QHBoxLayout())
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().addWidget(children)
            self._widget_references.append(children)
        else:
            if self.layout():
                self.setLayout(None)  # Remove layout if previously set
            if isinstance(children, str):
                self.setText(getTranslatedText(self._children))
                
            # self.setEnabled(not self._get_disabled())

        # Apply margin
        if self._get_margin() == "dense":
            self.setContentsMargins(4, 2, 4, 2)  # MUI dense margin

    def retranslateUi(self):
        """Update the UI text based on the current language and children."""
        children = self._get_children()
        if isinstance(children, str):
            self.setText(getTranslatedText(self._children))

    def _set_stylesheet(self, component_styled=None):
        """Apply styles based on theme, classes, and sx."""
        self.theme = useTheme()
        component_styled = component_styled or self.theme.components
        form_helper_text_styles = component_styled.get("FormHelperText", {}).get("styles", {})
        root_styles = form_helper_text_styles.get("root", {})
        root_qss = get_qss_style(root_styles)

        # Handle variant
        variant_styles = form_helper_text_styles.get("props", {}).get(f"{self._get_variant()}Variant", {})
        variant_qss = get_qss_style(variant_styles)

        # Handle color based on error and disabled
        color = (
            self.theme.palette.text.disabled if self._get_disabled()
            else self.theme.palette.error.main if self._get_error()
            else self.theme.palette.text.secondary
        )
        color_qss = f"color: {color};"

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

        # Apply MUI classes
        mui_classes = ["MuiFormHelperText-root", f"MuiFormHelperText-{self._get_variant()}"]
        if self._get_disabled():
            mui_classes.append("Mui-disabled")
        if self._get_error():
            mui_classes.append("Mui-error")
        if self._get_filled():
            mui_classes.append("MuiFormHelperText-filled")
        if self._get_focused():
            mui_classes.append("MuiFormHelperText-focused")
        if self._get_required():
            mui_classes.append("MuiFormHelperText-required")

        stylesheet = f"""
            #{self.objectName()} {{
                {root_qss}
                {variant_qss}
                {color_qss}
                {classes_qss}
            }}
            {sx_qss}
        """
        self.setStyleSheet(stylesheet)

    def _connect_signals(self):
        """Connect valueChanged signals of State parameters to their slots."""
        if isinstance(self._children, State):
            self._children.valueChanged.connect(self._on_children_changed)
        if isinstance(self._classes, State):
            self._classes.valueChanged.connect(self._on_classes_changed)
        if isinstance(self._component, State):
            self._component.valueChanged.connect(self._on_component_changed)
        if isinstance(self._disabled, State):
            self._disabled.valueChanged.connect(self._on_disabled_changed)
        if isinstance(self._error, State):
            self._error.valueChanged.connect(self._on_error_changed)
        if isinstance(self._filled, State):
            self._filled.valueChanged.connect(self._on_filled_changed)
        if isinstance(self._focused, State):
            self._focused.valueChanged.connect(self._on_focused_changed)
        if isinstance(self._margin, State):
            self._margin.valueChanged.connect(self._on_margin_changed)
        if isinstance(self._required, State):
            self._required.valueChanged.connect(self._on_required_changed)
        if isinstance(self._sx, State):
            self._sx.valueChanged.connect(self._on_sx_changed)
        if isinstance(self._variant, State):
            self._variant.valueChanged.connect(self._on_variant_changed)

    def _on_children_changed(self):
        """Handle changes to children."""
        self._set_children(self._children)
        self._init_ui()
        self._set_stylesheet()

    def _on_classes_changed(self):
        """Handle changes to classes."""
        self._set_classes(self._classes)
        self._set_stylesheet()

    def _on_component_changed(self):
        """Handle changes to component."""
        self._set_component(self._component)
        self._init_ui()
        self._set_stylesheet()

    def _on_disabled_changed(self):
        """Handle changes to disabled."""
        self._set_disabled(self._disabled)
        self._set_stylesheet()

    def _on_error_changed(self):
        """Handle changes to error."""
        self._set_error(self._error)
        self._set_stylesheet()

    def _on_filled_changed(self):
        """Handle changes to filled."""
        self._set_filled(self._filled)
        self._set_stylesheet()

    def _on_focused_changed(self):
        """Handle changes to focused."""
        self._set_focused(self._focused)
        self._set_stylesheet()

    def _on_margin_changed(self):
        """Handle changes to margin."""
        self._set_margin(self._margin)
        self._init_ui()

    def _on_required_changed(self):
        """Handle changes to required."""
        self._set_required(self._required)
        self._set_stylesheet()

    def _on_sx_changed(self):
        """Handle changes to sx."""
        self._set_sx(self._sx)
        self._set_stylesheet()

    def _on_variant_changed(self):
        """Handle changes to variant."""
        self._set_variant(self._variant)
        self._set_stylesheet()

 