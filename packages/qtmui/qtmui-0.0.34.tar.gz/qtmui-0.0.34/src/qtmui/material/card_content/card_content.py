import uuid
from typing import Optional, Union, Callable, Any, List, Dict

from qtmui.hooks import State, useEffect
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QLabel
from PySide6.QtCore import Qt

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.i18n.use_translation import translate, i18n
from ..utils.validate_params import _validate_param

class CardContent(QFrame):
    """
    A component that displays content within a card, typically used as a child of Card.

    The `CardContent` component is used to render content inside a card with customizable
    layout direction, height, and text. It supports all props of the Material-UI `CardContent`
    component, as well as additional props for variant, direction, height, and text. Props of
    the native component are supported via `**kwargs`.

    Parameters
    ----------
    children : State, Any, List[Any], or None, optional
        The content of the component, either a single widget or a list of widgets.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Custom variant of the component (e.g., "main"). Default is "main".
        Can be a `State` object for dynamic updates.
    direction : State or str, optional
        Direction of the layout ("column" or "row"). Default is "column".
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    height : State or int, optional
        Fixed height of the component in pixels. Default is None.
        Can be a `State` object for dynamic updates.
    text : State, str, Callable, or None, optional
        Text content to display, rendered as a QLabel. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        props of the native component (e.g., style, className).

    Attributes
    ----------
    VALID_DIRECTIONS : list[str]
        Valid values for the `direction` parameter: ["column", "row"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `variant`, `direction`, `height`, and `text` props are specific to this implementation
      and not part of Material-UI `CardContent`.
    - If both `children` and `text` are provided, both are rendered, with `text` as a QLabel.

    Demos:
    - CardContent: https://qtmui.com/material-ui/qtmui-card-content/

    API Reference:
    - CardContent API: https://qtmui.com/material-ui/api/card-content/
    """

    VALID_DIRECTIONS = ["column", "row"]

    def __init__(
        self,
        children: Optional[Union[State, Any, List[Any]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, Any]] = None,
        variant: Union[State, str] = "main",
        direction: Union[State, str] = "column",
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        height: Optional[Union[State, int]] = None,
        text: Optional[Union[State, str, Callable]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(str(uuid.uuid4()))

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_variant(variant)
        self._set_direction(direction)
        self._set_sx(sx)
        self._set_height(height)
        self._set_text(text)

        self._init_ui()


    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.card_content", param_name="children", supported_signatures=Union[State, Any, List[Any], type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.card_content", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.card_content", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.card_content", param_name="variant", supported_signatures=Union[State, str])
    def _set_variant(self, value):
        self._variant = value

    def _get_variant(self):
        return self._variant.value if isinstance(self._variant, State) else self._variant

    @_validate_param(file_path="qtmui.material.card_content", param_name="direction", supported_signatures=Union[State, str], valid_values=VALID_DIRECTIONS)
    def _set_direction(self, value):
        self._direction = value

    def _get_direction(self):
        return self._direction.value if isinstance(self._direction, State) else self._direction

    @_validate_param(file_path="qtmui.material.card_content", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.card_content", param_name="height", supported_signatures=Union[State, int, type(None)])
    def _set_height(self, value):
        if value is not None and value < 0:
            raise ValueError("height must be non-negative")
        self._height = value

    def _get_height(self):
        return self._height.value if isinstance(self._height, State) else self._height

    @_validate_param(file_path="qtmui.material.card_content", param_name="text", supported_signatures=Union[State, str, Callable, type(None)])
    def _set_text(self, value):
        self._text = value

    def _get_text(self):
        return self._text.value if isinstance(self._text, State) else self._text

        self._init_ui()
    
    def _init_ui(self):
        # self.setObjectName("PyCardContent")
        self.setObjectName(str(uuid.uuid4()))

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        if self._direction == "column":
            self.setLayout(QVBoxLayout())
            self.layout().setAlignment(Qt.AlignTop)
        else:
            self.setLayout(QHBoxLayout())
            self.layout().setAlignment(Qt.AlignLeft)

        if self._children:
            if isinstance(self._children, list) and len(self._children) > 0:
                for item in self._children:
                    self.layout().addWidget(item)
        elif self._text:
            self._lbl_text_content = QLabel()
            self.layout().addWidget(self._lbl_text_content)

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

    def retranslateUi(self):
        if hasattr(self, "_lbl_text_content"):
            if isinstance(self._text, Callable):
                self._lbl_text_content.setText(translate(self._text))
            else:
                self._lbl_text_content.setText(self._text)


    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyCardContent_root = component_styles[f"PyCardContent"].get("styles")["root"]
        PyCardContent_root_qss = get_qss_style(PyCardContent_root)

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
                #{self.objectName()} {{
                    {PyCardContent_root_qss}
                    {sx_qss}
                }}
            """
        )


