from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QEvent
from ..spacer import HSpacer
from ..button import IconButton
from ..stack import Stack
from ..py_iconify import PyIconify, Iconify
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.hooks import State
from ..utils.validate_params import _validate_param

class AccordionSummary(QPushButton):
    """
    A component that displays the summary content of an Accordion.

    The `AccordionSummary` component is used to render the clickable header of an
    `Accordion`, which toggles the visibility of the `AccordionDetails`. It inherits
    from `QPushButton` and supports all props of the Material-UI `ButtonBase` component
    via `**kwargs`. It provides customizable styling, an expandable icon, and focus
    handling for accessibility.

    Parameters
    ----------
    children : State, list, QWidget, or None, optional
        The content of the component, such as text or widgets. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    expandIcon : State, PyIconify, QWidget, or None, optional
        The icon to display as the expand indicator. Default is None.
        Can be a `State` object for dynamic updates.
    focusVisibleClassName : State or str, optional
        Class name applied when the element gains focus through keyboard interaction.
        Acts as a polyfill for the CSS :focus-visible selector. Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props used for each slot inside the component (e.g., content, expandIconWrapper,
        root). Default is {}. Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components used for each slot inside the component (e.g., content,
        expandIconWrapper, root). Default is {}. Can be a `State` object for dynamic
        updates.
    sx : State, dict, Callable, str, or None, optional
        The system prop that allows defining system overrides as well as additional CSS
        styles. Can be a CSS-like string, a dictionary of style properties, a callable
        returning styles, or a `State` object for dynamic styling. Default is None.
    *args
        Additional positional arguments passed to the parent `QPushButton` class.
    **kwargs
        Additional keyword arguments passed to the parent `QPushButton` class, supporting
        all props of the Material-UI `ButtonBase` component (e.g., `disabled`, `onClick`).

    Notes
    -----
    - Props of the `ButtonBase` component are available via `**kwargs`.
    - The component uses the theme's `MuiAccordionSummary` styles for default appearance.
    - The `focusVisibleClassName` prop is applied when the component gains focus via
      keyboard interaction, enhancing accessibility.

    Demos:
    - AccordionSummary: https://qtmui.com/material-ui/qtmui-accordion-summary/

    API Reference:
    - AccordionSummary API: https://qtmui.com/material-ui/api/accordion-summary/
    """

    def __init__(
        self,
        children: Optional[Union[State, List, QWidget]] = None,
        classes: Optional[Union[State, Dict]] = None,
        expandIcon: Optional[Union[State, PyIconify, QWidget]] = None,
        focusVisibleClassName: Optional[Union[State, str]] = None,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setObjectName("MuiAccordionSummary")
        self.installEventFilter(self)

        # Thiết lập các thuộc tính với dấu gạch dưới
        self._set_children(children)
        self._set_classes(classes)
        self._set_expandIcon(expandIcon)
        self._set_focusVisibleClassName(focusVisibleClassName)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)

        self._is_focus_visible = False
        self._setup_ui()

        theme = useTheme()
        theme.state.valueChanged.connect(self.__set_stylesheet)
        self.__set_stylesheet()

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="children", supported_signatures=Union[State, List, QWidget, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="expandIcon", supported_signatures=Union[State, Iconify, QWidget, type(None)])
    def _set_expandIcon(self, value):
        """Assign value to expandIcon."""
        self._expandIcon = value

    def _get_expandIcon(self):
        """Get the expandIcon value."""
        return self._expandIcon.value if isinstance(self._expandIcon, State) else self._expandIcon

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="focusVisibleClassName", supported_signatures=Union[State, str, type(None)])
    def _set_focusVisibleClassName(self, value):
        """Assign value to focusVisibleClassName."""
        self._focusVisibleClassName = value

    def _get_focusVisibleClassName(self):
        """Get the focusVisibleClassName value."""
        return self._focusVisibleClassName.value if isinstance(self._focusVisibleClassName, State) else self._focusVisibleClassName

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value or {}

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value or {}

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.accordion_summary", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    def _setup_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(16, 0, 16, 0)  # Default padding from MUI AccordionSummary
        self.setCursor(Qt.PointingHandCursor)

        children = self._get_children() or []
        if not isinstance(children, list):
            children = [children] if children else []

        # Handle expandIcon with slots.expandIconWrapper
        expand_icon_widget = None
        slots = self._get_slots()
        if slots.get("expandIconWrapper"):
            expand_icon_widget = slots["expandIconWrapper"]
        elif self._get_expandIcon():
            slot_props = self._get_slotProps()
            icon_props = slot_props.get("expandIconWrapper", {})
            expand_icon_widget = IconButton(icon=self._get_expandIcon(), size="small", **icon_props)

        if expand_icon_widget:
            children.append(expand_icon_widget)

        # Use slots.content if provided
        content_widget = None
        if slots.get("content"):
            content_widget = slots["content"]
        else:
            slot_props = self._get_slotProps()
            stack_props = slot_props.get("content", {})
            content_widget = Stack(
                direction="row",
                alignItems="center",
                sx={"min-height": 48},  # Default min-height from MUI AccordionSummary
                justifyContent="space-between",
                children=children,
                **stack_props
            )

        self.layout().addWidget(content_widget)

    def __set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components.get("MuiAccordionSummary", {})
        root_style = get_qss_style(component_styles.get("root", {}))

        # Apply sx styles
        sx_style = get_qss_style(self._get_sx()) if self._get_sx() else ""

        # Apply classes
        classes_style = get_qss_style(self._get_classes()) if self._get_classes() else ""

        # Apply focusVisibleClassName when focused via keyboard
        focus_visible_style = ""
        if self._is_focus_visible and self._get_focusVisibleClassName():
            focus_visible_style = get_qss_style({"className": self._get_focusVisibleClassName()})

        stylesheet = f"""
            #{self.objectName()} {{
                {root_style}
                {sx_style}
                {classes_style}
                {focus_visible_style}
            }}
        """
        self.setStyleSheet(stylesheet)

    def _toggle_icon(self, show_details):
        """Rotate the expand icon based on the show_details state."""
        expand_icon = self._get_expandIcon()
        # if isinstance(expand_icon, PyIconify):
        #     expand_icon._rotate = 180 if show_details else 0
        #     expand_icon.changeSvg()

    def eventFilter(self, obj, event):
        """Handle keyboard focus events to apply focusVisibleClassName."""
        if obj == self:
            if event.type() == QEvent.FocusIn:
                if event.reason() in (Qt.TabFocusReason, Qt.BacktabFocusReason):
                    self._is_focus_visible = True
                    self.__set_stylesheet()
            elif event.type() == QEvent.FocusOut:
                self._is_focus_visible = False
                self.__set_stylesheet()
        return super().eventFilter(obj, event)