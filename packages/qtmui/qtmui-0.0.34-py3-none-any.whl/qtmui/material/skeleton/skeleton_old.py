# from typing import Optional, Union, Callable, Any, Dict, List
# import uuid

# from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QSizePolicy
# from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPainterPath, QColor
# from PySide6.QtCore import QPropertyAnimation, QObject, Qt, QRect, Property, QEasingCurve
# from ..widget_base import PyWidgetBase

# from qtmui.material.styles import useTheme
# from qtmui.material.styles.create_theme.components.get_qss_styles import get_qss_style

# class RippleEffect(QObject):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._rectX1 = 0
#         self._rectY1 = 0
#         self._rectWidth = 100  # Chiều rộng của hình chữ nhật
#         self._rectHeight = 40  # Chiều cao của hình chữ nhật
#         self._max_rectX1 = 100  # Khung giới hạn cho hình chữ nhật di chuyển
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

#     # Property bindings for animation
#     rectX1 = Property(int, fget=rectX1, fset=setRectX1)
#     opacity = Property(float, fget=opacity, fset=setOpacity)
#     brush_color = Property(QColor, fget=brush_color, fset=setBrushColor)


# class Skeleton(QPushButton, PyWidgetBase):
#     def __init__(
#                 self,
#                 animation: Union[str, bool] = "pulse",  # Animation của Skeleton: 'pulse', 'wave' hoặc False (không có animation)
#                 children: Optional[Any] = None,  # Optional children để suy ra chiều rộng và chiều cao
#                 classes: Optional[Dict[str, str]] = None,  # Ghi đè hoặc mở rộng styles áp dụng cho component
#                 component: Optional[Any] = None,  # Component được sử dụng cho node gốc
#                 height: Union[int, str] = None,  # Chiều cao của Skeleton
#                 sx: Optional[Union[List[Union[Callable, dict, bool]], Callable, dict, bool]] = None,  # Hệ thống props để định nghĩa CSS tùy chỉnh
#                 variant: str = None,  # Kiểu hiển thị của Skeleton: 'circular', 'rectangular', 'rounded', 'text', v.v.
#                 width: Union[int, str] = 100,  # Chiều rộng của Skeleton
#                 key: str = None,  # Khóa cho component
#                 color: str = "#ededed", 
#                 fullwidth=False, 
#                 custom_radius=None, 
#                 duration=1500, 
#                 startColorAt=QColor(227, 227, 227), 
#                 endColorAt=QColor(217, 217, 217), 
#                 *args, **kwargs
#                 ):
#         super().__init__()

#         # Gán giá trị các thuộc tính cho instance của class
#         self._animation = animation
#         self._color = color

#         self._children = children
#         self._custom_radius = custom_radius
#         self._classes = classes or {}
#         self._component = component

#         self._height = height
#         self._sx = sx or []
#         self._variant = variant
#         self._width = width
#         self._key = key
#         self._height = height

#         self._fullwidth = fullwidth

#         self._duration = duration
#         self._start_color = startColorAt
#         self._end_color = endColorAt

#         self._init_ui()




#     def _init_ui(self):
#         self.setObjectName(str(uuid.uuid4()))

#         if self._variant:
#             if self._variant == "circular":
#                 if not self._width or not self._height:
#                     self._width = self._height = 40
#                 self._radius = self._custom_radius if self._custom_radius is not None else self._height / 2
#                 self.setFixedSize(self._width, self._height)
#             elif self._variant == "text" or self._variant == "rounded":
#                 self._radius = 4
#                 if not self._height:
#                     self._height = 24
#             elif self._variant == "rectangular":
#                 self._radius = 0
#                 if not self._height:
#                     self._height = 60
#             else:
#                 self._radius = self._custom_radius if self._custom_radius is not None else self._height / 2
#                 if not self._height:
#                     self._height = 24

#             if not self._width:
#                 self._fullwidth = True

#             # Thiết lập kích thước cho button
#             if self._fullwidth and self._variant != "circular":
#                 self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#                 self.setMinimumHeight(self._height)
#             else:
#                 if not self._height:
#                     self._height = 40
#                 self.setFixedSize(self._width, self._height)
#         else:
#             if not self._height:
#                 self._height = 24
#             if not self._width:
#                 self._width = 24
#             # Thiết lập kích thước cho button
#             if self._fullwidth:
#                 self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#                 self.setMinimumHeight(self._height)
#             else:
#                 self.setFixedSize(self._width, self._height)
#             self._radius = self._custom_radius if self._custom_radius is not None else self._height / 2

#         # Thiết lập bán kính mặc định

#         self.ripple_effect = RippleEffect(self)
#         self.animation_rectX1 = QPropertyAnimation(self.ripple_effect, b"rectX1", self)
#         self.opacity_animation = QPropertyAnimation(self.ripple_effect, b"opacity", self)
#         self.color_animation = QPropertyAnimation(self.ripple_effect, b"brush_color", self)

#         # Thiết lập animation dựa trên chế độ truyền vào
#         self.set_animation_mode(self._animation)

#         self.slot_set_stylesheet()
#         self.theme = useTheme()
#         self.theme.state.valueChanged.connect(self.slot_set_stylesheet)
#         self.destroyed.connect(self._on_destroyed)

#     def slot_set_stylesheet(self, value=None):
#         self._set_stylesheet()

#     def _set_stylesheet(self, component_styled=None):
#         self.theme = useTheme()

