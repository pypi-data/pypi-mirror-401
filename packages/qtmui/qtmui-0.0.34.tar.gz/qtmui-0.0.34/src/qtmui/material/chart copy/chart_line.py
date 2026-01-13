# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Optional, Union
import sys
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout
from PySide6.QtCharts import (
    QChart, 
    QChartView, 
    QLineSeries, 
    QBarCategoryAxis, 
    QChart,
    QChartView, 
)
from PySide6.QtGui import QGradient, QPen, QLinearGradient, QPainter, QColor, QBrush
from ..system.color_manipulator import alpha
from qtmui.material.styles import useTheme


class ChartLine(QWidget):
    def __init__(
        self,
        dir: str = "ltr",  # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
        type: str = "line",  # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
        series: object = None, 
        width: Optional[Union[str, int]] = None, 
        height: Optional[Union[str, int]] = None, 
        options: object = None,
        key: str = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._type = type
        self._series = series
        self._width = width
        self._height = height
        self._options = options

        self._init_line_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

    def _init_line_chart(self):
        self.theme = useTheme()

        if self._height:
            self.setFixedHeight(self._height)
        if self._width:
            self.setFixedWidth(self._width)

        self._line_series = []

        # Tạo một QLineSeries cho mỗi phần tử trong series
        for i, item in enumerate(self._series):
            series = QLineSeries()
            series.setName(item.get("name") or "")  # Đặt tên cho legend nếu có
            data = item.get("data", [])
            # Kiểm tra nếu mỗi điểm dữ liệu là dict chứa "x" và "y"
            for point in data:
                if isinstance(point, dict):
                    try:
                        x = float(point.get("x", 0))
                        y = float(point.get("y", 0))
                    except (ValueError, TypeError):
                        x, y = 0.0, 0.0
                else:
                    # Nếu không phải dict, hãy sử dụng index và giá trị đó (nếu phù hợp)
                    # Tuy nhiên, với đầu vào theo yêu cầu, chúng ta mong đợi dict.
                    x, y = 0.0, float(point)
                series.append(QPointF(x, y))
            self._line_series.append(series)

        # Tạo chart và thêm các series vào chart
        self.chart = QChart()
        for series in self._line_series:
            self.chart.addSeries(series)

        # Hiển thị legend và căn chỉnh vị trí của legend
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)

        # Tạo các trục mặc định cho chart
        self.chart.createDefaultAxes()

        # Nếu có tùy chọn x-axis categories, đặt lại trục x
        if self._options.get("xaxis") and "categories" in self._options["xaxis"]:
            axis_x = QBarCategoryAxis()
            axis_x.append(self._options["xaxis"]["categories"])
            self.chart.setAxisX(axis_x, self._line_series[0])
        elif self._options.get("categories"):
            axis_x = QBarCategoryAxis()
            axis_x.append(self._options["categories"])
            self.chart.setAxisX(axis_x, self._line_series[0])

        # Thiết lập ChartView
        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.layout().addWidget(self._chart_view)

    def _set_stylesheet(self):
        theme = useTheme()

        text_color = QColor(self.theme.palette.text.secondary)
        # 1. Màu cho tiêu đề
        self.chart.setTitleBrush(text_color)

        # 2. Màu cho nhãn trục
        for axis in self.chart.axes():
            axis.setLabelsBrush(text_color)

        # 3. Màu cho nhãn trong legend (nếu bật)
        legend = self.chart.legend()
        legend.setLabelBrush(text_color)

        # Set the chart's background
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(theme.palette.background.paper))  # Top color
        gradient.setColorAt(1.0, QColor(theme.palette.background.main))  # Bottom color
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        self.chart.setBackgroundBrush(gradient)
        self.chart.setBackgroundRoundness(10)  # Optional: Rounded edges for the background