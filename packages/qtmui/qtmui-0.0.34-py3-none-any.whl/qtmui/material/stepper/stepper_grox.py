# import uuid
# from typing import Optional, Union, List, Callable, Dict, Any, Type
# from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout
# from PyQt5.QtCore import Qt
# from ...base.widget_base import PyWidgetBase
# from qtmui.hooks import State
# from ...components.step import Step
# from ...components.box import Box
# from ...components.divider import Divider
# from qtmui.hooks.use_theme import useTheme
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
# from ...utils.validate_params import _validate_param

# class Stepper(QFrame, PyWidgetBase):
#     """
#     A stepper component, styled like Material-UI Stepper.

#     The `Stepper` component displays a sequence of steps, supporting active step selection,
#     horizontal or vertical orientation, and connectors between steps, aligning with MUI Stepper props.
#     Inherits from native component props.

#     Parameters
#     ----------
#     activeStep : State or int, optional
#         Sets the active step (zero-based index). Set to -1 to disable all steps. Default is 0.
#         Can be a `State` object for dynamic updates.
#     alternativeLabel : State or bool, optional
#         If True, step labels are positioned under icons when orientation is 'horizontal'. Default is False.
#         Can be a `State` object for dynamic updates.
#     children : State, List[QWidget], or None, optional
#         Two or more Step components. Default is None.
#         Can be a `State` object for dynamic updates.
#     classes : State or Dict, optional
#         Override or extend styles. Default is None.
#         Can be a `State` object for dynamic updates.
#     component : State, str, Type, or None, optional
#         Component used for the root node. Default is None (uses QFrame).
#         Can be a `State` object for dynamic updates.
#     connector : State, QWidget, or None, optional
#         Element placed between each step. Default is None (uses Divider).
#         Can be a `State` object for dynamic updates.
#     nonLinear : State or bool, optional
#         If True, does not enforce linear step progression. Default is False.
#         Can be a `State` object for dynamic updates.
#     orientation : State or str, optional
#         Component orientation ('horizontal' or 'vertical'). Default is 'horizontal'.
#         Can be a `State` object for dynamic updates.
#     sx : State, List, Dict, Callable, or None, optional
#         System prop for CSS overrides. Default is None.
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to QFrame, supporting native component props.

#     Notes
#     -----
#     - All 9 existing parameters are retained, with `connectorRender` replaced by `connector` to align with MUI Stepper.
#     - Requires at least two Step components in children.
#     - Supports dynamic updates via State objects.
#     - MUI classes applied: `MuiStepper-root`.

#     Demos:
#     - Stepper: https://qtmui.com/material-ui/qtmui-stepper/

#     API Reference:
#     - Stepper API: https://qtmui.com/material-ui/api/stepper/
#     """

#     VALID_ORIENTATIONS = ['horizontal', 'vertical']

#     def __init__(
#         self,
#         activeStep: Union[State, int] = 0,
#         alternativeLabel: Union[State, bool] = False,
#         children: Optional[Union[State, List[QWidget], None]] = None,
#         classes: Optional[Union[State, Dict, None]] = None,
#         component: Optional[Union[State, str, Type, None]] = None,
#         connector: Optional[Union[State, QWidget, None]] = None,
#         nonLinear: Union[State, bool] = False,
#         orientation: Union[State, str] = 'horizontal',
#         sx: Optional[Union[State, List, Dict, Callable, None]] = None,
#         **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.setObjectName(str(uuid.uuid4()))
#         PyWidgetBase._setUpUi(self)
#         self.theme = useTheme()
#         self._widget_references = []

#         # Set properties with validation
#         self._set_activeStep(activeStep)
#         self._set_alternativeLabel(alternativeLabel)
#         self._set_children(children)
#         self._set_classes(classes)
#         self._set_component(component)
#         self._set_connector(connector)
#         self._set_nonLinear(nonLinear)
#         self._set_orientation(orientation)
#         self._set_sx(sx)

