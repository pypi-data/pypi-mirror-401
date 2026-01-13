# qtmui/material/chart/chart_radial_bar.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, Callable
from math import radians
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QPainterPath, QFont
)

from qtmui.material.styles import useTheme


# Widget chỉ để vẽ – không có layout → an toàn 100%
class RadialBarCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_chart = parent
        self.setAttribute(Qt.WA_StyledBackground, False)

    def paintEvent(self, event):
        if not self.parent_chart:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        rect = self.rect()
        side = min(rect.width(), rect.height())
        draw_rect = QRectF(
            rect.width() / 2 - side / 2,
            rect.height() / 2 - side / 2,
            side, side
        ).adjusted(20, 20, -20, -20)  # margin đẹp

        center = draw_rect.center()
        max_radius = draw_rect.width() / 2
        inner_radius = max_radius * self.parent_chart.hollow_ratio
        bar_thickness = (max_radius - inner_radius) / max(1, len(self.parent_chart._series))

        # Vẽ từng thanh + track
        for idx, value in enumerate(self.parent_chart._series):
            percentage = value / self.parent_chart.base_value
            angle_span = self.parent_chart.total_angle * percentage

            outer_r = max_radius - idx * bar_thickness
            inner_r = outer_r - bar_thickness * 0.85
            mid_r = (outer_r + inner_r) / 2

            track_rect = QRectF(center.x() - mid_r, center.y() - mid_r, mid_r * 2, mid_r * 2)

            # Track
            track_pen = QPen(QColor(self.parent_chart.track_color), outer_r - inner_r, Qt.SolidLine, Qt.RoundCap)
            p.setPen(track_pen)
            p.drawArc(track_rect.toRect(), self.parent_chart.start_angle * 16, self.parent_chart.total_angle * 16)

            # Thanh chính
            color = QColor(self.parent_chart.colors[idx % len(self.parent_chart.colors)])
            pen = QPen(color, outer_r - inner_r, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen)

            path = QPainterPath()
            path.arcMoveTo(track_rect, self.parent_chart.start_angle)
            path.arcTo(track_rect, self.parent_chart.start_angle, angle_span)
            p.strokePath(path, pen)

        # Total ở giữa
        if self.parent_chart.show_total and self.parent_chart._series:
            total_val = sum(self.parent_chart._series) if self.parent_chart._total is None else self.parent_chart._total
            total_text = (
                self.parent_chart.total_formatter() if callable(self.parent_chart.total_formatter)
                else f"{total_val:,.0f}"
            )

            p.setPen(QColor(self.parent_chart.theme.palette.text.primary))
            # p.setFont(self.parent_chart.theme.typography.h5.font())
            p.drawText(draw_rect.toRect(), Qt.AlignCenter, total_text)

            # Subtitle
            subtitle = self.parent_chart._options.get("title", {}).get("text", "")
            if subtitle:
                p.setPen(QColor(self.parent_chart.theme.palette.text.secondary))
                # p.setFont(self.parent_chart.theme.typography.body2.font())
                p.drawText(draw_rect.adjusted(0, 40, 0, -20).toRect(), Qt.AlignCenter, subtitle)

        p.end()


class ChartRadialBar(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "radialBar",
        series: Optional[List[float]] = None,
        total: Optional[float] = None,
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: Optional[Dict[str, Any]] = None,
        key: Optional[str] = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(16, 16, 16, 8)
        self.layout().setSpacing(8)

        self._series = series or []
        self._total = total
        self._options = options or {}

        if width: self.setFixedWidth(int(width))
        if height: self.setFixedHeight(int(height))
        self.setMinimumSize(200, 240)

        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self.update)

        self.labels = self._options.get("labels", [f"Series {i+1}" for i in range(len(self._series))])
        self.colors = self._options.get("colors", [
            self.theme.palette.primary.main,
            self.theme.palette.secondary.main,
            self.theme.palette.success.main,
            self.theme.palette.warning.main,
            self.theme.palette.error.main,
        ])

        # Canvas vẽ chart
        self.canvas = RadialBarCanvas(self)
        self.layout().addWidget(self.canvas)

        # Label hiển thị % dưới chart
        self.percent_label = QLabel()
        self.percent_label.setAlignment(Qt.AlignCenter)
        self.percent_label.setFont(QFont("Segoe UI", 11))
        self.layout().addWidget(self.percent_label)

        self._prepare_options()
        self._update_percent_text()

    def _prepare_options(self):
        po = self._options.get("plotOptions", {}).get("radialBar", {})
        hollow = po.get("hollow", {}).get("size", "68%")
        self.hollow_ratio = float(hollow.rstrip("%")) / 100 if isinstance(hollow, str) else 0.68
        self.track_color = po.get("track", {}).get("background", "#e0e0e033")

        value_opts = po.get("dataLabels", {}).get("value", {})
        self.show_value = value_opts.get("show", True)

        total_opts = po.get("dataLabels", {}).get("total", {})
        self.show_total = total_opts.get("show", True)
        self.total_formatter = total_opts.get("formatter")

        self.base_value = self._total or 100.0
        self.start_angle = 270
        self.total_angle = 360

    def _update_percent_text(self):
        if not self.show_value or not self._series:
            self.percent_label.setText("")
            return

        parts = []
        for i, val in enumerate(self._series):
            percent = val / self.base_value * 100
            if percent > 0:
                text = f"{percent:.1f}%"
                color = self.colors[i % len(self.colors)]
                parts.append(f'<span style="color:{color}">{text}</span>')
        self.percent_label.setText(" • ".join(parts))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.canvas.update()
        self._update_percent_text()