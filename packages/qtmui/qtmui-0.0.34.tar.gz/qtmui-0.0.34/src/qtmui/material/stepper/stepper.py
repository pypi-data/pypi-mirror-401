import uuid
from typing import Optional, Union, List, Callable, Any
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout
from ..widget_base import PyWidgetBase

from qtmui.hooks import State

from .step import Step
from ..box import Box
from ..divider import Divider
from ..spacer import HSpacer

from qtmui.material.styles import useTheme
from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

class Stepper(QFrame, PyWidgetBase):
    """
    A stepper component, styled like Material-UI Stepper.

    The `Stepper` component displays a sequence of steps, supporting active step selection,
    horizontal or vertical orientation, and connectors between steps, aligning with MUI Stepper props.
    Inherits from native component props.

    Parameters
    ----------
    activeStep : State or int, optional
        Sets the active step (zero-based index). Set to -1 to disable all steps. Default is 0.
        Can be a `State` object for dynamic updates.
    alternativeLabel : State or bool, optional
        If True, step labels are positioned under icons when orientation is 'horizontal'. Default is False.
        Can be a `State` object for dynamic updates.
    children : State, List[QWidget], or None, optional
        Two or more Step components. Default is None.
        Can be a `State` object for dynamic updates.
    classes : State or Dict, optional
        Override or extend styles. Default is None.
        Can be a `State` object for dynamic updates.
    component : State, str, Type, or None, optional
        Component used for the root node. Default is None (uses QFrame).
        Can be a `State` object for dynamic updates.
    connector : State, QWidget, or None, optional
        Element placed between each step. Default is None (uses Divider).
        Can be a `State` object for dynamic updates.
    nonLinear : State or bool, optional
        If True, does not enforce linear step progression. Default is False.
        Can be a `State` object for dynamic updates.
    orientation : State or str, optional
        Component orientation ('horizontal' or 'vertical'). Default is 'horizontal'.
        Can be a `State` object for dynamic updates.
    sx : State, List, Dict, Callable, or None, optional
        System prop for CSS overrides. Default is None.
        Can be a `State` object for dynamic updates.
    **kwargs
        Additional keyword arguments passed to QFrame, supporting native component props.

    Notes
    -----
    - All 9 existing parameters are retained, with `connectorRender` replaced by `connector` to align with MUI Stepper.
    - Requires at least two Step components in children.
    - Supports dynamic updates via State objects.
    - MUI classes applied: `MuiStepper-root`.

    Demos:
    - Stepper: https://qtmui.com/material-ui/qtmui-stepper/

    API Reference:
    - Stepper API: https://qtmui.com/material-ui/api/stepper/
    """
    def __init__(self,
                 activeStep: Union[int, str, State] = 0,  # Step hiện tại (zero-based index)
                 alternativeLabel: bool = False,  # Nếu true, label sẽ dưới icon khi orientation là 'horizontal'
                 children: Optional[List[QWidget]] = None,  # Một hoặc nhiều <Step /> components
                 classes: Optional[dict] = None,  # Ghi đè hoặc mở rộng styles cho component
                 component: Optional[Union[str, Any]] = None,  # Component dùng cho node gốc (có thể là string hoặc component)
                 connectorRender: Callable = None,  # Phần tử nằm giữa mỗi step (mặc định là <StepConnector />)
                 nonLinear: bool = False,  # Nếu true, không kiểm soát luồng step theo dạng tuyến tính
                 orientation: str = 'horizontal',  # Hướng của Stepper: 'horizontal' | 'vertical'
                 sx: Optional[Union[List[Union[Callable, dict, bool]], Callable, dict, bool]] = None,  # CSS overrides
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._activeStep = activeStep
        self._alternativeLabel = alternativeLabel
        self._children = children or []
        self._classes = classes or {}
        self._component = component
        self._connectorRender = connectorRender
        self._nonLinear = nonLinear
        self._orientation = orientation
        self._sx = sx or []

        self._init_ui()

        self.slot_set_stylesheet()
        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
        self.destroyed.connect(self._on_destroyed)

    def slot_set_stylesheet(self):
        self._set_stylesheet()

    def _init_ui(self):
        self.setObjectName(str(uuid.uuid4()))
        layout_type = QVBoxLayout if self._orientation == 'vertical' else QHBoxLayout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        progress_layout = layout_type()

        self.layout().addLayout(progress_layout)

        # Add each step and connector if present
        if self._alternativeLabel:
            progress_component = [HSpacer()]
            for index, step in enumerate(self._children):
                progress_component.append(step)
                if index < len(self._children) - 1 and self._connectorRender:
                    progress_component.append(self._connectorRender())
            progress_component.append(HSpacer())
        else:
            progress_component = []
            for index, step in enumerate(self._children):
                progress_component.append(step)
                if index < len(self._children) - 1 and self._connectorRender:
                    progress_component.append(self._connectorRender())

        progress_layout.addWidget(
            Box(
                spacing=9,
                direction='row',
                children=progress_component
            )
        )

        if self._alternativeLabel:
            # Add each step and connector if present
            label_component = [Divider(color="transparent")]
            for index, step in enumerate(self._children):
                if isinstance(step, Step):
                    label_component.append(step._label)
                if index < len(self._children) and self._connectorRender:
                    label_component.append(Divider(color="transparent"))

            if self._alternativeLabel:
                progress_layout.addWidget(
                    Box(
                        direction="row",
                        spacing=6,
                        children=label_component
                    )
                )

        if self._activeStep:
            if not isinstance(self._activeStep, State):
                raise TypeError("activeStep must be type (State)")
            self._activeStep.valueChanged.connect(self._set_active_step)
            self._set_active_step(self._activeStep.value)

    def _set_stylesheet(self, component_styled=None):
        self.theme = useTheme()

        if not component_styled:
            component_styled = self.theme.components


        PyStepper_root = component_styled[f"PyStepper"].get("styles")["root"]
        PyStepper_root_qss = get_qss_style(PyStepper_root)
        
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
            
        self.setStyleSheet(
            f"""
                #{self.objectName()} {{
                    {PyStepper_root_qss}
                }}

                {sx_qss}

            """
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

    # Setters and Getters for props
    def _set_active_step(self, step: int):
        if step == 0:
            for stepWidget in self.findChildren(Step):
                if stepWidget._index == 0:
                    stepWidget._set_icon_widget(state="current")
                else:
                    stepWidget._set_icon_widget(state="nomal")
            return

        for stepWidget in self.findChildren(Step):
            if isinstance(stepWidget, Step):
                if stepWidget._index < step:
                    stepWidget._set_icon_widget(state="complete")
                elif stepWidget._index == step:
                    stepWidget._set_icon_widget(state="current")
                else:
                    stepWidget._set_icon_widget(state="nomal")


    def get_active_step(self):
        return self._activeStep

    def set_orientation(self, orientation: str):
        if orientation in ['horizontal', 'vertical']:
            self._orientation = orientation
            self._init_ui()  # Re-initialize layout based on new orientation

    def set_connector(self, connector: QWidget):
        self._connector = connector
        self.update_ui()

    def update_ui(self):
        # Cập nhật giao diện khi có sự thay đổi
        self.layout().update()
