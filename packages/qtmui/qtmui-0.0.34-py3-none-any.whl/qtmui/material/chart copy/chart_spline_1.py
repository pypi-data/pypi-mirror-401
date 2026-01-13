# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

from typing import Optional, Union
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QSplineSeries,
    QBarCategoryAxis,
    QValueAxis
)
from PySide6.QtGui import QPen, QPainter, QColor

from qtmui.material.styles import useTheme


class ChartSLine(QWidget):
    def __init__(
        self,
        dir: str = "ltr",
        type: str = "line",
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

        self._series_input = series or []
        self._options = options or {}
        self._width = width
        self._height = height

        self._init_chart()

        # Apply theme
        theme = useTheme()
        theme.state.valueChanged.connect(self._apply_theme)
        self._apply_theme()

    # -----------------------------------------------------------------------

    def _init_chart(self):
        if self._height:
            self.setFixedHeight(self._height)
        if self._width:
            self.setFixedWidth(self._width)

        # -----------------------------
        # Create spline series from data
        # -----------------------------
        self._spline_series_list = []

        for item in self._series_input:
            s = QSplineSeries()
            s.setName(item.get("name", ""))

            for idx, y in enumerate(item.get("data", [])):
                x = float(idx)
                y = float(y)
                s.append(QPointF(x, y))

            self._spline_series_list.append(s)

        # -----------------------------
        # Create Chart
        # -----------------------------
        self.chart = QChart()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)

        for s in self._spline_series_list:
            self.chart.addSeries(s)

        # Default numeric axes
        axis_x = QValueAxis()
        axis_y = QValueAxis()

        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)

        # Attach all series to axes
        for s in self._spline_series_list:
            s.attachAxis(axis_x)
            s.attachAxis(axis_y)

        # -----------------------------
        # CATEGORY AXIS (if provided)
        # -----------------------------
        categories = None

        if self._options.get("xaxis") and "categories" in self._options["xaxis"]:
            categories = self._options["xaxis"]["categories"]

        if categories:
            cat_axis = QBarCategoryAxis()
            cat_axis.append(categories)
            self.chart.removeAxis(axis_x)
            self.chart.addAxis(cat_axis, Qt.AlignBottom)

            for s in self._spline_series_list:
                s.attachAxis(cat_axis)

            # Fix Y range
            axis_y.setRange(0, max(max(item["data"]) for item in self._series_input))

        # -----------------------------
        # Chart View
        # -----------------------------
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout().addWidget(self.chart_view)

    # -----------------------------------------------------------------------

    def _apply_theme(self):
        theme = useTheme()

        text_color = QColor(theme.palette.text.secondary)
        primary_color = QColor(theme.palette.primary.main)

        # Apply to title
        self.chart.setTitleBrush(text_color)

        # Axis color
        for axis in self.chart.axes():
            axis.setLabelsBrush(text_color)
            axis.setTitleBrush(text_color)
            axis.setLinePen(QPen(text_color))

        # Legend
        legend = self.chart.legend()
        legend.setLabelBrush(text_color)

        # Apply colors to spline series
        for idx, s in enumerate(self._spline_series_list):
            pen = QPen(primary_color if idx == 0 else QColor(theme.palette.info.main))
            pen.setWidth(3)
            s.setPen(pen)