#         self._init_ui()
#         self._set_stylesheet()
#         self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
#         self.destroyed.connect(self._on_destroyed)

#     # Setter and Getter methods
#     @_validate_param(file_path="qtmui.material.stepper", param_name="activeStep", supported_signatures=Union[State, int])
#     def _set_activeStep(self, value):
#         self._activeStep = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._update_active_step)
#         self._update_active_step()

#     def _get_activeStep(self):
#         active_step = self._activeStep.value if isinstance(self._activeStep, State) else self._activeStep
#         return active_step if active_step >= -1 else 0

#     @_validate_param(file_path="qtmui.material.stepper", param_name="alternativeLabel", supported_signatures=Union[State, bool])
#     def _set_alternativeLabel(self, value):
#         self._alternativeLabel = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._init_ui)

#     def _get_alternativeLabel(self):
#         return self._alternativeLabel.value if isinstance(self._alternativeLabel, State) else self._alternativeLabel

#     @_validate_param(file_path="qtmui.material.stepper", param_name="children", supported_signatures=Union[State, List[QWidget], type(None)])
#     def _set_children(self, value):
#         self._children = value
#         if isinstance(value, list):
#             if len(value) < 2 or not all(isinstance(child, Step) for child in value):
#                 raise ValueError("Children must contain at least two Step components")
#             self._widget_references.extend(value)
#         if isinstance(value, State):
#             value.valueChanged.connect(self._init_ui)

#     def _get_children(self):
#         return self._children.value if isinstance(self._children, State) else self._children or []

#     @_validate_param(file_path="qtmui.material.stepper", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
#     def _set_classes(self, value):
#         self._classes = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._set_stylesheet)

#     def _get_classes(self):
#         return self._classes.value if isinstance(self._classes, State) else self._classes

#     @_validate_param(file_path="qtmui.material.stepper", param_name="component", supported_signatures=Union[State, str, Type, type(None)])
#     def _set_component(self, value):
#         self._component = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._set_stylesheet)

#     def _get_component(self):
#         return self._component.value if isinstance(self._component, State) else self._component

#     @_validate_param(file_path="qtmui.material.stepper", param_name="connector", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_connector(self, value):
#         self._connector = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)
#         if isinstance(value, State):
#             value.valueChanged.connect(self._init_ui)

#     def _get_connector(self):
#         return self._connector.value if isinstance(self._connector, State) else self._connector

#     @_validate_param(file_path="qtmui.material.stepper", param_name="nonLinear", supported_signatures=Union[State, bool])
#     def _set_nonLinear(self, value):
#         self._nonLinear = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._update_active_step)

#     def _get_nonLinear(self):
#         return self._nonLinear.value if isinstance(self._nonLinear, State) else self._nonLinear

#     @_validate_param(file_path="qtmui.material.stepper", param_name="orientation", supported_signatures=Union[State, str], valid_values=VALID_ORIENTATIONS)
#     def _set_orientation(self, value):
#         self._orientation = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._init_ui)

#     def _get_orientation(self):
#         orientation = self._orientation.value if isinstance(self._orientation, State) else self._orientation
#         return orientation if orientation in self.VALID_ORIENTATIONS else 'horizontal'

#     @_validate_param(file_path="qtmui.material.stepper", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
#     def _set_sx(self, value):
#         self._sx = value
#         if isinstance(value, State):
#             value.valueChanged.connect(self._set_stylesheet)

#     def _get_sx(self):
#         return self._sx.value if isinstance(self._sx, State) else self._sx

#     def _init_ui(self):
#         # Clear existing layout
#         if self.layout():
#             while self.layout().count():
#                 item = self.layout().takeAt(0)
#                 if item.widget():
#                     item.widget().deleteLater()
#                 elif item.layout():
#                     item.layout().deleteLater()

#         # Initialize layout
#         layout_type = QVBoxLayout if self._get_orientation() == 'vertical' else QHBoxLayout
#         self.setLayout(layout_type())
#         self.layout().setContentsMargins(0, 0, 0, 0)
#         self.layout().setSpacing(self.theme.spacing(2))

