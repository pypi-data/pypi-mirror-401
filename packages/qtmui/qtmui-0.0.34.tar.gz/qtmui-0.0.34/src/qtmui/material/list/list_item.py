import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from ..typography import Typography
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class ListItem(QFrame):
    """
    A component that renders a single item in a list, styled like Material-UI ListItem.

    The `ListItem` component is used to display a single item within a List, with support for
    secondary actions, dense layouts, dividers, and customizable alignment and padding.

    Parameters
    ----------
    key : State or str, optional
        The key for the list item, used for identification in lists. Default is None.
        Can be a `State` object for dynamic updates.
    alignItems : State or str, optional
        Defines the align-items style property ("center", "flex-start"). Default is "center".
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the list item (widgets, text, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "QFrame"). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    components : State or dict, optional
        The components used for each slot inside (deprecated). Default is {}.
        Can be a `State` object for dynamic updates.
    componentsProps : State or dict, optional
        Extra props for slot components (deprecated). Default is {}.
        Can be a `State` object for dynamic updates.
    ContainerComponent : State or str, optional
        The container component used when secondaryAction is the last child (deprecated). Default is "li".
        Can be a `State` object for dynamic updates.
    ContainerProps : State or dict, optional
        Props applied to the container component (deprecated). Default is {}.
        Can be a `State` object for dynamic updates.
    dense : State or bool, optional
        If True, uses compact vertical padding. Default is False (inherits from parent List).
        Can be a `State` object for dynamic updates.
    disableGutters : State or bool, optional
        If True, removes left and right padding. Default is False.
        Can be a `State` object for dynamic updates.
    disablePadding : State or bool, optional
        If True, removes all padding. Default is False.
        Can be a `State` object for dynamic updates.
    divider : State or bool, optional
        If True, adds a 1px light border to the bottom. Default is False.
        Can be a `State` object for dynamic updates.
    secondaryAction : State, QWidget, List[QWidget], or None, optional
        The element to display at the end of the list item. Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Extra props for slot components. Default is {}.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        The components used for each slot inside. Default is {}.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Attributes
    ----------
    VALID_ALIGN_ITEMS : list[str]
        Valid values for `alignItems`: ["center", "flex-start"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop supports widgets, text (rendered as Typography), or lists of widgets/text.
    - The `dense` prop defaults to the value inherited from the parent List component.
    - The `components`, `componentsProps`, `ContainerComponent`, and `ContainerProps` props are deprecated
      and will be removed in a future major release. Use `slots` and `slotProps` instead.

    Demos:
    - ListItem: https://qtmui.com/material-ui/qtmui-listitem/

    API Reference:
    - ListItem API: https://qtmui.com/material-ui/api/list-item/
    """

    VALID_ALIGN_ITEMS = ["center", "flex-start"]

    def __init__(
        self,
        key: Optional[Union[State, str]] = None,
        alignItems: Union[State, str] = "center",
        children: Optional[Union[State, QWidget, List[Union[QWidget, str]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, str]] = None,
        components: Optional[Union[State, Dict]] = None,
        componentsProps: Optional[Union[State, Dict]] = None,
        ContainerComponent: Optional[Union[State, str]] = "li",
        ContainerProps: Optional[Union[State, Dict]] = None,
        dense: Union[State, bool] = False,
        disableGutters: Union[State, bool] = False,
        disablePadding: Union[State, bool] = False,
        divider: Union[State, bool] = False,
        secondaryAction: Optional[Union[State, QWidget, List[QWidget]]] = None,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"ListItem-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_key(key)
        self._set_alignItems(alignItems)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_components(components or {})
        self._set_componentsProps(componentsProps or {})
        self._set_ContainerComponent(ContainerComponent)
        self._set_ContainerProps(ContainerProps or {})
        self._set_dense(dense)
        self._set_disableGutters(disableGutters)
        self._set_disablePadding(disablePadding)
        self._set_divider(divider)
        self._set_secondaryAction(secondaryAction)
        self._set_slotProps(slotProps or {})
        self._set_slots(slots or {})
        self._set_sx(sx)

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.listitem", param_name="key", supported_signatures=Union[State, str, type(None)])
    def _set_key(self, value):
        """Assign value to key."""
        self._key = value

    def _get_key(self):
        """Get the key value."""
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.listitem", param_name="alignItems", supported_signatures=Union[State, str], valid_values=VALID_ALIGN_ITEMS)
    def _set_alignItems(self, value):
        """Assign value to alignItems."""
        self._alignItems = value

    def _get_alignItems(self):
        """Get the alignItems value."""
        return self._alignItems.value if isinstance(self._alignItems, State) else self._alignItems

    @_validate_param(file_path="qtmui.material.listitem", param_name="children", supported_signatures=Union[State, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.listitem", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.listitem", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.listitem", param_name="components", supported_signatures=Union[State, Dict, type(None)])
    def _set_components(self, value):
        """Assign value to components."""
        self._components = value

    def _get_components(self):
        """Get the components value."""
        return self._components.value if isinstance(self._components, State) else self._components

    @_validate_param(file_path="qtmui.material.listitem", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_componentsProps(self, value):
        """Assign value to componentsProps."""
        self._componentsProps = value

    def _get_componentsProps(self):
        """Get the componentsProps value."""
        return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

    @_validate_param(file_path="qtmui.material.listitem", param_name="ContainerComponent", supported_signatures=Union[State, str, type(None)])
    def _set_ContainerComponent(self, value):
        """Assign value to ContainerComponent."""
        self._ContainerComponent = value

    def _get_ContainerComponent(self):
        """Get the ContainerComponent value."""
        return self._ContainerComponent.value if isinstance(self._ContainerComponent, State) else self._ContainerComponent

    @_validate_param(file_path="qtmui.material.listitem", param_name="ContainerProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_ContainerProps(self, value):
        """Assign value to ContainerProps."""
        self._ContainerProps = value

    def _get_ContainerProps(self):
        """Get the ContainerProps value."""
        return self._ContainerProps.value if isinstance(self._ContainerProps, State) else self._ContainerProps

    @_validate_param(file_path="qtmui.material.listitem", param_name="dense", supported_signatures=Union[State, bool])
    def _set_dense(self, value):
        """Assign value to dense."""
        self._dense = value

    def _get_dense(self):
        """Get the dense value."""
        return self._dense.value if isinstance(self._dense, State) else self._dense

    @_validate_param(file_path="qtmui.material.listitem", param_name="disableGutters", supported_signatures=Union[State, bool])
    def _set_disableGutters(self, value):
        """Assign value to disableGutters."""
        self._disableGutters = value

    def _get_disableGutters(self):
        """Get the disableGutters value."""
        return self._disableGutters.value if isinstance(self._disableGutters, State) else self._disableGutters

    @_validate_param(file_path="qtmui.material.listitem", param_name="disablePadding", supported_signatures=Union[State, bool])
    def _set_disablePadding(self, value):
        """Assign value to disablePadding."""
        self._disablePadding = value

    def _get_disablePadding(self):
        """Get the disablePadding value."""
        return self._disablePadding.value if isinstance(self._disablePadding, State) else self._disablePadding

    @_validate_param(file_path="qtmui.material.listitem", param_name="divider", supported_signatures=Union[State, bool])
    def _set_divider(self, value):
        """Assign value to divider."""
        self._divider = value

    def _get_divider(self):
        """Get the divider value."""
        return self._divider.value if isinstance(self._divider, State) else self._divider

    @_validate_param(file_path="qtmui.material.listitem", param_name="secondaryAction", supported_signatures=Union[State, QWidget, List, type(None)])
    def _set_secondaryAction(self, value):
        """Assign value to secondaryAction and store references."""
        self._secondaryAction = value

    def _get_secondaryAction(self):
        """Get the secondaryAction value."""
        return self._secondaryAction.value if isinstance(self._secondaryAction, State) else self._secondaryAction

    @_validate_param(file_path="qtmui.material.listitem", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.listitem", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.listitem", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx


    def _init_ui(self):
        # Thiết lập layout chính cho List
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)  # Bỏ các lề mặc định
        self.setLayout(self._layout)
        # self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        # self.setStyleSheet('background: green;')

        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                for widget in self._children:
                    if isinstance(widget, QWidget):
                        self.layout().addWidget(widget)
            elif isinstance(self._children, QWidget):
                self.layout().addWidget(self._children)
            
        if self._secondaryAction:
            if isinstance(self._secondaryAction, list):
                for widget in self._secondaryAction:
                    if isinstance(widget, QWidget):
                        self.layout().addWidget(widget)
            elif isinstance(self._secondaryAction, QWidget):
                self.layout().addWidget(self._secondaryAction)
 
