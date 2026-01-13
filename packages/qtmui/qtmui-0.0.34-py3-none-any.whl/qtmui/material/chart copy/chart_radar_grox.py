# src/qtmui/material/chart/chart_radar.py
from __future__ import annotations

from typing import List, Dict, Optional, Union, Callable
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import (
    QPolarChart,
    QChartView,
    QLineSeries,
    QAreaSeries,
    QValueAxis,
    QCategoryAxis,
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QLinearGradient, QGradient

from qtmui.hooks import State
from qtmui.material.styles import useTheme
from qtmui.material.system.color_manipulator import alpha


class ChartRadar(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "radar",
        series: List[Dict] = None,
        options: Optional[Dict] = None,
        height: Optional[Union[int, str]] = None,
        width: Optional[Union[int, str]] = None,
        title: Optional[Union[str, State, Callable]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.series = series or []
        self.options = options or {}
        self.title = title
        self._height = height
        self._width = width

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.theme = useTheme()
        self.theme.state.valueChanged.connect(self._update_theme)

        self._init_chart()
        self._update_theme()

    def _init_chart(self):
        self.chart = QPolarChart()
        self.chart.setAnimationOptions(QPolarChart.SeriesAnimations)
        self.chart.setBackgroundRoundness(0)

        # Title
        if self.title:
            title_text = self.title() if callable(self.title) else self.title
            self.chart.setTitle(str(title_text))

        # Categories từ options.xaxis.categories
        self.categories = self.options.get("xaxis", {}).get("categories", [])
        if not self.categories and self.series:
            if self.series:
                self.categories = [f"Cat {i+1}" for i in range(len(self.series[0].get("data", [])))]

        # Tính max value động
        all_values = [v for s in self.series for v in s.get("data", []) if isinstance(v, (int, float))]
        self.max_value = max(all_values, default=100)
        self.max_value = self.max_value * 1.1  # +10% padding

        # Axes
        self.angular_axis = self._create_angular_axis()
        self.radial_axis = self._create_radial_axis()

        self.chart.addAxis(self.angular_axis, QPolarChart.PolarOrientationAngular)
        self.chart.addAxis(self.radial_axis, QPolarChart.PolarOrientationRadial)

        # Series + Fill
        self._add_series()

        # Legend cơ bản (không floating phức tạp để tránh crash)
        legend_opts = self.options.get("legend", {})
        legend = self.chart.legend()
        legend.setVisible(legend_opts.get("show", True))
        legend.setAlignment(Qt.AlignBottom)
        legend.show()

        # ChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        if self._height:
            self.chart_view.setFixedHeight(int(self._height))
        if self._width:
            self.chart_view.setFixedWidth(int(self._width))

        self.layout().addWidget(self.chart_view)

    def _create_angular_axis(self):
        axis = QCategoryAxis()
        n = len(self.categories)
        if n > 0:
            step = 360.0 / n
            for i, label in enumerate(self.categories):
                axis.append(label, i * step)

        axis.setRange(0, 360)

        # Cách gọi đúng, ổn định trên mọi PySide6
        try:
            axis.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        except AttributeError:
            # Fallback cho phiên bản cũ
            axis.setLabelsPosition(1)

        return axis

    def _create_radial_axis(self):
        axis = QValueAxis()
        axis.setRange(0, self.max_value)
        axis.setTickCount(6)
        axis.setLabelFormat("%.0f")
        return axis

    def _add_series(self):
        colors = self.options.get("colors", [])
        if not colors:
            colors = [
                self.theme.palette.primary.main,
                self.theme.palette.warning.main,
                self.theme.palette.info.main,
                self.theme.palette.error.main,
                self.theme.palette.success.main,
            ]

        stroke_opts = self.options.get("stroke", {})
        fill_opts = self.options.get("fill", {})

        stroke_width = stroke_opts.get("width", 3)
        fill_opacity = fill_opts.get("opacity", 0.5)

        n_cats = len(self.categories) or 6
        angle_step = 360.0 / n_cats

        for idx, s in enumerate(self.series):
            name = s.get("name", f"Series {idx+1}")
            data = s.get("data", [])

            upper = QLineSeries()
            upper.setName(name)

            color_str = colors[idx % len(colors)]
            color = QColor(color_str)

            # Fill area (nếu có opacity)
            lower = None
            if fill_opacity > 0:
                lower = QLineSeries()

                fill_color = QColor(alpha(color_str, fill_opacity))
                brush = QBrush(fill_color)

                if fill_opts.get("gradient"):
                    grad = QLinearGradient()
                    grad.setCoordinateMode(QGradient.ObjectBoundingMode)
                    grad.setColorAt(0, QColor(alpha(color_str, fill_opts["gradient"].get("opacityFrom", 0.7))))
                    grad.setColorAt(1, QColor(alpha(color_str, fill_opts["gradient"].get("opacityTo", 0))))
                    brush = QBrush(grad)

                lower.setBrush(brush)

            pen = QPen(color)
            pen.setWidth(stroke_width)
            upper.setPen(pen)

            for i, value in enumerate(data):
                angle = i * angle_step
                radius = (value / self.max_value) * 100 if self.max_value > 0 else 0
                point = QPointF(angle, radius)
                upper.append(point)
                if lower:
                    lower.append(point)

            if lower:
                area = QAreaSeries(lower, upper)
                area.setName(name)
                self.chart.addSeries(area)
                area.attachAxis(self.angular_axis)
                area.attachAxis(self.radial_axis)
            else:
                self.chart.addSeries(upper)
                upper.attachAxis(self.angular_axis)
                upper.attachAxis(self.radial_axis)

    def _update_theme(self):
        theme = useTheme()

        # Background
        bg = QColor(theme.palette.background.paper)
        self.chart.setBackgroundBrush(QBrush(bg))
        self.chart.setPlotAreaBackgroundBrush(QBrush(bg))
        self.chart.setPlotAreaBackgroundVisible(True)

        # Title
        self.chart.setTitleBrush(QBrush(QColor(theme.palette.text.primary)))
        # self.chart.setTitleFont(QFont(theme.typography.h6.fontFamily, 16, QFont.Bold))

        # Grid & labels
        grid_color = QColor(theme.palette.divider)
        text_color = QColor(theme.palette.text.secondary)

        for axis in self.chart.axes():
            axis.setLabelsBrush(QBrush(text_color))
            axis.setLinePen(QPen(grid_color))
            axis.setGridLinePen(QPen(grid_color, 1, Qt.DashLine))

        # Legend
        legend = self.chart.legend()
        legend.setLabelColor(QColor(theme.palette.text.primary))
        # legend.setFont(QFont(theme.typography.body2.fontFamily, 12))