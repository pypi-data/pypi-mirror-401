from __future__ import annotations

from typing import Callable, Optional, Union, List, Dict
import math

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QPainterPath
from PySide6.QtCore import Qt, QPointF, QRectF

from qtmui.hooks import State
from qtmui.material.styles import useTheme


class ChartPolarArea(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        series: Optional[Union[List[Dict], List[float]]] = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: Optional[Dict] = None,
        key: str = None,
        title: Optional[Union[State, str, Callable]] = None,
        *args,
        **kwargs,
    ):
        """
        Nếu `series` là danh sách dict thì mong đợi có các key: "label", "value".
        Nếu là danh sách số thì dùng thêm options để truyền danh sách nhãn.
        """
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._options = options or {}
        self._title = title

        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)

        # Xử lý dữ liệu đầu vào
        if series and all(isinstance(item, dict) for item in series):
            self.values = [item.get("value", 0) for item in series]
            self.labels = [item.get("label", f"Category {i+1}") for i, item in enumerate(series)]
        elif series and all(isinstance(item, (int, float)) for item in series):
            self.values = series
            self.labels = self._options.get("labels", [f"Category {i+1}" for i in range(len(series))])
        else:
            self.values = []
            self.labels = []

        # Các màu sắc cho từng phân vùng, dùng options nếu có
        self.colors = self._options.get("colors", [
            "#ADD8E6",  # xanh lam nhạt
            "#FFFF00",  # vàng
            "#90EE90",  # xanh lá cây nhạt
            "#00008B",  # xanh lam đậm
            "#00CED1",  # xanh ngọc lam
            "#FFA500",  # cam
            "#006400",  # xanh lá cây đậm
            "#A52A2A",  # nâu
        ])
        # Màu stroke cho đường viền (mặc định dùng màu nền của theme)
        self.stroke_color = self._options.get("stroke", {}).get("colors", [useTheme().palette.background.paper])[0]
        # Độ mờ của màu fill (opacity từ 0 đến 1)
        self.fill_opacity = self._options.get("fill", {}).get("opacity", 0.8)
        # Giá trị tối đa hiển thị trên trục (theo mô tả: 25)
        self.max_value = 25

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        full_rect = self.rect()

        # Dành không gian cho biểu đồ và legend:
        legend_width = 120  # độ rộng dành cho legend bên phải
        chart_rect = full_rect.adjusted(0, 0, -legend_width, 0)

        center = QPointF(chart_rect.width() / 2, chart_rect.height() / 2)
        # Dịch chuyển tâm chart theo vị trí của chart_rect
        center.setX(center.x() + chart_rect.left())
        center.setY(center.y() + chart_rect.top())

        outer_radius = min(chart_rect.width(), chart_rect.height()) * 0.45

        # 1. Vẽ các vòng tròn đồng tâm (tick: 5, 10, 15, 20, 25)
        pen = QPen(QColor(self.stroke_color))
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        ticks = [5, 10, 15, 20, 25]
        for tick in ticks:
            r = (tick / self.max_value) * outer_radius
            painter.drawEllipse(center, r, r)
            # Vẽ nhãn tick bên phải vòng tròn
            painter.drawText(QPointF(center.x() + r + 2, center.y()), f"{tick}")

        # 2. Vẽ các trục (spokes)
        n = len(self.values)
        if n == 0:
            return
        sector_angle = 360 / n
        pen_spoke = QPen(QColor(self.stroke_color))
        pen_spoke.setStyle(Qt.SolidLine)
        painter.setPen(pen_spoke)
        for i in range(n):
            angle_deg = i * sector_angle
            angle_rad = math.radians(angle_deg)
            x = center.x() + outer_radius * math.cos(angle_rad)
            y = center.y() - outer_radius * math.sin(angle_rad)
            painter.drawLine(center, QPointF(x, y))
            # Vẽ nhãn cho mỗi trục (chú thích của danh mục) ngay ngoài biên chart
            label = self.labels[i] if i < len(self.labels) else f"Category {i+1}"
            label_x = center.x() + (outer_radius + 10) * math.cos(angle_rad)
            label_y = center.y() - (outer_radius + 10) * math.sin(angle_rad)
            painter.drawText(QPointF(label_x, label_y), label)

        # 3. Vẽ các phân vùng màu (Polar Area Chart kiểu Nightingale)
        for i, value in enumerate(self.values):
            r_value = (value / self.max_value) * outer_radius
            angle_center = i * sector_angle
            half_sector = sector_angle / 2
            start_angle = angle_center - half_sector
            end_angle = angle_center + half_sector

            # Tạo đường viền (path) cho sector
            path = QPainterPath()
            path.moveTo(center)
            start_rad = math.radians(start_angle)
            start_point = QPointF(
                center.x() + r_value * math.cos(start_rad),
                center.y() - r_value * math.sin(start_rad)
            )
            path.lineTo(start_point)
            # Vẽ cung với các điểm trung gian
            steps = 30
            for step in range(1, steps + 1):
                interp_angle = start_angle + (end_angle - start_angle) * (step / steps)
                interp_rad = math.radians(interp_angle)
                pt = QPointF(
                    center.x() + r_value * math.cos(interp_rad),
                    center.y() - r_value * math.sin(interp_rad)
                )
                path.lineTo(pt)
            path.lineTo(center)
            path.closeSubpath()

            # Lấy màu theo thứ tự, áp dụng độ mờ
            color = QColor(self.colors[i % len(self.colors)])
            color.setAlphaF(self.fill_opacity)
            painter.fillPath(path, QBrush(color))
            # Vẽ viền cho sector
            painter.setPen(QPen(QColor(self.stroke_color)))
            painter.drawPath(path)

        # 4. Vẽ tiêu đề (nếu có)
        if self._title:
            title_font = QFont()
            title_font.setBold(True)
            title_font.setPointSize(10)
            painter.setFont(title_font)
            painter.drawText(chart_rect.adjusted(10, 10, -10, -10), Qt.AlignTop | Qt.AlignHCenter, self._title)

        # 5. Vẽ legend (chú thích màu) bên phải biểu đồ
        legend_rect = QRectF(chart_rect.right() + 10, chart_rect.top(), legend_width - 10, full_rect.height())
        legend_font = QFont()
        legend_font.setPointSize(8)
        painter.setFont(legend_font)

        # Đặt màu văn bản cho legend rõ ràng (sử dụng màu text của theme)
        text_color = QColor(useTheme().palette.text.primary)
        
        swatch_size = 12
        spacing = 4
        y_offset = legend_rect.top() + 20  # vị trí bắt đầu vẽ legend

        for i, label in enumerate(self.labels):
            # Chọn màu từ danh sách colors
            color = QColor(self.colors[i % len(self.colors)])
            # Vẽ hình vuông màu (swatch)
            swatch_rect = QRectF(legend_rect.left(), y_offset, swatch_size, swatch_size)
            painter.fillRect(swatch_rect, QBrush(color))
            painter.setPen(QPen(QColor(self.stroke_color)))
            painter.drawRect(swatch_rect)
            # Tạo bounding rect cho text legend
            text_rect = QRectF(swatch_rect.right() + spacing, y_offset, legend_rect.width() - swatch_size - spacing, swatch_size)
            value_text = f"{self.values[i]}" if i < len(self.values) else ""
            full_text = f"{label}: {value_text}"
            painter.setPen(text_color)
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, full_text)
            y_offset += swatch_size + spacing + 4

        painter.end()
