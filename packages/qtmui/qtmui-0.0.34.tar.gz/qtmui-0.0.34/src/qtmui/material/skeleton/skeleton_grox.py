# from typing import Optional, Union, Callable, Any, Dict, List
# import uuid

# from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QSizePolicy
# from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPainterPath
# from PySide6.QtCore import QPropertyAnimation, QObject, Qt, QRect, Property, QEasingCurve
# from ..widget_base import PyWidgetBase
# from qtmui.material.styles import useTheme
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style
# from qtmui.hooks import State
# from ..utils.validate_params import _validate_param

# class RippleEffect(QObject):
#     """
#     A helper class to manage ripple animation effects for Skeleton.

#     Parameters
#     ----------
#     parent : QObject, optional
#         The parent object. Default is None.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._rectX1 = 0
#         self._rectY1 = 0
#         self._rectWidth = 100
#         self._rectHeight = 40
#         self._max_rectX1 = 100
#         self._opacity = 1.0
#         self._brush_color = QColor(227, 227, 227)

#     def rectX1(self):
#         return self._rectX1

#     def setRectX1(self, rectX1):
#         self._rectX1 = rectX1
#         self.parent().update()

#     def opacity(self):
#         return self._opacity

#     def setOpacity(self, opacity):
#         self._opacity = opacity
#         self.parent().update()

#     def brush_color(self):
#         return self._brush_color

#     def setBrushColor(self, brush_color):
#         self._brush_color = brush_color
#         self.parent().update()

#     rectX1 = Property(int, fget=rectX1, fset=setRectX1)
#     opacity = Property(float, fget=opacity, fset=setOpacity)
#     brush_color = Property(QColor, fget=brush_color, fset=setBrushColor)

# class Skeleton(PyWidgetBase):
#     """
#     A skeleton component, styled like Material-UI Skeleton.

#     The `Skeleton` component is a placeholder used to indicate loading content. It supports
#     animations and variants, aligning with MUI Skeleton props. Inherits from native component props.

#     Parameters
#     ----------
#     animation : State, str, or bool, optional
#         The animation type ('pulse', 'wave', False). Default is 'pulse'.
#         Can be a `State` object for dynamic updates.
#     children : State or QWidget, optional
#         Optional children to infer width and height from. Default is None.
#         Can be a `State` object for dynamic updates.
#     classes : State or Dict, optional
#         Override or extend styles applied to the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     component : State or type, optional
#         The component used for the root node. Default is None (uses QPushButton).
#         Can be a `State` object for dynamic updates.
#     height : State, int, or str, optional
#         Height of the skeleton. Default is None.
#         Can be a `State` object for dynamic updates.
#     sx : State, List, Dict, Callable, or None, optional
#         System prop for CSS overrides. Default is None.
#         Can be a `State` object for dynamic updates.
#     variant : State or str, optional
#         Type of skeleton ('circular', 'rectangular', 'rounded', 'text'). Default is None.
#         Can be a `State` object for dynamic updates.
#     width : State, int, or str, optional
#         Width of the skeleton. Default is 100.
#         Can be a `State` object for dynamic updates.
#     key : State or str, optional
#         Key for the component. Default is None.
#         Can be a `State` object for dynamic updates.
#     color : State or str, optional
#         Background color of the skeleton. Default is '#ededed'.
#         Can be a `State` object for dynamic updates.
#     fullwidth : State or bool, optional
#         If True, skeleton takes full width. Default is False.
#         Can be a `State` object for dynamic updates.
#     custom_radius : State, int, or None, optional
#         Custom radius for rounded corners. Default is None.
#         Can be a `State` object for dynamic updates.
#     duration : State or int, optional
#         Duration of the animation in milliseconds. Default is 1500.
#         Can be a `State` object for dynamic updates.
#     startColorAt : State or QColor, optional
#         Starting color for pulse animation. Default is QColor(227, 227, 227).
#         Can be a `State` object for dynamic updates.
#     endColorAt : State or QColor, optional
#         Ending color for pulse animation. Default is QColor(217, 217, 217).
#         Can be a `State` object for dynamic updates.
#     **kwargs
#         Additional keyword arguments passed to the parent component,
#         supporting native component props.

