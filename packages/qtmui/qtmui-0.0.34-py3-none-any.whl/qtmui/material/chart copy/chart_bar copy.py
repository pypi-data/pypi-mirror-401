# Copyright (C) 2022 The Pyact Company Ltd.
# SPDX-License-Identifier: LicenseRef-Pyact-Commercial OR BSD-3-Clause
from __future__ import annotations

from qtmui.hooks import State

"""..site_packages.qtcompat port of the areachart example from qtmui v1.0"""

from typing import Callable, Optional, Union, List, Dict, Any
import random
from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCharts import (QChart,
                              QChartView,
                              QLineSeries,
                              QAreaSeries,
                              QPercentBarSeries,
                              QBarCategoryAxis,
                              QBarSeries,
                              QBarSet,
                              QValueAxis,
                              )
from PySide6.QtGui import QGradient, QPen, QLinearGradient, QPainter, QColor, QBrush
from ..system.color_manipulator import alpha

from qtmui.material.styles import useTheme


class ChartBar(QWidget):
    def __init__(
                self,
                dir: str = "ltr", # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                type: str = "line", # "line" | "area" | "bar" | "pie" | "donut" | "radialBar" | "scatter" | "bubble" | "heatmap" | "candlestick" | "boxPlot" | "radar" | "polarArea" | "rangeBar" | "rangeArea" | "treemap"
                series: List[Dict[str, Any]] = None,
                width: Optional[Union[str, int]] = None,
                height: Optional[Union[str, int]] = None,
                options: Optional[Dict[str, Any]] = None,
                key: str = None,
                title: Optional[Union[State, str, Callable]] = None,
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
        self._title = title

        self._init_bar_chart()

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

    def _init_bar_chart(self):
        self.theme = useTheme()

        if self._type == "barPercent":
            self._bar_series = QPercentBarSeries()
        else:
            self._bar_series = QBarSeries()


        self.colors = []
        
        # Check if self._series is None or empty
        if not self._series:
            print("Error: self._series is None or empty.  No data to display.")
            return  # Exit the function if there's no data

        for i, item in enumerate(self._series):
            # Check if item is a dictionary and has the 'name' and 'data' keys
            if not isinstance(item, dict) or 'name' not in item or 'data' not in item:
                print(f"Error: Invalid data format in self._series[{i}].  Expected a dictionary with 'name' and 'data' keys.")
                continue  # Skip to the next item

            bar_set = QBarSet(item.get('name'))
            color = self._get_unique_color()
            self.colors.append(color)
            # print('color_________', color)
            bar_set.setPen(QPen(QColor(color)))
            bar_set.setBrush(QBrush(QColor(color)))

            # Check if item["data"] is a list
            if not isinstance(item["data"], list):
                print(f"Error: Invalid data format in self._series[{i}]['data']. Expected a list.")
                continue  # Skip to the next item

            for index, data in  enumerate(item["data"]):
                # Check if data is a number
                if not isinstance(data, (int, float)):
                    print(f"Error: Invalid data type in self._series[{i}]['data'][{index}]. Expected a number.")
                    continue  # Skip to the next data point
                bar_set.append(data)
            self._bar_series.append(bar_set)

        self.chart = QChart()
        self.chart.addSeries(self._bar_series)
        if self._title:
            self.chart.setTitle(self._title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.categories = self._options.get("categories") or self._options.get("xaxis").get("categories")
        print('self.categories___________', self.categories)
        self.axis_x = QBarCategoryAxis()
        if self.categories:
            self.axis_x.append(self.categories)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self._bar_series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()

        # Calculate the maximum value in the data to set the Y-axis range appropriately
        max_y = 15  # Default value
        if self._series:
            try:
                max_y = max(max(item['data']) for item in self._series if isinstance(item, dict) and isinstance(item.get('data'), list))
            except ValueError:
                print("Warning: Could not determine max_y from data.  Using default value of 15.")
            except Exception as e:
                print(f"Error calculating max_y: {e}")

        # self.axis_y.setRange(0, max_y * 1.1)  # Add a 10% buffer to the top
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self._bar_series.attachAxis(self.axis_y)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignTop)

        self._chart_view = QChartView(self.chart)
        # self._chart_view.setStyleSheet('background-color: transparent;')
        self._chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set Size Policy to Expanding
        self._chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
        # self.chart.setBackgroundBrush(gradient)
        # self.chart.setBackgroundBrush(QBrush(QColor(alpha(self.theme.palette.background.paper, 0.26))))
        self.chart.setBackgroundBrush(QBrush(QColor(self.theme.palette.background.paper)))
        self.chart.setBackgroundRoundness(10)  # Optional: Rounded edges for the background