# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Optional, Union
import sys
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout
from PySide6.QtCharts import (QChart, 
                              QChartView, 
                              QLineSeries, 
                              QAreaSeries,
                              QBarCategoryAxis, 
                              QBarSeries, 
                              QBarSet, 
                              QChart,
                              QChartView, 
                              QValueAxis,
                              )
from PySide6.QtGui import QGradient, QPen, QLinearGradient, QPainter, QColor

from qtmui.material.styles import useTheme


class ChartArea(QWidget):
    def __init__(
                self,
                dir: str = "ltr", # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                type: str = "line", # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
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
        self.layout().setContentsMargins(0,0,0,0)

        self._type = type
        self._series = series
        self._width = width
        self._height = height
        self._options = options

        self._init_area_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()

 
    def _init_area_chart(self):
        theme = useTheme()

        self._line_series = []

        for i, item in enumerate(self._series):
            self._line_series.append(QLineSeries())
            for index, value in  enumerate(item.get("data") or item):
                if self._options.get("categories"):
                    self._line_series[i].append(QPointF(self._options["categories"][index], value))

        self.series = QAreaSeries(*self._line_series)

        self.series.setName("Batman")
        self.pen = QPen(QColor(theme.palette.primary.main))
        self.pen.setWidth(1)
        self.series.setPen(self.pen)

        self.gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        self.gradient.setColorAt(0.0, QColor(theme.palette.primary.main))
        self.gradient.setColorAt(1.0, QColor(theme.palette.warning.main))
        self.gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        self.series.setBrush(self.gradient)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Simple areachart example")
        self.chart.createDefaultAxes()
        self.chart.axes(Qt.Orientation.Horizontal)[0].setRange(0, 20)
        self.chart.axes(Qt.Vertical)[0].setRange(0, 10)

        self._chart_view = QChartView(self.chart)
        # self._chart_view.setStyleSheet('background-color: transparent;')
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.layout().addWidget(self._chart_view)

    def _set_stylesheet(self):
        theme = useTheme()

        text_color = QColor(theme.palette.text.secondary)
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
        # self.chart.setBackgroundBrush(QBrush(alpha(theme.palette.background.paper, 0.26)))
        self.chart.setBackgroundRoundness(10)  # Optional: Rounded edges for the background
