import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QSizePolicy

from qtmui.hooks import State, useEffect
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.utils.validate_params import _validate_param
from qtmui.material.widget_base import PyWidgetBase
from qtmui.configs import LOAD_WIDGET_ASYNC

class List(QFrame, PyWidgetBase):
    """
    A component that renders a list of items, styled like Material-UI List.

    The `List` component is used to group and display a collection of items, with support for
    subheaders, dense layouts, and customizable padding and styles.

    Parameters
    ----------
    ariaLabelledby : State or str, optional
        The ID of the element that labels the list for accessibility. Default is None.
        Can be a `State` object for dynamic updates.
    children : State, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the list (widgets, text, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or str, optional
        The component used for the root node (e.g., "QFrame"). Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    dense : State or bool, optional
        If True, uses compact vertical padding for keyboard/mouse input. Default is False.
        Can be a `State` object for dynamic updates.
    disablePadding : State or bool, optional
        If True, removes vertical padding from the list. Default is False.
        Can be a `State` object for dynamic updates.
    subheader : State or QWidget, optional
        The content of the subheader (e.g., ListSubheader). Default is None.
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
    - The `children` prop supports widgets, text (rendered as Typography), or lists of widgets/text.
    - The `dense` prop affects child components via context, reducing spacing and margins.

    Demos:
    - List: https://qtmui.com/material-ui/qtmui-list/

    API Reference:
    - List API: https://qtmui.com/material-ui/api/list/
    """

    def __init__(
        self,
        ariaLabelledby: Optional[Union[State, str, Callable]] = None,
        children: Optional[Union[State, QWidget, List[Union[QWidget, str]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, str]] = None,
        dense: Union[State, bool] = False,
        disablePadding: Union[State, bool] = False,
        subheader: Optional[Union[State, QWidget]] = None,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(f"List-{str(uuid.uuid4())}")
        PyWidgetBase._setUpUi(self)

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_ariaLabelledby(ariaLabelledby)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_dense(dense)
        self._set_disablePadding(disablePadding)
        self._set_subheader(subheader)
        self._set_sx(sx)

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.list", param_name="ariaLabelledby", supported_signatures=Union[State, Callable, str, type(None)])
    def _set_ariaLabelledby(self, value):
        """Assign value to ariaLabelledby."""
        self._ariaLabelledby = value

    def _get_ariaLabelledby(self):
        """Get the ariaLabelledby value."""
        return self._ariaLabelledby.value if isinstance(self._ariaLabelledby, State) else self._ariaLabelledby

    @_validate_param(file_path="qtmui.material.list", param_name="children", supported_signatures=Union[State, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.list", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.list", param_name="component", supported_signatures=Union[State, str, type(None)])
    def _set_component(self, value):
        """Assign value to component."""
        self._component = value

    def _get_component(self):
        """Get the component value."""
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.list", param_name="dense", supported_signatures=Union[State, bool])
    def _set_dense(self, value):
        """Assign value to dense."""
        self._dense = value

    def _get_dense(self):
        """Get the dense value."""
        return self._dense.value if isinstance(self._dense, State) else self._dense

    @_validate_param(file_path="qtmui.material.list", param_name="disablePadding", supported_signatures=Union[State, bool])
    def _set_disablePadding(self, value):
        """Assign value to disablePadding."""
        self._disablePadding = value

    def _get_disablePadding(self):
        """Get the disablePadding value."""
        return self._disablePadding.value if isinstance(self._disablePadding, State) else self._disablePadding

    @_validate_param(file_path="qtmui.material.list", param_name="subheader", supported_signatures=Union[State, QWidget, type(None)])
    def _set_subheader(self, value):
        """Assign value to subheader."""
        self._subheader = value
        if isinstance(value, QWidget):
            self._widget_references.append(value)

    def _get_subheader(self):
        """Get the subheader value."""
        return self._subheader.value if isinstance(self._subheader, State) else self._subheader

    @_validate_param(file_path="qtmui.material.list", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)


        # Nếu prop `disablePadding` được đặt thành True, xóa padding
        if self._disablePadding:
            self._layout.setSpacing(0)

        # Nếu prop `dense` được đặt thành True, sử dụng padding nhỏ hơn
        elif self._dense:
            self._layout.setSpacing(3)  # Padding nhỏ hơn so với mặc định

        # Thêm các children (nếu có)
        if self._children:
            if isinstance(self._children, list):
                if isinstance(self._subheader, QWidget):
                    self._children.insert(0, self._subheader)
                
                for index, widget in enumerate(self._children):
                    if LOAD_WIDGET_ASYNC:
                        self._do_task_async(lambda index=index, widget=widget: self._layout.insertWidget(index, widget))
                    else:
                        self._layout.insertWidget(index, widget)
                
        self.theme = useTheme()
        
        useEffect(
            self._set_stylesheet,
            [self.theme.state]
        )
        
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
                List {{
                    {sx_qss}
                }}
            """
        )