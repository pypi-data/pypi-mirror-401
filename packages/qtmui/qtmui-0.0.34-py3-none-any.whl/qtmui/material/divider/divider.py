from typing import Optional, Union, Dict, Callable, List
import uuid

from ..system.color_manipulator import alpha
from PySide6.QtWidgets import QFrame, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..widget_base import PyWidgetBase
from ..utils.validate_params import _validate_param

class Divider(QFrame, PyWidgetBase):
    """
    A component that renders a divider line, either horizontal or vertical.

    The `Divider` component is used to separate content, supporting all props of the
    Material-UI `Divider` component, as well as additional custom props.

    Parameters
    ----------
    absolute : State or bool, optional
        If True, absolutely positions the divider. Default is False.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically text or sub-components. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, str, or None, optional
        The component used for the root node (e.g., "QFrame"). Default is None.
        Can be a `State` object for dynamic updates.
    flexItem : State or bool, optional
        If True, adjusts height for vertical dividers in flex containers. Default is False.
        Can be a `State` object for dynamic updates.
    light : State or bool, optional
        If True, uses a lighter color. Default is False.
        Deprecated: Use `sx={{ opacity: 0.6 }}` instead.
        Can be a `State` object for dynamic updates.
    orientation : State or str, optional
        The divider orientation ("horizontal" or "vertical"). Default is "horizontal".
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    textAlign : State, str, or None, optional
        Text alignment when children are present ("center", "left", "right"). Default is "center".
        Can be a `State` object for dynamic updates.
    variant : State, str, or None, optional
        The divider variant ("fullWidth", "inset", "middle"). Default is "fullWidth".
        Can be a `State` object for dynamic updates.
    color : State, str, or None, optional
        Background color of the divider (custom feature, not part of Material-UI). Default is None.
        Can be a `State` object for dynamic updates.
    height : State or int, optional
        Fixed height for horizontal dividers (custom feature, not part of Material-UI). Default is 1.
        Can be a `State` object for dynamic updates.
    width : State or int, optional
        Fixed width for vertical dividers (custom feature, not part of Material-UI). Default is 1.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_ORIENTATION : list[str]
        Valid values for `orientation`: ["horizontal", "vertical"].
    VALID_TEXT_ALIGN : list[str]
        Valid values for `textAlign`: ["center", "left", "right"].
    VALID_VARIANT : list[str]
        Valid values for `variant`: ["fullWidth", "inset", "middle"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `color`, `height`, and `width` parameters are custom features, not part of Material-UI's `Divider`.
    - The `light` prop is deprecated; use `sx={{ opacity: 0.6 }}` for similar effects.
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - Divider: https://qtmui.com/material-ui/qtmui-divider/

    API Reference:
    - Divider API: https://qtmui.com/material-ui/api/divider/
    """

    VALID_ORIENTATION = ["horizontal", "vertical"]
    VALID_TEXT_ALIGN = ["center", "left", "right"]
    VALID_VARIANT = ["fullWidth", "inset", "middle"]

    def __init__(
        self,
        absolute: Union[State, bool] = False,
        children: Optional[Union[State, QWidget, List[QWidget]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, str]] = None,
        flexItem: Union[State, bool] = False,
        light: Union[State, bool] = False,
        orientation: Union[State, str] = "horizontal",
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        textAlign: Optional[Union[State, str]] = "center",
        variant: Optional[Union[State, str]] = "fullWidth",
        color: Optional[Union[State, str]] = None,
        height: Union[State, int] = 1,
        width: Union[State, int] = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(str(uuid.uuid4()))

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_absolute(absolute)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_flexItem(flexItem)
        self._set_light(light)
        self._set_orientation(orientation)
        self._set_sx(sx)
        self._set_textAlign(textAlign)
        self._set_variant(variant)
        self._set_color(color)
        self._set_height(height)
        self._set_width(width)

        # Setup UI
        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.divider", param_name="absolute", supported_signatures=Union[State, bool])
    def _set_absolute(self, value):
        """Assign value to absolute."""
        self._absolute = value

    def _get_absolute(self):
        """Get the absolute value."""
        return self._absolute.value if isinstance(self._absolute, State) else self._absolute

    # @_validate_param(file_path="qtmui.material.divider", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children and store widget references."""
        self._widget_references.clear()
        self._children = value
        children = self._get_children()

        if isinstance(children, QWidget):
            self._widget_references.append(children)
            children.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        elif isinstance(children, list):
            for child in children:
                if child is None:
                    continue
                if isinstance(child, QWidget):
                    self._widget_references.append(child)
                    child.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                else:
                    raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
        elif children is not None:
            raise TypeError(f"children must be a State, QWidget, or list of QWidgets, but got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.divider", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.divider", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.divider", param_name="flexItem", supported_signatures=Union[State, bool])
    def _set_flexItem(self, value):
        """Assign value to flexItem."""
        self._flexItem = value

    def _get_flexItem(self):
        """Get the flexItem value."""
        return self._flexItem.value if isinstance(self._flexItem, State) else self._flexItem

    @_validate_param(file_path="qtmui.material.divider", param_name="light", supported_signatures=Union[State, bool])
    def _set_light(self, value):
        """Assign value to light."""
        self._light = value

    def _get_light(self):
        """Get the light value."""
        return self._light.value if isinstance(self._light, State) else self._light

    @_validate_param(file_path="qtmui.material.divider", param_name="orientation", supported_signatures=Union[State, str], valid_values=VALID_ORIENTATION)
    def _set_orientation(self, value):
        """Assign value to orientation."""
        self._orientation = value

    def _get_orientation(self):
        """Get the orientation value."""
        return self._orientation.value if isinstance(self._orientation, State) else self._orientation

    @_validate_param(file_path="qtmui.material.divider", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.divider", param_name="textAlign", supported_signatures=Union[State, str, type(None)], valid_values=VALID_TEXT_ALIGN)
    def _set_textAlign(self, value):
        """Assign value to textAlign."""
        self._textAlign = value

    def _get_textAlign(self):
        """Get the textAlign value."""
        return self._textAlign.value if isinstance(self._textAlign, State) else self._textAlign

    @_validate_param(file_path="qtmui.material.divider", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANT)
    def _set_variant(self, value):
        """Assign value to variant."""
        self._variant = value

    def _get_variant(self):
        """Get the variant value."""
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.divider", param_name="color", supported_signatures=Union[State, str, type(None)])
    def _set_color(self, value):
        """Assign value to color (custom feature)."""
        self._color = value

    def _get_color(self):
        """Get the color value."""
        return self._color.value if isinstance(self._color, State) else self._color

    @_validate_param(file_path="qtmui.material.divider", param_name="height", supported_signatures=Union[State, int])
    def _set_height(self, value):
        """Assign value to height (custom feature)."""
        self._height = value

    def _get_height(self):
        """Get the height value."""
        return self._height.value if isinstance(self._height, State) else self._height

    @_validate_param(file_path="qtmui.material.divider", param_name="width", supported_signatures=Union[State, int])
    def _set_width(self, value):
        """Assign value to width (custom feature)."""
        self._width = value

    def _get_width(self):
        """Get the width value."""
        return self._width.value if isinstance(self._width, State) else self._width

    def _init_ui(self):

        # self.setFixedSize(QSize(5, 5))

        if self._color is not None:
            if isinstance(self._color, State):
                self._color.valueChanged.connect(self._set_stylesheet)
        else:
            self._color = alpha(self.theme.palette.grey._500, 0.24)

        self.slot_set_stylesheet()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def slot_set_stylesheet(self, value=None):
        self._set_stylesheet()


    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components

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

        width = ""
        height = ""
        if self._orientation == "horizontal":
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            height = f"""
                    min-height: 1px;
                    max-height: 1px;
                    """
        else:
            width = f"""
                    min-width: 1px;
                    max-width: 1px;
                    """  
            self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)

        stylesheet = f"""
            Divider {{
                {width}
                {height}
                background-color: {self._color};
            }}

            {sx_qss}

        """

        self.setStyleSheet(stylesheet)