#         progress_layout = layout_type()
#         progress_layout.setSpacing(self.theme.spacing(2))
#         self.layout().addLayout(progress_layout)

#         # Add steps and connectors
#         children = self._get_children()
#         connector = self._get_connector() or Divider()

#         for index, step in enumerate(children):
#             step.setParent(self)
#             step.set_index(index)
#             step.set_last(index == len(children) - 1)
#             progress_layout.addWidget(step)
#             if index < len(children) - 1:
#                 connector_instance = connector() if callable(connector) else connector
#                 connector_instance.setParent(self)
#                 progress_layout.addWidget(connector_instance)
#                 self._widget_references.append(connector_instance)

#         # Add labels for alternativeLabel in horizontal orientation
#         if self._get_alternativeLabel() and self._get_orientation() == 'horizontal':
#             label_layout = QHBoxLayout()
#             label_layout.setSpacing(self.theme.spacing(2))
#             self.layout().addLayout(label_layout)
#             for index, step in enumerate(children):
#                 label = step._get_label()
#                 if label:
#                     label.setParent(self)
#                     label_layout.addWidget(label)
#                 if index < len(children) - 1:
#                     spacer = Divider(color="transparent")
#                     spacer.setParent(self)
#                     label_layout.addWidget(spacer)
#                     self._widget_references.append(spacer)

#         self._update_active_step()

#     def _set_stylesheet(self):
#         component_styled = self.theme.components
#         stepper_styles = component_styled.get("Stepper", {}).get("styles", {})
#         root_styles = stepper_styles.get("root", {})
#         root_qss = get_qss_style(root_styles)

#         # Handle classes
#         classes = self._get_classes() or {}
#         classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}")

#         # Handle sx
#         sx = self._get_sx()
#         sx_qss = ""
#         if sx:
#             if isinstance(sx, (list, dict)):
#                 sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
#             elif isinstance(sx, Callable):
#                 sx_result = sx()
#                 if isinstance(sx_result, (list, dict)):
#                     sx_qss = get_qss_style(sx_result, class_name=f"#{self.objectName()}")
#                 elif isinstance(sx_result, str):
#                     sx_qss = sx_result
#             elif isinstance(sx, str) and sx != "":
#                 sx_qss = sx

#         stylesheet = f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#                 background: transparent;
#                 padding: {self.theme.spacing(2)}px;
#             }}
#             {sx_qss}
#         """
#         self.setStyleSheet(stylesheet)

#     def _update_active_step(self):
#         active_step = self._get_activeStep()
#         non_linear = self._get_nonLinear()
#         children = self._get_children()

#         for index, step in enumerate(children):
#             if not isinstance(step, Step):
#                 continue
#             if active_step == -1:
#                 step.set_active(False)
#                 step.set_completed(False)
#                 step._set_icon_widget("inactive")
#             elif non_linear:
#                 step.set_active(index == active_step)
#                 step.set_completed(step._get_completed())
#                 step._set_icon_widget("current" if index == active_step else "normal")
#             else:
#                 step.set_active(index == active_step)
#                 step.set_completed(index < active_step)
#                 if index < active_step:
#                     step._set_icon_widget("complete")
#                 elif index == active_step:
#                     step._set_icon_widget("current")
#                 else:
#                     step._set_icon_widget("normal")

#     def _on_destroyed(self):
#         self._widget_references.clear()

#     def generate_stylesheet(self):
#         return self.styleSheet()

#     # Public setters
#     def set_active_step(self, step: int):
#         self._set_activeStep(step)
#         self._update_active_step()

#     def set_orientation(self, orientation: str):
#         self._set_orientation(orientation)
#         self._init_ui()

#     def set_connector(self, connector: QWidget):
#         self._set_connector(connector)
#         self._init_ui()

#     # Public getters
#     def get_active_step(self):
#         return self._get_activeStep()

#     def update_ui(self):
#         self._init_ui()
#         self._set_stylesheet()