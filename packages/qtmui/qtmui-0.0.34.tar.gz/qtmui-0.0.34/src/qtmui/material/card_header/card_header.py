import uuid
from typing import Optional, Union, Callable, Any, Dict, List
from PySide6.QtWidgets import QHBoxLayout, QFrame, QSizePolicy, QVBoxLayout, QWidget
from qtmui.hooks import State, useEffect
from ..typography import Typography
from ..box import Box
from ..spacer import HSpacer, VSpacer
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.i18n.use_translation import translate, i18n
from ..utils.validate_params import _validate_param

class CardHeader(QFrame):
    """
    A component that displays a header for a card, including avatar, title, subheader, and action.

    The `CardHeader` component is used to render a header section within a card, typically
    containing an avatar, title, subheader, and optional action button. It supports all props
    of the Material-UI `CardHeader` component, as well as additional props for custom children.
    Props of the native component are supported via `**kwargs`.

    Parameters
    ----------
    action : State, Any, or None, optional
        The action to display in the card header (e.g., button or icon). Default is None.
        Can be a `State` object for dynamic updates.
    avatar : State, Any, or None, optional
        The avatar element to display (e.g., Avatar component). Default is None.
        Can be a `State` object for dynamic updates.
    children : State, Any, List[Any], or None, optional
        Custom content of the component, used if title and subheader are not provided.
        Default is None. Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    disableTypography : State or bool, optional
        If True, title and subheader are not wrapped by Typography components.
        Default is False. Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (action, avatar, content, root, subheader, title).
        Default is None. Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (action, avatar, content, root, subheader, title).
        Default is None. Can be a `State` object for dynamic updates.
    subheader : State, Any, or None, optional
        The content of the subheader. Default is None.
        Can be a `State` object for dynamic updates.
    subheaderTypographyProps : State or dict, optional
        Props forwarded to the subheader Typography (if not disableTypography).
        Deprecated; use slotProps.subheader instead. Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    title : State, Any, or None, optional
        The content of the title. Default is None.
        Can be a `State` object for dynamic updates.
    titleTypographyProps : State or dict, optional
        Props forwarded to the title Typography (if not disableTypography).
        Deprecated; use slotProps.title instead. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QWidget` class, supporting
        props of the native component (e.g., style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `children` prop is specific to this implementation and not part of Material-UI `CardHeader`.
    - The `subheaderTypographyProps` and `titleTypographyProps` are deprecated; use `slotProps.subheader`
      and `slotProps.title` instead.
    - If `disableTypography` is True, `title` and `subheader` are rendered directly without Typography wrappers.

    Demos:
    - CardHeader: https://qtmui.com/material-ui/qtmui-card-header/

    API Reference:
    - CardHeader API: https://qtmui.com/material-ui/api/card-header/
    """

    def __init__(
        self,
        action: Optional[Union[State, Any]] = None,
        avatar: Optional[Union[State, Any]] = None,
        children: Optional[Union[State, Any, List[Any]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, Any]] = None,
        disableTypography: Union[State, bool] = False,
        slotProps: Optional[Union[State, Dict]] = None,
        slots: Optional[Union[State, Dict]] = None,
        subheader: Optional[Union[State, Any]] = None,
        subheaderTypographyProps: Optional[Union[State, Dict]] = None,
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        title: Optional[Union[State, str, Callable]] = None,
        titleTypographyProps: Optional[Union[State, Dict]] = None,
        **kwargs
    ):
        super().__init__()
        self.setObjectName(str(id(self)))

        # Set properties with validation
        self._set_action(action)
        self._set_avatar(avatar)
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_disableTypography(disableTypography)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_subheader(subheader)
        self._set_subheaderTypographyProps(subheaderTypographyProps)
        self._set_sx(sx)
        self._set_title(title)
        self._set_titleTypographyProps(titleTypographyProps)

        self._init_ui()

    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.card_header", param_name="action", supported_signatures=Union[State, Any, type(None)])
    def _set_action(self, value):
        self._action = value

    def _get_action(self):
        return self._action.value if isinstance(self._action, State) else self._action

    # @_validate_param(file_path="qtmui.material.card_header", param_name="avatar", supported_signatures=Union[State, Any, type(None)])
    def _set_avatar(self, value):
        self._avatar = value

    def _get_avatar(self):
        return self._avatar.value if isinstance(self._avatar, State) else self._avatar

    # @_validate_param(file_path="qtmui.material.card_header", param_name="children", supported_signatures=Union[State, Any, List[Any], type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.card_header", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.card_header", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.card_header", param_name="disableTypography", supported_signatures=Union[State, bool])
    def _set_disableTypography(self, value):
        self._disableTypography = value

    def _get_disableTypography(self):
        return self._disableTypography.value if isinstance(self._disableTypography, State) else self._disableTypography

    @_validate_param(file_path="qtmui.material.card_header", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value or {}

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.card_header", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value or {}

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    # @_validate_param(file_path="qtmui.material.card_header", param_name="subheader", supported_signatures=Union[State, Any, type(None)])
    def _set_subheader(self, value):
        self._subheader = value

    def _get_subheader(self):
        return self._subheader.value if isinstance(self._subheader, State) else self._subheader

    @_validate_param(file_path="qtmui.material.card_header", param_name="subheaderTypographyProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_subheaderTypographyProps(self, value):
        self._subheaderTypographyProps = value

    def _get_subheaderTypographyProps(self):
        return self._subheaderTypographyProps.value if isinstance(self._subheaderTypographyProps, State) else self._subheaderTypographyProps

    @_validate_param(file_path="qtmui.material.card_header", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.card_header", param_name="title", supported_signatures=Union[State, Any, type(None)])
    def _set_title(self, value):
        self._title = value

    def _get_title(self):
        return self._title.value if isinstance(self._title, State) else self._title

    @_validate_param(file_path="qtmui.material.card_header", param_name="titleTypographyProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_titleTypographyProps(self, value):
        self._titleTypographyProps = value

    def _get_titleTypographyProps(self):
        return self._titleTypographyProps.value if isinstance(self._titleTypographyProps, State) else self._titleTypographyProps

        
    def _init_ui(self):

        self._lbl_subheader = None

        # self.setObjectName("PyCardHeader")

        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        if self._avatar:
            self.layout().addWidget(self._avatar)

        if self._title:
            self._lbl_title = Typography(text=self._title, variant="subtitle2")
            
        if self._subheader:
            self._lbl_subheader = Typography(text=self._subheader, variant="body2")

        if self._title:
            if self._subheader:
                self.layout().addWidget(
                    Box(
                        children=[
                            self._lbl_title,
                            VSpacer(),
                            self._lbl_subheader,
                        ]
                    )
                )
            else:
                self.layout().addWidget(
                    Box(
                        children=[
                            VSpacer(),
                            self._lbl_title,
                            VSpacer(),
                        ]
                    )
                )
        elif self._children:
            for widget in self._children:
                self.layout().addWidget(widget)

        if self._action:
            if isinstance(self._action, QWidget):
                self.layout().addWidget(HSpacer())
                self.layout().addWidget(self._action)


        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

        i18n.langChanged.connect(self.retranslateUi)
        self.retranslateUi()

    def retranslateUi(self):
        if hasattr(self, "_lbl_title"):
            if isinstance(self._title, State):
                if isinstance(self._title.value, Callable):
                    self._lbl_title.setText(translate(self._title))
                else:
                    self._lbl_title.setText(self._title.value)
            else:
                if isinstance(self._title, Callable):
                    self._lbl_title.setText(translate(self._title))
                else:
                    if isinstance(self._title, str):
                        self._lbl_title.setText(self._title)
                    elif isinstance(self._title, QWidget):
                        self._lbl_title.setLayout(QVBoxLayout())
                        self._lbl_title.layout().addWidget(Typography(text=self._title))

        if hasattr(self, "_lbl_subheader"):
            if isinstance(self._subheader, State):
                if isinstance(self._subheader.value, Callable):
                    self._lbl_subheader.setText(translate(self._subheader.value))
                else:
                    if self._lbl_subheader:
                        self._lbl_subheader.setText(self._subheader.value)
            else:
                if isinstance(self._subheader, Callable):
                    self._lbl_subheader.setText(translate(self._subheader))
                elif isinstance(self._subheader, QWidget):
                    self._lbl_subheader.setLayout(QHBoxLayout())
                    self._lbl_subheader.layout().setContentsMargins(0,0,0,0)
                    self._lbl_subheader.layout().addWidget(self._subheader)
                else:
                    if self._lbl_subheader:
                        self._lbl_subheader.setText(self._subheader)
                

    def _set_stylesheet(self):
        theme = useTheme()
        component_styles = theme.components

        PyCardHeader_root = component_styles[f"PyCardHeader"].get("styles")["root"]
        PyCardHeader_root_qss = get_qss_style(PyCardHeader_root)

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
                
        
        stylesheet = f"""
                #{self.objectName()} {{
                    {PyCardHeader_root_qss}
                    {sx_qss}
                }}
            """
            
        self.setStyleSheet(stylesheet)