#     Notes
#     -----
#     - Existing parameters (14) are retained and aligned with MUI Skeleton.
#     - MUI classes applied: `MuiSkeleton-root`.
#     - Integrates with `RippleEffect` for animations.

#     Demos:
#     - Skeleton: https://qtmui.com/material-ui/qtmui-skeleton/

#     API Reference:
#     - Skeleton API: https://qtmui.com/material-ui/api/skeleton/
#     """

#     VALID_ANIMATIONS = ['pulse', 'wave', False]
#     VALID_VARIANTS = ['circular', 'rectangular', 'rounded', 'text']

#     def __init__(
#         self,
#         animation: Union[State, str, bool] = "pulse",
#         children: Optional[Union[State, QWidget]] = None,
#         classes: Optional[Union[State, Dict]] = None,
#         component: Optional[Union[State, type]] = None,
#         height: Optional[Union[State, int, str]] = None,
#         sx: Optional[Union[State, List, Dict, Callable]] = None,
#         variant: Optional[Union[State, str]] = None,
#         width: Optional[Union[State, int, str]] = 100,
#         key: Optional[Union[State, str]] = None,
#         color: Optional[Union[State, str]] = "#ededed",
#         fullwidth: Union[State, bool] = False,
#         custom_radius: Optional[Union[State, int]] = None,
#         duration: Union[State, int] = 1500,
#         startColorAt: Union[State, QColor] = QColor(227, 227, 227),
#         endColorAt: Union[State, QColor] = QColor(217, 217, 217),
#         *args, **kwargs
#     ):
#         # Use component if provided, else default to QPushButton
#         root_component = (component.value if isinstance(component, State) else component) or QPushButton
#         super().__init__(*args, **kwargs)
#         self.__class__ = type('Skeleton', (root_component, PyWidgetBase), {})
#         self.theme = useTheme()
#         self._widget_references = []

#         # Set properties with validation
#         self._set_animation(animation)
#         self._set_children(children)
#         self._set_classes(classes)
#         self._set_component(component)
#         self._set_height(height)
#         self._set_sx(sx)
#         self._set_variant(variant)
#         self._set_width(width)
#         self._set_key(key)
#         self._set_color(color)
#         self._set_fullwidth(fullwidth)
#         self._set_custom_radius(custom_radius)
#         self._set_duration(duration)
#         self._set_startColorAt(startColorAt)
#         self._set_endColorAt(endColorAt)

#         self._init_ui()
#         self.slot_set_stylesheet()
#         self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
#         self.destroyed.connect(self._on_destroyed)
#         self._connect_signals()

#     # Setter and Getter methods
#     @_validate_param(file_path="qtmui.material.skeleton", param_name="animation", supported_signatures=Union[State, str, bool], valid_values=VALID_ANIMATIONS)
#     def _set_animation(self, value):
#         """Assign value to animation."""
#         self._animation = value
#         if hasattr(self, 'ripple_effect'):
#             self.set_animation_mode(self._get_animation())

#     def _get_animation(self):
#         """Get the animation value."""
#         return self._animation.value if isinstance(self._animation, State) else self._animation

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="children", supported_signatures=Union[State, QWidget, type(None)])
#     def _set_children(self, value):
#         """Assign value to children."""
#         self._children = value
#         if isinstance(value, QWidget):
#             self._widget_references.append(value)
#         elif isinstance(value, State) and isinstance(value.value, QWidget):
#             self._widget_references.append(value.value)

#     def _get_children(self):
#         """Get the children value."""
#         return self._children.value if isinstance(self._children, State) else self._children

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="classes", supported_signatures=Union[State, Dict, type(None)])
#     def _set_classes(self, value):
#         """Assign value to classes."""
#         self._classes = value

#     def _get_classes(self):
#         """Get the classes value."""
#         return self._classes.value if isinstance(self._classes, State) else self._classes

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="component", supported_signatures=Union[State, type, type(None)])
#     def _set_component(self, value):
#         """Assign value to component."""
#         self._component = value

#     def _get_component(self):
#         """Get the component value."""
#         return self._component.value if isinstance(self._component, State) else self._component

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="height", supported_signatures=Union[State, int, str, type(None)])
#     def _set_height(self, value):
#         """Assign value to height."""
#         self._height = value

