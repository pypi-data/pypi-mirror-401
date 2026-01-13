import uuid
from typing import Optional, Union, Dict, List, Callable
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QGroupBox, QSizePolicy, QWidget
from PySide6.QtCore import Qt
from qtmui.hooks import State, useEffect
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from qtmui.material.styles import useTheme
from qtmui.i18n.use_translation import i18n
from qtmui.utils.translator import getTranslatedText
from ..typography import Typography
from ..utils.validate_params import _validate_param

class GroupBox(QGroupBox):
    """
    A component that groups content with a title, styled like a Material-UI container.

    The `GroupBox` component is a styled `QGroupBox` that supports Material-UI-like props for
    grouping content with a title, customizable styles, and accessibility features.

    Parameters
    ----------
    children : State, str, QWidget, List[Union[QWidget, str]], or None, optional
        The content of the component (text, widget, or list of widgets/text). Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, the content is disabled. Default is False.
        Can be a `State` object for dynamic updates.
    title : State or str, optional
        The title of the group box. Default is an empty string.
        Can be a `State` object for dynamic updates.
    sx : State, list, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QGroupBox` class,
        supporting props of the native component (e.g., parent, style, className).

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `parent`, `style`, `className`).
    - The `children` prop supports text (rendered as Typography), widgets, or lists of widgets/text.
    - The `disabled` prop applies to child widgets when set to True.

    Demos:
    - GroupBox: https://qtmui.com/material-ui/qtmui-groupbox/

    API Reference:
    - GroupBox API: https://qtmui.com/material-ui/api/groupbox/
    """

    def __init__(
        self,
        children: Optional[Union[State, str, QWidget, List[Union[QWidget, str]]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        disabled: Union[State, bool] = False,
        title: Optional[Union[str, State, Callable]] = '',
        sx: Optional[Union[State, List, Dict, Callable, str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(f"GroupBox-{str(uuid.uuid4())}")

        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_disabled(disabled)
        self._set_title(title)
        self._set_sx(sx)

        self._init_ui()


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.groupbox", param_name="children", supported_signatures=Union[State, str, QWidget, List, type(None)])
    def _set_children(self, value):
        """Assign value to children and store references."""
        self._children = value

    def _get_children(self):
        """Get the children value."""
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.groupbox", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        """Assign value to classes."""
        self._classes = value

    def _get_classes(self):
        """Get the classes value."""
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.groupbox", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        """Assign value to disabled."""
        self._disabled = value

    def _get_disabled(self):
        """Get the disabled value."""
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.groupbox", param_name="title", supported_signatures=Union[State, Callable, str])
    def _set_title(self, value):
        """Assign value to title."""
        self._title = value

    def _get_title(self):
        """Get the title value."""
        return self._title.value if isinstance(self._title, State) else self._title

    @_validate_param(file_path="qtmui.material.groupbox", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        """Assign value to sx."""
        self._sx = value

    def _get_sx(self):
        """Get the sx value."""
        return self._sx.value if isinstance(self._sx, State) else self._sx
    

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(9,27,9,9)
        self.layout().setAlignment(Qt.AlignTop)

        if isinstance(self._children, list):
            for item in self._children:
                self.layout().addWidget(item)

        i18n.langChanged.connect(self.reTranslation)
        self.reTranslation()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def reTranslation(self):
        if self._title:
            self.setTitle(getTranslatedText(self._title))

    def _set_stylesheet(self):
        self.theme = useTheme()
        PyGroupBox_styles = self.theme.components["PyGroupBox"].get("styles")
        PyGroupBox_styles_root_qss = get_qss_style(PyGroupBox_styles["root"])
        PyGroupBox_styles_title_qss = get_qss_style(PyGroupBox_styles["title"])

        stylesheet = f"""
            #{self.objectName()}  {{
                {PyGroupBox_styles_root_qss}
            }}

            #{self.objectName()}::hover  {{
                border: 1px solid black;
            }}

            #{self.objectName()}::title  {{
                {PyGroupBox_styles_title_qss}
            }}
        """
        # print('stylesheet__________', stylesheet)
        self.setStyleSheet(stylesheet)

