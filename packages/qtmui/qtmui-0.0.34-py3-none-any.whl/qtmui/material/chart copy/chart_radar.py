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
)
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont

from qtmui.hooks import State
from qtmui.material.styles import useTheme


class ChartRadar(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        series: List[Dict] = [],
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

        self._init_radar_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_radar_chart(self):
        self.theme = useTheme()
        self.chart = QPolarChart()


        # Lấy categories từ options, nếu không có thì dùng list rỗng
        self.categories = self.options.get("xaxis", {}).get("categories", [])

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
        angle_step = 360 / len(self.categories) if self.categories else 0

        # Tạo nhãn theo thứ tự ban đầu:
        for i, category in enumerate(self.categories):
            angle = i * angle_step + 60  # Giá trị góc tính theo 0, 60, 120, ... nếu có 6 category
            axis.append(category, angle)

        axis.setRange(0, 360)
        axis.setLabelsFont(QFont("Arial", 10))
        return axis


    def _create_radial_axis(self):
        axis = QValueAxis()
        axis.setTickCount(5)
        axis.setLabelFormat("%d")
        axis.setRange(0, 100)  # Giả định giá trị max là 100
        return axis

    def _add_data_series(self):
        colors = self.options.get("colors", [
            self.theme.palette.primary.main,
            self.theme.palette.secondary.main,
            self.theme.palette.error.main,
        ])

        max_value = 100  # Giả định giá trị max là 100

        for idx, series_data in enumerate(self.series):
            series = QLineSeries()
            series.setName(series_data.get("name", f"Series {idx+1}"))

            angle_step = 360 / len(series_data["data"])
            for i, value in enumerate(series_data["data"]):
                # Tính góc: 0, 60, 120, ... (không cần cộng thêm offset)
                angle = i * angle_step
                radius = (value / max_value) * 100  # Scale về khoảng 0-100
                series.append(QPointF(angle, radius))

            pen = QPen(QColor(colors[idx % len(colors)]))
            pen.setWidth(2)
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
