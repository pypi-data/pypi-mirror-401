import uuid
from typing import Optional, Union, List, Callable, Any
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Signal, Qt

from qtmui.hooks import useState

from qtmui.material.styles import useTheme

from ..box import Box
from ..view import View
from ..avatar import Avatar
from ..py_iconify import PyIconify

class Step(QFrame):
    """
    A step component, styled like Material-UI Step.

    The `Step` component represents a single step in a Stepper, supporting active, completed,
    disabled, and expanded states, aligning with MUI Step props. Inherits from native component props.

    Parameters
    ----------
    active : State or bool, optional
        If True, sets the step as active. Default is False.
        Can be a `State` object for dynamic updates.
    alternativeLabel : State or bool, optional
        If True, uses alternative label styling (qtmui-specific). Default is False.
        Can be a `State` object for dynamic updates.
    children : State, List[QWidget], QWidget, or None, optional
        Step sub-components such as StepLabel, StepContent. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    completed : State or bool, optional
        If True, marks the step as completed. Default is False.
        Can be a `State` object for dynamic updates.
    component : State, str, Type, or None, optional
        Component used for the root node. Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    disabled : State or bool, optional
        If True, disables the step. Default is False.
        Can be a `State` object for dynamic updates.
    expanded : State or bool, optional
        If True, expands the step. Default is False.
        Can be a `State` object for dynamic updates.
    error : State or bool, optional
        If True, indicates an error state (qtmui-specific). Default is False.
        Can be a `State` object for dynamic updates.
    index : State, int, or None, optional
        Position of the step, inherited from Stepper. Default is None.
        Can be a `State` object for dynamic updates.
    label : State, QWidget, or None, optional
        Label for the step (qtmui-specific). Default is None.
        Can be a `State` object for dynamic updates.
    key : State or Any, optional
        Unique key identifier. Default is None.
        Can be a `State` object for dynamic updates.
    last : State or bool, optional
        If True, displays the step as the last one. Default is False.
        Can be a `State` object for dynamic updates.
    optional : State or bool, optional
        If True, marks the step as optional (qtmui-specific). Default is False.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting native component props.

    Signals
    -------
    themeChanged : Signal()
        Emitted when the theme changes.

    Notes
    -----
    - All 15 existing parameters are retained to align with qtmui-specific features.
    - `alternativeLabel`, `error`, `label`, and `optional` are qtmui-specific and not part of MUI Step.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiStep-root`.

    Demos:
    - Step: https://qtmui.com/material-ui/qtmui-step/

    API Reference:
    - Step API: https://qtmui.com/material-ui/api/step/
    """
    themeChanged = Signal()

    def __init__(self,
                 active: bool = False,  # Xác định step hiện tại có active hay không
                 alternativeLabel: bool = False,  
                 children: Optional[list] = None,  # Các Step sub-components như StepLabel, StepContent
                 classes: Optional[dict] = None,  # Ghi đè hoặc mở rộng styles áp dụng cho component
                 completed: bool = False,  # Đánh dấu step là completed
                 component: Optional[Union[str, Any]] = None,  # Component dùng cho node gốc
                 disabled: bool = False,  # Nếu true, step bị disable
                 expanded: bool = False,  # Mở rộng step
                 error: bool = False,  # Có lỗi
                 index: Optional[int] = None,  # Vị trí của step, thừa kế từ Stepper nếu không truyền vào
                 label: Optional[QWidget] = None,  # Vị trí của step, thừa kế từ Stepper nếu không truyền vào
                 key: Optional[str] = None,  # Vị trí của step, thừa kế từ Stepper nếu không truyền vào
                 last: bool = False,  # Nếu true, step được hiển thị là step cuối
                 optionnal: bool = False,
                 sx: Optional[Union[List[Union[Callable, dict, bool]], Callable, dict, bool]] = None,  # CSS overrides
                 *args, **kwargs):
        super().__init__()
        self.setObjectName(str(uuid.uuid4()))

        self._active = active
        self._alternativeLabel = alternativeLabel
        self._children = children
        self._classes = classes or {}
        self._completed = completed
        self._component = component
        self._disabled = disabled
        self._expanded = expanded
        self._error = error
        self._index = index
        self._label = label
        self._key = key
        self._last = last
        self._optionnal = optionnal
        self._sx = sx or []

        self._init_ui()

        # self.setStyleSheet(f'#{self.objectName()} {{background: gray;}}')

    def _init_ui(self):
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # self.layout().setSpacing(0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout().setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        avatar_props = {}
        if self._completed:
            avatar_props = {
                "color": "error" if self._error else "primary",
                "icon": ':/baseline/resource_qtmui/baseline/done.svg',
                "size": 32
            }
        else:
            avatar_props = {
                "color": "error" if self._error else "#DFE3E8",
                "customText": True,
                "text": str(self._index+1),
                "size": 32
            }
        
        # self._iconWidget, self._setIconWidget = useState(
        #     Box(
        #         id=f"step_icon{uuid.uuid4()}",
        #         align="center",
        #         width=self._label.width() if self._label else None,
        #         children=[
        #             Avatar(**avatar_props)
        #         ]
        #     )
        # )
        self._iconWidget, self._setIconWidget = useState(None)

        try:
            self.layout().addWidget(
                View(content=self._iconWidget)
            )
        except Exception as e:
            import traceback
            traceback.print_exc()


        # Thêm từng child component vào layout
        if self._children:
            for child in self._children:
                if isinstance(child, QWidget):
                    self.layout().addWidget(child)
        
        # Áp dụng trạng thái disabled nếu có
        self.setEnabled(not self._disabled)

        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self._set_theme)

    def _set_icon_widget(self, state):
        theme = useTheme()

        if state == "complete":
            self._setIconWidget(
                Box(
                    id=f"step_icon{uuid.uuid4()}",
                    align="center",
                    direction="row",
                    width=self._label.sizeHint().width() if self._label else None,
                    children=[
                        Avatar(
                            color = "primary",
                            icon = PyIconify(key="material-symbols:done", color="palette.common.white"),
                            size = 32
                        )
                    ]
                )
            )
        elif state == "error":
            self._setIconWidget(
                Box(
                    id=f"step_icon{uuid.uuid4()}",
                    align="center",
                    direction="row",
                    width=self._label.sizeHint().width() if self._label else None,
                    children=[
                        Avatar(
                            color = "error",
                            icon = PyIconify(key="material-symbols:done", color="palette.common.white"),
                            size = 32
                        )
                    ]
                )
            )
        elif state == "current":
            self._setIconWidget(
                Box(
                    id=f"step_icon{uuid.uuid4()}",
                    align="center",
                    direction="row",
                    width=self._label.sizeHint().width() if self._label else None,
                    children=[
                        Avatar(
                            color = theme.palette.primary.main,
                            customText = True,
                            text = str(self._index+1),
                            size = 32
                        )
                    ]
                )
            )
        else:
            self._setIconWidget(
                Box(
                    id=f"step_icon{uuid.uuid4()}",
                    direction="row",
                    align="center",
                    width=self._label.sizeHint().width() if self._label else None,
                    children=[
                        Avatar(
                            color = "#DFE3E8",
                            customText = True,
                            text = str(self._index+1),
                            size = 32
                        ),
                    ]
                )
            )
            # self._setIconWidget(
            #     Avatar(
            #         color = "#DFE3E8",
            #         customText = True,
            #         text = str(self._index+1),
            #         size = 32
            #     )
            # )

    def _set_theme(self):
        # self._styled_step.setStyleSheet(
        #     self._styled_step.styleSheet() + f"""
        #         QPushButton {{
        #             background-color: transparent;
        #         }}
        #         QPushButton:hover {{
        #             background-color: transparent;
        #         }}
        #     """
        # )
        pass

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
    def set_active(self, active: bool):
        self._active = active
        self.update_ui()

    def get_active(self):
        return self._active

    def set_completed(self, completed: bool):
        self._completed = completed
        self.update_ui()

    def get_completed(self):
        return self._completed

    def set_disabled(self, disabled: bool):
        self._disabled = disabled
        self.setEnabled(not disabled)

    def get_disabled(self):
        return self._disabled

    def set_expanded(self, expanded: bool):
        self._expanded = expanded
        self.update_ui()

    def get_expanded(self):
        return self._expanded

    def set_last(self, last: bool):
        self._last = last
        self.update_ui()

    def get_last(self):
        return self._last

    def set_index(self, index: int):
        self._index = index
        self.update_ui()

    def get_index(self):
        return self._index

    def update_ui(self):
        """ Cập nhật giao diện khi có sự thay đổi """
        self.layout().update()

