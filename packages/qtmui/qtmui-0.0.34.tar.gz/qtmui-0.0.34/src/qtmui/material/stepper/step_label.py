import uuid
from typing import Optional, Union, List, Callable, Any
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFrame, QSizePolicy
from PySide6.QtCore import Qt

from ..typography import Typography
from ..box import Box
from ..spacer import VSpacer
from ..list import ListItemAvatar
from ..avatar import Avatar

class StepLabel(QFrame):
    """
    A step label component, styled like Material-UI StepLabel.

    The `StepLabel` component displays a label for a step in a Stepper, supporting icon overrides,
    optional content, and error states, aligning with MUI StepLabel props. Inherits from native
    component props.

    Parameters
    ----------
    children : State, str, QWidget, or None, optional
        Content of the label, typically a string title. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    componentsProps : State or Dict, optional
        Props for slots inside (deprecated, use slotProps). Default is None.
        Can be a `State` object for dynamic updates.
    completed : State or bool, optional
        If True, marks the step as completed (qtmui-specific). Default is False.
        Can be a `State` object for dynamic updates.
    error : State or bool, optional
        If True, marks the step as failed. Default is False.
        Can be a `State` object for dynamic updates.
    icon : State, str, QWidget, or None, optional
        Overrides the default step icon. Default is None.
        Can be a `State` object for dynamic updates.
    index : State, int, or None, optional
        Position of the step, inherited from Stepper (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    optional : State, str, QWidget, or None, optional
        Optional content to display. Default is None.
        Can be a `State` object for dynamic updates.
    slotProps : State or Dict, optional
        Props for each slot (label, root, stepIcon). Default is None.
        Can be a `State` object for dynamic updates.
    slots : State or Dict, optional
        Components for each slot (label, root, stepIcon). Default is None.
        Can be a `State` object for dynamic updates.
    StepIconComponent : State, str, Type, or None, optional
        Component to replace StepIcon (deprecated, use slots.stepIcon). Default is None.
        Can be a `State` object for dynamic updates.
    StepIconProps : State or Dict, optional
        Props for StepIcon (deprecated, use slotProps.stepIcon). Default is None.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    text : State, str, or None, optional
        Alternative text content (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    width : State, int, or None, optional
        Width of the label (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting native component props.

    Notes
    -----
    - All 15 existing parameters are retained to align with qtmui-specific features.
    - `completed`, `index`, `text`, and `width` are qtmui-specific and not part of MUI StepLabel.
    - `componentsProps`, `StepIconComponent`, and `StepIconProps` are deprecated; use `slotProps` and `slots`.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiStepLabel-root`.

    Demos:
    - StepLabel: https://qtmui.com/material-ui/qtmui-step-label/

    API Reference:
    - StepLabel API: https://qtmui.com/material-ui/api/step-label/
    """
    def __init__(self,
                 children: Optional[Union[str, QWidget]] = None,  # Tiêu đề của label, thường là string
                 classes: Optional[dict] = None,  # Ghi đè hoặc mở rộng styles áp dụng cho component
                 componentsProps: Optional[dict] = None,  # Thuộc tính đã bị deprecated, dùng cho các slot bên trong
                 completed: bool = False,  # Đánh dấu step là completed
                 error: bool = False,  # Nếu true, step được đánh dấu là lỗi
                 icon: Optional[Union[str, QWidget]] = None,  # Ghi đè icon mặc định của step
                 index: Optional[int] = None,  # Vị trí của step, thừa kế từ Stepper nếu không truyền vào
                 optional: Optional[Union[str, QWidget]] = None,  # Node tùy chọn để hiển thị
                 slotProps: Optional[dict] = None,  # Thuộc tính cho mỗi slot bên trong (label, stepIcon)
                 slots: Optional[dict] = None,  # Component dùng cho từng slot bên trong
                 StepIconComponent: Optional[Any] = None,  # Component thay thế StepIcon mặc định
                 StepIconProps: Optional[dict] = None,  # Props cho StepIcon element
                 sx: Optional[Union[List[Union[Callable, dict, bool]], Callable, dict, bool]] = None,  # CSS overrides
                 text: Optional[str] = "",  # CSS overrides
                 width: Optional[int] = None,  # CSS overrides
                 *args, **kwargs):
        super().__init__()

        self._children = children
        self._completed = completed
        self._classes = classes or {}
        self._componentsProps = componentsProps or {}
        self._error = error
        self._icon = icon
        self._index = index
        self._optional = optional
        self._slotProps = slotProps or {}
        self._slots = slots or {}
        self._StepIconComponent = StepIconComponent
        self._StepIconProps = StepIconProps or {}
        self._sx = sx or []
        self._text = text
        self._width = width

        self._init_ui()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignVCenter)  # căn giữa theo chiều dọc
        # self.setStyleSheet(f'#{self.objectName()} {{background: pink;}}')
        self.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        self.layout().setContentsMargins(0,0,0,0)


        avatar_props = {}
        if self._completed:
            avatar_props = {
                "color": self._error or "primary",
                "icon": self._icon or ':/baseline/resource_qtmui/baseline/done.svg',
                "size": 32
            }
        else:
            avatar_props = {
                "color": self._error or "#DFE3E8",
                "customText": True,
                "text": str(self._index+1),
                "size": 32
            }

        # Thêm các children (nếu có)
        if self._children:
            if not isinstance(self._children, list):
                raise TypeError("children must be type (list)")

        self.layout().addWidget(
            Box(
                direction="row",
                # hightLight=True,
                spacing=6,
                children=self._children or [
                    ListItemAvatar(
                        children=[
                            Avatar(**avatar_props)
                        ]
                    ),
                    Box(
                        sx={"width": self._width},
                        children=[
                            VSpacer(),
                            Typography(variant="body1", text=self._text, color= self._error or "textSecondary"),
                            self._optional,
                            VSpacer()
                        ]
                    )
                ]
            )
        )


    def generate_stylesheet(self):
        styles = []
        if isinstance(self._sx, list):
            for style_item in self._sx:
                if isinstance(style_item, dict):
                    for key, value in style_item.items():
                        styles.append(f"{key}: {value};")
                elif callable(style_item):
                    generated_style = style_item()
                    styles.append(generated_style)
        return " ".join(styles)

    # Setters và Getters cho các props
    def set_error(self, error: bool):
        self._error = error
        self.update_ui()

    def get_error(self):
        return self._error

    def set_icon(self, icon: Union[str, QWidget]):
        self._icon = icon
        self.update_ui()

    def get_icon(self):
        return self._icon

    def set_optional(self, optional: Union[str, QWidget]):
        self._optional = optional
        self.update_ui()

    def get_optional(self):
        return self._optional

    def set_children(self, children: Union[str, QWidget]):
        self._children = children
        self.update_ui()

    def get_children(self):
        return self._children

    def update_ui(self):
        """ Cập nhật giao diện khi có sự thay đổi """
        self.layout().update()