#     def _get_height(self):
#         """Get the height value."""
#         return self._height.value if isinstance(self._height, State) else self._height

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="sx", supported_signatures=Union[State, List, Dict, Callable, type(None)])
#     def _set_sx(self, value):
#         """Assign value to sx."""
#         self._sx = value

#     def _get_sx(self):
#         """Get the sx value."""
#         return self._sx.value if isinstance(self._sx, State) else self._sx

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="variant", supported_signatures=Union[State, str, type(None)], valid_values=VALID_VARIANTS)
#     def _set_variant(self, value):
#         """Assign value to variant."""
#         self._variant = value

#     def _get_variant(self):
#         """Get the variant value."""
#         return self._variant.value if isinstance(self._variant, State) else self._variant

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="width", supported_signatures=Union[State, int, str, type(None)])
#     def _set_width(self, value):
#         """Assign value to width."""
#         self._width = value

#     def _get_width(self):
#         """Get the width value."""
#         return self._width.value if isinstance(self._width, State) else self._width

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="key", supported_signatures=Union[State, str, type(None)])
#     def _set_key(self, value):
#         """Assign value to key."""
#         self._key = value

#     def _get_key(self):
#         """Get the key value."""
#         return self._key.value if isinstance(self._key, State) else self._key

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="color", supported_signatures=Union[State, str, type(None)])
#     def _set_color(self, value):
#         """Assign value to color."""
#         self._color = value

#     def _get_color(self):
#         """Get the color value."""
#         return self._color.value if isinstance(self._color, State) else self._color

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="fullwidth", supported_signatures=Union[State, bool])
#     def _set_fullwidth(self, value):
#         """Assign value to fullwidth."""
#         self._fullwidth = value

#     def _get_fullwidth(self):
#         """Get the fullwidth value."""
#         return self._fullwidth.value if isinstance(self._fullwidth, State) else self._fullwidth

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="custom_radius", supported_signatures=Union[State, int, type(None)])
#     def _set_custom_radius(self, value):
#         """Assign value to custom_radius."""
#         self._custom_radius = value

#     def _get_custom_radius(self):
#         """Get the custom_radius value."""
#         return self._custom_radius.value if isinstance(self._custom_radius, State) else self._custom_radius

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="duration", supported_signatures=Union[State, int])
#     def _set_duration(self, value):
#         """Assign value to duration."""
#         self._duration = value

#     def _get_duration(self):
#         """Get the duration value."""
#         return self._duration.value if isinstance(self._duration, State) else self._duration

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="startColorAt", supported_signatures=Union[State, QColor])
#     def _set_startColorAt(self, value):
#         """Assign value to startColorAt."""
#         self._startColorAt = value

#     def _get_startColorAt(self):
#         """Get the startColorAt value."""
#         return self._startColorAt.value if isinstance(self._startColorAt, State) else self._startColorAt

#     @_validate_param(file_path="qtmui.material.skeleton", param_name="endColorAt", supported_signatures=Union[State, QColor])
#     def _set_endColorAt(self, value):
#         """Assign value to endColorAt."""
#         self._endColorAt = value

#     def _get_endColorAt(self):
#         """Get the endColorAt value."""
#         return self._endColorAt.value if isinstance(self._endColorAt, State) else self._endColorAt

#     def _init_ui(self):
#         """Initialize the UI based on props."""
#         self.setObjectName(str(uuid.uuid4()))

#         # Infer size from children if not provided
#         children = self._get_children()
#         if children and isinstance(children, QWidget) and (not self._get_width() or not self._get_height()):
#             size = children.sizeHint()
#             self._width = self._width or size.width()
#             self._height = self._height or size.height()

