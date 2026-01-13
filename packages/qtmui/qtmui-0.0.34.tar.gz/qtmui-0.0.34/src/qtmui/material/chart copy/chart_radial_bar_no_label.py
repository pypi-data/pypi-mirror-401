# qtmui/material/chart/chart_radial_bar.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, Callable
from math import cos, radians, sin
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter, QColor, QBrush, QPen, QPainterPath, QFontMetrics
)

from qtmui.material.styles import useTheme


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
        self._series = series or []
        self._total = total  # nếu có thì dùng làm base 100%
        self._options = options or {}
        self._width = int(width) if width else None
        self._height = int(height) if height else None

        if self._width: self.setFixedWidth(self._width)
        if self._height: self.setFixedHeight(self._height)
        self.setMinimumSize(180, 180)

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

        self._prepare_options()

    def _prepare_options(self):
        po = self._options.get("plotOptions", {}).get("radialBar", {})

        # Hollow size
        hollow = po.get("hollow", {}).get("size", "65%")
        self.hollow_ratio = float(hollow.rstrip("%")) / 100 if isinstance(hollow, str) else 0.65

        # Track (nền)
        self.track_color = po.get("track", {}).get("background", "#e0e0e033")
        self.track_opacity = po.get("track", {}).get("opacity", 0.2)

        # Data labels
        self.data_labels = po.get("dataLabels", {})
        self.show_names = self.data_labels.get("name", {}).get("show", True)
        self.show_values = self.data_labels.get("value", {}).get("show", True)

        # Total
        total_opts = self.data_labels.get("total", {})
        self.show_total = total_opts.get("show", True)
        self.total_formatter = total_opts.get("formatter")

        # Start từ 12h (top), đi theo chiều kim đồng hồ
        self.start_angle = 270  # 12h
        self.total_angle = 360

        # Base value
        self.base_value = self._total or 100.0

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        rect = self.rect()
        side = min(rect.width(), rect.height())
        draw_rect = QRectF(
            rect.width() / 2 - side / 2 + 16,
            rect.height() / 2 - side / 2 + 16,
            side - 32,
            side - 32
        )
        center = draw_rect.center()
        max_radius = draw_rect.width() / 2

        inner_radius = max_radius * self.hollow_ratio
        bar_thickness = (max_radius - inner_radius) / max(1, len(self._series))

        # Vẽ từng thanh + track riêng
        current_angle = self.start_angle

        for idx, value in enumerate(self._series):
            percentage = value / self.base_value
            angle_span = self.total_angle * percentage

            outer_r = max_radius - idx * bar_thickness
            inner_r = outer_r - bar_thickness * 0.85
            mid_r = (outer_r + inner_r) / 2

            # === VẼ TRACK (NỀN XÁM) RIÊNG CHO TỪNG THANH ===
            track_pen = QPen(QColor(self.track_color), outer_r - inner_r, Qt.SolidLine, Qt.RoundCap)
            p.setPen(track_pen)
            p.setBrush(Qt.NoBrush)
            track_rect = QRectF(center.x() - mid_r, center.y() - mid_r, mid_r * 2, mid_r * 2)
            p.drawArc(track_rect.toRect(), self.start_angle * 16, self.total_angle * 16)

            # === VẼ THANH CHÍNH ===
            color = QColor(self.colors[idx % len(self.colors)])
            pen = QPen(color, outer_r - inner_r, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen)

            path = QPainterPath()
            path.arcMoveTo(track_rect, self.start_angle)
            path.arcTo(track_rect, self.start_angle, angle_span)
            p.strokePath(path, pen)

            # === VẼ NAME + VALUE Ở CUỐI VÒNG CUNG ===
            if (self.show_names or self.show_values) and value > 0:
                end_angle = self.start_angle + angle_span
                rad = radians(end_angle - 90)
                label_x = center.x() + (mid_r + 10) * cos(rad)
                label_y = center.y() + (mid_r + 10) * sin(rad)

                text = ""
                if self.show_names:
                    text += self.labels[idx]
                if self.show_values and self.show_names:
                    text += "\n"
                if self.show_values:
                    text += f"{value:,.0f}"

                p.setPen(QColor(self.theme.palette.text.secondary))
                # p.setFont(self.theme.typography.body2.font())
                fm = QFontMetrics(p.font())
                text_rect = fm.boundingRect(0, 0, 1000, 1000, Qt.AlignCenter, text)
                p.drawText(QPointF(label_x - text_rect.width() / 2, label_y + text_rect.height() / 2), text)

        # === VẼ TOTAL Ở GIỮA ===
        if self.show_total and self._series:
            total_val = sum(self._series) if self._total is None else self._total
            total_text = self.total_formatter() if callable(self.total_formatter) else f"{total_val:,.0f}"

            p.setPen(QColor(self.theme.palette.text.primary))
            # p.setFont(self.theme.typography.h5.font())
            p.drawText(draw_rect.toRect(), Qt.AlignCenter, total_text)

            # Sub label nếu có
            subtitle = self._options.get("title", {}).get("text", "")
            if subtitle:
                p.setPen(QColor(self.theme.palette.text.secondary))
                # p.setFont(self.theme.typography.body2.font())
                p.drawText(draw_rect.adjusted(0, 30, 0, -30).toRect(), Qt.AlignCenter, subtitle)

        p.end()