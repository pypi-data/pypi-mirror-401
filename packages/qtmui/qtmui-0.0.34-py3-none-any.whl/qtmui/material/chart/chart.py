# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Optional, Union
import sys
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout

from PySide6.QtGui import QGradient, QPen, QLinearGradient, QPainter

from .chart_line import ChartLine
from .chart_spline import ChartSpline
from .chart_area import ChartArea
from .chart_bar import ChartBar
from .chart_donut import ChartDonut
from .chart_radial_bar import ChartRadialBar
from .chart_pie import ChartPie
from .chart_radar import ChartRadar
from .chart_polar_area import ChartPolarArea


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
                total: int = None,
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
        elif type == "spline":
            line_chart = ChartSpline(
                type=type,
                series=series,
                width=width,
                height=height,
                options=options
            )
            self.layout().addWidget(line_chart)
        elif type == "area" or type == "mixed":
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
        elif type == "donut":
            bar_chart = ChartDonut(
                series=series,
                width=width,
                height=height,
                options=options
            )
            self.layout().addWidget(bar_chart)
        elif type == "radialBar":
            bar_chart = ChartRadialBar(
                series=series,
                width=width,
                height=height,
                options=options,
                total=total,
            )
            self.layout().addWidget(bar_chart)
        elif type == "pie":
            bar_chart = ChartPie(
                series=series,
                width=width,
                height=height,
                options=options,
            )
            self.layout().addWidget(bar_chart)
        elif type == "radar":
            bar_chart = ChartRadar(
                series=series,
                width=width,
                height=height,
                options=options,
            )
            self.layout().addWidget(bar_chart)
        elif type == "polarArea":
            bar_chart = ChartPolarArea(
                series=series,
                width=width,
                height=height,
                options=options,
            )
            self.layout().addWidget(bar_chart)

        if height:
             self.setFixedHeight(height)