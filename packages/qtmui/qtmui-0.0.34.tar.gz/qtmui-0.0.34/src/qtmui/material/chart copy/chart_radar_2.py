from __future__ import annotations

from typing import Callable, Optional, Union, List, Dict
import math

from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
    QCategoryAxis,
    QPolarChart,
    QAreaSeries,
    QBarSet,
    QBarSeries,
    QBarCategoryAxis
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont

from qtmui.hooks import State
from qtmui.material.styles import useTheme


class ChartPolarArea(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        series: List[int] = [],  # Thay đổi kiểu dữ liệu của series
        width: Optional[Union[str, int]] = None,
        height: Optional[Union[str, int]] = None,
        options: Optional[Dict] = None,
        key: str = None,
        title: Optional[Union[State, str, Callable]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.series = series
        self.options = options or {}
        self.title = title
        self._height = height
        self._width = width

        self._init_polar_area_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_polar_area_chart(self):
        self.theme = useTheme()
        self.chart = QPolarChart()

        # Lấy labels từ options, nếu không có thì dùng list rỗng
        self.labels = self.options.get("labels", [])

        if self._width:
            self.setFixedWidth(self._width)
        if self._height:
            self.setFixedHeight(self._height)

        # Tạo các trục tọa độ cực
        self.angular_axis = self._create_angular_axis()
        self.radial_axis = self._create_radial_axis()

        # Thêm các trục vào chart
        self.chart.addAxis(self.angular_axis, QPolarChart.PolarOrientationAngular)
        self.chart.addAxis(self.radial_axis, QPolarChart.PolarOrientationRadial)

        # Thêm các series dữ liệu
        self._add_data_series()

        # Cấu hình chart
        if self.title:
            self.chart.setTitle(self.title)

        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart.legend().show()

        # Tạo ChartView
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout().addWidget(self.chart_view)

    def _create_angular_axis(self):
        axis = QCategoryAxis()
        angle_step = 360 / len(self.labels) if self.labels else 0

        # Tạo nhãn theo thứ tự ban đầu:
        for i, label in enumerate(self.labels):
            angle = i * angle_step  # Giá trị góc tính theo 0, 60, 120, ... nếu có 6 label
            axis.append(label, angle)

        axis.setRange(0, 360)
        axis.setLabelsFont(QFont("Arial", 10))
        return axis


    def _create_radial_axis(self):
        axis = QValueAxis()
        axis.setTickCount(5)
        axis.setLabelFormat("%d")
        max_value = max(self.series) if self.series else 100
        axis.setRange(0, max_value * 1.2)  # Điều chỉnh range theo giá trị max
        return axis

    def _add_data_series(self):
        colors = self.options.get("colors", [self.theme.palette.primary.main])
        fill_opacity = self.options.get("fill", {}).get("opacity", 0.8)

        max_value = max(self.series) if self.series else 100

        # Tạo QAreaSeries cho biểu đồ vùng cực
        series = QAreaSeries()

        # Tạo QLineSeries cho đường viền
        line_series = QLineSeries()

        angle_step = 360 / len(self.series)
        for i, value in enumerate(self.series):
            # Tính góc: 0, 60, 120, ...
            angle = i * angle_step
            radius = (value)  # Sử dụng trực tiếp giá trị

            line_series.append(QPointF(angle, radius))


        series.setUpperSeries(line_series)

        # Tạo màu cho khu vực
        for i, value in enumerate(self.series):
            color = QColor(colors[i % len(colors)])
            brush = QBrush(color)
            # brush.setOpacity(fill_opacity)
            series.setBrush(brush)

            # Không vẽ đường viền, chỉ fill màu
            pen = QPen(color)
            pen.setWidth(0)
            series.setPen(pen)

        self.chart.addSeries(series)
        series.attachAxis(self.angular_axis)
        series.attachAxis(self.radial_axis)


    def _set_stylesheet(self):
        theme = useTheme()
        # Cấu hình màu sắc
        self.chart.setBackgroundBrush(QBrush(QColor(theme.palette.background.paper)))
        self.chart.setTitleBrush(QBrush(QColor(theme.palette.text.primary)))

        # Cập nhật màu cho các trục
        text_color = QColor(theme.palette.text.secondary)
        for axis in self.chart.axes():
            axis.setLabelsBrush(QBrush(text_color))
            axis.setLinePenColor(text_color)
            axis.setGridLineColor(QColor(theme.palette.divider))

        # Cập nhật legend
        self.chart.legend().setLabelColor(text_color)
