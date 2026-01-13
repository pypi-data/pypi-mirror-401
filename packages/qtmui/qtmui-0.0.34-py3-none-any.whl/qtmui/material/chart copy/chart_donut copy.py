# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

from qtmui.hooks import State


"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Callable, Optional, Union
import random
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import (QChart, 
                              QChartView, 
                              QPieSeries, 
                              QChart,
                              QChartView, 
                              )
from PySide6.QtGui import QGradient, QLinearGradient, QPainter, QColor, QBrush
from ..system.color_manipulator import alpha

from qtmui.material.styles import useTheme


class ChartDonut(QWidget):
    def __init__(
                self,
                dir: str = "ltr", # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                series: object = None, 
                width: Optional[Union[str, int]] = None, 
                height: Optional[Union[str, int]] = None, 
                options: object = None,
                key: str = None,
                title: Optional[Union[State, str, Callable]] = None,
                *args,
                **kwargs
                ):
        super().__init__(*args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        self._series = series
        self._width = width
        self._height = height
        self._options = options
        self._title = title

        self._init_donut_chart()

        theme = useTheme()
        useEffect(
            self._set_stylesheet,
            [theme.state]
        )
        self._set_stylesheet()


    def _get_unique_color(self):
        colorPalette = getattr(self.theme.palette, ['primary', 'secondary', 'success', 'warning', 'error', 'info'][random.randint(0, 4)])
        color = getattr(colorPalette, ['main', 'dark', 'darker', 'light', 'lighter'][random.randint(0, 4)])
        if color in self.colors:
            return self._get_unique_color()
        return color

    def _init_donut_chart(self):
        self.theme = useTheme()

        # Tạo PieSeries (Donut Chart)
        series = QPieSeries()
        for index, label in enumerate(self._options["labels"], 0):
            series.append(label, self._series[index])
            
        # Tạo hiệu ứng donut bằng cách đặt kích thước lỗ trống
        for slice in series.slices():
            slice.setLabel("{}: {:.1f}%".format(slice.label(), slice.percentage() * 100))
            # slice.setColor(QColor(self.theme.palette.warning.main))
        
        series.setHoleSize(0.6)  # Điều chỉnh kích thước lỗ trống của donut
        
        # Tạo biểu đồ
        self.chart = QChart()
        self.chart.addSeries(series)
        if self._title:
            self.chart.setTitle(self._title)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        
        # Tạo chart view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layout().addWidget(self.chart_view)


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
        # self.chart.setBackgroundBrush(gradient)
        # self.chart.setBackgroundBrush(QBrush(QColor(alpha(self.theme.palette.background.paper, 0.26))))
        self.chart.setBackgroundBrush(QBrush(QColor(self.theme.palette.background.paper)))
        self.chart.setBackgroundRoundness(10)  # Optional: Rounded edges for the background

