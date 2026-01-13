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
from PySide6.QtGui import QGradient, QPen, QLinearGradient, QPainter

from .chart_line import ChartLine
from .map_change_theme import ChartArea
from .chart_bar import ChartBar


class Chart(QWidget):
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

        if type == "line":
            line_chart = ChartLine(
                type=type,
                series=series,
                width=width,
                height=height,
                options=options
            )
            self.layout().addWidget(line_chart)
        elif type == "area":
            area_chart = ChartArea(
                type=type,
                series=series,
                width=width,
                height=height,
                options=options
            )
            self.layout().addWidget(area_chart)
        elif type == "bar":
            bar_chart = ChartBar(
                type=type,
                series=series,
                width=width,
                height=height,
                options=options
            )
            self.layout().addWidget(bar_chart)

        if height:
             self.setFixedHeight(height)