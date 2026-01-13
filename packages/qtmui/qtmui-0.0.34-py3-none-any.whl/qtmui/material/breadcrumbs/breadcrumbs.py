import asyncio
from typing import Optional, Union, Callable, Any, Dict, List
import uuid

from qtmui.hooks import State, useEffect
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QPushButton
from PySide6.QtCore import Qt, QSize, QTimer

from qtmui.material.spacer import HSpacer
from qtmui.material.py_svg_widget import PySvgWidget
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import translate, i18n
from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

class Breadcrumbs(QWidget, PyWidgetBase):
    """
    A component that displays a list of breadcrumbs with customizable separators and collapse behavior.

    The `Breadcrumbs` component is used to show navigation paths, with support for collapsing
    items when the number of breadcrumbs exceeds a specified maximum. It supports all props
    of the Material-UI `Breadcrumbs` component, as well as props of the `Typography` component
    via `**kwargs`.

    Parameters
    ----------
    children : State or List[Any], optional
        The content of the Breadcrumbs, typically a list of `Typography` or other components.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    expandText : State or str, optional
        Label for the expand button, used when breadcrumbs are collapsed.
        Default is "Show path". Can be a `State` object for dynamic updates.
    itemsAfterCollapse : State or int, optional
        Number of items to show after the ellipsis when collapsed. Default is 1.
        Can be a `State` object for dynamic updates.
    itemsBeforeCollapse : State or int, optional
        Number of items to show before the ellipsis when collapsed. Default is 1.
        Can be a `State` object for dynamic updates.
    maxItems : State or int, optional
        Maximum number of breadcrumbs to display before collapsing. Default is 8.
        Can be a `State` object for dynamic updates.
    separator : State, str, Any, or None, optional
        Custom separator between breadcrumbs. Can be a string, component, or other node.
        Default is "/". Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (e.g., collapsedIcon). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (e.g., CollapsedIcon). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class, supporting
        props of the `Typography` component (e.g., variant, color).

    Attributes
    ----------
    VALID_SEPARATOR_TYPES : list[str]
        Valid types for the `separator` parameter: ["str", "Typography", "PyToolButton", "custom"].

    Notes
    -----
    - Props of the `Typography` component are supported via `**kwargs` (e.g., `variant`, `color`).
    - When the number of children exceeds `maxItems`, the component collapses to show
      `itemsBeforeCollapse` items, an ellipsis, and `itemsAfterCollapse` items.
    - The `separator` can be a string, `Typography`, `PyToolButton`, or custom component.

    Demos:
    - Breadcrumbs: https://qtmui.com/material-ui/qtmui-breadcrumbs/

    API Reference:
    - Breadcrumbs API: https://qtmui.com/material-ui/api/breadcrumbs/
    """

    VALID_SEPARATOR_TYPES = ["str", "Typography", "PyToolButton", "custom"]

    def __init__(
        self,
        children: Optional[Union[State, List[Any]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, Any]] = None,
        expandText: Union[State, str] = "Show path",
        itemsAfterCollapse: Union[State, int] = 1,
        itemsBeforeCollapse: Union[State, int] = 1,
        maxItems: Union[State, int] = 8,
        separator: QWidget = None,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_expandText(expandText)
        self._set_itemsAfterCollapse(itemsAfterCollapse)
        self._set_itemsBeforeCollapse(itemsBeforeCollapse)
        self._set_maxItems(maxItems)
        self._set_separator(separator)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_sx(sx)

        self._is_collapsed = False  # Track collapse state

        self._init_ui()
        self._set_stylesheet()

        # i18n.langChanged.connect(self.retranslateUi)
        self.theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        self.destroyed.connect(self._on_destroyed)

    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="children", supported_signatures=Union[State, List[Any], type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="expandText", supported_signatures=Union[State, str])
    def _set_expandText(self, value):
        self._expandText = value

    def _get_expandText(self):
        return self._expandText.value if isinstance(self._expandText, State) else self._expandText

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="itemsAfterCollapse", supported_signatures=Union[State, int])
    def _set_itemsAfterCollapse(self, value):
        if value < 0:
            raise ValueError("itemsAfterCollapse must be non-negative")
        self._itemsAfterCollapse = value

    def _get_itemsAfterCollapse(self):
        return self._itemsAfterCollapse.value if isinstance(self._itemsAfterCollapse, State) else self._itemsAfterCollapse

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="itemsBeforeCollapse", supported_signatures=Union[State, int])
    def _set_itemsBeforeCollapse(self, value):
        if value < 0:
            raise ValueError("itemsBeforeCollapse must be non-negative")
        self._itemsBeforeCollapse = value

    def _get_itemsBeforeCollapse(self):
        return self._itemsBeforeCollapse.value if isinstance(self._itemsBeforeCollapse, State) else self._itemsBeforeCollapse

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="maxItems", supported_signatures=Union[State, int])
    def _set_maxItems(self, value):
        if value < (self._get_itemsBeforeCollapse() + self._get_itemsAfterCollapse()):
            raise ValueError("maxItems must be at least itemsBeforeCollapse + itemsAfterCollapse")
        self._maxItems = value

    def _get_maxItems(self):
        return self._maxItems.value if isinstance(self._maxItems, State) else self._maxItems

    # @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="separator", supported_signatures=Union[State, str, Any, type(None)])
    def _set_separator(self, value):
        self._separator = value

    def _get_separator(self):
        return self._separator.value if isinstance(self._separator, State) else self._separator

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value or {}

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value or {}

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.breadcrumbs", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx
    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))

        self._children = self.insert_between_elements(self._children)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.layout().setContentsMargins(0,0,0,0)
        
        if isinstance(self._children, list):
            for index, widget in enumerate(self._children, 0):
                if index != len(self._children) - 1:
                    widget.setParent(self)
                    widget.setCursor(Qt.PointingHandCursor)
                self.layout().addWidget(widget)
                
        self.layout().addWidget(HSpacer())
        
    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

        PyBreadcrumbs_root = component_styled[f"PyBreadcrumbs"].get("styles")["root"]
        PyBreadcrumbs_root_qss = get_qss_style(PyBreadcrumbs_root)

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

        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyBreadcrumbs_root_qss}
                }}

                {sx_qss}

            """
        )

    def insert_between_elements(self, lst):
        result = [elem for i in range(len(lst)) for elem in (lst[i], PySvgWidget(key="iconoir:slash") if self._separator == None else self._separator() if callable(self._separator) else None)][:-1]
        return result