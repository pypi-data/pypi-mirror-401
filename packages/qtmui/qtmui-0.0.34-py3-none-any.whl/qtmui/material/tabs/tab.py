from typing import Dict, Optional, Union, List, Callable, Any

from qtmui.hooks import State
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from ..utils.validate_params import _validate_param
from qtmui.material.styles import useTheme

class Tab(QFrame):
    """
    A tab component, styled like Material-UI Tab.

    The `Tab` component displays a tab with a label, icon, and optional content, aligning with
    MUI Tab props. Inherits from ButtonBase props.

    Parameters
    ----------
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, disables the tab. Default is False.
        Can be a `State` object for dynamic updates.
    disableFocusRipple : State or bool, optional
        If True, disables keyboard focus ripple. Default is False.
        Can be a `State` object for dynamic updates.
    disableRipple : State or bool, optional
        If True, disables the ripple effect. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State, str, QWidget, or None, optional
        Icon to display. Default is None.
        Can be a `State` object for dynamic updates.
    iconPosition : State or str, optional
        Position of the icon relative to the label ('top', 'end', 'start', 'bottom').
        Default is 'top'.
        Can be a `State` object for dynamic updates.
    label : State, str, QWidget, or None, optional
        Label element. Default is None.
        Can be a `State` object for dynamic updates.
    key : State, Any, or None, optional
        Unique key for the tab (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    value : State, Any, or None, optional
        Value of the tab. Default is None.
        Can be a `State` object for dynamic updates.
    wrapped : State or bool, optional
        If True, label can span two lines. Default is False.
        Can be a `State` object for dynamic updates.
    children : State, List[QWidget], QWidget, or None, optional
        Content of the tab (qtmui-specific, unsupported in MUI). Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting ButtonBase props.

    Notes
    -----
    - `children` is unsupported in MUI but supported in qtmui as a fallback for label.
    - `key` is a qtmui-specific feature for tab management.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiTab-root`.

    Demos:
    - Tab: https://qtmui.com/material-ui/qtmui-tab/

    API Reference:
    - Tab API: https://qtmui.com/material-ui/api/tab/
    """

    VALID_POSITIONS = ['top', 'end', 'start', 'bottom']

    def __init__(
        self,
        classes: Optional[Union[State, Dict, None]]=None,
        disabled: Union[State, bool]=False,
        disableFocusRipple: Union[State, bool]=False,
        disableRipple: Union[State, bool]=False,
        icon: Optional[Union[State, str, QWidget, None]]=None,
        iconPosition: Union[State, str]="top",
        label: Optional[Union[State, str, QWidget, None]]=None,
        key: Optional[Union[State, Any, None]]=None,
        sx: Optional[Union[State, List, Dict, Callable, None]]=None,
        value: Optional[Union[State, Any, None]]=None,
        wrapped: Union[State, bool]=False,
        children: Optional[Union[State, List[QWidget], QWidget, None]]=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.setObjectName(str(id(self)))
        self.theme = useTheme()
        self._widget_references = []

        # Set properties with validation
        self._set_classes(classes)
        self._set_disabled(disabled)
        self._set_disableFocusRipple(disableFocusRipple)
        self._set_disableRipple(disableRipple)
        self._set_icon(icon)
        self._set_iconPosition(iconPosition)
        self._set_label(label)
        self._set_key(key)
        self._set_sx(sx)
        self._set_value(value)
        self._set_wrapped(wrapped)
        self._set_children(children)

        self._rendered = False


    # Setter and Getter methods
    @_validate_param(file_path="qtmui.material.tab", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    @_validate_param(file_path="qtmui.material.tab", param_name="disabled", supported_signatures=Union[State, bool])
    def _set_disabled(self, value):
        self._disabled = value

    def _get_disabled(self):
        return self._disabled.value if isinstance(self._disabled, State) else self._disabled

    @_validate_param(file_path="qtmui.material.tab", param_name="disableFocusRipple", supported_signatures=Union[State, bool])
    def _set_disableFocusRipple(self, value):
        self._disableFocusRipple = value

    def _get_disableFocusRipple(self):
        return self._disableFocusRipple.value if isinstance(self._disableFocusRipple, State) else self._disableFocusRipple

    @_validate_param(file_path="qtmui.material.tab", param_name="disableRipple", supported_signatures=Union[State, bool])
    def _set_disableRipple(self, value):
        self._disableRipple = value

    def _get_disableRipple(self):
        return self._disableRipple.value if isinstance(self._disableRipple, State) else self._disableRipple

    # @_validate_param(file_path="qtmui.material.tab", param_name="icon", supported_signatures=Union[State, str, QWidget, type(None)])
    def _set_icon(self, value):
        self._icon = value

    def _get_icon(self):
        return self._icon.value if isinstance(self._icon, State) else self._icon

    @_validate_param(file_path="qtmui.material.tab", param_name="iconPosition", supported_signatures=Union[State, str], valid_values=VALID_POSITIONS)
    def _set_iconPosition(self, value):
        self._iconPosition = value

    def _get_iconPosition(self):
        position = self._iconPosition.value if isinstance(self._iconPosition, State) else self._iconPosition
        return position if position in self.VALID_POSITIONS else 'top'

    @_validate_param(file_path="qtmui.material.tab", param_name="label", supported_signatures=Union[State, str, Callable, QWidget, type(None)])
    def _set_label(self, value):
        self._label = value

    def _get_label(self):
        return self._label.value if isinstance(self._label, State) else self._label

    # @_validate_param(file_path="qtmui.material.tab", param_name="key", supported_signatures=Union[State, Any, type(None)])
    def _set_key(self, value):
        self._key = value

    def _get_key(self):
        return self._key.value if isinstance(self._key, State) else self._key

    @_validate_param(file_path="qtmui.material.tab", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    # @_validate_param(file_path="qtmui.material.tab", param_name="value", supported_signatures=Union[State, Any, type(None)])
    def _set_value(self, value):
        self._value = value

    def _get_value(self):
        return self._value.value if isinstance(self._value, State) else self._value

    @_validate_param(file_path="qtmui.material.tab", param_name="wrapped", supported_signatures=Union[State, bool])
    def _set_wrapped(self, value):
        self._wrapped = value

    def _get_wrapped(self):
        return self._wrapped.value if isinstance(self._wrapped, State) else self._wrapped

    # @_validate_param(file_path="qtmui.material.tab", param_name="children", supported_signatures=Union[State, List[QWidget], QWidget, type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children


    def _init_ui(self):
        if self._rendered:
            return
        self._rendered = True
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(0,0,0,0)
        if self._children:
            if isinstance(self._children, list):
                for widget in self._children:
                    self.layout().addWidget(widget)
            elif isinstance(self._children, Callable):
                self.layout().addWidget(self._children())
            else:
                self.layout().addWidget(self._children)



    def generate_stylesheet(self):
        # Dùng để tạo CSS từ thuộc tính sx
        styles = []
        if isinstance(self._sx, list):
            for style_item in self._sx:
                if isinstance(style_item, dict):
                    # Thêm từng thuộc tính CSS từ dict
                    for key, value in style_item.items():
                        styles.append(f"{key}: {value};")
                elif callable(style_item):
                    # Nếu style là một hàm, gọi hàm đó để lấy giá trị CSS
                    generated_style = style_item()
                    styles.append(generated_style)
        return " ".join(styles)

    # Setter và getter cho các thuộc tính
    def set_disabled(self, disabled: bool):
        self._disabled = disabled
        self.setEnabled(not disabled)

    def set_value(self, value: Any):
        self._value = value

    def get_value(self):
        return self._value

    def set_icon(self, icon: Union[str, Any]):
        self._icon = icon
        # Cập nhật icon khi thay đổi
        if isinstance(icon, str):
            self.setIcon(icon)

    def set_label(self, label: str):
        self._label = label
        self.setText(label)

    def set_wrapped(self, wrapped: bool):
        self._wrapped = wrapped
        # Cập nhật nếu cần xử lý việc nhãn hiển thị trên nhiều dòng

    def set_icon_position(self, position: str):
        if position in ['top', 'end', 'start', 'bottom']:
            self._iconPosition = position
            # Cập nhật vị trí của icon

