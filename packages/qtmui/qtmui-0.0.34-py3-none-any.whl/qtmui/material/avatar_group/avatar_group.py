from typing import Optional, Any, Union, Callable, List, Dict

from qtmui.hooks import State, useEffect
from PySide6.QtWidgets import QFrame, QHBoxLayout

from ..avatar import Avatar
from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
from ..utils.validate_params import _validate_param

class AvatarGroup(QFrame):
    """
    A component that displays a group of avatars with customizable spacing and surplus rendering.

    The `AvatarGroup` component stacks avatars horizontally, limiting the number displayed based on
    the `max` prop and rendering surplus avatars using a custom renderer or a default `+x` avatar.
    It supports all props of the Material-UI `AvatarGroup` component, including native component
    props via `**kwargs`.

    Parameters
    ----------
    children : State or List[Avatar], optional
        The avatars to stack. Must be a list of `Avatar` components. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or dict, optional
        Override or extend the styles applied to the component. Default is None.
        Can be a `State` object for dynamic updates.
    component : State or Any, optional
        Component used for the root node (e.g., HTML element or custom component).
        Default is None. Can be a `State` object for dynamic updates.
    componentsProps : State or dict, optional
        Extra props for slot components (e.g., additionalAvatar). Deprecated: Use `slotProps` instead.
        Default is None. Can be a `State` object for dynamic updates.
    max : State or int, optional
        Maximum number of avatars to show before displaying a surplus indicator. Default is 5.
        Can be a `State` object for dynamic updates.
    renderSurplus : State or Callable, optional
        Custom renderer for surplus avatars. Signature: function(surplus: int) => Any.
        Default is None (uses default `+x` Avatar). Can be a `State` object for dynamic updates.
    slotProps : State or dict, optional
        Props for each slot (e.g., additionalAvatar, surplus). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or dict, optional
        Components for each slot (e.g., surplus). Default is None.
        Can be a `State` object for dynamic updates.
    spacing : State, str, or int, optional
        Spacing between avatars. Valid values: 'small' (4px), 'medium' (8px), or a number.
        Default is 'medium'. Can be a `State` object for dynamic updates.
    sx : State, dict, Callable, str, or None, optional
        System prop for CSS overrides and additional styles. Default is None.
        Can be a `State` object for dynamic updates.
    total : State or int, optional
        Total number of avatars, used to calculate surplus. Defaults to len(children) if not set.
        Can be a `State` object for dynamic updates.
    variant : State or str, optional
        Shape of the avatars. Valid values: 'circular', 'rounded', 'square'. Default is 'circular'.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to the parent `QFrame` class, supporting
        native component props (e.g., style, className).

    Attributes
    ----------
    VALID_VARIANTS : list[str]
        Valid values for the `variant` parameter: ["circular", "rounded", "square"].
    VALID_SPACING : list[str]
        Valid string values for the `spacing` parameter: ["small", "medium"].

    Notes
    -----
    - Props of the native component are supported via `**kwargs` (e.g., `style`, `className`).
    - The `componentsProps` prop is deprecated; use `slotProps` instead.
    - If `renderSurplus` is not provided, surplus avatars are rendered as an `Avatar` with text `+x`.

    Demos:
    - AvatarGroup: https://qtmui.com/material-ui/qtmui-avatar-group/

    API Reference:
    - AvatarGroup API: https://qtmui.com/material-ui/api/avatar-group/
    """

    VALID_VARIANTS = ["circular", "rounded", "square"]
    VALID_SPACING = ["small", "medium"]

    def __init__(
        self,
        children: Optional[Union[State, List[Avatar]]] = None,
        classes: Optional[Union[State, Dict]] = None,
        component: Optional[Union[State, Any]] = None,
        componentsProps: Optional[Union[State, Dict]] = None,
        max: Union[State, int] = 5,
        renderSurplus: Optional[Union[State, Callable[[int], Any]]] = None,
        slotProps: Optional[Union[State, Dict[str, Union[Callable, Dict]]]] = None,
        slots: Optional[Union[State, Dict[str, Any]]] = None,
        spacing: Union[State, str, int] = "medium",
        sx: Optional[Union[State, Dict, Callable, str]] = None,
        total: Optional[Union[State, int]] = None,
        variant: Union[State, str] = "circular",
        **kwargs
    ):
        super().__init__(**kwargs)

        # Set properties with validation
        self._set_children(children)
        self._set_classes(classes)
        self._set_component(component)
        self._set_componentsProps(componentsProps)
        self._set_max(max)
        self._set_renderSurplus(renderSurplus)
        self._set_slotProps(slotProps)
        self._set_slots(slots)
        self._set_spacing(spacing)
        self._set_sx(sx)
        self._set_total(total)
        self._set_variant(variant)

        self._init_ui()
        # self._set_stylesheet()

        self.theme = useTheme()
        # useEffect(
        #     self._set_stylesheet,
        #     [self.theme.state]
        # )
        # self.destroyed.connect(self._on_destroyed)

    # Setter and Getter methods for all parameters
    # @_validate_param(file_path="qtmui.material.avatar_group", param_name="children", supported_signatures=Union[State, List[Avatar], type(None)])
    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children.value if isinstance(self._children, State) else self._children

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
    def _set_classes(self, value):
        self._classes = value

    def _get_classes(self):
        return self._classes.value if isinstance(self._classes, State) else self._classes

    # @_validate_param(file_path="qtmui.material.avatar_group", param_name="component", supported_signatures=Union[State, Any, type(None)])
    def _set_component(self, value):
        self._component = value

    def _get_component(self):
        return self._component.value if isinstance(self._component, State) else self._component

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="componentsProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_componentsProps(self, value):
        self._componentsProps = value

    def _get_componentsProps(self):
        return self._componentsProps.value if isinstance(self._componentsProps, State) else self._componentsProps

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="max", supported_signatures=Union[State, int])
    def _set_max(self, value):
        self._max = value

    def _get_max(self):
        return self._max.value if isinstance(self._max, State) else self._max

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="renderSurplus", supported_signatures=Union[State, Callable, type(None)])
    def _set_renderSurplus(self, value):
        self._renderSurplus = value

    def _get_renderSurplus(self):
        return self._renderSurplus.value if isinstance(self._renderSurplus, State) else self._renderSurplus

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="slotProps", supported_signatures=Union[State, Dict, type(None)])
    def _set_slotProps(self, value):
        self._slotProps = value or {}

    def _get_slotProps(self):
        return self._slotProps.value if isinstance(self._slotProps, State) else self._slotProps

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="slots", supported_signatures=Union[State, Dict, type(None)])
    def _set_slots(self, value):
        self._slots = value or {}

    def _get_slots(self):
        return self._slots.value if isinstance(self._slots, State) else self._slots

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="spacing", supported_signatures=Union[State, str, int], valid_values=VALID_SPACING)
    def _set_spacing(self, value):
        self._spacing = value

    def _get_spacing(self):
        return self._spacing.value if isinstance(self._spacing, State) else self._spacing

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="sx", supported_signatures=Union[State, Dict, Callable, str, type(None)])
    def _set_sx(self, value):
        self._sx = value

    def _get_sx(self):
        return self._sx.value if isinstance(self._sx, State) else self._sx

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="total", supported_signatures=Union[State, int, type(None)])
    def _set_total(self, value):
        if value is not None:
            self._total = value
        else:
            children = self._get_children()
            self._total = len(children) if children else 0

    def _get_total(self):
        return self._total.value if isinstance(self._total, State) else self._total

    @_validate_param(file_path="qtmui.material.avatar_group", param_name="variant", supported_signatures=Union[State, str], valid_values=VALID_VARIANTS)
    def _set_variant(self, value):
        self._variant = value

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        avatar_count = 0
        avatar_w = 0
        avatar_size = 0
        total_w = 0

        self.layout().addWidget(Avatar(text=f"+{len(self._children) - 3}", customText=True, size=self._children[0]._size, color="primary", borderWidth=1))
        for avatar in self._children:
            if isinstance(avatar, Avatar):
                total_w  += avatar.sizeHint().width()
                if avatar_w == 0:
                    avatar_w = total_w
                    avatar_size = avatar._size
                self.layout().addWidget(avatar)
                avatar_count += 1
                if avatar_count == 3:
                    break

        # self.layout().insertWidget(-1, Avatar(text=f"+{len(self._children) - avatar_count}", customText=True, size=avatar_size, color="primary"))
        widgets = self.findChildren(Avatar)
        # widgets.reverse()
        for index, widget in enumerate(widgets, 0):
            # if index < 3:
                self.layout().insertWidget(0, widget)
            # else:
            #     self.layout().insertWidget(-1, widget)

        self.layout().setContentsMargins(0,0,avatar_w,0)

        if len(self._children) > 1:
            self.setFixedWidth(total_w)

    # Getter và Setter cho các thuộc tính

    @property
    def children(self) -> Optional[Any]:
        """Các avatar cần được xếp chồng lên nhau."""
        return self._children

    @children.setter
    def children(self, value: Optional[Any]):
        self._children = value

    @property
    def classes(self) -> Optional[Dict]:
        """Ghi đè hoặc mở rộng các style áp dụng cho component."""
        return self._classes

    @classes.setter
    def classes(self, value: Optional[Dict]):
        self._classes = value

    @property
    def component(self) -> Optional[Any]:
        """Component được sử dụng cho node gốc, có thể là HTML element hoặc component."""
        return self._component

    @component.setter
    def component(self, value: Optional[Any]):
        self._component = value

    @property
    def componentsProps(self) -> Optional[Dict[str, Any]]:
        """Props bổ sung cho các slot component (đã deprecated)."""
        return self._componentsProps

    @componentsProps.setter
    def componentsProps(self, value: Optional[Dict[str, Any]]):
        self._componentsProps = value

    @property
    def max(self) -> Optional[int]:
        """Số lượng avatar tối đa trước khi hiển thị dấu +x."""
        return self._max

    @max.setter
    def max(self, value: Optional[int]):
        self._max = value

    @property
    def renderSurplus(self) -> Optional[Callable[[int], Any]]:
        """Hàm custom render cho các avatar dư thừa."""
        return self._renderSurplus

    @renderSurplus.setter
    def renderSurplus(self, value: Optional[Callable[[int], Any]]):
        self._renderSurplus = value

    @property
    def slotProps(self) -> Optional[Dict[str, Union[Callable, Dict]]]:
        """Thuộc tính sử dụng cho mỗi slot bên trong AvatarGroup."""
        return self._slotProps

    @slotProps.setter
    def slotProps(self, value: Optional[Dict[str, Union[Callable, Dict]]]):
        self._slotProps = value

    @property
    def slots(self) -> Optional[Dict[str, Any]]:
        """Component sử dụng cho mỗi slot bên trong AvatarGroup."""
        return self._slots

    @slots.setter
    def slots(self, value: Optional[Dict[str, Any]]):
        self._slots = value

    @property
    def spacing(self) -> Union[str, int]:
        """Khoảng cách giữa các avatar ('medium', 'small', hoặc số)."""
        return self._spacing

    @spacing.setter
    def spacing(self, value: Union[str, int]):
        self._spacing = value

    @property
    def sx(self) -> Optional[Union[List[Union[Callable, Dict, bool]], Callable, Dict, bool]]:
        """Prop hệ thống cho phép định nghĩa CSS overrides hoặc thêm CSS styles."""
        return self._sx

    @sx.setter
    def sx(self, value: Optional[Union[List[Union[Callable, Dict, bool]], Callable, Dict, bool]]):
        self._sx = value

    @property
    def total(self) -> Optional[int]:
        """Tổng số avatar, được sử dụng để tính số lượng avatar dư thừa."""
        return self._total

    @total.setter
    def total(self, value: Optional[int]):
        self._total = value

    @property
    def variant(self) -> str:
        """Kiểu của avatar ('circular', 'rounded', 'square', hoặc string)."""
        return self._variant

    @variant.setter
    def variant(self, value: str):
        self._variant = value
