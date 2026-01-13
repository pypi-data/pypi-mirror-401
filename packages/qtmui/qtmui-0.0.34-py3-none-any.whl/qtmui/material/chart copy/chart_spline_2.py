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
    QValueAxis,
    QScatterSeries,
    QLineSeries,
)
from PySide6.QtGui import QPen, QPainter, QColor, QFont

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
        
        self.hover_mark_positions = [10, 41, 35, 51, 49, 62, 69, 91, 148]

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
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%d") # hiển thị giá trị nguyên trên trục Y/ mặc định float


        # -----------------------------
        # CATEGORY AXIS (if provided)
        # -----------------------------
        categories = None

        if self._options.get("xaxis") and "categories" in self._options["xaxis"]:
            categories = self._options["xaxis"]["categories"]

        if categories:
            self.axis_x = QBarCategoryAxis()
            
            self.axis_x.append(categories)

            # Fix Y range
            self.axis_y.setRange(0, max(max(item["data"]) for item in self._series_input))
        else:
            self.axis_x = QValueAxis()
            
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
            
        for s in self._spline_series_list:
            s.attachAxis(self.axis_x)
            s.attachAxis(self.axis_y)
            
        # ----------- MARKER SERIES -------------------
        self.marker_series = QScatterSeries()
        self.marker_series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        self.marker_series.setMarkerSize(10)
        self.marker_series.setColor(QColor("#ff0000"))
        self.marker_series.setBorderColor(QColor("#ffffff"))

        # Lấy series đầu tiên làm dữ liệu tham chiếu
        if self._spline_series_list:
            s0 = self._spline_series_list[0]
            for x in self.hover_mark_positions:
                if 0 <= x < s0.count():
                    p = s0.at(x)
                    self.marker_series.append(p)

        self.chart.addSeries(self.marker_series)
        self.marker_series.attachAxis(self.axis_x)
        self.marker_series.attachAxis(self.axis_y)

        # ----------- HIGHLIGHT MARKER -------------------
        self.hover_point = QScatterSeries()
        self.hover_point.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        self.hover_point.setMarkerSize(14)
        self.hover_point.setColor(QColor("#00e5ff"))
        self.hover_point.setBorderColor(QColor("#ffffff"))
        self.hover_point.hide()

        self.chart.addSeries(self.hover_point)
        self.hover_point.attachAxis(self.axis_x)
        self.hover_point.attachAxis(self.axis_y)

        # ----------- HOVER VERTICAL LINE -------------------
        self.hover_line = QLineSeries()
        self.hover_line.setPen(QPen(QColor("#8888ff"), 1, Qt.DashLine))
        self.hover_line.hide()
            
        self.chart.addSeries(self.hover_line)
        self.hover_line.attachAxis(self.axis_x)
        self.hover_line.attachAxis(self.axis_y)


        # -----------------------------
        # Chart View
        # -----------------------------
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout().addWidget(self.chart_view)
        
        # ----------------- ENABLE MOUSE MOVE -------------------
        self.chart_view.setMouseTracking(True)
        self.chart_view.mouseMoveEvent = self._mouse_move_event
        
    # -----------------------------------------------------------------------

    def _mouse_move_event(self, event):
        print("Mouse move:", event.pos())
        pos = event.pos()
        chart_pos = self.chart.mapToValue(pos, self._spline_series_list[0])

        x = chart_pos.x()

        # tìm x gần nhất trong hover_mark_positions
        nearest = min(self.hover_mark_positions, key=lambda v: abs(v - x))
        
        print("Nearest x:", nearest)

        s0 = self._spline_series_list[0]
        if 0 <= nearest < s0.count():
            point = s0.at(nearest)

            # update highlight marker
            self.hover_point.clear()
            self.hover_point.append(point)
            self.hover_point.show()

            # update vertical line
            ymin = self.axis_y.min()
            ymax = self.axis_y.max()

            self.hover_line.clear()
            self.hover_line.append(point.x(), ymin)
            self.hover_line.append(point.x(), ymax)
            self.hover_line.show()

        return QChartView.mouseMoveEvent(self.chart_view, event)

    # -----------------------------------------------------------------------

    def _apply_theme(self):
        theme = useTheme()

        text_color = QColor(theme.palette.text.secondary)
        primary_color = QColor(theme.palette.primary.main)

        # Apply to title
        self.chart.setTitleBrush(text_color)
        # self.chart.setTitleFont(theme.typography.subtitle1.toQFont())

        # label font
        font = QFont()
        font.setPointSize(8)
        font.setWeight(QFont.Weight(600))

        # Axis x style
        ## for axis in self.chart.axes():
        pen = QPen(Qt.PenStyle.DashLine)
        ## pen.setWidth(1)
        pen.setWidthF(0.2)
        pen.setColor(text_color)
        self.axis_x.setGridLinePen(pen)
        self.axis_x.setGridLineVisible(False) # ẩn grid line dọc
        ## axis.setGridLineVisible(False) # ẩn grid line
        self.axis_x.setLabelsBrush(text_color)
        self.axis_x.setTitleBrush(text_color)
        self.axis_x.setLinePen(pen)
        # self.axis_x.setLabelsFont(theme.typography.body2.toQFont())
        self.axis_x.setLabelsFont(font)
        self.axis_x.setLabelsColor(text_color)

        # Axis y style
        self.axis_y.setLinePen(Qt.PenStyle.NoPen)
        self.axis_y.setGridLinePen(pen)
        # self.axis_y.setLabelsFont(theme.typography.body2.toQFont())
        # self.axis_y.setLabelsFont(theme.typography.body2.toQFont())
        self.axis_y.setLabelsFont(font)
        self.axis_y.setLabelsColor(text_color)

        # Legend
        legend = self.chart.legend()
        legend.setLabelBrush(text_color)

        # Apply colors to spline series
        for idx, s in enumerate(self._spline_series_list):
            pen = QPen(primary_color if idx == 0 else QColor(theme.palette.info.main))
            pen.setWidth(3)
            s.setPen(pen)