#         # Set variant-specific properties
#         if self._get_variant():
#             if self._get_variant() == "circular":
#                 self._width = self._height = self._get_width() or self._get_height() or 40
#                 self._radius = self._get_custom_radius() if self._get_custom_radius() is not None else self._height / 2
#                 self.setFixedSize(self._width, self._height)
#             elif self._get_variant() == "text":
#                 self._radius = self._get_custom_radius() if self._get_custom_radius() is not None else 4
#                 self._height = self._get_height() or 24
#             elif self._get_variant() == "rounded":
#                 self._radius = self._get_custom_radius() if self._get_custom_radius() is not None else 4
#                 self._height = self._get_height() or 24
#             elif self._get_variant() == "rectangular":
#                 self._radius = self._get_custom_radius() if self._get_custom_radius() is not None else 0
#                 self._height = self._get_height() or 60
#             if not self._get_width() and self._get_fullwidth():
#                 self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#                 self.setMinimumHeight(self._height)
#             else:
#                 self.setFixedSize(self._get_width() or 100, self._height)
#         else:
#             self._radius = self._get_custom_radius() if self._get_custom_radius() is not None else (self._get_height() or 24) / 2
#             self._height = self._get_height() or 24
#             self._width = self._get_width() or 100
#             if self._get_fullwidth():
#                 self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#                 self.setMinimumHeight(self._height)
#             else:
#                 self.setFixedSize(self._width, self._height)

#         # Initialize ripple effect and animations
#         self.ripple_effect = RippleEffect(self)
#         self.animation_rectX1 = QPropertyAnimation(self.ripple_effect, b"rectX1", self)
#         self.opacity_animation = QPropertyAnimation(self.ripple_effect, b"opacity", self)
#         self.color_animation = QPropertyAnimation(self.ripple_effect, b"brush_color", self)

#         # Set animation mode
#         self.set_animation_mode(self._get_animation())

#     def slot_set_stylesheet(self, value=None):
#         """Set the stylesheet for the Skeleton."""
#         self._set_stylesheet()

#     def _set_stylesheet(self, component_styled=None):
#         """Apply stylesheet based on theme and props."""
#         self.theme = useTheme()
#         component_styled = component_styled or self.theme.components
#         skeleton_styles = component_styled.get("Skeleton", {}).get("styles", {})
#         root_styles = skeleton_styles.get("root", {})
#         root_qss = get_qss_style(root_styles)

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

#         # Handle classes
#         classes = self._get_classes()
#         classes_qss = get_qss_style(classes, class_name=f"#{self.objectName()}") if classes else ""

#         # Apply MUI classes
#         mui_classes = ["MuiSkeleton-root"]

#         stylesheet = f"""
#             #{self.objectName()} {{
#                 {root_qss}
#                 {classes_qss}
#                 background: {self._get_color() or '#ededed'};
#             }}
#             {sx_qss}
#         """
#         self.setStyleSheet(stylesheet)

#     def set_animation_mode(self, animation):
#         """Set the animation mode for the skeleton."""
#         if animation == "wave":
#             self.animation_rectX1.setEasingCurve(QEasingCurve.Linear)
#             self.opacity_animation.setEasingCurve(QEasingCurve.Linear)

#             self.ripple_effect._max_rectX1 = self.width()
#             self.ripple_effect.opacity = 0.3
#             self.animation_rectX1.setStartValue(-self.ripple_effect._rectWidth)
#             self.animation_rectX1.setEndValue(self.width())
#             self.animation_rectX1.setDuration(self._get_duration())

#             self.opacity_animation.setStartValue(0.7)
#             self.opacity_animation.setEndValue(0.0)
#             self.opacity_animation.setDuration(self._get_duration())

#             self.animation_rectX1.setLoopCount(-1)
#             self.opacity_animation.setLoopCount(-1)

#             self.animation_rectX1.start()
#             self.opacity_animation.start()

#         elif animation == "pulse":
#             self.color_animation.setKeyValueAt(0.0, self._get_startColorAt())
#             self.color_animation.setKeyValueAt(0.5, self._get_endColorAt())
#             self.color_animation.setKeyValueAt(1.0, self._get_startColorAt())

#             self.color_animation.setEasingCurve(QEasingCurve.InOutQuad)
#             self.color_animation.setDuration(self._get_duration())
#             self.color_animation.setLoopCount(-1)
#             self.color_animation.start()

#         elif animation is False:
#             self.animation_rectX1.stop()
#             self.opacity_animation.stop()
#             self.color_animation.stop()
#             self.ripple_effect.setBrushColor(QColor(227, 227, 227))

