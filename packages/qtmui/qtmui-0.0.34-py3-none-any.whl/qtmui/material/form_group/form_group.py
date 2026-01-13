from typing import Optional, Union, Dict, Callable, List
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QWidget
from PySide6.QtCore import Qt
import uuid
from qtmui.hooks import State
from ...material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class FormGroup(QFrame):
    """
    A component that groups form controls like checkboxes or radios.

    The `FormGroup` component is used to group multiple form controls, supporting all
    props of the Material-UI `FormGroup` component.

    Parameters
    ----------
    children : State, QWidget, List[QWidget], or None, optional
        The content of the component, typically FormControlLabel or FormControl components.
        Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    row : State or bool, optional
        If True, displays the group in a compact row. Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `children` prop must be a `QWidget`, a list of `QWidget` instances, or a `State` object.

    Demos:
    - FormGroup: https://qtmui.com/material-ui/qtmui-formgroup/

    API Reference:
    - FormGroup API: https://qtmui.com/material-ui/api/form-group/
    """

    def __init__(
        self,
        children: Optional[Union[State, QWidget, List[QWidget], Callable]] = None,
        classes: Optional[Union[State, Dict]] = None,
        row: Union[State, bool] = False,
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"PyFormGroup-{str(uuid.uuid4())}")

        # Initialize theme
        self.theme = useTheme()

        # Store widget references to prevent Qt deletion
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_row(row)
        self._set_sx(sx)

        # Setup UI
        self._init_ui()


    # Setter and Getter methods
    # @_validate_param(file_path="qtmui.material.formgroup", param_name="children", supported_signatures=Union[State, QWidget, List[QWidget], type(None)])
    def _set_children(self, value):
        """Assign value to children and store widget references."""
        # self._widget_references.clear()
        self._children = value
        # children = self._get_children()

        # if isinstance(children, QWidget):
        #     self._widget_references.append(children)
        #     children.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # elif isinstance(children, list):
        #     for child in children:
        #         if child is None:
        #             continue
        #         if isinstance(child, QWidget):
        #             self._widget_references.append(child)
        #             child.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        #         else:
        #             raise TypeError(f"Each element in children must be a QWidget, but got {type(child)}")
        # elif children is not None:
        #     raise TypeError(f"children must be a State, QWidget, or list of QWidgets, but got {type(children)}")

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.formgroup", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.formgroup", param_name="row", supported_signatures=Union[State, bool])
    def _set_row(self, value):
        """Assign value to row."""
        self._row = value

    def _get_row(self):
        """Get the row value."""
        return self._row.value if isinstance(self._row, State) else self._row

    @_validate_param(file_path="qtmui.material.formgroup", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx


    def _init_ui(self):

        if self._row:
            self.setLayout(QHBoxLayout())
        else:
            self.setLayout(QVBoxLayout())

        # self.layout().setContentsMargins(0,0,0,0)
        # self.layout().setSpacing(0)

        if self._sx != None:
            self.setObjectName(str(uuid.uuid4()))
            self.setStyleSheet('''#{}  {{ {} }}'''.format(self.objectName(), self._sx)) # str multi line
            

        if isinstance(self._children, list) and len(self._children) > 0:
            for item in self._children:
                self.layout().addWidget(item)



