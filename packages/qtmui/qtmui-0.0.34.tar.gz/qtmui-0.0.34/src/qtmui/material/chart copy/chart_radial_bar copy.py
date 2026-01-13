from __future__ import annotations
from typing import Optional, Union
from math import pi, cos, sin
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QGradient, QLinearGradient, QPainter, QColor, QBrush, QFont, QPen, QPainterPath

from qtmui.material.styles import useTheme

class ChartRadialBar(QWidget):
    def __init__(
        self,
        series: list = None,   # Ví dụ: [76]
        total: int = None,     # Tổng giá trị dùng làm tham chiếu; nếu không truyền, mặc định là 100
        options: dict = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._series = series or []
        # Nếu total không được truyền vào, mặc định dùng 100
        self._total = total if total is not None else 100
        self._options = options or {}
        self._width = int(width) if width else 200
        self._height = int(height) if height else 200
        self.theme = useTheme()
        
        self.setMinimumSize(self._width, self._height)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._init_widget()
        
        self.useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_widget(self):
        if self._width:
            self.setFixedWidth(self._width)
        if self._height:
            self.setFixedHeight(self._height)
        self._add_center_label()

    def upd(self, data: list):
         self._series = data
         self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), self.theme.palette.background.paper)
        
        # Tính toán hình chữ nhật vẽ, giảm bớt cho pen width
        rect = self.rect().adjusted(8, 8, -8, -8)
        side = min(rect.width(), rect.height())
        x = rect.x() + (rect.width() - side) / 2
        y = rect.y() + (rect.height() - side) / 2
        draw_rect = QRectF(x, y, side, side)
        
        # Lấy các thông số radialBar từ options.plotOptions.radialBar
        plotOpts = self._options.get("plotOptions", {}).get("radialBar", {})
        start_angle = plotOpts.get("startAngle", -90)
        end_angle = plotOpts.get("endAngle", 90)
        total_span = end_angle - start_angle  # ví dụ: 180
        
        # Tính hollow size nếu có, giả sử dạng "56%"
        hollowOpts = plotOpts.get("hollow", {})
        hollow_size_str = hollowOpts.get("size", "0%")
        try:
            hollow_ratio = float(hollow_size_str.strip('%')) / 100.0
        except Exception:
            hollow_ratio = 0
        
        outer_radius = draw_rect.width() / 2
        if hollow_ratio > 0:
            inner_radius = outer_radius * hollow_ratio
            pen_width = outer_radius - inner_radius
            # Vẽ arc ở vị trí trung bình giữa outer và inner
            arc_center_radius = (outer_radius + inner_radius) / 2
        else:
            inner_radius = 0
            pen_width = 8
            arc_center_radius = outer_radius - pen_width / 2
        
        # Tạo gradient brush từ options.fill.gradient.colorStops nếu có
        fillOpts = self._options.get("fill", {})
        if fillOpts.get("type") == "gradient":
            gradientOpts = fillOpts.get("gradient", {})
            colorStops = gradientOpts.get("colorStops", [])
            if len(colorStops) >= 2:
                grad = QLinearGradient(draw_rect.topLeft(), draw_rect.bottomLeft())
                color0 = colorStops[0].get("color", "#00c6ff")
                color1 = colorStops[1].get("color", "#0072ff")
                grad.setColorAt(0, QColor(color0))
                grad.setColorAt(1, QColor(color1))
                brush = QBrush(grad)
            else:
                brush = QBrush(QColor(self.theme.palette.primary.main))
        else:
            brush = QBrush(QColor(self.theme.palette.primary.main))
        
        # Lấy progress từ series (giả sử series[0] là số, ví dụ 76)
        progress = 0
        if self._series:
            try:
                progress = float(self._series[0])
            except Exception:
                progress = 0
        
        # Tính góc span của progress
        progress_span = progress / 100 * total_span
        
        # Tính rectangle chứa arc dựa trên arc_center_radius
        center = draw_rect.center()
        arc_rect = QRectF(
            center.x() - arc_center_radius,
            center.y() - arc_center_radius,
            2 * arc_center_radius,
            2 * arc_center_radius
        )
        
        path = QPainterPath()
        path.arcMoveTo(arc_rect, start_angle)
        path.arcTo(arc_rect, start_angle, progress_span)
        
        pen = QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setBrush(brush)
        pen.setWidthF(pen_width)
        p.strokePath(path, pen)
        
        p.end()

    def _add_center_label(self):
        if self._total is None:
            return
        
        # Nếu có cấu hình dataLabels.total trong options, sử dụng nó; nếu không, dùng fallback
        plotOpts = self._options.get("plotOptions", {}).get("radialBar", {})
        dataLabels = plotOpts.get("dataLabels", {})
        totalOpts = dataLabels.get("total", {})
        if totalOpts:
            total_text = totalOpts.get("label", f"Used of {self._series[0] / 100 * self._total} / {self._total}GB")
            fontSize = totalOpts.get("fontSize", self.theme.typography.body2.fontSize)
            fontWeight = totalOpts.get("fontWeight", self.theme.typography.body2.fontWeight)
            color = totalOpts.get("color", self.theme.palette.text.disabled)
        else:
            total_text = f"Used of {self._series[0] / 100 * self._total} / {self._total}GB"
            fontSize = "14px"
            fontWeight = "bold"
            color = self.theme.palette.text.primary
        
        self.total_value_label = QLabel(total_text, self)
        self.total_value_label.setAlignment(Qt.AlignCenter)
        self.total_value_label.setStyleSheet(f"color: {color}; font-size: {fontSize}; font-weight: {fontWeight};")
        
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.total_value_label)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        center_widget = QWidget(self)
        center_widget.setLayout(center_layout)
        self.layout().addWidget(center_widget)
        self.layout().setAlignment(Qt.AlignCenter)
        
        # Cập nhật vị trí khi kích thước thay đổi
        self.resizeEvent = lambda event: self._update_center_label_position(center_widget)

    def _update_center_label_position(self, center_widget):
        rect = self.rect().adjusted(8, 8, -8, -8)
        side = min(rect.width(), rect.height())
        x = rect.x() + (rect.width() - side) / 2
        y = rect.y() + (rect.height() - side) / 2
        draw_rect = QRectF(x, y, side, side)
        center_widget.setGeometry(QRectF(draw_rect).toRect())

    def _set_stylesheet(self):
        self.theme = useTheme()
        self.update()
        if hasattr(self, "total_value_label"):
            self.total_value_label.setStyleSheet(f"color: {self.theme.palette.text.primary}; font-size: 14px; font-weight: bold;")