#     def paintEvent(self, event):
#         """Custom paint event for rendering skeleton with animation."""
#         super().paintEvent(event)
#         if self._get_animation() == "pulse" and self.ripple_effect.brush_color is not None:
#             painter = QPainter(self)
#             painter.setRenderHint(QPainter.Antialiasing, True)
#             painter.setPen(Qt.NoPen)

#             clip_path = QPainterPath()
#             clip_path.addRoundedRect(0, 0, self.width(), self.height(), self._radius, self._radius)
#             painter.setClipPath(clip_path)

#             gradient = QLinearGradient(0, 0, self.width(), 0)
#             gradient.setColorAt(0.0, self.ripple_effect.brush_color)
#             gradient.setColorAt(1.0, self.ripple_effect.brush_color)

#             painter.setBrush(QBrush(gradient))
#             rect = QRect(0, 0, self.width(), self.height())
#             painter.drawRoundedRect(rect, self._radius, self._radius)

#             painter.end()

#         elif self._get_animation() == "wave" and self.ripple_effect.opacity > 0:
#             painter = QPainter(self)
#             painter.setRenderHint(QPainter.Antialiasing, True)
#             painter.setPen(Qt.NoPen)

#             clip_path = QPainterPath()
#             clip_path.addRoundedRect(0, 0, self.width(), self.height(), self._radius, self._radius)
#             painter.setClipPath(clip_path)

#             gradient = QLinearGradient(self.ripple_effect.rectX1, 0,
#                                       self.ripple_effect.rectX1 + self.ripple_effect._rectWidth, 0)
#             gradient.setColorAt(0.0, QColor(227, 227, 227))
#             gradient.setColorAt(0.5, QColor(217, 217, 217))
#             gradient.setColorAt(1.0, QColor(227, 227, 227))

#             painter.setBrush(QBrush(gradient))
#             path = QPainterPath()
#             rect = QRect(self.ripple_effect.rectX1, 0, self.ripple_effect._rectWidth, self.height())
#             path.addRoundedRect(rect, self._radius, self._radius)
#             painter.drawPath(path)

#             painter.end()

#     def _connect_signals(self):
#         """Connect valueChanged signals of State parameters to their slots."""
#         if isinstance(self._animation, State):
#             self._animation.valueChanged.connect(self._on_animation_changed)
#         if isinstance(self._children, State):
#             self._children.valueChanged.connect(self._on_children_changed)
#         if isinstance(self._classes, State):
#             self._classes.valueChanged.connect(self.slot_set_stylesheet)
#         if isinstance(self._height, State):
#             self._height.valueChanged.connect(self._on_size_changed)
#         if isinstance(self._sx, State):
#             self._sx.valueChanged.connect(self.slot_set_stylesheet)
#         if isinstance(self._variant, State):
#             self._variant.valueChanged.connect(self._on_variant_changed)
#         if isinstance(self._width, State):
#             self._width.valueChanged.connect(self._on_size_changed)
#         if isinstance(self._color, State):
#             self._color.valueChanged.connect(self.slot_set_stylesheet)
#         if isinstance(self._fullwidth, State):
#             self._fullwidth.valueChanged.connect(self._on_size_changed)
#         if isinstance(self._custom_radius, State):
#             self._custom_radius.valueChanged.connect(self._on_variant_changed)
#         if isinstance(self._duration, State):
#             self._duration.valueChanged.connect(self._on_duration_changed)
#         if isinstance(self._startColorAt, State):
#             self._startColorAt.valueChanged.connect(self._on_colors_changed)
#         if isinstance(self._endColorAt, State):
#             self._endColorAt.valueChanged.connect(self._on_colors_changed)

#     def _on_animation_changed(self):
#         """Handle animation change."""
#         self.set_animation_mode(self._get_animation())

#     def _on_children_changed(self):
#         """Handle children change."""
#         self._init_ui()

#     def _on_size_changed(self):
#         """Handle size change."""
#         self._init_ui()

#     def _on_variant_changed(self):
#         """Handle variant change."""
#         self._init_ui()

#     def _on_duration_changed(self):
#         """Handle duration change."""
#         self.set_animation_mode(self._get_animation())

#     def _on_colors_changed(self):
#         """Handle colors change."""
#         self.set_animation_mode(self._get_animation())

#     def _on_destroyed(self):
#         """Clean up on destruction."""
#         self._widget_references.clear()