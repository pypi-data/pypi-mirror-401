from typing import Optional, Union, Dict, List, Callable
from PySide6.QtGui import QMouseEvent, QColor
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QSizePolicy, QVBoxLayout, QGraphicsDropShadowEffect, QPushButton

from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from .accordion_summary import AccordionSummary
from .accordion_details import AccordionDetails
from ..utils.validate_params import _validate_param

class Accordion(QFrame):
    """
    An accordion widget that can expand or collapse to show or hide content.

    The `Accordion` widget provides a collapsible container for organizing content in a
    user interface. It supports expansion and collapse states, customizable styles, and
    transitions. It inherits properties from `QFrame` and extends them with additional
    customization options such as default expansion, disabled state, and gutter control.
    Props of the Material-UI Paper component are also supported, such as `elevation` and
    `variant`.

    Parameters
    ----------
    children : State or list, optional
        The content of the component, typically including `AccordionSummary` and
        `AccordionDetails`. Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    defaultExpanded : State or bool, optional
        If true, expands the accordion by default. Default is False.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If true, the component is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If true, removes the margin between expanded accordion items and the increase
        of height. Default is False. Can be a `State` object for dynamic updates.
    elevation : State or int, optional
        The elevation level of the component, affecting the shadow depth (0-24).
        Default is 1. Can be a `State` object for dynamic updates.
    expanded : State or bool, optional
        If true, expands the accordion; otherwise, collapses it. Setting this prop
        enables control over the accordion. Default is False.
        Can be a `State` object for dynamic updates.
    fullWidth : State or bool, optional
        If true, the accordion takes up the full width of its container. Default is True.
        Can be a `State` object for dynamic updates.
    key : State or str, optional
        A unique identifier for the accordion, used in controlled state scenarios.
        Default is None. Can be a `State` object for dynamic updates.
    onChange : State or Callable, optional
        Callback fired when the expand/collapse state changes.
        Signature: function(event: object, expanded: bool) => void.
        Default is None. Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props used for each slot inside the component (e.g., heading, root, transition).
        Default is {}. Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components used for each slot inside the component (e.g., heading, root, transition).
        Default is {}. Can be a `State` object for dynamic updates.
    square : State or bool, optional
        If true, rounded corners are disabled. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, or str, optional
        Custom styles for the component. Can be a CSS-like string, a dictionary of
        style properties, a callable returning styles, or a `State` object for dynamic
        styling. Default is {"width": "100%"}.
    TransitionComponent : State or Any, optional
        The component used for the transition. Default is None.
        Deprecated: Use slots.transition instead. This prop will be removed in a future
        major release. Can be a `State` object for dynamic updates.
    TransitionProps : State or dict, optional
        Props applied to the transition element. Default is {}.
        Deprecated: Use slotProps.transition instead. This prop will be removed in a
        future major release. Can be a `State` object for dynamic updates.
    variant : State or str, optional
        The visual style of the component. Valid values include "elevation", "outlined".
        Default is "elevation". Can be a `State` object for dynamic updates.

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["elevation", "outlined"].

    Signals
    -------
    stateChanged : Signal(bool)
        Emitted when the expand/collapse state changes.

    Demos:
    - Accordion: https://qtmui.com/material-ui/qtmui-accordion/

    API Reference:
    - Accordion API: https://qtmui.com/material-ui/api/accordion/
    """

    stateChanged = Signal(bool)
    VALID_VARIANTS = ["elevation", "outlined"]

    def __init__(
        self,
        children: Optional[Union[State, List]] = None,
        classes: Optional[Union[State, Dict]] = None,
        defaultExpanded: Optional[Union[State, bool]] = False,
        disabled: Optional[Union[State, bool]] = False,
        disableGutters: Optional[Union[State, bool]] = False,
        elevation: Optional[Union[State, int]] = 1,
        expanded: Optional[Union[State, bool]] = False,
        fullWidth: Optional[Union[State, bool]] = True,
        key: Optional[Union[State, str]] = None,
        onChange: Optional[Union[State, Callable]] = None,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        square: Optional[Union[State, bool]] = False,
        sx: Optional[Union[State, Dict, Callable, str]] = {"width": "100%"},
        TransitionComponent: Optional[Union[State, object]] = None,
        TransitionProps: Optional[Union[State, Dict]] = None,
        variant: Optional[Union[State, str]] = "elevation",
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName("PyAccordion")

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_children(children)
        self._set_classes(classes)
        self._set_defaultExpanded(defaultExpanded)
        self._set_disabled(disabled)
        self._set_disableGutters(disableGutters)
        self._set_elevation(elevation)
        self._set_expanded(expanded)
        self._set_fullWidth(fullWidth)
        self._set_key(key)
        self._set_onChange(onChange)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_square(square)
        self._set_sx(sx)
        self._set_TransitionComponent(TransitionComponent)
        self._set_TransitionProps(TransitionProps)
        self._set_variant(variant)

        self._accordion_shadow = None
        self._accordion_root_style = None
        self._accordion_expanded_style = None
        self._accordion_disabled_style = None
        self._accordion_summary_root_style = None
        self._accordion_summary_disabled_style = None
        self._accordion_summary_disabled_typography_style = None

        self.init_mode = True
        self._init_ui()

    @_validate_param(file_path="qtmui.material.accordion", param_name="children", supported_signatures=Union[State, List, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.accordion", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.accordion", param_name="defaultExpanded", supported_signatures=Union[State, bool, type(None)])
    def _set_defaultExpanded(self, value):
        """Assign value to defaultExpanded."""
        self._defaultExpanded = value

    def _get_defaultExpanded(self):
        """Get the defaultExpanded value."""
        return self._defaultExpanded.value if isinstance(self._defaultExpanded, State) else self._defaultExpanded

    @_validate_param(file_path="qtmui.material.accordion", param_name="disabled", supported_signatures=Union[State, bool, type(None)])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.accordion", param_name="disableGutters", supported_signatures=Union[State, bool, type(None)])
    def _set_disableGutters(self, value):
        """Assign value to disableGutters."""
        self._disableGutters = value

    def _get_disableGutters(self):
        """Get the disableGutters value."""
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    # @_validate_param(file_path="qtmui.material.accordion", param_name="elevation", supported_signatures=Union[State, int, type(None)], valid_values=range(0, 25))
    def _set_elevation(self, value):
        """Assign value to elevation."""
        self._elevation = value

    def _get_elevation(self):
        """Get the elevation value."""
        return self._elevation.value if isinstance(self._elevation, State) else self._elevation

    @_validate_param(file_path="qtmui.material.accordion", param_name="expanded", supported_signatures=Union[State, bool, type(None)])
    def _set_expanded(self, value):
        """Assign value to expanded."""
        self._expanded = value

    def _get_expanded(self):
        """Get the expanded value."""
        return self._expanded.value if isinstance(self._expanded, State) else self._expanded

    @_validate_param(file_path="qtmui.material.accordion", param_name="fullWidth", supported_signatures=Union[State, bool, type(None)])
    def _set_fullWidth(self, value):
        """Assign value to fullWidth."""
        self._fullWidth = value

    def _get_fullWidth(self):
        """Get the fullWidth value."""
        return self._fullWidth.value if isinstance(self._fullWidth, State) else self._fullWidth

    @_validate_param(file_path="qtmui.material.accordion", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.accordion", param_name="onChange", supported_signatures=Union[State, Callable, type(None)])
    def _set_onChange(self, value):
        """Assign value to onChange."""
        self._onChange = value

    def _get_onChange(self):
        """Get the onChange value."""
        return self._onChange.value if isinstance(self._onChange, State) else self._onChange

    @_validate_param(file_path="qtmui.material.accordion", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value or {}

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.accordion", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value or {}

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.accordion", param_name="square", supported_signatures=Union[State, bool, type(None)])
    def _set_square(self, value):
        """Assign value to square."""
        self._square = value

    def _get_square(self):
        """Get the square value."""
        return self._square.value if isinstance(self._square, State) else self._square

    @_validate_param(file_path="qtmui.material.accordion", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value or {"width": "100%"}

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.accordion", param_name="TransitionComponent", supported_signatures=Union[State, object, type(None)])
    def _set_TransitionComponent(self, value):
        """Assign value to TransitionComponent."""
        self._TransitionComponent = value

    def _get_TransitionComponent(self):
        """Get the TransitionComponent value."""
        return self._TransitionComponent.value if isinstance(self._TransitionComponent, State) else self._TransitionComponent

    @_validate_param(file_path="qtmui.material.accordion", param_name="TransitionProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_TransitionProps(self, value):
        """Assign value to TransitionProps."""
        self._TransitionProps = value or {}

    def _get_TransitionProps(self):
        """Get the TransitionProps value."""
        return self._TransitionProps.value if isinstance(self._TransitionProps, State) else self._TransitionProps

    @_validate_param(file_path="qtmui.material.accordion", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    def _init_ui(self):
        self.setLayout(QVBoxLayout())
        if not self._get_disableGutters():
            self.layout().setContentsMargins(8, 8, 8, 8)
            self.layout().setSpacing(3)
        else:
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().setSpacing(0)

        if self._get_children():
            for item in self._get_children():
                if item is not None:
                    self.layout().addWidget(item)

        self._accordion_summary: AccordionSummary = self.findChildren(AccordionSummary)[0]
        self._accordion_details: AccordionDetails = self.findChildren(AccordionDetails)[0]
        self._accordion_summary.clicked.connect(self._toogle)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        if isinstance(self._expanded, State):
            self._expanded.valueChanged.connect(self._set_controlled_state)
            self._expanded_value = self._expanded.value
            self._set_controlled_state(self._expanded.value)
        else:
            self._expanded_value = self._expanded

        if self._get_disabled():
            self.setEnabled(False)

        self._set_default_state()

        theme = useTheme()
        theme.state.valueChanged.connect(self.__set_stylesheet)
        self.__set_stylesheet()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

    def retranslateUi(self):
        pass

    def _get_theme_style(self):
        theme = useTheme()
        component_styles = theme.components

        # Styles for Accordion
        PyAccordion = component_styles["PyAccordion"].get("styles")
        MuiAccordionSummary = component_styles["MuiAccordionSummary"].get("styles")
        PyAccordionDetail = component_styles["PyAccordionDetail"].get("styles")

        slots_style = PyAccordion["root"]["slots"]
        slots_expanded = slots_style["expanded"]
        disabled_qss = get_qss_style(slots_style["disabled"])
        slots_expanded_style = get_qss_style(slots_expanded)

        self._accordion_root_style = get_qss_style(PyAccordion["root"])
        self._accordion_shadow = slots_expanded.get("box-shadow", "0px 2px 4px rgba(0,0,0,0.2)")
        self._accordion_summary_root_style = get_qss_style(MuiAccordionSummary["root"])
        self._accordion_summary_disabled_style = get_qss_style(MuiAccordionSummary["root"]["slots"]["disabled"])
        self._accordion_summary_disabled_typography_style = get_qss_style(
            MuiAccordionSummary["root"]["slots"]["disabled"]["typography"]["root"]
        )
        self.PyAccordionDetail_root_qss = get_qss_style(PyAccordionDetail["root"])

        # Handle variant-specific styles
        border_style = "border: 1px solid rgba(0,0,0,0.12);" if self._get_variant() == "outlined" else ""
        border_radius = "border-radius: 0px;" if self._get_square() else "border-radius: 4px;"

        self._accordion_expanded_style = f"""
            /* expanded style */
            {slots_expanded_style}
            {border_style}
            {border_radius}
        """
        self._accordion_disabled_style = f"""
            /* disabled style */
            {disabled_qss}
        """ if self._get_disabled() else ""

    def _set_expanded_state(self, expanded):
        self._get_theme_style()

        accordion_sx_qss = get_qss_style(self._sx) if self._sx else ""
        if self._get_fullWidth() and not accordion_sx_qss:
            accordion_sx_qss = "width: 100%;"

        accordion_summary_sx_qss = get_qss_style(self._accordion_summary._sx) if self._accordion_summary._sx else ""

        accordion_stylesheet = f"""
            {self._accordion_root_style}
            {self._accordion_expanded_style if expanded else ""}
            {self._accordion_disabled_style}
            /* sx */
            {accordion_sx_qss}
        """
        accordion_summary_stylesheet = f"""
            {self._accordion_summary_root_style}
            {self._accordion_summary_disabled_style if self._get_disabled() else ""}
            /* sx */
            {accordion_summary_sx_qss}
        """

        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {accordion_stylesheet}
                }}
                #{self._accordion_summary.objectName()} {{
                    {accordion_summary_stylesheet}
                }}
                #{self._accordion_details.objectName()} {{
                    {self.PyAccordionDetail_root_qss}
                }}
            """
        )

        if expanded and self._get_variant() == "elevation":
            elevation = self._get_elevation() or 1
            blur_radius = min(4 + elevation * 2, 24)
            offset_y = min(2 + elevation, 8)
            self._setShadowEffect(blurRadius=blur_radius, offset=(0, offset_y), color=QColor(0, 0, 0, 50))
        else:
            self.setGraphicsEffect(None)

    def _setShadowEffect(self, blurRadius=10, offset=(0, 2), color=QColor(0, 0, 0, 50)):
        """Add shadow to the accordion based on elevation."""
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        self.setGraphicsEffect(shadowEffect)

    def _set_default_state(self):
        if self._get_defaultExpanded():
            if not self._accordion_details.isVisible():
                self._accordion_details.show()
            self._accordion_summary._toggle_icon(show_details=True)
            self._set_expanded_state(True)
        else:
            self._accordion_details.hide()
            self._accordion_summary._toggle_icon(show_details=False)
            self._set_expanded_state(False)
        self._expanded_value = self._get_defaultExpanded()

    def _set_controlled_state(self, value):
        if self._get_key() == value:
            if not self._accordion_details.isVisible():
                self._accordion_details.show()
            self._accordion_summary._toggle_icon(show_details=True)
            self._set_expanded_state(True)
        else:
            self._accordion_details.hide()
            self._accordion_summary._toggle_icon(show_details=False)
            self._set_expanded_state(False)
        self._expanded_value = value

    def _toogle(self):
        if not isinstance(self._expanded, State):
            if not self._expanded_value:
                if not self._accordion_details.isVisible():
                    self._accordion_details.show()
                self._accordion_summary._toggle_icon(show_details=True)
                self._set_expanded_state(True)
            else:
                self._accordion_details.hide()
                self._accordion_summary._toggle_icon(show_details=False)
                self._set_expanded_state(False)
            self._expanded_value = not self._expanded_value
        else:
            self._expanded_value = not self._expanded_value

        self.stateChanged.emit(self._expanded_value)
        if self._onChange:
            # self._onChange(self._get_key(), self._expanded_value)
            self._onChange(self._get_key())

    def __set_stylesheet(self):
        if hasattr(self, "_expanded_value"):
            if not self._expanded_value:
                self._set_expanded_state(False)
            else:
                self._set_expanded_state(True)

