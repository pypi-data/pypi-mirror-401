import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.widget_base.widget_base import PyWidgetBase
from ..typography import Typography
from ..utils.validate_params import _validate_param
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class ListItemText(QFrame, PyWidgetBase):
    """
    A component that renders primary and secondary text within a ListItem, styled like Material-UI ListItemText.

    The `ListItemText` component is used to display primary and optional secondary text in a ListItem, with support
    for typography customization, indentation, and styling overrides.

    Parameters
    ----------
    children : State, str, QWidget, List[Union[str, QWidget]], or None, optional
        Alias for the `primary` prop. The main content element. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    disableTypography : State or bool, optional
        If True, the children won't be wrapped by a Typography component. Default is False.
        Can be a `State` object for dynamic updates.
    id : State or str, optional
        The identifier for the component. Default is None.
        Can be a `State` object for dynamic updates.
    inset : State or bool, optional
        If True, the children are indented. Default is False.
        Can be a `State` object for dynamic updates.
    onClick : State or Callable, optional
        Callback function triggered when the component is clicked. Default is None.
        Can be a `State` object for dynamic updates.
    primary : State, str, QWidget, List[Union[str, QWidget]], or None, optional
        The main content element. Default is None.
        Can be a `State` object for dynamic updates.
    primaryTypographyProps : State or dict, optional
        Props forwarded to the primary Typography component (if `disableTypography` is False). Default is None.
        Deprecated: Use `slotProps.primary` instead.
        Can be a `State` object for dynamic updates.
    secondary : State, str, QWidget, List[Union[str, QWidget]], or None, optional
        The secondary content element. Default is None.
        Can be a `State` object for dynamic updates.
    secondaryTypographyProps : State or dict, optional
        Props forwarded to the secondary Typography component (if `disableTypography` is False). Default is None.
        Deprecated: Use `slotProps.secondary` instead.
        Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (`primary`, `root`, `secondary`). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components used for each slot (`primary`, `root`, `secondary`). Default is None.
        Can be a `State` object for dynamic updates.
    spacing : State or int, optional
        The spacing between primary and secondary content. Default is 6.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class,
        supporting props of the native component (e.g., parent, style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop is an alias for `primary`. If both are provided, `primary` takes precedence.
    - The `primaryTypographyProps` and `secondaryTypographyProps` are deprecated; use `slotProps.primary` and `slotProps.secondary` instead.
    - The component uses a QVBoxLayout to stack primary and secondary content vertically.

    Demos:
    - ListItemText: https://qtmui.com/material-ui/qtmui-listitemtext/

    API Reference:
    - ListItemText API: https://qtmui.com/material-ui/api/list-item-text/
    """

    def __init__(
        self,
        children: Optional[Union[State, str, QWidget, List[Union[str, QWidget]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        disableTypography: Union[State, bool] = False,
        id: Optional[Union[State, str]] = None,
        inset: Union[State, bool] = False,
        onClick: Optional[Union[State, Callable]] = None,
        primary: Optional[Union[State, str, QWidget, List[Union[str, QWidget]]]] = None,
        primaryTypographyProps: Optional[Union[State, Dict]] = None,
        secondary: Optional[Union[State, str, QWidget, List[Union[str, QWidget]]]] = None,
        secondaryTypographyProps: Optional[Union[State, Dict]] = None,
        slotProps: Optional[Union[State, Dict[str, Union[Dict, Callable]]]] = None,
        slots: Optional[Union[State, Dict[str, str]]] = None,
        spacing: Union[State, int] = 6,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        PyWidgetBase._setUpUi(self)
        
        self.setObjectName(f"ListItemText-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_disableTypography(disableTypography)
        self._set_id(id)
        self._set_inset(inset)
        self._set_onClick(onClick)
        self._set_primary(primary or children)  # primary takes precedence, else use children
        self._set_primaryTypographyProps(primaryTypographyProps)
        self._set_secondary(secondary)
        self._set_secondaryTypographyProps(secondaryTypographyProps)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_spacing(spacing)
        self._set_sx(sx)

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.listitemtext", param_name="children", supported_signatures=Union[State, str, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="disableTypography", supported_signatures=Union[State, bool])
    def _set_disableTypography(self, value):
        """Assign value to disableTypography."""
        self._disableTypography = value

    def _get_disableTypography(self):
        """Get the disableTypography value."""
        return self._disableTypography.value if isinstance(self._disableTypography, State) else self._disableTypography

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="id", supported_signatures=Union[State, str, type(None)])
    def _set_id(self, value):
        """Assign value to id."""
        self._id = value

    def _get_id(self):
        """Get the id value."""
        return self._id.value if isinstance(self._id, State) else self._id

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="inset", supported_signatures=Union[State, bool])
    def _set_inset(self, value):
        """Assign value to inset."""
        self._inset = value

    def _get_inset(self):
        """Get the inset value."""
        return self._inset.value if isinstance(self._inset, State) else self._inset

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="onClick", supported_signatures=Union[State, Callable, type(None)])
    def _set_onClick(self, value):
        """Assign value to onClick."""
        self._onClick = value

    def _get_onClick(self):
        """Get the onClick value."""
        return self._onClick.value if isinstance(self._onClick, State) else self._onClick

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="primary", supported_signatures=Union[State, str, Callable, QWidget, List, type(None)])
    def _set_primary(self, value):
        """Assign value to primary and store references."""
        self._primary = value

    def _get_primary(self):
        """Get the primary value."""
        return self._primary.value if isinstance(self._primary, State) else self._primary

    def _get_primary_widgets(self):
        """Get the widgets in primary."""
        primary = self._get_primary()
        if isinstance(primary, list):
            return [item for item in primary if isinstance(item, QWidget)]
        elif isinstance(primary, QWidget):
            return [primary]
        return []

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="primaryTypographyProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_primaryTypographyProps(self, value):
        """Assign value to primaryTypographyProps."""
        self._primaryTypographyProps = value or {}

    def _get_primaryTypographyProps(self):
        """Get the primaryTypographyProps value."""
        return self._primaryTypographyProps.value if isinstance(self._primaryTypographyProps, State) else self._primaryTypographyProps

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="secondary", supported_signatures=Union[State, str, QWidget, List, type(None)])
    def _set_secondary(self, value):
        """Assign value to secondary and store references."""
        self._widget_references = [w for w in self._widget_references if w not in self._get_secondary_widgets()]
        self._secondary = value
        secondary = value.value if isinstance(value, State) else value

        if isinstance(secondary, list):
            for item in secondary:
                if isinstance(item, QWidget):
                    self._widget_references.append(item)
                elif not isinstance(item, (str, type(None))):
                    raise TypeError(f"Each element in secondary must be a str, QWidget, or None, got {type(item)}")
        elif isinstance(secondary, QWidget):
            self._widget_references.append(secondary)
        elif secondary is not None and not isinstance(secondary, str):
            raise TypeError(f"secondary must be a State, str, QWidget, list, or None, got {type(secondary)}")

    def _get_secondary(self):
        """Get the secondary value."""
        return self._secondary.value if isinstance(self._secondary, State) else self._secondary

    def _get_secondary_widgets(self):
        """Get the widgets in secondary."""
        secondary = self._get_secondary()
        if isinstance(secondary, list):
            return [item for item in secondary if isinstance(item, QWidget)]
        elif isinstance(secondary, QWidget):
            return [secondary]
        return []

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="secondaryTypographyProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_secondaryTypographyProps(self, value):
        """Assign value to secondaryTypographyProps."""
        self._secondaryTypographyProps = value or {}

    def _get_secondaryTypographyProps(self):
        """Get the secondaryTypographyProps value."""
        return self._secondaryTypographyProps.value if isinstance(self._secondaryTypographyProps, State) else self._secondaryTypographyProps

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        """Assign value to slotProps."""
        self._slotProps = value or {}

    def _get_slotProps(self):
        """Get the slotProps value."""
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        """Assign value to slots."""
        self._slots = value or {}

    def _get_slots(self):
        """Get the slots value."""
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="spacing", supported_signatures=Union[State, int])
    def _set_spacing(self, value):
        """Assign value to spacing."""
        self._spacing = value

    def _get_spacing(self):
        """Get the spacing value."""
        return self._spacing.value if isinstance(self._spacing, State) else self._spacing

    @_validate_param(file_path="qtmui.material.listitemtext", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx


    def _init_ui(self):

        # Tạo layout QVBoxLayout
        self._layout = QVBoxLayout(self)
        # self._layout.setContentsMargins(6, 0, 0, 0)
        self._layout.setSpacing(self._spacing)
        self.setLayout(self._layout)
        # self.layout().setAlignment(Qt.AlignCenter) # ra giữa theo chiều ngang và cả chiều dọc
        self.layout().setAlignment(Qt.AlignVCenter)  # căn giữa theo chiều dọc

        self.setAttribute(Qt.WA_TransparentForMouseEvents) # Điều này cho phép các sự kiện chuột (bao gồm hover) có thể đi qua và được lắng nghe bởi QPushButton.

        # Nếu có primary text, thêm nó vào layout
        if self._primary:
            primary_label = self._create_primary_label()
            self._layout.addWidget(primary_label)

        # Nếu có secondary text, thêm nó vào layout
        if self._secondary:
            secondary_label = self._create_secondary_label()
            self._layout.addWidget(secondary_label)

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()

    def _set_stylesheet(self, component_styles=None):
        theme = useTheme()

        if not component_styles:
            component_styles = theme.components
        
        sx_qss = ""
        if self._sx:
            if isinstance(self._sx, dict):
                sx_qss = get_qss_style(self._sx)
            elif isinstance(self._sx, Callable):
                sx = self._sx()
                if isinstance(sx, dict):
                    sx_qss = get_qss_style(sx)
                elif isinstance(sx, str):
                    sx_qss = sx
            elif isinstance(self._sx, str) and self._sx != "":
                sx_qss = self._sx

        self.setStyleSheet(
            f"""
                ListItemText {{
                    {sx_qss}
                }}
            """
        )

    def _create_primary_label(self):
        """Tạo label cho primary text"""
        if self._disableTypography:
            # Không sử dụng Typography
            
            primary_label = QLabel(self._primary)
        else:
            if self._primaryTypographyProps:
                primary_label = QFrame()
                primary_label.setLayout(QHBoxLayout())
                primary_label.layout().setContentsMargins(0,0,0,0)
                primary_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                if isinstance(self._primary, list):
                    for item in self._primary:
                        if isinstance(item, str):
                            text_item = Typography(text=item, **self._primaryTypographyProps)
                            primary_label.layout().addWidget(text_item)
                        elif isinstance(item, Callable):
                            text_item = Typography(text=item, **self._primaryTypographyProps)
                            primary_label.layout().addWidget(text_item)
                        elif isinstance(item, QWidget):
                            primary_label.layout().addWidget(item)
                else:
                    primary_label = Typography(text=self._primary, **self._primaryTypographyProps)
            else:
                primary_label = Typography(variant='subtitle2', text=self._primary, color='textPrimary')
        return primary_label

    def _create_secondary_label(self):
        """Tạo label cho secondary text"""
        # self.setMinimumHeight(48)

        if self._disableTypography:
            # Không sử dụng Typography
            secondary_label = QLabel(self._secondary)
        else:
            if self._secondaryTypographyProps:
                secondary_label = QFrame()
                secondary_label.setLayout(QHBoxLayout())
                secondary_label.layout().setContentsMargins(0,0,0,0)
                secondary_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                if isinstance(self._secondary, list):
                    for item in self._secondary:
                        # print('item___________', item)
                        if isinstance(item, str):
                            text_item = Typography(text=item,**self._secondaryTypographyProps)
                            secondary_label.layout().addWidget(text_item)
                        elif isinstance(item, Callable):
                            text_item = Typography(text=item,**self._secondaryTypographyProps)
                            secondary_label.layout().addWidget(text_item)
                        elif isinstance(item, QWidget):
                            secondary_label.layout().addWidget(item)
                else:
                    secondary_label = Typography(text=self._secondary, **self._secondaryTypographyProps)
            else:
                secondary_label = Typography(variant='caption', text=self._secondary, color='textSecondary')
        return secondary_label

    def _apply_sx(self, sx):
        """Áp dụng overrides styles từ sx"""
        if isinstance(sx, dict):
            for key, value in sx.items():
                self.setStyleSheet(f"{key}: {value};")
        elif callable(sx):
            sx(self)

    def _apply_classes(self, classes):
        """Áp dụng các class CSS từ classes"""
        if isinstance(classes, dict):
            styles = "; ".join([f"{k}: {v}" for k, v in classes.items()])
            self.setStyleSheet(styles)

    def mouseReleaseEvent(self, event):
        if self._onClick:
            self._onClick()
        return super().mouseReleaseEvent(event)