#         if not component_styled:
#             component_styled = self.theme.components

#         PySkeleton_root = component_styled[f"PySkeleton"].get("styles")["root"]
#         PySkeleton_root_qss = get_qss_style(PySkeleton_root)

#         sx_qss = ""
#         if self._sx:
#             if isinstance(self._sx, dict):
#                 sx_qss = get_qss_style(self._sx, class_name=f"#{self.objectName()}")
#             elif isinstance(self._sx, Callable):
#                 sx = self._sx()
#                 if isinstance(sx, dict):
#                     sx_qss = get_qss_style(sx, class_name=f"#{self.objectName()}")
#                 elif isinstance(sx, str):
#                     sx_qss = sx
#             elif isinstance(self._sx, str) and self._sx != "":
#                 sx_qss = self._sx

#         self.setStyleSheet(f"""
#             #{self.objectName()} {{
#                 {PySkeleton_root_qss}
#             }}

#             {sx_qss}

#         """)

#     def set_animation_mode(self, animation):
#         if animation == "wave":
#             self.animation_rectX1.setEasingCurve(QEasingCurve.Linear)
#             self.opacity_animation.setEasingCurve(QEasingCurve.Linear)

#             self.ripple_effect._max_rectX1 = self.width()
#             self.ripple_effect.opacity = 0.3
#             self.animation_rectX1.setStartValue(-self.ripple_effect._rectWidth)
#             self.animation_rectX1.setEndValue(self.width())
#             self.animation_rectX1.setDuration(1500)

#             self.opacity_animation.setStartValue(0.7)
#             self.opacity_animation.setEndValue(0.0)
#             self.opacity_animation.setDuration(1500)

#             self.animation_rectX1.setLoopCount(-1)
#             self.opacity_animation.setLoopCount(-1)

#             self.animation_rectX1.start()
#             self.opacity_animation.start()

#         elif animation == "pulse":
#             # Thiết lập animation thay đổi màu từ startColorAt -> endColorAt -> startColorAt
#             self.color_animation.setKeyValueAt(0.0, self._start_color)  # Bắt đầu với startColorAt
#             self.color_animation.setKeyValueAt(0.5, self._end_color)  # Ở giữa duration, đạt endColorAt
#             self.color_animation.setKeyValueAt(1.0, self._start_color)  # Quay lại startColorAt

#             self.color_animation.setEasingCurve(QEasingCurve.InOutQuad)
#             self.color_animation.setDuration(self._duration)
#             self.color_animation.setLoopCount(-1)
#             self.color_animation.start()

#         elif animation == False:
#             self.animation_rectX1.stop()
#             self.color_animation.stop()
#             self.ripple_effect.setBrushColor(QColor(227, 227, 227))  # Reset màu mặc định

#     def paintEvent(self, event):
#         super().paintEvent(event)
#         if self._animation == "pulse":
#             if self.ripple_effect.brush_color is not None:
#                 painter = QPainter(self)
#                 painter.setRenderHint(QPainter.Antialiasing, True)
#                 painter.setPen(Qt.NoPen)

#                 # Tạo vùng cắt hình chữ nhật bo tròn
#                 clip_path = QPainterPath()
#                 clip_path.addRoundedRect(0, 0, self.width(), self.height(), self._radius, self._radius)  # Giới hạn vùng cắt
#                 painter.setClipPath(clip_path)

#                 # Tạo gradient cho hình chữ nhật với màu của animation
#                 gradient = QLinearGradient(0, 0, self.width(), 0)
#                 gradient.setColorAt(0.0, self.ripple_effect.brush_color)
#                 gradient.setColorAt(1.0, self.ripple_effect.brush_color)

#                 painter.setBrush(QBrush(gradient))

#                 # Vẽ hình chữ nhật bo tròn
#                 rect = QRect(0, 0, self.width(), self.height())
#                 painter.drawRoundedRect(rect, self._radius, self._radius)

#                 painter.end()

#         elif self._animation == "wave":
#             if self.ripple_effect.opacity > 0:
#                 painter = QPainter(self)
#                 painter.setRenderHint(QPainter.Antialiasing, True)
#                 painter.setPen(Qt.NoPen)

#                 # Tạo vùng cắt hình chữ nhật bo tròn
#                 clip_path = QPainterPath()
#                 clip_path.addRoundedRect(0, 0, self.width(), self.height(), self._radius, self._radius)  # Giới hạn vùng cắt
#                 painter.setClipPath(clip_path)

#                 # Tạo gradient cho hình chữ nhật
#                 gradient = QLinearGradient(self.ripple_effect.rectX1, 0,
#                                         self.ripple_effect.rectX1 + self.ripple_effect._rectWidth, 0)
#                 gradient.setColorAt(0.0, QColor(227, 227, 227))  # Màu sáng
#                 gradient.setColorAt(0.5, QColor(217, 217, 217))  # Màu tối ở giữa
#                 gradient.setColorAt(1.0, QColor(227, 227, 227))  # Màu sáng

#                 painter.setBrush(QBrush(gradient))

#                 # Vẽ hình chữ nhật bo tròn
#                 path = QPainterPath()
#                 rect = QRect(self.ripple_effect.rectX1, 0, self.ripple_effect._rectWidth, self.height())
#                 path.addRoundedRect(rect, self._radius, self._radius)  # Bo góc tròn với radius tùy chỉnh
#                 painter.drawPath(path)

#                 painter.end()

